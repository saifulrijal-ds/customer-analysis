import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')
st.title("Customer Analysis")
st.header("RFM and Quartile Analysis")

@st.cache_data
def load_data():
    df = pd.read_csv("data/Customer analysis.csv", sep='\t')
    df["MntAllProducts_Monetary"] = df[[
        "MntWines", 
        "MntFruits", 
        "MntMeatProducts", 
        "MntFishProducts", 
        "MntSweetProducts", 
        "MntGoldProds"
        ]].sum(axis=1)
    df["NumAllPurchases_Frequency"] = df[[
        "NumWebPurchases", 
        "NumCatalogPurchases", 
        "NumStorePurchases"]].sum(axis=1)
    df['Recency_Quartile'] = pd.qcut(df['Recency'], 4, labels=list(range(1, 5)))
    df['Frequency_Quartile'] = pd.qcut(df['NumAllPurchases_Frequency'], 4, labels=list(range(4, 0, -1)))
    df['Monetary_Quartile'] = pd.qcut(df['MntAllProducts_Monetary'], 4, labels=list(range(4, 0, -1)))
    df['RFM_Score'] = df['Recency_Quartile'].astype(str) + df['Frequency_Quartile'].astype(str) + df['Monetary_Quartile'].astype(str)
    def categorize_rfm(x):
        if x == '111':
            return 'Core'
        elif x[1] == '1':
            return 'Loyal'
        elif x[2] == '1':
            return 'Whales'
        elif x[-2:] in ['13', '14']:
            return 'Promising'
        elif x.startswith('14'):
            return 'Rookies'
        elif x.startswith('44'):
            return 'Slipping'
        elif x.endswith('4'):
            return 'Risk'
        elif x.startswith('4'):
            return 'Churned'
        else:
            return 'Regular'
    df['RFM_Category'] = df['RFM_Score'].apply(categorize_rfm)
    return df

df = load_data()
st.subheader("Dataset")
st.dataframe(df)

def plot_recency_distribution():
    st.subheader("Recency : Number of days since customer's last purchase")
    fig = px.histogram(df, x='Recency')
    st.plotly_chart(fig)

st.header("Recency")
plot_recency_distribution()

st.header("Frequency")
freq_col_1, freq_col_2 = st.columns(2)

@st.experimental_fragment
def plot_frequency_histogram():
    st.subheader("Distribution of number of purchases")
    selected_freq_column = st.selectbox("Select a column", 
                                        ["NumWebPurchases", 
                                         "NumCatalogPurchases", 
                                         "NumStorePurchases", 
                                         "NumAllPurchases_Frequency"])
    fig = px.histogram(df, x=selected_freq_column)
    st.plotly_chart(fig)

with freq_col_1:
    plot_frequency_histogram()

def plot_freq_corr():
    st.subheader("Correlation between places (number of purchases)")
    corr_matrix = df[[
        "NumWebPurchases", 
        "NumCatalogPurchases", 
        "NumStorePurchases"
    ]].corr(method='spearman')
    fig = px.imshow(corr_matrix, text_auto=True)
    st.plotly_chart(fig)

with freq_col_2:
    plot_freq_corr()

st.header("Monetary")
product_col_1, product_col_2 = st.columns(2)

@st.experimental_fragment
def plot_product_histogram():
    st.subheader("Distribution of spent amounts.")
    selected_product_column = st.selectbox("Select a column", [
        "MntWines",
        "MntFruits",
        'MntMeatProducts', 
        'MntFishProducts', 
        'MntSweetProducts',
        'MntGoldProds',
        "MntAllProducts_Monetary"
    ])
    fig = px.histogram(df, x=selected_product_column)
    st.plotly_chart(fig)

with product_col_1:
    plot_product_histogram()

def plot_product_corr():
    st.subheader("Correlation between products")
    corr_matrix = df[[
        "MntWines",
        "MntFruits",
        'MntMeatProducts', 
        'MntFishProducts', 
        'MntSweetProducts',
        'MntGoldProds'
    ]].corr(method='spearman')
    fig = px.imshow(corr_matrix, text_auto=True)
    st.plotly_chart(fig)

with product_col_2:
    plot_product_corr()
