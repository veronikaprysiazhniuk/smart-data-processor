"""
📊 Smart Invoice & Data Processor
AI-powered tool that transforms messy business data into clean reports.

Portfolio Demo by Veronika Prysiazhniuk
- Processes CSV, Excel files automatically
- AI generates business insights from your data
- Interactive charts and downloadable reports

Deploy: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime
import json
import re

# ─── Page Config ───
st.set_page_config(
    page_title="Smart Data Processor",
    page_icon="📊",
    layout="wide"
)

# ─── Custom CSS ───
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        color: #6b7280;
        font-size: 1rem;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e293b;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
    }
    .insight-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 4px solid #0284c7;
        padding: 16px 20px;
        border-radius: 0 10px 10px 0;
        margin: 10px 0;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ───
st.markdown('<div class="main-header">📊 Smart Data Processor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload any CSV or Excel file → Get instant analysis, visualizations, and AI-powered insights</div>', unsafe_allow_html=True)

# ─── Helper Functions ───
def detect_column_types(df):
    """Intelligently categorize columns"""
    types = {
        'numeric': [],
        'categorical': [],
        'datetime': [],
        'text': [],
        'currency': []
    }
    
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            # Check if it looks like currency (has $ or € or large values)
            col_lower = col.lower()
            if any(word in col_lower for word in ['price', 'amount', 'cost', 'revenue', 'total', 'fee', 'salary', 'payment', 'invoice', 'budget']):
                types['currency'].append(col)
            else:
                types['numeric'].append(col)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            types['datetime'].append(col)
        else:
            # Try to parse as date
            try:
                sample = df[col].dropna().head(20)
                if len(sample) > 0:
                    pd.to_datetime(sample, infer_datetime_format=True)
                    types['datetime'].append(col)
                    continue
            except (ValueError, TypeError):
                pass
            
            nunique = df[col].nunique()
            if nunique < min(20, len(df) * 0.3):
                types['categorical'].append(col)
            else:
                types['text'].append(col)
    
    return types

def generate_insights(df, col_types):
    """Generate AI-like business insights from data"""
    insights = []
    
    # Dataset overview
    insights.append(f"📋 **Dataset Overview:** {len(df):,} rows × {len(df.columns)} columns. "
                   f"{'No missing data detected.' if df.isnull().sum().sum() == 0 else f'{df.isnull().sum().sum():,} missing values found across {(df.isnull().sum() > 0).sum()} columns.'}")
    
    # Currency/financial insights
    for col in col_types['currency']:
        total = df[col].sum()
        mean = df[col].mean()
        median = df[col].median()
        std = df[col].std()
        
        insights.append(f"💰 **{col}:** Total = ${total:,.2f} | Average = ${mean:,.2f} | Median = ${median:,.2f}")
        
        if std > mean * 0.5:
            insights.append(f"⚠️ **High variance in {col}** — standard deviation (${std:,.2f}) is {'%.0f' % (std/mean*100)}% of the mean. Investigate outliers.")
        
        # Top/bottom
        if len(df) > 5:
            top_val = df[col].nlargest(1).values[0]
            bot_val = df[col].nsmallest(1).values[0]
            if top_val > mean * 3:
                insights.append(f"🔴 **Outlier detected in {col}:** Max value (${top_val:,.2f}) is {top_val/mean:.1f}x the average.")
    
    # Numeric insights
    for col in col_types['numeric'][:3]:
        correlation_found = False
        for col2 in col_types['currency']:
            corr = df[[col, col2]].corr().iloc[0,1]
            if abs(corr) > 0.5:
                direction = "positive" if corr > 0 else "negative"
                insights.append(f"📈 **Correlation found:** {col} has a {direction} correlation ({corr:.2f}) with {col2}.")
                correlation_found = True
    
    # Categorical insights
    for col in col_types['categorical'][:2]:
        top = df[col].value_counts().head(3)
        total = len(df)
        top_items = ", ".join([f"{idx} ({count/total*100:.0f}%)" for idx, count in top.items()])
        insights.append(f"📊 **{col} distribution:** Top categories: {top_items}")
        
        # Revenue by category if available
        for money_col in col_types['currency'][:1]:
            by_cat = df.groupby(col)[money_col].sum().sort_values(ascending=False)
            top_cat = by_cat.index[0]
            top_pct = by_cat.iloc[0] / by_cat.sum() * 100
            insights.append(f"💡 **{top_cat}** accounts for {top_pct:.0f}% of total {money_col}.")
    
    # Datetime insights
    for col in col_types['datetime']:
        try:
            dates = pd.to_datetime(df[col])
            date_range = (dates.max() - dates.min()).days
            insights.append(f"📅 **Time range ({col}):** {date_range} days (from {dates.min().strftime('%Y-%m-%d')} to {dates.max().strftime('%Y-%m-%d')})")
        except:
            pass
    
    return insights

def create_summary_excel(df, col_types, insights):
    """Generate a clean Excel report"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Raw data
        df.to_excel(writer, sheet_name='Raw Data', index=False)
        
        # Summary statistics
        desc = df.describe(include='all').round(2)
        desc.to_excel(writer, sheet_name='Statistics')
        
        # Insights
        insights_df = pd.DataFrame({'Insight': [i.replace('**', '').replace('*', '') for i in insights]})
        insights_df.to_excel(writer, sheet_name='AI Insights', index=False)
        
        # Category breakdowns
        for cat_col in col_types['categorical'][:3]:
            for num_col in (col_types['currency'] + col_types['numeric'])[:2]:
                try:
                    pivot = df.groupby(cat_col)[num_col].agg(['sum', 'mean', 'count']).round(2)
                    pivot.columns = [f'Total {num_col}', f'Average {num_col}', 'Count']
                    pivot = pivot.sort_values(f'Total {num_col}', ascending=False)
                    sheet_name = f'{cat_col[:15]} by {num_col[:12]}'[:31]
                    pivot.to_excel(writer, sheet_name=sheet_name)
                except:
                    pass
    
    return output.getvalue()

