"""
Smart Data Processor — Executive Business Intelligence
Story-driven data analysis: every section answers a question, every chart has a conclusion.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Smart Data Processor", page_icon="◆", layout="wide", initial_sidebar_state="expanded")

# ─── Premium CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.stApp{font-family:'Inter',-apple-system,sans-serif}
#MainMenu,header,footer{visibility:hidden}
section[data-testid="stSidebar"]{background:#0c1929;border-right:1px solid #1a2744}
section[data-testid="stSidebar"] .stMarkdown p,section[data-testid="stSidebar"] label{color:#8298b5!important}
section[data-testid="stSidebar"] h1,section[data-testid="stSidebar"] h2,section[data-testid="stSidebar"] h3,section[data-testid="stSidebar"] h4{color:#c8d8ec!important}
.block-container{padding-top:2rem;max-width:1000px}

.report-header{padding:0 0 1.5rem;border-bottom:2px solid #1e3a5f;margin-bottom:2rem}
.report-brand{display:flex;align-items:center;gap:10px}
.report-icon{width:10px;height:10px;background:#3b82f6;border-radius:2px}
.report-company{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:#64748b}
.report-title{font-size:26px;font-weight:700;color:#0f172a;margin:12px 0 4px;letter-spacing:-0.8px}
.report-meta{font-size:13px;color:#94a3b8}

.exec-summary{background:#f0f5ff;border:1px solid #c7d9f5;border-radius:10px;padding:20px 24px;margin:1.5rem 0}
.exec-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#2563eb;margin-bottom:8px}
.exec-text{font-size:15px;color:#1e293b;line-height:1.7;font-weight:400}
.exec-text b{font-weight:600}

.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:1.5rem 0}
.kpi{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:18px 16px;position:relative;overflow:hidden}
.kpi::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px}
.kpi-1::after{background:#3b82f6}.kpi-2::after{background:#10b981}.kpi-3::after{background:#f59e0b}.kpi-4::after{background:#64748b}
.kpi-label{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.7px;color:#64748b;margin-bottom:6px}
.kpi-val{font-size:26px;font-weight:700;color:#0f172a;letter-spacing:-0.5px}
.kpi-note{font-size:11px;color:#94a3b8;margin-top:4px}

.q-section{margin:2.5rem 0 0}
.q-bar{display:flex;align-items:center;gap:12px;padding-bottom:8px;border-bottom:1px solid #e2e8f0;margin-bottom:1rem}
.q-num{font-size:11px;font-weight:700;color:#3b82f6;min-width:16px}
.q-text{font-size:15px;font-weight:600;color:#0f172a}

.conclusion{background:#f8fafc;border-left:3px solid #3b82f6;padding:14px 18px;border-radius:0 8px 8px 0;margin:12px 0;font-size:13px;color:#334155;line-height:1.7}
.conclusion.risk{border-left-color:#f59e0b;background:#fffbeb}
.conclusion.problem{border-left-color:#ef4444;background:#fef2f2}
.conclusion.good{border-left-color:#10b981;background:#f0fdf4}
.conclusion-label{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:4px}
.conclusion .conclusion-label{color:#2563eb}
.conclusion.risk .conclusion-label{color:#d97706}
.conclusion.problem .conclusion-label{color:#dc2626}
.conclusion.good .conclusion-label{color:#059669}

.action-box{background:#0c1929;border-radius:10px;padding:22px 24px;margin:1.5rem 0;color:white}
.action-box h4{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#60a5fa;margin-bottom:12px}
.action-item{display:flex;gap:10px;padding:8px 0;border-bottom:1px solid #1a2744;font-size:13px;color:#c8d8ec;line-height:1.6}
.action-item:last-child{border:none}
.action-num{color:#3b82f6;font-weight:700;min-width:20px}

.chart-wrap{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:4px 8px;margin:8px 0}
.app-footer{margin-top:3rem;padding:1.5rem 0;border-top:1px solid #e2e8f0;text-align:center;font-size:11px;color:#94a3b8}
.stDownloadButton>button{background:#1e3a5f!important;color:white!important;border:none!important;border-radius:8px!important;font-weight:600!important}
.stDownloadButton>button:hover{background:#2d4a6f!important}
@media(max-width:768px){.kpi-row{grid-template-columns:repeat(2,1fr)}}
</style>
""", unsafe_allow_html=True)

