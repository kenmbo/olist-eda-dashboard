from jupyter_dash import JupyterDash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Create the Dash app
app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"])
app.config.suppress_callback_exceptions = True

# Define figures for each section
figs_order_analysis = {"Fig1": fig1, "Fig2": fig2, "Fig3": fig3, "Fig6":fig6, "Fig9":fig9, "Map":fig13}
figs_top_orders = {"Fig4": fig4, "Fig5": fig5}
figs_predictions = {"Fig7": fig7, "Fig8": fig8}
figs_delivery = {"Fig10": fig10, "Fig15": fig15, "Fig16":fig16}
figs_reviews = {"Fig14": fig14, "Fig11": fig11}
figs_order_origin = {"Fig17": fig17, "Fig18": fig18}

# Define tabs and icons
tabs_dict = {
    "Order Analysis": ("fas fa-box", figs_order_analysis),
    "Top Orders": ("fas fa-chart-bar", figs_top_orders),
    "Predictions": ("fas fa-line-chart", figs_predictions),
    "Delivery": ("fas fa-truck", figs_delivery),
    "Reviews Analysis": ("fas fa-star", figs_reviews),
    "Order Origin": ("fas fa-globe", figs_order_origin)
}

# Sidebar Layout
sidebar = html.Div(
    [
        html.Button("☰", id="toggle-button", style={
            "width": "100%", "backgroundColor": "#000", "color": "white", "border": "none", "fontSize": "24px"
        }),
        html.Div(
            dbc.Nav(
                [
                    dbc.NavLink(
                        html.Div([html.Span(className=icon, style={"marginRight": "10px"}), html.Span(name, className="link-text")]),
                        href="#", id=f"{name.lower().replace(' ', '-')}-link", active="exact"
                    ) for name, (icon, _) in tabs_dict.items()
                ],
                vertical=True, pills=True
            ),
            id="sidebar-content"
        ),
    ],
    id="sidebar",
    style={
        "width": "200px", "backgroundColor": "#000", "color": "white",
        "height": "100vh", "position": "fixed", "top": 0, "left": 0, "padding": "10px",
        "transition": "width 0.3s"
    }
)

sidebar_short = html.Div(
    id="mySidebar",
    className="sidebar",
    children=[
        html.Div(
            dbc.Nav(
                [
                    dbc.NavLink(
                        html.Div([html.Span(className=icon, style={"marginRight": "10px"}), html.Span(name, className="link-text")]),
                        href="#", id=f"{name.lower().replace(' ', '-')}-link", active="exact"
                    ) for name, (icon, _) in tabs_dict.items()
                ],
                vertical=True, pills=True
            ),
            id="sidebar-content"
        )
    ],
    style={
        "width": "300px", "backgroundColor": "#000", "color": "white",
        "height": "100vh", "position": "fixed", "top": 0, "left": "-13vw", "padding": "10px",
        "transition": "all 0.3s", "zIndex" : 99999999,
    }
)

# Main content area
content = html.Div(id="page-content", style={"padding": "20px", "marginLeft": "20px", "transition": "margin-left 0.3s"})

# Layout
app.layout = html.Div([sidebar_short, content])

# Sidebar toggle callback
@app.callback(
    [Output("sidebar", "style"), Output("sidebar-content", "style"), Output("page-content", "style")],
    [Input("toggle-button", "n_clicks")],
    [State("sidebar", "style")],
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, current_style):
    if current_style["width"] == "200px":
        # Collapse sidebar
        return {"width": "60px", "backgroundColor": "#000", "color": "white", "height": "100vh"}, {"display": "none"}, {"padding": "20px", "marginLeft": "60px"}
    else:
        # Expand sidebar
        return {"width": "200px", "backgroundColor": "#000", "color": "white", "height": "100vh"}, {"display": "block"}, {"padding": "20px", "marginLeft": "200px"}


def display_figures_tab(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.Div("Select a tab from the sidebar.")

    tab_clicked = ctx.triggered[0]["prop_id"].split(".")[0]
    tab_name = tab_clicked.replace("-link", "").replace("-", " ").title()
    _, figs = tabs_dict[tab_name]

    dropdown = dcc.Dropdown(
        id="figure-dropdown",
        options=[{"label": key, "value": key} for key in figs.keys()],
        placeholder="Select a figure",
        style={"marginTop": "20px", "width": "50%"}
    )
    return html.Div([
        html.H3(f"Figures for {tab_name}"), dropdown,
        html.Div(id="figure-container")
    ])

# Callback to update the displayed figure based on dropdown selection
@app.callback(
    Output("figure-container", "children"),
    [Input("figure-dropdown", "value"), State("figure-dropdown", "options")],
    prevent_initial_call=True
)
def display_selected_figure(selected_value, options):
    if not selected_value:
        return html.Div("Please select a figure from the dropdown.")

    fig_name = next((opt['label'] for opt in options if opt['value'] == selected_value), None)
    all_figs = {**figs_order_analysis, **figs_top_orders, **figs_predictions, **figs_delivery, **figs_reviews, **figs_order_origin}
    figure = all_figs.get(fig_name)

    return dcc.Graph(figure=figure)
