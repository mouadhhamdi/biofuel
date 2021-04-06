import dash_core_components as dcc
import dash_html_components as html
import base64


def get_logo_image():
    image_filename = './data_dash/mercuria_logo.png'  # replace with your own image
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return encoded_image


load_layout = html.Div(children=[
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
                   "margin-left": "550px"}),

    html.Div(
        children=[
            dcc.Upload(
                id='upload-pdf',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select PDF')
                ]),
                style={
                    'width': '60%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'font-family': 'Open Sans Condensed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    "background-color": "#f8f9fa",
                    "margin-left": "300px",
                    "margin-top": "70px",
                },
                # Allow multiple files to be uploaded
                multiple=False
            ),
        ]
    ),
    html.Div(id='output-pdf'),
    html.Div(id='table-output')
])