def sfig(fig,h=370):
    fig.update_layout(font=dict(family="Inter",color="#334155"),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=40,r=16,t=44,b=36),height=h,title_font=dict(size=13,color="#475569",family="Inter"),xaxis=dict(gridcolor='#f1f5f9',linecolor='#e2e8f0',tickfont=dict(size=10,color="#94a3b8")),yaxis=dict(gridcolor='#f1f5f9',linecolor='#e2e8f0',tickfont=dict(size=10,color="#94a3b8")),legend=dict(font=dict(size=10)))
    return fig

def detect(df):
    t={'numeric':[],'categorical':[],'datetime':[],'text':[],'currency':[]}
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            if any(w in c.lower() for w in['price','amount','cost','revenue','total','fee','salary','payment','invoice','budget','profit','margin','sales','income','expense']):t['currency'].append(c)
            else:t['numeric'].append(c)
        elif pd.api.types.is_datetime64_any_dtype(df[c]):t['datetime'].append(c)
        else:
            try:
                s=df[c].dropna().head(20)
                if len(s)>0:pd.to_datetime(s,infer_datetime_format=True);t['datetime'].append(c);continue
            except:pass
            if df[c].nunique()<min(20,len(df)*0.3):t['categorical'].append(c)
            else:t['text'].append(c)
    return t

def make_excel(df,ct,story,recs):
    out=BytesIO()
    with pd.ExcelWriter(out,engine='openpyxl') as w:
        df.to_excel(w,sheet_name='Raw Data',index=False)
        df.describe(include='all').round(2).to_excel(w,sheet_name='Statistics')
        pd.DataFrame([{'Section':s[0],'Finding':s[1]} for s in story]).to_excel(w,sheet_name='Key Findings',index=False)
        pd.DataFrame([{'#':i+1,'Action':r} for i,r in enumerate(recs)]).to_excel(w,sheet_name='Recommendations',index=False)
        for cc in ct['categorical'][:3]:
            for nc in(ct['currency']+ct['numeric'])[:1]:
                try:
                    p=df.groupby(cc)[nc].agg(['sum','mean','count']).round(2)
                    p['Share %']=(p['sum']/p['sum'].sum()*100).round(1)
                    p.columns=['Total','Average','Count','Share %']
                    p.sort_values('Total',ascending=False).to_excel(w,sheet_name=f'{cc[:20]} Breakdown'[:31])
                except:pass
    return out.getvalue()

