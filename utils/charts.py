import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

muted_blues = [
    "#8DA9C4", "#A3BCD6", "#C0D6DF", "#E5EFF5", "#B4C5D4", "#6C8AA3", "#345B73"
]

common_layout = dict(
    plot_bgcolor='#f7f9fb',
    paper_bgcolor='#f7f9fb',
    font=dict(color='#2a5177'),
    legend_title_text="Metric",
    margin=dict(t=60, b=40)
)

def generate_monthly_chart(df):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()

    # Filter to the last 12 available months
    max_month = df['Month'].max()
    min_month = max_month - pd.DateOffset(months=11)
    df = df[df['Month'] >= min_month]

    grouped = df.groupby('Month')['Units Sold'].sum().reset_index()

    fig = px.bar(
        grouped,
        x='Month',
        y='Units Sold',
        title="Monthly Units Sold",
        labels={'Month': 'Month', 'Units Sold': 'Units Sold'},
        color_discrete_sequence=muted_blues
    )

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Units Sold',
        height=400,
        showlegend=False,
    )

    fig.update_layout(**common_layout)
    return fig 

def generate_inventory_sales_chart(df, threshold):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()

    agg_df = df.groupby('Month').agg({
        'Units Sold': 'sum',
        'Inventory Level': 'sum'
    }).reset_index()

    color = muted_blues[0]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=agg_df['Month'],
            y=agg_df['Units Sold'],
            mode='lines+markers',
            name='Units Sold',
            line=dict(color=color),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=agg_df['Month'],
            y=agg_df['Inventory Level'],
            mode='lines+markers',
            name='Inventory Level',
            line=dict(color=color, dash='dot'),
        )
    )

    low_inv = agg_df[agg_df['Inventory Level'] <= threshold]
    if not low_inv.empty:
        fig.add_trace(
            go.Scatter(
                x=low_inv['Month'],
                y=low_inv['Inventory Level'],
                mode='markers',
                marker=dict(color='red', size=8, symbol='x'),
                name=f"Inventory ≤ {threshold}"
            )
        )

    fig.update_layout(
        height=600,
        title_text="Monthly Inventory & Sales Overview",
    )
    fig.update_layout(**common_layout)

    fig.update_xaxes(title_text="Month")
    fig.update_yaxes(title_text="Count")
    return fig
    
def generate_category_treemap(df):
    agg = df.groupby(['Region', 'Category'])['Units Sold'].sum().reset_index()
    fig = px.treemap(
        agg,
        path=['Region', 'Category'],
        values='Units Sold',
        color='Region',
        color_discrete_sequence=muted_blues,
        title="Sales Share : Categories per region",
    )

    fig.update_layout(**common_layout)
    return fig 

def generate_promo_impact(df):
    agg = df.groupby(['Category', 'Promotion'])['Units Sold'].mean().reset_index()
    agg['Promotion'] = agg['Promotion'].map({0: 'No Promo', 1: 'Promo'})

    fig = px.bar(
        agg,
        x='Category',
        y='Units Sold',
        color='Promotion',
        barmode='group',
        title='Avg Units Sold per Category — Promo vs No Promo',
        labels={'Units Sold': 'Avg Units Sold'},
        color_discrete_sequence=muted_blues
    )
    fig.update_layout(**common_layout)
    return fig

def generate_discount_distribution(df):
    df = df[df['Promotion'] == 1].copy()
    df['Rounded Discount'] = (df['Discount'] * 2).round() / 2

    fig = px.box(
        df,
        x='Rounded Discount',
        y='Units Sold',
        title='Distribution of Units Sold at Each Discount Level (Promos Only)',
        labels={'Rounded Discount': 'Discount (%)'},
        color_discrete_sequence=muted_blues
    )
    fig.update_layout(**common_layout)
    return fig

def generate_avg_demand(df): 
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
        color_continuous_scale=[
            [0.0, "#E5EFF5"],
            [0.25, "#C0D6DF"],
            [0.5, "#A3BCD6"],
            [0.75, "#8DA9C4"],
            [1.0, "#6C8AA3"]
        ],
        labels={'Demand': 'Avg Demand', 'Price Bin Label': 'Price Range', 'Discount Bin Label': 'Discount Range'},
        title='Average Demand by Price & Discount'
    )
    fig.update_layout(**common_layout)
    return fig 

def generate_empty_graph():
    return px.bar(title="No Data Available")