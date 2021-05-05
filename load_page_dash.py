import dash_core_components as dcc
import dash_html_components as html
import base64
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from server import app
import time
from extract_yellow_data_pdf import YellowPdfParser


def get_logo_image():
    """

    :return: logo image
    """
    image_filename = './data_dash/mercuria_logo.png'  # replace with your own image
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return encoded_image


layout = \
        html.Div(children=[
        html.Img(title='Bio Fuel',
                 src='data:image/png;base64,{}'.format(get_logo_image().decode()),
                 height=100,
                 width=100,
                 style={'display': 'inline-block'}),

        html.H1(children='Bio Fuel',
                style={'color': '111',
                       'font-family': 'Open Sans Condensed',
                       'font-size': '80px',
                       'font-weight': 'bold',
                       'letter-spacing': '-1px',
                       'line-height': '1',
                       'text-align': 'center',
                       'display': 'inline-block',
                       "margin": "0em 30%"}),

        html.Div(
            children=[
                dcc.Upload(
                    id='upload-yellow-pdf',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select PDF'),
                    ]),
                    style={
                        'width': '50%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'font-family': 'Open Sans Condensed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        "background-color": "#f8f9fa",
                        "margin": " 0 25%",
                    },
                    # Allow multiple files to be uploaded
                    multiple=False
                ),
            ]
        ),
        html.Hr(),
        html.Div(id='yellow-pdf-pos'),
    ], style={'padding': '0', 'width': '100%'})


@app.callback(Output('yellow-pdf-pos', 'children'),
              [Input('upload-yellow-pdf', 'contents')],
              [State('upload-yellow-pdf', 'filename'),
               State('upload-yellow-pdf', 'last_modified')])
def show_pdf(content, name, date):
    """

    :param content: uploaded file content
    :param name: uploaded file name
    :param date: uploaded file date
    :return: the pdf and the extracted information in table
    """
    if content is not None:
        return YellowPdfParser.parse_pdf_content_dash(content, name, date)
    else:
        return ''


@app.callback([Output('submit-yellow-pos-loading', 'children'),
               Output('alert-yellow-pos', 'children')],
              [Input('submit-yellow-pos', 'n_clicks')])
def submit_pdf(n_clicks):
    """

    :param n_clicks: on click submit the pdf
    :return: alert message
    """
    if 0 < n_clicks < 2:
        print(n_clicks)
        time.sleep(2)
        return '', dbc.Alert("POS added to database.", color="success")
    if n_clicks > 1:
        return '', dbc.Alert("POS already added to database.", color="danger")
    return '', ''