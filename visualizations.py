import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_cost_histograms(order_product_and_shipping_costs_df):
    """Creates subplots for product costs and shipping costs."""
    fig = make_subplots(
        rows=1, cols=2, 
        subplot_titles=("Product cost for orders < R$500", "Shipping cost for orders < R$80")
    )

    # Left histogram (Product cost)
    fig.add_trace(
        go.Histogram(
            x=order_product_and_shipping_costs_df['product_cost'],
            nbinsx=1000,
            name='Product Cost',
            marker_color='#6c87a3'
        ),
        row=1, col=1
    )
    fig.update_xaxes(range=[0, 500], title_text="Product cost (Brazilian reals)", row=1, col=1)
    fig.update_yaxes(title_text="Frequency", row=1, col=1)

    # Right histogram (Shipping cost)
    fig.add_trace(
        go.Histogram(
            x=order_product_and_shipping_costs_df['shipping_cost'],
            nbinsx=800,
            name='Shipping Cost',
            marker_color='#ad865f'
        ),
        row=1, col=2
    )
    fig.update_xaxes(range=[0, 80], title_text="Shipping cost (Brazilian reals)", row=1, col=2)
    fig.update_yaxes(title_text="Frequency", row=1, col=2)
    
    return fig

def create_seller_review_scatter(seller_review_scores_and_sales_df):
    """Creates a scatter plot of total sales vs avg review scores."""
    fig = px.scatter(
        seller_review_scores_and_sales_df, 
        x='total_sales', 
        y='avg_review_score',
        size='num_orders', 
        color='num_orders',
        log_x=True,
        opacity=0.7,
        trendline="lowess",
        trendline_options=dict(frac=0.1)
    )
    return fig
