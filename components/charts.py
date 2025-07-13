from dash import dcc

from utils.charts import generate_monthly_chart, generate_inventory_sales_chart, generate_category_treemap, generate_promo_impact, generate_discount_distribution, generate_avg_demand

muted_blues = [
    "#8DA9C4", "#A3BCD6", "#C0D6DF", "#E5EFF5", "#B4C5D4", "#6C8AA3", "#345B73"
]

def initialize_chart(data):
    return dcc.Graph(id='graph-id', figure=generate_monthly_chart(data)) 

def initialize_inventory_sales_chart(data, threshold=10):
    return dcc.Graph(id='inventory-sales-chart', figure=generate_inventory_sales_chart(data, threshold))

def initialize_category_region_treemap(df):
    return dcc.Graph(id='category-region-treemap', figure=generate_category_treemap(df))

def initialize_promo_vs_no_promo(df):
    return dcc.Graph(id='promo-impact-delta-chart', figure=generate_promo_impact(df))

def initialize_discount_disctribution(df):
    return dcc.Graph(id='discount-vs-sales-chart', figure=generate_discount_distribution(df))

def initialize_price_demand_correlation_chart(df):
    return dcc.Graph(id='price-demand-heatmap', figure=generate_avg_demand(df))

