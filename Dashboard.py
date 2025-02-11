# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# import data
df = pd.read_csv("all_data.csv")

# Mengubah kolom menjadi datetime
datetime_columns = ['order_approved_at']
for column in datetime_columns:
    df[column] = pd.to_datetime(df[column])

# Create function to create a certain dataframe
def create_top_product(df):
    # create top product dataframe
    filtered = df[df.order_status == "delivered"]
    top_product = filtered.groupby("product_category_name_english").order_id.count().reset_index()
    # rename column
    top_product.rename(columns = {"order_id": "order_id", "product_category_name_english": "Category"}, inplace = True)
    #sort the data
    top_product.sort_values(by="order_id", ascending = False, inplace = True)
    return top_product

def create_bystate(df):
    bystate = df.groupby(by="customer_state_full").customer_id.nunique().reset_index()
    # rename column
    bystate.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    #sort the data
    bystate.sort_values(by="customer_count",ascending = False, inplace = True)
    return bystate

def create_bycity(df):
    bycity = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    # rename column
    bycity.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    #sort the data
    bycity.sort_values(by="customer_count", ascending = False, inplace = True)
    return bycity

def create_order_bytime(df):
    filtered = df[df.order_status == "delivered"]
    order_bytime = filtered.groupby(by="delivery_order_month_year").order_id.count().reset_index()
    # rename column
    order_bytime.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    #sort the data
    order_bytime.sort_index(inplace = True)
    return order_bytime

def create_avgtime_perstate(df):
    avgtime_perstate = df.groupby(by="customer_state_full").delivered_time.mean().reset_index()
    # rename column
    avgtime_perstate.rename(columns={
        "customer_state_full": "state"
    }, inplace=True)
    #sort the data
    avgtime_perstate.sort_index(inplace = True)
    return avgtime_perstate

def create_pay_method(df):
    filtered = df[df.order_status == "delivered"]
    pay_method = filtered["payment_type"].value_counts()
    return pay_method

def create_review(df):
    filtered = df[df.order_status == "delivered"]
    review = filtered["review_score"].value_counts()
    return review

def create_time_review(df):
    filtered = df[df.order_status == "delivered"]
    time_review = filtered[['delivered_time', 'review_score']].corr()
    return time_review



min_date = df["order_approved_at"].min()
max_date = df["order_approved_at"].max()

# Create sidebar
with st.sidebar:
    st.header("DASHBOARD")
    st.subheader("OCHA TANIYA BRIGIDTA")
    st.image("Ocha.JPG")
    # Add date filter
    start_date, end_date = st.date_input(
    label='Rentang Waktu',min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date])

    # Create a main data frame that effected by filters
    main_df = df[(df["order_approved_at"].dt.date >= start_date) & 
                (df["order_approved_at"].dt.date <= end_date)]

# Create Header
st.header("E-Commerce Analysis Dashboard")

# Create pivot table for charts
top_product = create_top_product(main_df)
bycity = create_bycity(main_df)
bystate = create_bystate(main_df)
order_bytime = create_order_bytime(main_df)
avgtime_perstate = create_avgtime_perstate(main_df)
pay_method = create_pay_method(main_df)
review = create_review(main_df)
time_review = create_time_review(main_df)

#Create 2 coulomn for scorecard
col1, col2 = st.columns(2)
with col1:
    filtered = main_df[main_df.order_status=="delivered"]
    total_sold_items = filtered["order_id"].count()
    st.metric("Total Sold Items", f"{total_sold_items}")

with col2:
    filtered = main_df[main_df.order_status=="delivered"]
    total_revenue = filtered["payment_value"].sum()
    st.metric("Total Revenue", f"${total_revenue/1000:.2f}")

st.subheader("Customer Demographics")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(30, 20))
    sns.barplot(
        y="customer_count", 
        x="customer_state_full",
        data=bystate.sort_values(by="customer_count", ascending=False).head(5),
        ax=ax
    )
    ax.set_title("Number of Customer by State (Top 5)", fontweight = "bold", fontsize = 100, loc="center")
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(30, 20))
    sns.barplot(
        y="customer_count", 
        x="customer_city",
        data = bycity.sort_values(by="customer_count", ascending=False).head(5),
        ax=ax
    )
    ax.set_title("Number of Customer by City (Top 5)", fontweight = "bold", fontsize = 100, loc="center")
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)


st.subheader("Order Count per Product Category")
# Create figure and axes
fig, ax = plt.subplots(ncols = 2)
# Create barplot for top product
sns.barplot(data = top_product.head(10), y = "Category", x = "order_id", width = 0.5, ax = ax[0])
ax[0].set_title("Top 10 Products", fontweight = "bold", fontsize = 12)
ax[0].set_xlabel("")
sns.despine(ax = ax[0])
# Create barplot for bottom product
sns.barplot(data = top_product.tail(10), y = "Category", x = "order_id", width = 0.5, ax = ax[1])
ax[1].set_title("Bottom 10 Products", fontweight = "bold", fontsize = 12)
ax[1].set_xlabel("")
sns.despine(ax = ax[1])
fig.tight_layout()
plt.show()
st.pyplot(fig)

st.subheader("Order Trends by Delivered Time")
fig, ax = plt.subplots()
# Create lineplot
sns.lineplot(data = order_bytime, x = "delivery_order_month_year", y = "order_count")
# Create label
ax.set_ylabel("")
ax.set_xlabel("")
plt.xticks(rotation = 45)
sns.despine()
plt.show()
st.pyplot(fig)

st.subheader("Avarage Delivered Time per State")
fig, ax = plt.subplots(figsize=(30, 20))
sns.barplot(
y="delivered_time", 
x="state",
data = avgtime_perstate.sort_values(by = "delivered_time",ascending=False).head(10),
ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Payment Method")
    # create figure and axes
    fig, ax = plt.subplots(figsize = (5,5))
    
    # create pie chart
    ax.pie(pay_method, wedgeprops = {"width": 0.5}, startangle = 90,
          textprops = {"fontweight" : "bold"})
    
    ax.legend(pay_method.index)
    
    plt.show()
    st.pyplot(fig)
 
with col2:
    st.subheader("Number of Reviews")
    # create figure and axes
    fig, ax = plt.subplots(figsize = (5,5))
    
    # create pie chart
    ax.pie(review, wedgeprops = {"width": 0.5}, startangle = 90,
          textprops = {"fontweight" : "bold"})
    
    ax.legend(review.index)
    
    plt.show()
    st.pyplot(fig)

