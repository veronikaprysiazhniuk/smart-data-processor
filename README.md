# 📊 Smart Data Processor

> AI-powered data analysis tool that transforms messy business data into clean reports with insights and visualizations.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red)
![License](https://img.shields.io/badge/License-MIT-green)

## What It Does

Upload any CSV or Excel file and get:
- **Automatic column detection** — identifies currency, dates, categories, and numeric data
- **AI-powered insights** — outlier detection, correlations, distribution analysis
- **Interactive visualizations** — bar charts, time series, distributions, pie charts
- **Downloadable reports** — clean Excel workbook with multiple analysis sheets

## Use Cases

| Industry | Problem Solved | Time Saved |
|----------|---------------|------------|
| Finance | Invoice analysis & anomaly detection | 3+ hours/report |
| Sales | Pipeline analysis by category/rep | 2+ hours/report |
| E-commerce | Revenue breakdown by product/channel | 2+ hours/report |
| Any | Messy spreadsheet → clean report | 1-3 hours |

## Quick Start

```bash
# Clone
git clone https://github.com/veronikaprysiazhniuk/smart-data-processor.git
cd smart-data-processor

# Install
pip install -r requirements.txt

# Run
streamlit run app.py
```

## Deploy (Free)

### Streamlit Cloud (Recommended)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → Deploy

### Railway / Render
Both offer free tiers. Just connect your GitHub repo.

## Tech Stack

- **Python 3.10+** — Core language
- **Pandas** — Data processing & analysis
- **Plotly** — Interactive visualizations
- **Streamlit** — Web interface
- **OpenPyXL** — Excel report generation

## How It Works

1. **Upload** → File is read and parsed (CSV or Excel)
2. **Detect** → Columns are auto-categorized (currency, date, categorical, numeric)
3. **Analyze** → Statistical analysis + business insight generation
4. **Visualize** → Charts auto-generated based on data types
5. **Export** → Multi-sheet Excel report with insights

## Screenshots

*[Add screenshots of your running app here]*

## Author

**Veronika Prysiazhniuk** — Data Analyst & AI Automation Specialist

- Physics background with ML research experience
- Specializing in turning business data into actionable insights
- Available for freelance projects: https://www.upwork.com/freelancers/~01d67eff79a13e80dc?mp_source=share

## License

MIT License — free to use and modify.
