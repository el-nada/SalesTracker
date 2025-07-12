import dash
from dash import html, dcc, dash_table
import numpy as np
import plotly.express as px
import pandas as pd

def initialize_chart(data):
    fig = px.line(data, x='Date', y='Units Sold', color='Store ID')
    return dcc.Graph(id='graph-id', figure=fig)

def initialize_inventory_sales_chart(df, threshold=10):
    # 1) Base time‐series for Units Sold and Inventory Level
    fig = px.line(
        df,
        x='Date',
        y=['Units Sold', 'Inventory Level'],
        color='Store ID',
        title="Units Sold & Inventory Level Over Time",
        labels={'value': 'Count', 'Date': 'Date'}
    )

    # 2) Find all points where Inventory Level ≤ threshold
    low_inv = df[df['Inventory Level'] <= threshold]
    if not low_inv.empty:
        fig.add_scatter(
            x=low_inv['Date'],
            y=low_inv['Inventory Level'],
            mode='markers',
            marker=dict(color='red', size=8, symbol='x'),
            name=f"Inventory ≤ {threshold}"
        )

    fig.update_layout(legend_title_text="Metric / Store")
    return dcc.Graph(id='inventory-sales-chart', figure=fig)


def initialize_category_region_stacked_bar(df):
    agg = df.groupby(['Region', 'Category'])['Units Sold'].sum().reset_index()
    fig = px.bar(
        agg,
        x='Region',
        y='Units Sold',
        color='Category',
        title="Units Sold by Category ⎯ Stacked per Region",
        labels={'Units Sold': 'Total Units Sold'}
    )
    fig.update_layout(barmode='stack')
    return dcc.Graph(id='category-region-bar-chart', figure=fig)

def initialize_category_region_treemap(df):
    agg = df.groupby(['Region', 'Category'])['Units Sold'].sum().reset_index()
    fig = px.treemap(
        agg,
        path=['Region', 'Category'],
        values='Units Sold',
        title="Sales Share : Categories per region"
    )
    return dcc.Graph(id='category-region-treemap', figure=fig)

def initialize_promotion_over_time_chart(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month  # Integer 1-12

    # Group by month and promotion
    grouped = df.groupby(['Month', 'Promotion'])['Units Sold'].mean().unstack()
    grouped.columns = ['No Promo', 'Promo']
    grouped['Promo Impact'] = grouped['Promo'] - grouped['No Promo']
    
    grouped = grouped.reset_index()  # Avoid ambiguity
    grouped['Month Name'] = grouped['Month'].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%b'))

    grouped = grouped.sort_values('Month')

    fig = px.line(
        grouped,
        x='Month Name',
        y='Promo Impact',
        markers=True,
        title="Monthly Sales Impact of Promotions (Promo - No Promo)"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Promo Sales Impact (Δ Units Sold)",
        height=500
    )

    return dcc.Graph(id='promo-impact-delta-chart', figure=fig)


def initialize_discount_vs_sales_chart(df):
    promo_df = df[df['Promotion'] == 1].copy()

    # Round discount to nearest 0.5 for grouping
    promo_df['Rounded Discount'] = (promo_df['Discount'] * 2).round() / 2

    grouped = promo_df.groupby('Rounded Discount')['Units Sold'].mean().reset_index()

    fig = px.line(
        grouped,
        x='Rounded Discount',
        y='Units Sold',
        markers=True,
        title="Avg Units Sold by Discount (Promotions Only)"
    )

    fig.update_layout(height=500)
    return dcc.Graph(id='discount-vs-sales-chart', figure=fig)


def initialize_discount_vs_sales_scatter(df):
    # Show how discount percentage correlates with units sold
    if 'Discount' not in df.columns:
        # If discounts are 0/1 only, you might skip or convert to %
        df['DiscountPct'] = df['Discount'] * 100
    else:
        df['DiscountPct'] = df['Discount']
    
    fig = px.scatter(
        df,
        x='DiscountPct',
        y='Units Sold',
        color='Promotion',
        title="Discount % vs Units Sold (colored by Promotion)",
        labels={'DiscountPct': 'Discount (%)'}
    )
    return dcc.Graph(id='discount-sales-scatter', figure=fig)


def initialize_seasonality_epidemic_chart(df):
    import plotly.express as px
    import pandas as pd

    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    fig = px.line(
        df,
        x='Date',
        y='Units Sold',
        color='Category',
        animation_frame='Seasonality',
        title="Units Sold Over Time by Category (Animated by Season)"
    )

    # Identify epidemic periods
    epid_df = df[df['Epidemic'] == 1].copy()
    epid_df['gap'] = epid_df['Date'].diff().dt.days.gt(1).cumsum()

    # Add vertical rectangles for epidemic periods
    for _, group in epid_df.groupby('gap'):
        start_date = group['Date'].min()
        end_date = group['Date'].max()
        fig.add_vrect(
            x0=start_date, x1=end_date,
            fillcolor="red", opacity=0.15, line_width=0,
            layer="below",
            annotation_text="Epidemic", annotation_position="top left"
        )

    fig.update_layout(height=600)
    return dcc.Graph(id='seasonality-epidemic-chart', figure=fig)



def initialize_price_demand_correlation_chart(df):
    df = df[['Price', 'Discount', 'Demand']].copy()
    df = df[
        (df['Price'] <= df['Price'].quantile(0.99)) &
        (df['Discount'] <= df['Discount'].quantile(0.99)) &
        (df['Demand'] <= df['Demand'].quantile(0.99))
    ]

    # Bin price and discount
    df['Price Bin'] = pd.cut(df['Price'], bins=10)
    discount_bins = np.arange(0, df['Discount'].max() + 5, 5)
    df['Discount Bin'] = pd.cut(df['Discount'], bins=discount_bins)

    # Group by bins and calculate mean demand
    grouped = df.groupby(['Price Bin', 'Discount Bin'], observed=False)['Demand'].mean().reset_index()


    # Convert bins to string for better axis labels
    grouped['Price Bin Label'] = grouped['Price Bin'].astype(str)
    grouped['Discount Bin Label'] = grouped['Discount Bin'].astype(str)

    fig = px.density_heatmap(
        grouped,
        x='Price Bin Label',
        y='Discount Bin Label',
        z='Demand',
        color_continuous_scale='Viridis',
        labels={'Demand': 'Avg Demand', 'Price Bin Label': 'Price Range', 'Discount Bin Label': 'Discount Range'},
        title='Average Demand by Price & Discount'
    )

    fig.update_layout(height=600)
    return dcc.Graph(id='price-demand-heatmap', figure=fig)


def initialize_weather_sales_bar(df):
    if 'Weather Condition' not in df.columns:
        return dcc.Graph(id='weather-sales-bar', figure={})

    agg = df.groupby('Weather Condition')['Units Sold'].mean().reset_index()
    fig = px.bar(
        agg,
        x='Weather Condition',
        y='Units Sold',
        title="Avg Units Sold by Weather Condition",
        labels={'Units Sold': 'Avg Units Sold'}
    )
    return dcc.Graph(id='weather-sales-bar', figure=fig)
