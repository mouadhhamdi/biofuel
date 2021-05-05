import dash_bootstrap_components as dbc
import dash_html_components as html
from load_page_dash import get_logo_image
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from server import app

home_button = dbc.NavItem(dbc.NavLink('Upload yellow POS', href="load_pdf", external_link=True, className='navlinks'))
statistic_button = dbc.NavItem(dbc.NavLink('Upload bleu POS', href="load_bleu_pdf", external_link=True, className='navlinks'))
navbar = html.Div(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Page 1", href="/page-1", id="page-1-link"),
                dbc.NavLink("Page 2", href="/page-2", id="page-2-link"),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1",href="/page-3", id="page-3-link"),
                dbc.DropdownMenuItem("Entry 2",href="/page-4", id="page-4-link"),
            ],
        )
            ],
            brand="Navbar with active links",
            color="primary",
            dark=True,
        ),
        dbc.Container(id="page-content", className="pt-4"),
    ]
)


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return html.P("This is the content of page 1!")
    elif pathname == "/page-2":
        return html.P("This is the content of page 2. Yay!")
    elif pathname == "/page-3":
        return html.P("Oh cool, this is page 3!")
    elif pathname == "/page-4":
        return html.P("Oh cool, this is page 4!")

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