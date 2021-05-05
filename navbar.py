import dash_bootstrap_components as dbc
import dash_html_components as html
from load_page_dash import get_logo_image
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from server import app
from load_page_dash import layout as load_layout

navbar = html.Div(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Upload POS", href="/load_pos", id="page-1-link"),
                dbc.NavLink("Upload Bleu POS", href="/load_bleu_pos", id="page-2-link"),
            ],
            brand="Proof Of Sustainability",
            color="#b20000",
            dark=True,
        ),
        dbc.Container(id="page-content", className="pt-4"),
    ],  style={'background': 'bleu'}
)


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 2)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 2)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/load_pos"]:
        return load_layout
    elif pathname == "/load_bleu_pos":
        return html.P("This is the content of page 2")

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open