# ─── Main App ───
uploaded_file = st.file_uploader(
    "Drop your file here",
    type=['csv', 'xlsx', 'xls'],
    help="Supports CSV, Excel (.xlsx, .xls). Max 200MB."
)

# Demo data option
use_demo = st.checkbox("🎯 No file? Use demo invoice data to see how it works")

if use_demo:
    # Generate realistic demo data
    import random
    random.seed(42)
    
    n = 150
    clients = ['Acme Corp', 'TechFlow Ltd', 'NovaStar', 'BluePeak Inc', 'DataVibe', 'CloudScale', 'PixelForge', 'MetricLabs']
    services = ['AI Chatbot Setup', 'Data Analysis', 'Automation Workflow', 'API Integration', 'Dashboard Build', 'Web Scraping']
    statuses = ['Paid', 'Paid', 'Paid', 'Pending', 'Overdue']
    
    demo_data = {
        'Invoice_ID': [f'INV-{1000+i}' for i in range(n)],
        'Date': pd.date_range('2024-01-01', periods=n, freq='2D'),
        'Client': [random.choice(clients) for _ in range(n)],
        'Service': [random.choice(services) for _ in range(n)],
        'Hours': [round(random.uniform(2, 40), 1) for _ in range(n)],
        'Hourly_Rate': [random.choice([35, 50, 65, 80, 100]) for _ in range(n)],
        'Total_Amount': [0] * n,
        'Status': [random.choice(statuses) for _ in range(n)]
    }
    
    df = pd.DataFrame(demo_data)
    df['Total_Amount'] = (df['Hours'] * df['Hourly_Rate']).round(2)
    # Add some realistic noise
    df.loc[df.sample(10).index, 'Total_Amount'] *= 1.5  # Some premium jobs
    df['Total_Amount'] = df['Total_Amount'].round(2)
    
    uploaded_file = True  # Flag to proceed

elif uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

