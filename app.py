"""
Smart Data Processor — Executive Business Intelligence
E-commerce / Retail focused. Story-driven analysis with forecasting.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Smart Data Processor",page_icon="◆",layout="wide",initial_sidebar_state="expanded")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.stApp{font-family:'Inter',-apple-system,sans-serif;background:#f8fafc}
#MainMenu,header,footer{visibility:hidden}
section[data-testid="stSidebar"]{background:#0c1929;border-right:1px solid #1a2744}
section[data-testid="stSidebar"] .stMarkdown p,section[data-testid="stSidebar"] label{color:#8298b5!important;font-size:13px}
section[data-testid="stSidebar"] h1,section[data-testid="stSidebar"] h2,section[data-testid="stSidebar"] h3,section[data-testid="stSidebar"] h4{color:#c8d8ec!important}
.block-container{padding-top:2rem;max-width:1060px}
.rh{padding:0 0 20px;border-bottom:2px solid #1e3a5f;margin-bottom:24px}
.rh-brand{display:flex;align-items:center;gap:8px}
.rh-dot{width:10px;height:10px;background:#3b82f6;border-radius:2px}
.rh-co{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:#64748b}
.rh-title{font-size:24px;font-weight:700;color:#0f172a;margin:10px 0 2px;letter-spacing:-0.5px}
.rh-meta{font-size:13px;color:#64748b}
.es{background:#eef4ff;border:1px solid #c7d9f5;border-radius:10px;padding:18px 22px;margin:16px 0}
.es-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#2563eb;margin-bottom:6px}
.es-text{font-size:14px;color:#1e293b;line-height:1.7}
.es-text b{font-weight:600}
.kr{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:16px 0 24px}
.kc{background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:16px;position:relative;overflow:hidden}
.kc::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px}
.kc-1::after{background:#3b82f6}.kc-2::after{background:#10b981}.kc-3::after{background:#f59e0b}.kc-4::after{background:#64748b}
.kc-l{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.7px;color:#64748b;margin-bottom:4px}
.kc-v{font-size:24px;font-weight:700;color:#0f172a;letter-spacing:-0.5px}
.kc-n{font-size:11px;color:#94a3b8;margin-top:3px}
.qs{margin:28px 0 0}
.qb{display:flex;align-items:center;gap:10px;padding-bottom:8px;border-bottom:1px solid #cbd5e1;margin-bottom:14px}
.qn{font-size:12px;font-weight:700;color:#3b82f6}
.qt{font-size:15px;font-weight:600;color:#0f172a}
.co{background:#fff;border:1px solid #e2e8f0;border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;padding:14px 18px;margin:10px 0;font-size:13px;color:#334155;line-height:1.7}
.co.risk{border-left-color:#f59e0b;background:#fffbeb}.co.bad{border-left-color:#ef4444;background:#fef2f2}.co.good{border-left-color:#10b981;background:#f0fdf4}
.co-l{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:3px}
.co .co-l{color:#2563eb}.co.risk .co-l{color:#d97706}.co.bad .co-l{color:#dc2626}.co.good .co-l{color:#059669}
.ab{background:#0c1929;border-radius:10px;padding:20px 22px;margin:16px 0;color:white}
.ab h4{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#60a5fa;margin-bottom:10px}
.ai{display:flex;gap:10px;padding:7px 0;border-bottom:1px solid #1a2744;font-size:13px;color:#c8d8ec;line-height:1.6}
.ai:last-child{border:none}
.ai-n{color:#3b82f6;font-weight:700;min-width:20px}
.cw{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:12px 12px 4px;margin:8px 0}
.af{margin-top:32px;padding:16px 0;border-top:1px solid #e2e8f0;text-align:center;font-size:11px;color:#94a3b8}
.stDownloadButton>button{background:#1e3a5f!important;color:white!important;border:none!important;border-radius:8px!important;font-weight:600!important}
.pt{width:100%;border-collapse:collapse;font-size:13px;margin:8px 0}
.pt th{background:#f1f5f9;padding:10px 12px;text-align:left;font-weight:600;color:#334155;border-bottom:2px solid #e2e8f0;font-size:12px}
.pt td{padding:9px 12px;border-bottom:1px solid #f1f5f9;color:#475569}
.pt tr:hover td{background:#f8fafc}
.pt .num{text-align:right;font-variant-numeric:tabular-nums}
.rank-1{color:#059669;font-weight:600}.rank-bad{color:#dc2626;font-weight:600}
@media(max-width:768px){.kr{grid-template-columns:repeat(2,1fr)}}
</style>
""",unsafe_allow_html=True)

