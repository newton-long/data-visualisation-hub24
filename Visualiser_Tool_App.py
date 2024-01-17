"""
Interactive web application, for data visualisations.
Single web page -> can specify what visualisations the user is looking for.
Data provided is stored in SQL Lite database for transportable use.
"""
import dash
import dash_bootstrap_components as dbc
from Helper_Functions import *


# Create instance of dash component with VAPOR aesthetic
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX])

navbar = dbc.NavbarSimple(
    brand="HUB24",
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Performance", href="/performance")),
        dbc.NavItem(dbc.NavLink("Sales", href="/sales")),
    ],
    sticky="top",
)


# Congregate pages together -> all pages in the registry are linked through the navbar
app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)
