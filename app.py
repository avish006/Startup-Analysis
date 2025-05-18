import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import numpy as np

st.set_page_config(page_title="Startup Ecosystem Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("D:\VSCode Projects\Startup Analysis Project\cleaned_startup_data (1).csv")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.to_period('M')
    return df

df = load_data()

def human_format(num):
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f} Billion"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.2f} Million"
    elif num >= 1_000:
        return f"{num / 1_000:.2f} Thousand"
    else:
        return str(num)

# Sidebar filters
st.sidebar.header("Filters")
year_filter = st.sidebar.multiselect("Select Year(s)", sorted(df['Year'].dropna().unique()), default=sorted(df['Year'].dropna().unique()))


st.sidebar.subheader("Industry Filter")
select_all_industry = st.sidebar.checkbox("Select All Industry", value=True)

all_industry = sorted(df['Industry'].dropna().unique())

if select_all_industry:
    industry_filter = all_industry
else:
    industry_filter = st.sidebar.multiselect(
        "Search & Select Industry(s)",
        options=all_industry,
        default=[]
    )


st.sidebar.subheader("Startup Filter")
select_all_startups = st.sidebar.checkbox("Select All Startups", value=True)

all_startups = sorted(df['Startup Name'].dropna().unique())

if select_all_startups:
    startup_filter = all_startups
else:
    startup_filter = st.sidebar.multiselect(
        "Search & Select Startup(s)",
        options=all_startups,
        default=[]
    )
filtered_df = df[
    (df['Year'].isin(year_filter)) &
    (df['Industry'].isin(industry_filter)) &
    (df['Startup Name'].isin(startup_filter))
]

# Header
st.title("📊 Indian Startup Ecosystem Dashboard")
st.markdown("Gain insights into funding patterns, top industries, investor behavior, and growth trends.")

# KPIs
col1, col2, col3 = st.columns(3)
val = human_format(filtered_df['Amount in USD'].sum())
col1.metric("💰 Total Funding", f"${val}")
col2.metric("🚀 Startups Funded", f"{filtered_df['Startup Name'].nunique()}")
col3.metric("📅 Time Span", f"{filtered_df['Year'].min()} - {filtered_df['Year'].max()}")

st.divider()

# Tabs for better UX
tab1, tab2, tab3 = st.tabs(["📈 Funding Trends", "🌆 Geography & Industry", "🧠 Investors & Startups"])

with tab1:
    # Monthly funding trend
    st.subheader("📈 Monthly Funding Over Time")
    monthly_funding = filtered_df.copy()
    monthly_funding['Month'] = monthly_funding['Date'].dt.to_period('M').astype(str)
    monthly_funding = monthly_funding.groupby('Month')['Amount in USD'].sum().reset_index()

    labels = monthly_funding['Month'].values
    steps = 6
    tick_positions = range(0, len(labels), steps)
    tick_labels = labels[::steps]

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=monthly_funding, x='Month', y='Amount in USD', ax=ax1)
    ax1.set_xticks(tick_positions)
    ax1.set_xticklabels(tick_labels, rotation=45)
    ax1.set_title("Monthly Funding Trends")
    ax1.tick_params(axis='x', rotation=45)
    st.pyplot(fig1)
    

    # Yearly growth
    st.subheader("📉 Year-over-Year Funding Growth")
    yearly_growth = filtered_df.groupby('Year')['Amount in USD'].sum().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=yearly_growth, x='Year', y='Amount in USD', marker='o', ax=ax2)
    ax2.set_title("Total Funding by Year")
    st.pyplot(fig2)

    # Average funding by industry
    st.subheader("💸 Avg. Funding by Industry")
    avg_funding = filtered_df.groupby('Industry')['Amount in USD'].mean().sort_values(ascending=False).head(10).reset_index()
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=avg_funding, x='Amount in USD', y='Industry', palette='cubehelix', ax=ax3)
    ax3.set_title("Top 10 Industries by Avg. Deal Size")
    st.pyplot(fig3)