def sfig(fig,h=360):
    fig.update_layout(font=dict(family="Inter",color="#334155",size=12),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=50,r=24,t=56,b=48),height=h,title_font=dict(size=13,color="#475569"),xaxis=dict(gridcolor='#f1f5f9',linecolor='#e2e8f0',tickfont=dict(size=11,color="#64748b")),yaxis=dict(gridcolor='#f1f5f9',linecolor='#e2e8f0',tickfont=dict(size=11,color="#64748b")),legend=dict(font=dict(size=11)))
    return fig

def detect(df):
    t={'numeric':[],'categorical':[],'datetime':[],'text':[],'currency':[]}
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            cl=c.lower()
            if any(w in cl for w in['price','amount','cost','revenue','total','fee','salary','payment','profit','margin','sales','income','expense','budget']):t['currency'].append(c)
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
        df_out=df.copy()
        for c in ct['datetime']:
            try:df_out[c]=df_out[c].dt.strftime('%Y-%m-%d')
            except:pass
        df_out.to_excel(w,sheet_name='Raw Data',index=False)
        ws=w.sheets['Raw Data']
        for i,col in enumerate(df_out.columns,1):
            max_len=max(len(str(col)),df_out.iloc[:50,i-1].astype(str).str.len().max() if len(df_out)>0 else 10)
            ws.column_dimensions[chr(64+i) if i<27 else 'A'+chr(64+i-26)].width=min(max_len+3,30)
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

