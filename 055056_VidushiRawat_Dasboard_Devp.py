import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

# Set the title of the dashboard
st.markdown(
    """
    <h1 style='text-align: center; color: #C5F96F; font-family: "Arial"; font-size: 40px;'>Imports/Exports Dashboard</h1>
    """, 
    unsafe_allow_html=True
)

# Load the dataset directly from a specified file path
data_path = r"C:\Users\vidus\OneDrive\Desktop\dep\Imports_Exports_Dataset.csv"  # Modify the path as needed
dataset = pd.read_csv(data_path)

# Sample dataset
sdset = dataset.sample(n=min(3001, len(dataset)), random_state=55056)  # Adjust to actual length

# Add a year dropdown in the sidebar
sdset['Date'] = pd.to_datetime(sdset['Date'], format='%d-%m-%Y', errors='coerce')  # Handle parsing errors
sdset['Year'] = sdset['Date'].dt.year
years = sdset['Year'].unique()
selected_year = st.sidebar.selectbox("Select a year:", sorted(years))

# Filter the dataset based on the selected year
filtered_data = sdset[sdset['Year'] == selected_year]

# Dropdown selection for charts
st.sidebar.header("Select Chart")
chart_options = [
    "Payment Method Distribution",
    "Total Transaction Value by Category",
    "Percentage of Total Transaction Value by Shipping Method",
    "Correlation Matrix Heatmap",
    "Boxplot of Value by Top 10 Products",
    "Violin Plot of Value by Category",
    "Scatter Plot: Weight vs Value",
    "Average Weight for Top 5 Products by Value Segmented by Import/Export"
]

selected_chart = st.sidebar.selectbox("Select a chart to display:", chart_options)

if selected_chart == "Payment Method Distribution":
    # Payment Method Distribution
    st.subheader('Distribution of Transactions by Payment Method')
    payment_method_totals = filtered_data.groupby('Payment_Terms').size().reset_index(name='Count')
    fig_payment = px.pie(payment_method_totals, names='Payment_Terms', values='Count', 
                          title='Distribution of Transactions by Payment Method',
                          color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_payment.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white', title_x=0.5)
    st.plotly_chart(fig_payment)

elif selected_chart == "Total Transaction Value by Category":
    # Total Transaction Value by Category
    st.subheader('Total Transaction Value by Category')
    category_totals = filtered_data.groupby('Category').agg({'Value': 'sum'}).reset_index()
    category_totals.rename(columns={'Value': 'Transaction Value'}, inplace=True)
    category_totals = category_totals.sort_values(by='Transaction Value', ascending=False)

    # Highest Transaction Value
    highest_transaction = category_totals.loc[category_totals['Transaction Value'].idxmax()]
    st.write(f"Category with the highest transaction value: {highest_transaction['Category']} - Value: {highest_transaction['Transaction Value']}")

    # Bar Plot
    fig_bar = px.bar(category_totals, x='Category', y='Transaction Value', 
                     title='Total Transaction Value by Category (Descending Order)', 
                     labels={'Transaction Value': 'Total Transaction Value', 'Category': 'Category'},
                     color='Category', color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_bar.update_layout(xaxis_title='Category', yaxis_title='Total Transaction Value', title_x=0.5, 
                          plot_bgcolor='black', paper_bgcolor='black', font_color='white')
    st.plotly_chart(fig_bar)

elif selected_chart == "Percentage of Total Transaction Value by Shipping Method":
    # Percentage of Total Transaction Value by Shipping Method
    st.subheader('Percentage of Total Transaction Value by Shipping Method')
    shipping_value_totals = filtered_data.groupby('Shipping_Method').agg({'Value': 'sum'}).reset_index()
    fig_shipping = px.pie(shipping_value_totals, names='Shipping_Method', values='Value', 
                           title='Percentage of Total Transaction Value by Shipping Method',
                           color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_shipping.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white', title_x=0.5)
    st.plotly_chart(fig_shipping)

elif selected_chart == "Correlation Matrix Heatmap":
    # Correlation Matrix Heatmap
    st.subheader('Correlation Matrix Heatmap')
    non_categorical_vars = filtered_data[['Quantity', 'Value', 'Weight']]
    correlation_matrix = non_categorical_vars.corr()
    st.write("Correlation Matrix:")
    st.dataframe(correlation_matrix)

    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.5f')
    st.pyplot(plt)


elif selected_chart == "Boxplot of Value by Top 10 Products":
    # Boxplot of Value by Top 10 Products
    st.subheader('Boxplot of Value by Top 10 Products')
    top_10_categories = filtered_data['Product'].value_counts().nlargest(10).index
    top_10_sample = filtered_data[filtered_data['Product'].isin(top_10_categories)]
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Product', y='Value', data=top_10_sample, palette='bright', flierprops=dict(marker='o', color='red', markersize=6))
    plt.title('Boxplot of Value by Top 10 Products')
    plt.xticks(rotation=90)
    st.pyplot(plt)

elif selected_chart == "Violin Plot of Value by Category":
    # Violin Plot of Value by Category
    st.subheader('Violin Plot of Value by Category')
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=filtered_data, x='Category', y='Value', palette='muted')
    plt.title('Violin Plot of Value by Category')
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    st.pyplot(plt)

elif selected_chart == "Scatter Plot: Weight vs Value":
    # Scatter Plot: Weight vs Value
    st.subheader('Scatter Plot of Weight vs Value')
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Weight', y='Value', data=filtered_data, alpha=0.7)
    plt.title('Scatter Plot of Weight vs Value', fontsize=16)
    plt.xlabel('Weight', fontsize=14)
    plt.ylabel('Value', fontsize=14)
    plt.grid(True)
    st.pyplot(plt)

elif selected_chart == "Average Weight for Top 5 Products by Value Segmented by Import/Export":
    # Average Weight for Top 5 Products by Value
    st.subheader('Average Weight for Top 5 Products by Value Segmented by Import/Export')
    top_5_products = filtered_data.groupby('Product')['Value'].sum().nlargest(5).index
    top_5_data = filtered_data[filtered_data['Product'].isin(top_5_products)]
    avg_weight_top_5 = top_5_data.groupby(['Product', 'Import_Export'])['Weight'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Product', y='Weight', hue='Import_Export', data=avg_weight_top_5, palette='viridis')
    plt.title('Average Weight for Top 5 Products by Value Segmented by Import/Export', fontsize=16)
    plt.xlabel('Product', fontsize=14)
    plt.ylabel('Average Weight', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend(title='Import/Export')
    st.pyplot(plt)