with tab2:
    # Top funded industries
    st.subheader("🏭 Top Funded Industries")
    industry_funding = filtered_df.groupby('Industry')['Amount in USD'].sum().sort_values(ascending=False).head(10).reset_index()
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=industry_funding, y='Industry', x='Amount in USD', palette='magma', ax=ax4)
    ax4.set_title("Top Funded Industries")
    st.pyplot(fig4)

    # Funding by city
    st.subheader("🌆 Funding by City")
    city_funding = filtered_df.groupby('Location')['Amount in USD'].sum().sort_values(ascending=False).head(10).reset_index()
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=city_funding, x='Location', y='Amount in USD', palette='coolwarm', ax=ax5)
    ax5.set_title("Top Cities by Total Funding")
    st.pyplot(fig5)

    # Funding type pie
    st.subheader("🥧 Funding Type Distribution")
    type_dist = filtered_df['Investment Type'].value_counts().head(5)

    fig6, ax6 = plt.subplots(figsize=(7, 7))

    # Plot the donut chart without labels or percentages
    wedges, texts = ax6.pie(
        type_dist,
        labels=None,
        startangle=90,
        wedgeprops=dict(width=0.5),
    )

    # Custom label placement: outside with lines
    for i, wedge in enumerate(wedges):
        angle = (wedge.theta2 + wedge.theta1) / 2
        x = np.cos(np.deg2rad(angle))
        y = np.sin(np.deg2rad(angle))

        # Position outside the donut
        label_x = 1.2 * x
        label_y = 1.2 * y

        percent = 100 * type_dist.values[i] / type_dist.sum()
        ax6.text(label_x, label_y, f"{percent:.1f}%", ha='center', va='center', fontsize=10)

        # Draw the leader line
        ax6.plot([0.5 * x, label_x], [0.5 * y, label_y], color='gray', lw=0.8)

    # Add legend
    ax6.legend(wedges, type_dist.index, title="Funding Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax6.set_title("Top Funding Types", fontsize=14)
    ax6.axis('equal')

    st.pyplot(fig6)


    # Funding stage count
    st.subheader("🪜 Deal Count by Stage")
    stage_count = filtered_df['Investment Type'].value_counts().reset_index().head(10)

    stage_count.columns = ['Stage', 'Count']
    fig7, ax7 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=stage_count, x='Stage', y='Count', palette='Set2', ax=ax7)
    ax7.set_title("Deals by Investment Stage")
    ax7.set_xticklabels(ax7.get_xticklabels(), rotation=45)
    st.pyplot(fig7)

with tab3:
    # Top investors
    st.subheader("🧠 Top Investors by Deal Count")
    top_investors = filtered_df['Investors'].dropna().str.split(',').explode().str.strip()
    top_investors_count = top_investors.value_counts().head(10).reset_index()
    top_investors_count.columns = ['Investor', 'Deals']
    fig8, ax8 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top_investors_count, x='Deals', y='Investor', palette='viridis', ax=ax8)
    ax8.set_title("Most Active Investors")
    st.pyplot(fig8)

    # Top funded startups
    st.subheader("🏆 Top Funded Startups")
    top_startups = filtered_df.groupby('Startup Name')['Amount in USD'].sum().sort_values(ascending=False).head(10).reset_index()
    fig9, ax9 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top_startups, x='Amount in USD', y='Startup Name', palette='YlGnBu', ax=ax9)
    ax9.set_title("Top 10 Funded Startups")
    st.pyplot(fig9)

    # Investor diversity donut
    st.subheader("🎯 Investor Portfolio Diversity")
    selected_investor = st.selectbox("Choose an Investor", options=top_investors_count['Investor'])
    investor_df = filtered_df[filtered_df['Investors'].str.contains(selected_investor, case=False, na=False)]
    sector_distribution = investor_df['Industry'].value_counts().head(5)
    fig10, ax10 = plt.subplots()
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return f'{pct:.1f}%\n({val:,})'
        return my_autopct

    ax10.pie(sector_distribution, labels=sector_distribution.index, startangle=90,
            wedgeprops=dict(width=0.5),
            autopct=make_autopct(sector_distribution.values))
    ax10.set_title(f"{selected_investor}'s Top Industries")
    st.pyplot(fig10)

# Download section
st.subheader("📥 Download Filtered Data")
buffer = BytesIO()
filtered_df.to_csv(buffer, index=False)
st.download_button("Download CSV", buffer.getvalue(), "filtered_data.csv", "text/csv")

st.caption("Made with ❤️ by Avish")
