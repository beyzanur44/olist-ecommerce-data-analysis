import pandas as pd     

orders = pd.read_csv("D:/1/ME/portfolio (1)/pörtfolyo.2026/001.README.md/archive/olist_orders_dataset.csv")

#print(orders.shape)
#print(orders.head)
#print(orders.info())
#print(orders.columns)
#print(orders.isnull().sum())
#print(orders["order_status"].value_counts())
#print(orders.duplicated().sum())
#print(orders.describe())


customers = pd.read_csv(r"D:\1\ME\portfolio (1)\pörtfolyo.2026\001.README.md\archive\olist_customers_dataset.csv")
#print(customers.shape)
#print(customers.head)
#print(customers.info)
#print(customers.columns)
#print(customers.isnull().sum())
#print(customers.duplicated().sum())
#print(customers.describe())

merged = pd.merge(
    orders,
    customers,
    on="customer_id",
    how="inner"
)

#print(merged.shape)
#print(merged.head())

order_items = pd.read_csv(r"D:\1\ME\portfolio (1)\pörtfolyo.2026\001.README.md\archive\olist_order_items_dataset.csv")
#print(order_items.shape)
#print(order_items.head)
#print(order_items.info)
#print(order_items.columns)
#print(order_items.isnull().sum())
#print(order_items.duplicated().sum())
#print(order_items.describe())

products = pd.read_csv(r"D:\1\ME\portfolio (1)\pörtfolyo.2026\001.README.md\archive\olist_products_dataset.csv")

#print(products.shape)
#print(products.head)
#print(products.info)
#print(products.columns)
#print(products.isnull().sum())
#print(products.duplicated().sum())
#print(products.describe())
merged = pd.merge(
    merged,
    order_items,
    on="order_id",
    how="inner"
)

#print(merged.shape)

merged = pd.merge(
    merged,
    products,
    on="product_id",
    how="left"
)

#print(merged.shape)

#print(merged["product_category_name"].value_counts().head(10))
#print(merged.columns)

#print(merged.groupby("product_category_name")["price"].sum().sort_values(ascending=False).head(10))

merged.groupby("customer_state")["price"] \
       .sum() \
       .sort_values(ascending=False) \
       .head(10)

#print(merged.columns)

merged.groupby("seller_id")["price"] \
.sum() \
.sort_values(ascending=False) \
.head(10)

merged["order_purchase_timestamp"] = pd.to_datetime(
    merged["order_purchase_timestamp"]
)

merged["purchase_month"] = merged["order_purchase_timestamp"].dt.month_name()
result= merged.groupby("purchase_month")["price"].sum().sort_values(ascending=False)
#print(result)

merged["order_delivered_customer_date"] = pd.to_datetime(
    merged["order_delivered_customer_date"]
)

merged["delivery_days"] = (
    merged["order_delivered_customer_date"]
    - merged["order_purchase_timestamp"]
).dt.days
merged["delivery_days"].mean()

#print("Average:", merged["delivery_days"].mean())
#print("Minimum:", merged["delivery_days"].min())
#print("Maximum:", merged["delivery_days"].max())

#print(merged["order_status"].value_counts())


result = merged.groupby("order_status")["order_id"].nunique().sort_values(ascending=False)
#print(result)

merged["order_estimated_delivery_date"] =pd.to_datetime(
    merged["order_estimated_delivery_date"]
)

merged["order_delivered_customer_date"] = pd.to_datetime(
    merged["order_delivered_customer_date"]
)

merged["delivery_difference_days"] = (
     merged["order_delivered_customer_date"]
    - merged["order_estimated_delivery_date"]
).dt.days

merged["delivery_difference_days"].mean()

#print("average difference:" , merged["delivery_difference_days"].mean())
#print("minimum difference:", merged["delivery_difference_days"].min())
#print("maximum different:", merged["delivery_difference_days"].max())

result= (
    merged.groupby("customer_state")["delivery_days"]
    .mean()
    .sort_values(ascending=False)
)

#print(result.head(10))

#print(merged["customer_unique_id"].nunique())

customer_orders =(
    merged.groupby("customer_unique_id")["order_id"]
    .nunique()
)

#print(customer_orders.head(5))

repeat_customers=(customer_orders > 1).sum()
#print("repeat customers:",repeat_customers)

repeat_customers_rate = (
    repeat_customers / customer_orders.shape[0]
    *100
)
#print("repeat_customers_rate:",repeat_customers_rate)

order_values = (
    merged.groupby("order_id")["price"]
    .sum()
)

print(order_values.head())

average_order_value = order_values.mean()
print("average order value:",average_order_value)

#print("average order value:", order_values.mean())
#print("minimum order value", order_values.min())
#print("maximüm order value:",order_values.max())

result = (
    merged.groupby("customer_state")["customer_unique_id"]
    .nunique()
    .sort_values(ascending=False)
)
#print(result.head(10))

top_states = ["SP", "RJ", "MG"]

result = (
    merged[merged["customer_state"].isin(top_states)]
    .groupby(["customer_state", "product_category_name"])["order_id"]
    .nunique()
    .reset_index(name="order_count")
    .sort_values(
        ["customer_state", "order_count"],
        ascending=[True, False]
    )
)

#print(result.head(15))
#print(result[result["customer_state"] == "SP"].head(10))
#print(result[result["customer_state"] == "RJ"].head(10))
#print(result[result["customer_state"] == "MG"].head(10))

merged["purchase_date"] = pd.to_datetime(
    merged["order_purchase_timestamp"]
)

monthly_revenue = (
    merged.groupby(
        merged["purchase_date"].dt.to_period("M")
    )["price"]
    .sum()
)
#print(monthly_revenue)

merged["purchase_date"] = pd.to_datetime(
    merged["order_purchase_timestamp"]
)

monthly_revenue = (
    merged.groupby(
        merged["purchase_date"].dt.to_period("M")
    )["price"]
    .sum()
)

#print(monthly_revenue)

category_analysis = (
    merged.groupby("product_category_name")
    .agg(
        total_revenue=("price", "sum"),
        order_count=("order_id", "nunique")
    )
)
category_analysis["revenue_per_order"] = (
    category_analysis["total_revenue"]
    / category_analysis["order_count"]
)
result = category_analysis.sort_values(
    "revenue_per_order",
    ascending=False
)

#print(result.head(10))