# Sidebar
with st.sidebar:
    st.markdown('<div style="padding:0.5rem 0 1rem"><div style="display:flex;align-items:center;gap:8px"><div style="width:8px;height:8px;background:#3b82f6;border-radius:2px"></div><span style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;color:#60a5fa">Smart Data Processor</span></div><p style="font-size:16px;font-weight:600;color:#e2e8f0;margin:8px 0 0">Business Intelligence</p></div>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### Data source")
    uploaded_file=st.file_uploader("",type=['csv','xlsx','xls'],label_visibility="collapsed")
    use_demo=st.checkbox("Load sample dataset",help="E-commerce retail sales data")
    st.markdown("---")
    st.markdown('<p style="font-size:10px;color:#475569;line-height:1.5">All processing happens locally.<br>No data is stored or shared.</p>',unsafe_allow_html=True)

# Data
df=None
if use_demo:
    import random;random.seed(42);n=500
    products=['Wireless Headphones','Smart Watch','Laptop Stand','USB-C Hub','Mechanical Keyboard','Monitor Light Bar','Webcam HD','Desk Mat','Phone Charger','Bluetooth Speaker']
    categories=['Electronics','Accessories','Audio','Computing','Peripherals']
    regions=['North America','Europe','Asia Pacific','Latin America']
    channels=['Online Store','Amazon','Retail Partners','Direct Sales']
    reps=['Sarah Chen','Marcus Webb','Elena Rossi','James Park','Olivia Santos']
    prod_cat={'Wireless Headphones':'Audio','Smart Watch':'Electronics','Laptop Stand':'Accessories','USB-C Hub':'Computing','Mechanical Keyboard':'Peripherals','Monitor Light Bar':'Accessories','Webcam HD':'Electronics','Desk Mat':'Accessories','Phone Charger':'Electronics','Bluetooth Speaker':'Audio'}
    dates=pd.date_range('2023-01-01','2024-12-31',periods=n)
    data={'Order_ID':[f'ORD-{10000+i}' for i in range(n)],'Date':dates,'Product':[random.choice(products) for _ in range(n)],'Region':[random.choice(regions) for _ in range(n)],'Sales_Channel':[random.choice(channels) for _ in range(n)],'Sales_Rep':[random.choice(reps) for _ in range(n)],'Units_Sold':[random.randint(1,25) for _ in range(n)],'Unit_Price':[0.0]*n,'Revenue':[0.0]*n,'Cost':[0.0]*n}
    df=pd.DataFrame(data)
    df['Category']=df['Product'].map(prod_cat)
    prices={'Wireless Headphones':79.99,'Smart Watch':199.99,'Laptop Stand':49.99,'USB-C Hub':34.99,'Mechanical Keyboard':129.99,'Monitor Light Bar':59.99,'Webcam HD':89.99,'Desk Mat':29.99,'Phone Charger':24.99,'Bluetooth Speaker':69.99}
    df['Unit_Price']=df['Product'].map(prices)
    df['Revenue']=(df['Units_Sold']*df['Unit_Price']).round(2)
    margins={'Audio':0.45,'Electronics':0.35,'Accessories':0.55,'Computing':0.30,'Peripherals':0.40}
    df['Cost']=(df['Revenue']*(1-df['Category'].map(margins))).round(2)
    df['Profit']=(df['Revenue']-df['Cost']).round(2)
    # Add seasonality
    df.loc[df['Date'].dt.month==11,'Revenue']*=1.6
    df.loc[df['Date'].dt.month==12,'Revenue']*=1.8
    df.loc[df['Date'].dt.month==11,'Profit']*=1.6
    df.loc[df['Date'].dt.month==12,'Profit']*=1.8
    df['Revenue']=df['Revenue'].round(2);df['Profit']=df['Profit'].round(2)
elif uploaded_file:
    try:df=pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    except Exception as e:st.error(f"Error: {e}")

if df is None:
    st.markdown('<div class="rh"><div class="rh-brand"><div class="rh-dot"></div><span class="rh-co">Smart Data Processor</span></div><div class="rh-title">Business Intelligence Report</div><div class="rh-meta">Upload a dataset to generate your executive analysis</div></div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1:st.markdown('<div style="padding:20px 0"><p style="font-size:14px;font-weight:600;color:#0f172a;margin-bottom:6px">1. Upload your data</p><p style="font-size:13px;color:#64748b;line-height:1.6">CSV or Excel — sales records, invoices, financial data, CRM exports, inventory reports.</p></div>',unsafe_allow_html=True)
    with c2:st.markdown('<div style="padding:20px 0"><p style="font-size:14px;font-weight:600;color:#0f172a;margin-bottom:6px">2. Get structured insights</p><p style="font-size:13px;color:#64748b;line-height:1.6">Each finding answers a business question — with data as evidence and recommendations attached.</p></div>',unsafe_allow_html=True)
    with c3:st.markdown('<div style="padding:20px 0"><p style="font-size:14px;font-weight:600;color:#0f172a;margin-bottom:6px">3. Export & act</p><p style="font-size:13px;color:#64748b;line-height:1.6">Download multi-sheet Excel reports with breakdowns, forecasts, and action items.</p></div>',unsafe_allow_html=True)
    st.info("Use the sidebar to upload a file or check **Load sample dataset** to explore.")
else:
    ct=detect(df)
    for c in ct['datetime']:
        try:df[c]=pd.to_datetime(df[c])
        except:pass
    mc=ct['currency'][0] if ct['currency'] else (ct['numeric'][0] if ct['numeric'] else None)
    story=[];recs=[]

    # Header
    st.markdown(f'<div class="rh"><div class="rh-brand"><div class="rh-dot"></div><span class="rh-co">Smart Data Processor</span></div><div class="rh-title">Business Intelligence Report</div><div class="rh-meta">{datetime.now().strftime("%B %d, %Y")} · {len(df):,} records · {len(df.columns)} fields</div></div>',unsafe_allow_html=True)

    if mc:
        total=df[mc].sum();avg=df[mc].mean();med=df[mc].median();mx=df[mc].max()
        miss=df.isnull().sum().sum()
        # Exec summary
        ep=[f"Total <b>{mc.replace('_',' ').lower()}</b> across {len(df):,} orders is <b>${total:,.0f}</b>."]
        if ct['categorical']:
            tc=df.groupby(ct['categorical'][0])[mc].sum().sort_values(ascending=False)
            ep.append(f"<b>{tc.index[0]}</b> leads at {tc.iloc[0]/total*100:.0f}% share.")
        if ct['datetime']:
            try:
                ts=df.set_index(ct['datetime'][0])[mc].resample('M').sum()
                if len(ts)>=6:
                    h1=ts.iloc[:len(ts)//2].mean();h2=ts.iloc[len(ts)//2:].mean()
                    ch=(h2-h1)/h1*100
                    if ch>5:ep.append(f"Second half trending <b>+{ch:.0f}%</b> above first half.")
                    elif ch<-5:ep.append(f"Second half trending <b>{ch:.0f}%</b> below first half.")
            except:pass
        st.markdown(f'<div class="es"><div class="es-label">Executive summary</div><div class="es-text">{" ".join(ep)}</div></div>',unsafe_allow_html=True)

        # KPIs
        profit_col=[c for c in ct['currency'] if 'profit' in c.lower()]
        profit_total=df[profit_col[0]].sum() if profit_col else total*0.35
        margin_pct=profit_total/total*100 if total>0 else 0
        st.markdown(f'<div class="kr"><div class="kc kc-1"><div class="kc-l">Total {mc.replace("_"," ")}</div><div class="kc-v">${total:,.0f}</div><div class="kc-n">{len(df):,} orders</div></div><div class="kc kc-2"><div class="kc-l">Gross profit</div><div class="kc-v">${profit_total:,.0f}</div><div class="kc-n">Margin: {margin_pct:.1f}%</div></div><div class="kc kc-3"><div class="kc-l">Average order</div><div class="kc-v">${avg:,.0f}</div><div class="kc-n">Median: ${med:,.0f}</div></div><div class="kc kc-4"><div class="kc-l">Largest order</div><div class="kc-v">${mx:,.0f}</div><div class="kc-n">{mx/avg:.1f}x average</div></div></div>',unsafe_allow_html=True)

    # ═══ Q1: REVENUE BREAKDOWN ═══
    if mc and ct['categorical']:
        st.markdown('<div class="qs"><div class="qb"><span class="qn">Q1</span><span class="qt">Where is the revenue concentrated?</span></div></div>',unsafe_allow_html=True)
        cc=ct['categorical'][0];by_cat=df.groupby(cc)[mc].sum().sort_values(ascending=True)
        colors=['#1e3a5f' if i==len(by_cat)-1 else '#3b82f6' if i>=len(by_cat)-3 else '#93c5fd' for i in range(len(by_cat))]
        fig=go.Figure(go.Bar(y=by_cat.index,x=by_cat.values,orientation='h',marker_color=colors,text=[f'${v:,.0f}' for v in by_cat.values],textposition='inside',textfont=dict(size=11,color='white'),insidetextanchor='end'))
        fig.update_layout(title=f'{mc.replace("_"," ")} by {cc.replace("_"," ")}',yaxis_title='',xaxis=dict(showgrid=False,showticklabels=False))
        st.markdown('<div class="cw">',unsafe_allow_html=True);st.plotly_chart(sfig(fig),use_container_width=True);st.markdown('</div>',unsafe_allow_html=True)
        top2=by_cat.iloc[-2:].sum()/by_cat.sum()*100
        cclass='risk' if top2>60 else 'co'
        story.append(('Concentration',f'{by_cat.index[-1]} leads. Top 2 = {top2:.0f}%.'))
        st.markdown(f'<div class="co {cclass}"><div class="co-l">{"Concentration risk" if top2>60 else "Revenue distribution"}</div><b>{by_cat.index[-1]}</b> generates {by_cat.iloc[-1]/by_cat.sum()*100:.0f}% of total revenue. Top 2 segments account for <b>{top2:.0f}%</b>. {"High concentration — diversification recommended." if top2>60 else "Distribution is relatively balanced."}</div>',unsafe_allow_html=True)
        if top2>60:recs.append("Reduce revenue concentration by investing in growth of underperforming segments.")

    # ═══ Q2: TOP & BOTTOM PERFORMERS ═══
    if mc and ct['categorical']:
        st.markdown('<div class="qs"><div class="qb"><span class="qn">Q2</span><span class="qt">Who are the top and bottom performers?</span></div></div>',unsafe_allow_html=True)
        # Try different categoricals for best performer table
        perf_col=ct['categorical'][1] if len(ct['categorical'])>1 else ct['categorical'][0]
        perf=df.groupby(perf_col)[mc].agg(['sum','mean','count']).round(2).sort_values('sum',ascending=False)
        perf['share']=(perf['sum']/perf['sum'].sum()*100).round(1)
        top5=perf.head(5);bot3=perf.tail(3) if len(perf)>5 else pd.DataFrame()

        # Top performers table
        rows=""
        for i,(idx,r) in enumerate(top5.iterrows()):
            cls='rank-1' if i==0 else ''
            rows+=f'<tr><td class="{cls}">{i+1}. {idx}</td><td class="num">${r["sum"]:,.0f}</td><td class="num">${r["mean"]:,.0f}</td><td class="num">{r["count"]:.0f}</td><td class="num">{r["share"]}%</td></tr>'
        st.markdown(f'<div class="cw" style="padding:16px"><p style="font-size:12px;font-weight:600;color:#059669;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">Top performers — {perf_col.replace("_"," ")}</p><table class="pt"><tr><th>{perf_col.replace("_"," ")}</th><th style="text-align:right">Total {mc.replace("_"," ")}</th><th style="text-align:right">Average</th><th style="text-align:right">Orders</th><th style="text-align:right">Share</th></tr>{rows}</table></div>',unsafe_allow_html=True)

        if len(bot3)>0:
            brows=""
            for i,(idx,r) in enumerate(bot3.iterrows()):
                brows+=f'<tr><td class="rank-bad">{idx}</td><td class="num">${r["sum"]:,.0f}</td><td class="num">${r["mean"]:,.0f}</td><td class="num">{r["count"]:.0f}</td><td class="num">{r["share"]}%</td></tr>'
            st.markdown(f'<div class="cw" style="padding:16px"><p style="font-size:12px;font-weight:600;color:#dc2626;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px">Underperformers — need attention</p><table class="pt"><tr><th>{perf_col.replace("_"," ")}</th><th style="text-align:right">Total</th><th style="text-align:right">Average</th><th style="text-align:right">Orders</th><th style="text-align:right">Share</th></tr>{brows}</table></div>',unsafe_allow_html=True)
            story.append(('Performers',f'Top: {top5.index[0]}. Bottom: {bot3.index[0]}.'))
            st.markdown(f'<div class="co"><div class="co-l">Performance gap</div><b>{top5.index[0]}</b> outperforms <b>{bot3.index[0]}</b> by {top5["sum"].iloc[0]/bot3["sum"].iloc[0]:.1f}x in total revenue. Evaluate whether underperformers need more resources or should be phased out.</div>',unsafe_allow_html=True)
            recs.append(f"Investigate why {bot3.index[0]} underperforms — is it market conditions, pricing, or lack of investment?")

    # ═══ Q3: TREND + YoY ═══
    if mc and ct['datetime']:
        dc=ct['datetime'][0]
        st.markdown('<div class="qs"><div class="qb"><span class="qn">Q3</span><span class="qt">How is performance trending over time?</span></div></div>',unsafe_allow_html=True)
        ts=df.set_index(dc)[mc].resample('W').sum().reset_index()
        fig2=go.Figure()
        fig2.add_trace(go.Scatter(x=ts[dc],y=ts[mc],mode='lines',line=dict(color='#3b82f6',width=2),fill='tozeroy',fillcolor='rgba(59,130,246,0.06)',name='Weekly'))
        if len(ts)>4:
            ma=ts[mc].rolling(4,min_periods=1).mean()
            fig2.add_trace(go.Scatter(x=ts[dc],y=ma,mode='lines',line=dict(color='#1e3a5f',width=2,dash='dot'),name='4-week avg'))
        fig2.update_layout(title=f'{mc.replace("_"," ")} — weekly trend',showlegend=True,legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='left'),xaxis_title='',yaxis_title='')
        st.markdown('<div class="cw">',unsafe_allow_html=True);st.plotly_chart(sfig(fig2),use_container_width=True);st.markdown('</div>',unsafe_allow_html=True)

        # YoY comparison
        monthly=df.set_index(dc)[mc].resample('M').sum()
        years=monthly.index.year.unique()
        if len(years)>=2:
            st.markdown('<p style="font-size:13px;font-weight:600;color:#334155;margin:16px 0 8px">Year-over-year comparison</p>',unsafe_allow_html=True)
            fig_yoy=go.Figure()
            ycolors=['#93c5fd','#3b82f6','#1e3a5f']
            for i,yr in enumerate(sorted(years)):
                yr_data=monthly[monthly.index.year==yr]
                fig_yoy.add_trace(go.Bar(x=[d.strftime('%b') for d in yr_data.index],y=yr_data.values,name=str(yr),marker_color=ycolors[i%len(ycolors)]))
            fig_yoy.update_layout(title='Monthly revenue — year over year',barmode='group',xaxis_title='',yaxis_title='',legend=dict(orientation='h',yanchor='bottom',y=1.02))
            st.markdown('<div class="cw">',unsafe_allow_html=True);st.plotly_chart(sfig(fig_yoy),use_container_width=True);st.markdown('</div>',unsafe_allow_html=True)

            # YoY growth calc
            for yr in sorted(years):
                if yr>years.min():
                    curr=monthly[monthly.index.year==yr].sum()
                    prev=monthly[monthly.index.year==yr-1].sum()
                    if prev>0:
                        growth=(curr-prev)/prev*100
                        cls='good' if growth>0 else 'bad'
                        story.append(('YoY',f'{yr} vs {yr-1}: {"+" if growth>0 else ""}{growth:.0f}%'))
                        st.markdown(f'<div class="co {cls}"><div class="co-l">{yr} vs {yr-1}</div>Revenue {"grew" if growth>0 else "declined"} by <b>{abs(growth):.1f}%</b> year-over-year (${prev:,.0f} → ${curr:,.0f}). {"Strong growth momentum — maintain current strategies." if growth>10 else "Modest growth — explore new channels." if growth>0 else "Declining — investigate causes and reallocate budget."}</div>',unsafe_allow_html=True)

    # ═══ Q4: FORECAST ═══
    if mc and ct['datetime']:
        st.markdown('<div class="qs"><div class="qb"><span class="qn">Q4</span><span class="qt">What does the forecast look like?</span></div></div>',unsafe_allow_html=True)
        monthly=df.set_index(ct['datetime'][0])[mc].resample('M').sum()
        if len(monthly)>=4:
            x=np.arange(len(monthly));y=monthly.values
            z=np.polyfit(x,y,1);p=np.poly1d(z)
            # Forecast next 6 months
            future_x=np.arange(len(monthly),len(monthly)+6)
            future_y=p(future_x)
            future_dates=pd.date_range(monthly.index[-1]+pd.DateOffset(months=1),periods=6,freq='M')

            fig_fc=go.Figure()
            fig_fc.add_trace(go.Scatter(x=monthly.index,y=monthly.values,mode='lines+markers',line=dict(color='#3b82f6',width=2),marker=dict(size=4),name='Actual'))
            fig_fc.add_trace(go.Scatter(x=monthly.index,y=p(x),mode='lines',line=dict(color='#64748b',width=1,dash='dot'),name='Trend'))
            fig_fc.add_trace(go.Scatter(x=future_dates,y=future_y,mode='lines+markers',line=dict(color='#10b981',width=2,dash='dash'),marker=dict(size=5,symbol='diamond'),name='Forecast (6 months)',fill='tozeroy',fillcolor='rgba(16,185,129,0.05)'))
            fig_fc.update_layout(title='Revenue forecast — 6-month projection (linear trend)',showlegend=True,legend=dict(orientation='h',yanchor='bottom',y=1.02),xaxis_title='',yaxis_title='')
            st.markdown('<div class="cw">',unsafe_allow_html=True);st.plotly_chart(sfig(fig_fc,380),use_container_width=True);st.markdown('</div>',unsafe_allow_html=True)

            monthly_growth=z[0]
            fc_total=future_y.sum()
            direction='upward' if monthly_growth>0 else 'downward'
            story.append(('Forecast',f'6-month projection: ${fc_total:,.0f}. Trend: {direction}.'))
            st.markdown(f'<div class="co {"good" if monthly_growth>0 else "risk"}"><div class="co-l">6-month forecast</div>Based on historical trend, projected revenue for the next 6 months is <b>${fc_total:,.0f}</b> (avg ${fc_total/6:,.0f}/month). Trend direction: <b>{direction}</b>. Note: this is a linear projection — actual results will vary based on seasonality and business decisions.</div>',unsafe_allow_html=True)
            recs.append("Use this forecast as a baseline for budget planning. Adjust for known seasonality (Q4 holiday peaks) and planned campaigns.")

    # ═══ Q5: ATTENTION ═══
    if mc:
        st.markdown('<div class="qs"><div class="qb"><span class="qn">Q5</span><span class="qt">What needs immediate attention?</span></div></div>',unsafe_allow_html=True)
        issues=False
        q1=df[mc].quantile(0.25);q3=df[mc].quantile(0.75);iqr=q3-q1
        outs=df[(df[mc]<q1-1.5*iqr)|(df[mc]>q3+1.5*iqr)]
        if 0<len(outs)<len(df)*0.15:
            issues=True
            story.append(('Outliers',f'{len(outs)} records outside normal range.'))
            st.markdown(f'<div class="co bad"><div class="co-l">{len(outs)} outliers detected</div><b>{len(outs)}</b> orders ({len(outs)/len(df)*100:.1f}%) fall outside the expected range (${q1-1.5*iqr:,.0f} – ${q3+1.5*iqr:,.0f}). Combined value: <b>${outs[mc].sum():,.0f}</b>. Review for data errors or investigate as exceptional transactions.</div>',unsafe_allow_html=True)
            recs.append(f"Review {len(outs)} flagged outlier orders for data accuracy.")

        std=df[mc].std();mean=df[mc].mean()
        if mean>0 and std>mean*0.7:
            issues=True
            st.markdown(f'<div class="co risk"><div class="co-l">High variance</div>Standard deviation (${std:,.0f}) is {std/mean*100:.0f}% of the mean. Individual orders vary significantly — segment by category for more accurate projections.</div>',unsafe_allow_html=True)

        miss=df.isnull().sum();miss_cols=miss[miss>0]
        if len(miss_cols)>0:
            issues=True
            st.markdown(f'<div class="co risk"><div class="co-l">Missing data</div>{miss_cols.sum()} missing values across {len(miss_cols)} columns. Clean before using for decisions.</div>',unsafe_allow_html=True)
            recs.append(f"Fix {miss_cols.sum()} missing values before reporting.")
        if not issues:
            st.markdown('<div class="co good"><div class="co-l">All clear</div>No significant outliers or data quality issues. Data is clean and ready for decision-making.</div>',unsafe_allow_html=True)

    # ═══ RECOMMENDATIONS ═══
    if not recs:recs.append("Data looks healthy. Continue monitoring monthly.")
    recs.append("Share this report with stakeholders and align on priorities for next quarter.")
    st.markdown('<div class="qs"><div class="qb"><span class="qn">→</span><span class="qt">Recommended next steps</span></div></div>',unsafe_allow_html=True)
    items=''.join([f'<div class="ai"><span class="ai-n">{i+1}.</span><span>{r}</span></div>' for i,r in enumerate(recs)])
    st.markdown(f'<div class="ab"><h4>◆ Action items</h4>{items}</div>',unsafe_allow_html=True)

    # Data & Export
    with st.expander("View raw data"):st.dataframe(df.head(50),use_container_width=True)
    st.markdown("")
    d1,d2=st.columns(2)
    d1.download_button("Download Excel report",data=make_excel(df,ct,story,recs),file_name=f"report_{datetime.now().strftime('%Y%m%d')}.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    d2.download_button("Download CSV",data=df.to_csv(index=False).encode('utf-8'),file_name=f"data_{datetime.now().strftime('%Y%m%d')}.csv",mime="text/csv")
    st.markdown('<div class="af">Smart Data Processor · Executive Business Intelligence<br>All data processed locally · No information stored or shared</div>',unsafe_allow_html=True)