# ─── Sidebar ───
with st.sidebar:
    st.markdown('<div style="padding:0.5rem 0 1rem"><div style="display:flex;align-items:center;gap:8px"><div style="width:8px;height:8px;background:#3b82f6;border-radius:2px"></div><span style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;color:#60a5fa">Smart Data Processor</span></div><p style="font-size:16px;font-weight:600;color:#e2e8f0;margin:8px 0 0">Business Intelligence</p></div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### Data source")
    uploaded_file=st.file_uploader("",type=['csv','xlsx','xls'],label_visibility="collapsed")
    use_demo=st.checkbox("Load sample dataset")
    st.markdown("---")
    st.markdown('<p style="font-size:10px;color:#475569;line-height:1.5">All processing happens locally in your browser. No data is stored, transmitted, or shared with third parties.</p>',unsafe_allow_html=True)

# ─── Data ───
df=None
if use_demo:
    import random;random.seed(42);n=200
    clients=['Meridian Group','TechVault Inc','Apex Solutions','CloudBridge','NovaTech','QuantumLeap','BlueShore Capital','Stellar Dynamics']
    services=['AI Integration','Data Pipeline','Automation Setup','Dashboard Build','API Development','ML Model Training']
    statuses=['Paid','Paid','Paid','Paid','Pending','Overdue']
    regions=['Europe','Europe','North America','North America','Asia Pacific','Middle East']
    df=pd.DataFrame({'Invoice_ID':[f'INV-{2000+i}' for i in range(n)],'Date':pd.date_range('2024-01-01',periods=n,freq='2D'),'Client':[random.choice(clients) for _ in range(n)],'Service':[random.choice(services) for _ in range(n)],'Region':[random.choice(regions) for _ in range(n)],'Hours':[round(random.uniform(4,60),1) for _ in range(n)],'Hourly_Rate':[random.choice([45,65,85,100,125,150]) for _ in range(n)],'Total_Amount':[0]*n,'Status':[random.choice(statuses) for _ in range(n)]})
    df['Total_Amount']=(df['Hours']*df['Hourly_Rate']).round(2)
    df.loc[df.sample(15,random_state=42).index,'Total_Amount']*=random.uniform(1.3,2.0)
    df['Total_Amount']=df['Total_Amount'].round(2)
    df['Profit_Margin']=(df['Total_Amount']*pd.Series([random.uniform(0.15,0.55) for _ in range(n)])).round(2)
elif uploaded_file:
    try:df=pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    except Exception as e:st.error(f"Error: {e}")

if df is None:
    st.markdown('<div class="report-header"><div class="report-brand"><div class="report-icon"></div><span class="report-company">Smart Data Processor</span></div><div class="report-title">Business Intelligence Report</div><div class="report-meta">Upload a dataset to generate your executive analysis</div></div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1:st.markdown('<div style="padding:24px 0"><p style="font-size:13px;font-weight:600;color:#1e293b;margin-bottom:6px">1. Upload your data</p><p style="font-size:13px;color:#64748b;line-height:1.6">Any CSV or Excel file — sales records, invoices, financial data, CRM exports.</p></div>',unsafe_allow_html=True)
    with c2:st.markdown('<div style="padding:24px 0"><p style="font-size:13px;font-weight:600;color:#1e293b;margin-bottom:6px">2. Get structured analysis</p><p style="font-size:13px;color:#64748b;line-height:1.6">Each finding answers a specific business question with data as evidence.</p></div>',unsafe_allow_html=True)
    with c3:st.markdown('<div style="padding:24px 0"><p style="font-size:13px;font-weight:600;color:#1e293b;margin-bottom:6px">3. Export & act</p><p style="font-size:13px;color:#64748b;line-height:1.6">Download a multi-sheet Excel report with findings, breakdowns, and recommendations.</p></div>',unsafe_allow_html=True)
    st.info("Use the sidebar to upload a file or check **Load sample dataset** to explore.")
else:
    ct=detect(df)
    for c in ct['datetime']:
        try:df[c]=pd.to_datetime(df[c])
        except:pass

    money_cols=ct['currency']+ct['numeric']
    cat_cols=ct['categorical']
    date_cols=ct['datetime']
    mc=money_cols[0] if money_cols else None
    story=[]
    recs=[]

    # ─── Header ───
    st.markdown(f'<div class="report-header"><div class="report-brand"><div class="report-icon"></div><span class="report-company">Smart Data Processor</span></div><div class="report-title">Business Intelligence Report</div><div class="report-meta">{datetime.now().strftime("%B %d, %Y")} · {len(df):,} records · {len(df.columns)} fields analyzed</div></div>',unsafe_allow_html=True)

    # ─── Executive Summary ───
    if mc:
        total=df[mc].sum();avg=df[mc].mean();med=df[mc].median()
        miss=df.isnull().sum().sum();dups=df.duplicated().sum()

        # Build executive summary text
        exec_parts=[]
        exec_parts.append(f"Total <b>{mc.replace('_',' ').lower()}</b> across {len(df):,} records is <b>${total:,.0f}</b> (avg ${avg:,.0f} per record).")
        if cat_cols:
            top_cat=df.groupby(cat_cols[0])[mc].sum().sort_values(ascending=False)
            top_name=top_cat.index[0];top_pct=top_cat.iloc[0]/total*100
            exec_parts.append(f"<b>{top_name}</b> leads with {top_pct:.0f}% of total value.")
        if date_cols:
            try:
                ts=df.set_index(date_cols[0])[mc].resample('M').sum()
                if len(ts)>=3:
                    recent=ts.iloc[-2:].mean();earlier=ts.iloc[:-2].mean()
                    if earlier>0:
                        ch=(recent-earlier)/earlier*100
                        if ch>10:exec_parts.append(f"Revenue trend is <b>up {ch:.0f}%</b> vs historical average.")
                        elif ch<-10:exec_parts.append(f"Revenue trend is <b>down {abs(ch):.0f}%</b> vs historical average.")
                        else:exec_parts.append("Revenue trend is <b>stable</b>.")
            except:pass
        if miss>0:exec_parts.append(f"{miss} missing values detected — review data quality.")

        st.markdown(f'<div class="exec-summary"><div class="exec-label">Executive summary</div><div class="exec-text">{" ".join(exec_parts)}</div></div>',unsafe_allow_html=True)

        # KPIs
        mx=df[mc].max()
        paid=len(df[df[cat_cols[-1]]=='Paid']) if cat_cols and 'Paid' in df[cat_cols[-1]].values else len(df)
        st.markdown(f'<div class="kpi-row"><div class="kpi kpi-1"><div class="kpi-label">Total value</div><div class="kpi-val">${total:,.0f}</div><div class="kpi-note">{len(df):,} records</div></div><div class="kpi kpi-2"><div class="kpi-label">Average per record</div><div class="kpi-val">${avg:,.0f}</div><div class="kpi-note">Median ${med:,.0f}</div></div><div class="kpi kpi-3"><div class="kpi-label">Largest single record</div><div class="kpi-val">${mx:,.0f}</div><div class="kpi-note">{mx/avg:.1f}x the average</div></div><div class="kpi kpi-4"><div class="kpi-label">Data completeness</div><div class="kpi-val">{100-miss/(df.shape[0]*df.shape[1])*100:.0f}%</div><div class="kpi-note">{miss} missing · {dups} duplicates</div></div></div>',unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # Q1: WHERE IS THE MONEY?
    # ═══════════════════════════════════════════
    if mc and cat_cols:
        st.markdown('<div class="q-section"><div class="q-bar"><span class="q-num">Q1</span><span class="q-text">Where is the money concentrated?</span></div></div>',unsafe_allow_html=True)

        cc=cat_cols[0]
        by_cat=df.groupby(cc)[mc].agg(['sum','mean','count']).sort_values('sum',ascending=False)
        by_cat['pct']=by_cat['sum']/by_cat['sum'].sum()*100

        # Chart
        top8=by_cat.head(8)
        colors=['#1e3a5f' if i==0 else '#3b82f6' if i==1 else '#93c5fd' for i in range(len(top8))]
        fig=go.Figure(go.Bar(y=top8.index[::-1],x=top8['sum'].values[::-1],orientation='h',marker_color=colors[::-1],text=[f'${v:,.0f} ({p:.0f}%)' for v,p in zip(top8['sum'].values[::-1],top8['pct'].values[::-1])],textposition='auto',textfont=dict(size=11,color='white')))
        fig.update_layout(title=f'{mc.replace("_"," ")} by {cc.replace("_"," ")}',yaxis_title='',xaxis_title='',xaxis=dict(showgrid=False,showticklabels=False))
        st.markdown('<div class="chart-wrap">',unsafe_allow_html=True)
        st.plotly_chart(sfig(fig),use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

        # Conclusion
        top2_pct=by_cat['pct'].iloc[:2].sum()
        conc_class='risk' if top2_pct>60 else 'conclusion'
        conc_label='Concentration risk' if top2_pct>60 else 'Finding'
        story.append(('Revenue concentration',f'{by_cat.index[0]} leads with {by_cat["pct"].iloc[0]:.0f}%. Top 2 = {top2_pct:.0f}%.'))

        st.markdown(f'<div class="conclusion {conc_class}"><div class="conclusion-label">{conc_label}</div><b>{by_cat.index[0]}</b> generates {by_cat["pct"].iloc[0]:.0f}% of total {mc.replace("_"," ").lower()} (${by_cat["sum"].iloc[0]:,.0f}). The top 2 ({cc.replace("_"," ").lower()}s) account for <b>{top2_pct:.0f}%</b> combined. {"This level of concentration creates dependency risk — if this segment declines, overall revenue is significantly impacted." if top2_pct>60 else "Distribution is relatively healthy across segments."}</div>',unsafe_allow_html=True)

        if top2_pct>60:recs.append(f"Reduce concentration risk: develop strategies to grow revenue from underperforming {cc.replace('_',' ').lower()} segments.")

        # Second categorical if exists
        if len(cat_cols)>1:
            cc2=cat_cols[1]
            by_c2=df.groupby(cc2)[mc].mean().sort_values(ascending=False).head(8)
            fig2=go.Figure(go.Bar(x=by_c2.index,y=by_c2.values,marker_color=['#1e3a5f' if i==0 else '#93c5fd' for i in range(len(by_c2))],text=[f'${v:,.0f}' for v in by_c2.values],textposition='outside',textfont=dict(size=11,color='#475569')))
            fig2.update_layout(title=f'Average {mc.replace("_"," ")} by {cc2.replace("_"," ")}',xaxis_title='',yaxis_title='',yaxis=dict(showgrid=True))
            st.markdown('<div class="chart-wrap">',unsafe_allow_html=True)
            st.plotly_chart(sfig(fig2,340),use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)

            ratio=by_c2.iloc[0]/by_c2.iloc[-1] if by_c2.iloc[-1]>0 else 0
            story.append(('Value per segment',f'Highest avg: {by_c2.index[0]} (${by_c2.iloc[0]:,.0f}). Lowest: {by_c2.index[-1]} (${by_c2.iloc[-1]:,.0f}). Ratio: {ratio:.1f}x.'))
            st.markdown(f'<div class="conclusion"><div class="conclusion-label">Value analysis</div><b>{by_c2.index[0]}</b> has the highest average value at ${by_c2.iloc[0]:,.0f} per record — <b>{ratio:.1f}x higher</b> than {by_c2.index[-1]} (${by_c2.iloc[-1]:,.0f}). Consider prioritizing high-value {cc2.replace("_"," ").lower()} segments for resource allocation.</div>',unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # Q2: WHAT'S THE TREND?
    # ═══════════════════════════════════════════
    if mc and date_cols:
        st.markdown('<div class="q-section"><div class="q-bar"><span class="q-num">Q2</span><span class="q-text">How is performance changing over time?</span></div></div>',unsafe_allow_html=True)

        dc=date_cols[0]
        ts=df.set_index(dc)[mc].resample('W').sum().reset_index()

        fig3=go.Figure()
        fig3.add_trace(go.Scatter(x=ts[dc],y=ts[mc],mode='lines',line=dict(color='#3b82f6',width=2),fill='tozeroy',fillcolor='rgba(59,130,246,0.06)',name='Weekly'))
        if len(ts)>4:
            ma=ts[mc].rolling(4,min_periods=1).mean()
            fig3.add_trace(go.Scatter(x=ts[dc],y=ma,mode='lines',line=dict(color='#1e3a5f',width=2,dash='dot'),name='4-week moving avg'))
        fig3.update_layout(title=f'{mc.replace("_"," ")} — weekly performance',xaxis_title='',yaxis_title='',showlegend=True,legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='left'))
        st.markdown('<div class="chart-wrap">',unsafe_allow_html=True)
        st.plotly_chart(sfig(fig3),use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)

        # Trend conclusion
        try:
            monthly=df.set_index(dc)[mc].resample('M').sum()
            if len(monthly)>=3:
                recent=monthly.iloc[-2:].mean();earlier=monthly.iloc[:-2].mean()
                if earlier>0:
                    ch=(recent-earlier)/earlier*100
                    if ch>10:
                        story.append(('Trend','Upward — recent periods +{:.0f}% vs average.'.format(ch)))
                        st.markdown(f'<div class="conclusion good"><div class="conclusion-label">Positive trend</div>Recent periods are <b>{ch:.0f}% above</b> the historical average (${recent:,.0f}/month vs ${earlier:,.0f}/month). This upward momentum should be sustained through continued investment in growth drivers.</div>',unsafe_allow_html=True)
                    elif ch<-10:
                        story.append(('Trend','Downward — recent periods {:.0f}% vs average.'.format(ch)))
                        st.markdown(f'<div class="conclusion problem"><div class="conclusion-label">Declining trend</div>Recent periods are <b>{abs(ch):.0f}% below</b> the historical average (${recent:,.0f}/month vs ${earlier:,.0f}/month). Investigate root causes — is this seasonal, client-specific, or systemic?</div>',unsafe_allow_html=True)
                        recs.append("Investigate revenue decline: analyze by segment and time period to identify specific causes.")
                    else:
                        story.append(('Trend','Stable — within ±10% of average.'))
                        st.markdown(f'<div class="conclusion"><div class="conclusion-label">Stable performance</div>Revenue is within <b>±10%</b> of the historical average. Performance is consistent but consider whether current levels meet growth targets.</div>',unsafe_allow_html=True)
        except:pass

    # ═══════════════════════════════════════════
    # Q3: WHAT NEEDS ATTENTION?
    # ═══════════════════════════════════════════
    if mc:
        st.markdown('<div class="q-section"><div class="q-bar"><span class="q-num">Q3</span><span class="q-text">What needs immediate attention?</span></div></div>',unsafe_allow_html=True)

        issues_found=False

        # Outliers
        q1=df[mc].quantile(0.25);q3=df[mc].quantile(0.75);iqr=q3-q1
        outs=df[(df[mc]<q1-1.5*iqr)|(df[mc]>q3+1.5*iqr)]
        if 0<len(outs)<len(df)*0.15:
            issues_found=True
            high_outs=outs[outs[mc]>q3+1.5*iqr]
            low_outs=outs[outs[mc]<q1-1.5*iqr]
            story.append(('Outliers',f'{len(outs)} records outside expected range. Total value: ${outs[mc].sum():,.0f}.'))

            # Show outlier distribution
            fig4=go.Figure()
            fig4.add_trace(go.Histogram(x=df[mc],nbinsx=30,marker_color='#93c5fd',marker_line_width=0,name='Normal'))
            if len(high_outs)>0:
                fig4.add_trace(go.Histogram(x=high_outs[mc],nbinsx=10,marker_color='#ef4444',marker_line_width=0,name=f'High outliers ({len(high_outs)})'))
            if len(low_outs)>0:
                fig4.add_trace(go.Histogram(x=low_outs[mc],nbinsx=10,marker_color='#f59e0b',marker_line_width=0,name=f'Low outliers ({len(low_outs)})'))
            fig4.update_layout(title=f'{mc.replace("_"," ")} distribution with outliers highlighted',barmode='overlay',xaxis_title=mc.replace('_',' '),yaxis_title='Count',showlegend=True,legend=dict(orientation='h',yanchor='bottom',y=1.02))
            fig4.update_traces(opacity=0.7)
            st.markdown('<div class="chart-wrap">',unsafe_allow_html=True)
            st.plotly_chart(sfig(fig4),use_container_width=True)
            st.markdown('</div>',unsafe_allow_html=True)

            st.markdown(f'<div class="conclusion problem"><div class="conclusion-label">{len(outs)} outliers require review</div><b>{len(high_outs)} records</b> are unusually high and <b>{len(low_outs)} records</b> are unusually low compared to the expected range (${q1-1.5*iqr:,.0f} – ${q3+1.5*iqr:,.0f}). Combined outlier value: <b>${outs[mc].sum():,.0f}</b>. Verify whether these represent data errors, exceptional deals, or legitimate edge cases.</div>',unsafe_allow_html=True)
            recs.append(f"Review {len(outs)} flagged outlier records. Verify data accuracy and categorize as legitimate or errors.")

        # Variance
        std=df[mc].std();mean=df[mc].mean()
        if mean>0 and std>mean*0.7:
            issues_found=True
            cv=std/mean*100
            story.append(('Variance',f'High coefficient of variation ({cv:.0f}%). Std dev: ${std:,.0f} vs mean ${mean:,.0f}.'))
            st.markdown(f'<div class="conclusion risk"><div class="conclusion-label">High variance</div>The coefficient of variation is <b>{cv:.0f}%</b> (std dev ${std:,.0f} vs mean ${mean:,.0f}). This means individual records vary significantly from the average — forecasting based on averages alone would be unreliable. Segment the data by category for more accurate projections.</div>',unsafe_allow_html=True)
            recs.append("Create segmented forecasts instead of using overall averages — the high variance makes aggregate projections unreliable.")

        # Missing data
        miss=df.isnull().sum()
        miss_cols=miss[miss>0]
        if len(miss_cols)>0:
            issues_found=True
            st.markdown(f'<div class="conclusion risk"><div class="conclusion-label">Missing data</div>{miss_cols.sum()} missing values across {len(miss_cols)} columns: {", ".join([f"<b>{c}</b> ({v})" for c,v in miss_cols.items()])}. Clean or impute before using this data for decision-making.</div>',unsafe_allow_html=True)
            recs.append(f"Address {miss_cols.sum()} missing values in {len(miss_cols)} columns before using data for reporting.")

        # Status breakdown if exists
        if cat_cols:
            last_cat=cat_cols[-1]
            if any(s in df[last_cat].values for s in['Overdue','overdue','Late','Failed','Cancelled']):
                status_counts=df[last_cat].value_counts()
                problem_statuses=[s for s in['Overdue','overdue','Late','Failed','Cancelled'] if s in status_counts.index]
                if problem_statuses:
                    prob_count=sum(status_counts[s] for s in problem_statuses)
                    prob_pct=prob_count/len(df)*100
                    if mc:
                        prob_value=df[df[last_cat].isin(problem_statuses)][mc].sum()
                        st.markdown(f'<div class="conclusion problem"><div class="conclusion-label">Payment issues</div><b>{prob_count} records ({prob_pct:.1f}%)</b> have problematic status ({", ".join(problem_statuses)}), representing <b>${prob_value:,.0f}</b> in value. Prioritize collection on overdue accounts.</div>',unsafe_allow_html=True)
                        recs.append(f"Prioritize collection: {prob_count} records (${prob_value:,.0f}) are overdue or problematic.")
                        issues_found=True

        if not issues_found:
            st.markdown('<div class="conclusion good"><div class="conclusion-label">All clear</div>No significant outliers, missing data issues, or anomalies detected. Data quality is high and distribution is healthy.</div>',unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # RECOMMENDATIONS
    # ═══════════════════════════════════════════
    if not recs:recs.append("Continue monitoring key metrics monthly using this tool.")
    recs.append("Share this report with stakeholders and schedule a review meeting to align on priorities.")

    st.markdown('<div class="q-section"><div class="q-bar"><span class="q-num">→</span><span class="q-text">Recommended next steps</span></div></div>',unsafe_allow_html=True)

    items=''.join([f'<div class="action-item"><span class="action-num">{i+1}.</span><span>{r}</span></div>' for i,r in enumerate(recs)])
    st.markdown(f'<div class="action-box"><h4>◆ Action items</h4>{items}</div>',unsafe_allow_html=True)

    # ─── Data & Export ───
    with st.expander("View raw data"):st.dataframe(df.head(50),use_container_width=True)

    st.markdown("")
    d1,d2=st.columns(2)
    d1.download_button("Download Excel report",data=make_excel(df,ct,story,recs),file_name=f"report_{datetime.now().strftime('%Y%m%d')}.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    d2.download_button("Download CSV",data=df.to_csv(index=False).encode('utf-8'),file_name=f"data_{datetime.now().strftime('%Y%m%d')}.csv",mime="text/csv")

    st.markdown('<div class="app-footer">Smart Data Processor · Executive Business Intelligence<br>All data processed locally · No information stored or shared</div>',unsafe_allow_html=True)