if uploaded_file:
    # Detect column types
    col_types = detect_column_types(df)
    
    # Try to convert potential datetime columns
    for col in col_types['datetime']:
        try:
            df[col] = pd.to_datetime(df[col])
        except:
            pass
    
    # ─── Quick Stats ───
    st.markdown("---")
    st.markdown("### ⚡ Quick Stats")
    
    cols = st.columns(4)
    cols[0].metric("Rows", f"{len(df):,}")
    cols[1].metric("Columns", f"{len(df.columns)}")
    
    if col_types['currency']:
        main_currency = col_types['currency'][0]
        cols[2].metric(f"Total {main_currency}", f"${df[main_currency].sum():,.2f}")
        cols[3].metric(f"Avg {main_currency}", f"${df[main_currency].mean():,.2f}")
    else:
        missing = df.isnull().sum().sum()
        cols[2].metric("Missing Values", f"{missing:,}")
        cols[3].metric("Data Types", f"{df.dtypes.nunique()}")
    
    # ─── Data Preview ───
    with st.expander("📋 Data Preview (first 10 rows)", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)
    
    # ─── AI Insights ───
    st.markdown("### 🧠 AI-Powered Insights")
    insights = generate_insights(df, col_types)
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    
    # ─── Visualizations ───
    st.markdown("### 📈 Auto-Generated Visualizations")
    
    chart_cols = st.columns(2)
    
    chart_idx = 0
    
    # Chart 1: Category breakdown (bar chart)
    if col_types['categorical'] and (col_types['currency'] or col_types['numeric']):
        cat_col = col_types['categorical'][0]
        val_col = (col_types['currency'] + col_types['numeric'])[0]
        
        agg_data = df.groupby(cat_col)[val_col].sum().sort_values(ascending=True).tail(10)
        
        fig1 = px.bar(
            x=agg_data.values,
            y=agg_data.index,
            orientation='h',
            title=f'{val_col} by {cat_col}',
            labels={'x': val_col, 'y': cat_col},
            color=agg_data.values,
            color_continuous_scale='Viridis'
        )
        fig1.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        chart_cols[chart_idx % 2].plotly_chart(fig1, use_container_width=True)
        chart_idx += 1
    
    # Chart 2: Time series if datetime exists
    if col_types['datetime'] and (col_types['currency'] or col_types['numeric']):
        date_col = col_types['datetime'][0]
        val_col = (col_types['currency'] + col_types['numeric'])[0]
        
        ts_data = df.set_index(date_col)[val_col].resample('W').sum().reset_index()
        
        fig2 = px.line(
            ts_data,
            x=date_col,
            y=val_col,
            title=f'{val_col} Over Time (Weekly)',
            labels={date_col: 'Date', val_col: val_col}
        )
        fig2.update_traces(line_color='#667eea', line_width=2.5)
        fig2.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
        chart_cols[chart_idx % 2].plotly_chart(fig2, use_container_width=True)
        chart_idx += 1
    
    # Chart 3: Distribution
    if col_types['currency'] or col_types['numeric']:
        val_col = (col_types['currency'] + col_types['numeric'])[0]
        
        fig3 = px.histogram(
            df,
            x=val_col,
            nbins=30,
            title=f'Distribution of {val_col}',
            color_discrete_sequence=['#764ba2']
        )
        fig3.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
        chart_cols[chart_idx % 2].plotly_chart(fig3, use_container_width=True)
        chart_idx += 1
    
    # Chart 4: Pie chart for categories
    if col_types['categorical'] and (col_types['currency'] or col_types['numeric']):
        cat_col = col_types['categorical'][0]
        val_col = (col_types['currency'] + col_types['numeric'])[0]
        
        pie_data = df.groupby(cat_col)[val_col].sum().sort_values(ascending=False).head(8)
        
        fig4 = px.pie(
            values=pie_data.values,
            names=pie_data.index,
            title=f'{val_col} Share by {cat_col}',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig4.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
        chart_cols[chart_idx % 2].plotly_chart(fig4, use_container_width=True)
        chart_idx += 1
    
    # Chart 5: Second categorical if available
    if len(col_types['categorical']) > 1 and (col_types['currency'] or col_types['numeric']):
        cat_col = col_types['categorical'][1]
        val_col = (col_types['currency'] + col_types['numeric'])[0]
        
        agg2 = df.groupby(cat_col)[val_col].mean().sort_values(ascending=False).head(10)
        
        fig5 = px.bar(
            x=agg2.index,
            y=agg2.values,
            title=f'Average {val_col} by {cat_col}',
            labels={'x': cat_col, 'y': f'Avg {val_col}'},
            color_discrete_sequence=['#0ea5e9']
        )
        fig5.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
        chart_cols[chart_idx % 2].plotly_chart(fig5, use_container_width=True)
        chart_idx += 1
    
    # ─── Download Report ───
    st.markdown("---")
    st.markdown("### 📥 Download Report")
    
    col_dl1, col_dl2 = st.columns(2)
    
    # Excel report
    excel_data = create_summary_excel(df, col_types, insights)
    col_dl1.download_button(
        "📊 Download Full Excel Report",
        data=excel_data,
        file_name=f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    # CSV
    csv_data = df.to_csv(index=False).encode('utf-8')
    col_dl2.download_button(
        "📋 Download Cleaned CSV",
        data=csv_data,
        file_name=f"cleaned_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )

else:
    # Landing state
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📂 Upload Any Data")
        st.markdown("CSV, Excel — messy or clean. The tool handles it all automatically.")
    
    with col2:
        st.markdown("#### 🧠 AI Analysis")
        st.markdown("Automatic insights: outliers, trends, correlations, category breakdowns.")
    
    with col3:
        st.markdown("#### 📊 Visual Reports")
        st.markdown("Interactive charts + downloadable Excel reports. Ready for your client in seconds.")
    
    st.markdown("---")
    st.markdown("*Built with Python, Pandas, Plotly, and Streamlit. Processes files locally — your data stays private.*")
