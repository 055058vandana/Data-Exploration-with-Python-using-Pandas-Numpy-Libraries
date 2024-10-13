import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
import numpy as np
import networkx as nx

# Main function
def main():
    st.title("Streamlit Dashboard")
    
    # Load the Data
    file_path = "C:\\Users\\RAJESH KUMAR JAIN\\Desktop\\import export.csv"
    
    # Check if file exists
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.write(df)  # Display the dataframe in the Streamlit app
    else:
        st.error("File not found!")
        return
    
    # Create a sample of 3001 observations
    sd = df.sample(n=3001, random_state=55058)
    st.write(sd)

    # Box Plot of Transaction Values by Category
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Category', y='Value', data=df)
    plt.title('Box Plot of Transaction Values by Category')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Number of Transactions by Country
    country_counts = df['Country'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=country_counts.index, y=country_counts.values, color='blue')
    plt.xticks(rotation=90)
    plt.title('Number of Transactions by Country')
    st.pyplot(plt)

    # Transactions over Time
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['YearMonth'] = df['Date'].dt.to_period('M')
    transaction_trends = df.groupby('YearMonth').size()
    plt.figure(figsize=(10, 6))
    transaction_trends.plot(kind='line', marker='o')
    plt.title('Transactions Over Time')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Imports vs Exports Pie Chart
    import_export_counts = df['Import_Export'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(import_export_counts, labels=import_export_counts.index, autopct='%1.1f%%',
            colors=['skyblue', 'lightgreen'], startangle=90)
    plt.title('Imports vs Exports')
    st.pyplot(plt)

    # Imports and Exports by Country (Stacked Bar)
    country_import_export = df.groupby(['Country', 'Import_Export']).size().unstack()
    plt.figure(figsize=(12, 7))
    country_import_export.plot(kind='bar', stacked=True, colormap='coolwarm')
    plt.title('Imports and Exports by Country')
    plt.xticks(rotation=90)
    st.pyplot(plt)

    # Top 10 Products by Trade Value
    top_products = df.groupby('Product')['Value'].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_products.index, y=top_products.values, palette='rocket')
    plt.xticks(rotation=45)
    plt.title('Top 10 Products by Trade Value')
    st.pyplot(plt)

    # Weight vs Value Scatter Plot by Shipping Method
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Weight', y='Value', hue='Shipping_Method', data=df, palette='Set1')
    plt.title('Weight vs Value of Transactions (by Shipping Method)')
    st.pyplot(plt)

    # Distribution of Transaction Weights with Multiple Colors
    plt.figure(figsize=(10, 6))
    weights = df['Weight']
    bins = np.linspace(weights.min(), weights.max(), 21)
    counts, _ = np.histogram(weights, bins)
    for count, x in zip(counts, range(len(counts))):
        plt.bar(bins[x:x+2][0], count, width=bins[x+1]-bins[x], color=sns.color_palette("viridis", len(counts))[x], edgecolor='black', alpha=0.7)
    plt.title('Distribution of Transaction Weights with Multiple Colors')
    st.pyplot(plt)

    # Number of Transactions by Payment Terms
    payment_term_counts = df['Payment_Terms'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=payment_term_counts.index, y=payment_term_counts.values, palette='mako')
    plt.xticks(rotation=45)
    plt.title('Number of Transactions by Payment Terms')
    st.pyplot(plt)

    # Correlation Heatmap of Trade Variables
    corr = df[['Quantity', 'Value', 'Weight']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap of Trade Variables')
    st.pyplot(plt)

    # Trade Volume by Country (Geographical Heatmap using Plotly)
    country_trade = df.groupby('Country')['Value'].sum().reset_index()
    fig = px.choropleth(
        country_trade,
        locations="Country",
        locationmode='country names',
        color="Value",
        hover_name="Country",
        title="Trade Volume by Country"
    )
    st.plotly_chart(fig)

    # Trade Volume by Product (Treemap using Plotly)
    fig = px.treemap(df, path=['Product'], values='Value', title='Trade Volume by Product')
    st.plotly_chart(fig)

    # Weight Distribution by Shipping Method (Violin Plot using Plotly)
    fig = px.violin(df, y='Weight', x='Shipping_Method', box=True, title='Weight Distribution by Shipping Method')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
