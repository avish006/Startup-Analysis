# Indian Startup Ecosystem Analysis Dashboard

This interactive dashboard provides a deep analytical look into the Indian startup funding landscape. Explore trends, track investor behavior, analyze funding rounds, and evaluate the startup ecosystem across industries, cities, and time.

Live Demo 👉 [Click Here to View Dashboard](https://startup-funding-analyzer.streamlit.app/)

## 📌 Project Highlights

- **Time Series Analysis** of monthly & yearly funding trends
- **City & Industry Filters** with cleaned categories (`Bangalore → Bengaluru`, `Fintech`, `EdTech`, etc.)
- **Top Investors** with deal counts and portfolio diversity visualized as donut charts
- **Startup-level Filtering** with smart search + "Select All" toggle
- **Deal Stage & Funding Type Distributions** (Bar & Pie Charts)
- **Top Startups**, **Top Industries**, **Top Cities** by funding
- **Cleaned & deduplicated fields** (e.g. `consumer internet`, `consumer portal` → `Consumer Internet`)
- **Export filtered data as downloadable CSV8**


## 🧠 Technologies Used

- **Python 3.9+**
- **Streamlit** for frontend
- **Pandas** for data wrangling
- **Seaborn / Matplotlib** for plotting
- **GitHub** + **Streamlit Cloud** for deployment


## 🗃️ Dataset

The dataset is sourced from public Kaggle repositories related to Indian startup funding. It includes:

- Startup Name
- Industry
- Investment Type
- Investors
- Amount Raised
- City / Location
- Date of Funding

Dataset: [Download Dataset](https://www.kaggle.com/datasets/riteshsoun/indian-startup-funding-jan-2015-april-2021)

Custom cleaning applied to:
- Merge duplicate industry/location labels
- Standardize missing or unknown values
- Extract relevant columns

