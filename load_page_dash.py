import dash_core_components as dcc
import dash_html_components as html
import base64
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from server import app
import time
import dash_table
import io
from pdf2image import convert_from_bytes
import os
from extract_data_text import YellowTextScrapper, BlueTextScrapper
from extract_data_pdf import PdfParser
from pandas import json_normalize


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
                 height=120,
                 width=120,
                 style={'display': 'inline-block',"margin": " 1% 1%",
},
                 ),

        html.H1('Bio Fuel',
                style={'color': '111',
                       'font-family': 'Open Sans Condensed',
                       'font-size': '80px',
                       'font-weight': 'bold',
                       'letter-spacing': '-1px',
                       'line-height': '1',
                       'text-align': 'center',
                       'display': 'inline-block',
                       "margin": "0em 35%"}),

        html.Div(
            children=[
                dcc.Upload(
                    id='upload-pdf',
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
        html.Div(id='pdf-pos', style={'margin': '0', 'padding': '0'}),
    ])


@app.callback(Output('pdf-pos', 'children'),
              [Input('upload-pdf', 'contents')],
              [State('upload-pdf', 'filename'),
               State('upload-pdf', 'last_modified')])
def show_pdf(content, name, date):
    """

    :param content: uploaded file content
    :param name: uploaded file name
    :param date: uploaded file date
    :return: the pdf and the extracted information in table
    """
    if content is not None:
        return parse_pdf_content_dash(content)


def pil_to_b64_dash(im):
    """

    :param im: images
    :return: images in byte format
    """
    buffered = io.BytesIO()
    im.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())

    return bytes("data:image/jpeg;base64,", encoding='utf-8') + img_str

def parse_pdf_content_dash(contents):
    """

    :param contents: pdf content
    :param filename: name of the pdf
    :param date: date of upload of the pdf
    :return: div with the pdf and dashtable of the extracted information
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if decoded[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')

    pdf_folder_path = "data_dash/data_dash_pdf"
    text_folder_path = "data_dash/data_dash_text"

    try:
        os.mkdir(pdf_folder_path)
        os.mkdir(text_folder_path)
    except OSError:
        print("Directory %s already exists" % pdf_folder_path)
        print("Directory %s already exists" % text_folder_path)
    else:
        print("Successfully created directory %s" % pdf_folder_path)

    pdf_file_path = os.path.join(pdf_folder_path,"pos.pdf")
    text_file_path = os.path.join(text_folder_path,"pos.txt")
    with open(pdf_file_path, 'wb') as f:
        f.write(decoded)
        f.close()

    pdfParseObject = PdfParser(path_to_pdf=pdf_file_path, path_to_text=text_file_path)
    pdfParseObject.save_text_no_empty_lines_pdf()

    with open(text_file_path) as f:
        text = f.read()

    if 'V4.4' in text :
        textScrapperObject = BlueTextScrapper(path_to_text=text_file_path)
    else:
        textScrapperObject = YellowTextScrapper(path_to_text=text_file_path)

    fields_df = json_normalize(textScrapperObject.get_all_fields())

    images = convert_from_bytes(decoded)
    encoded_first_page = pil_to_b64_dash(images[0])
    encoded_second_page = pil_to_b64_dash(images[1])

    return render_pdf_extract_dash(encoded_first_page, encoded_second_page, fields_df)

def render_pdf_extract_dash(encoded_first_page, encoded_second_page, fields_df):
    """

    :param encoded_first_page: first pdf page
    :param encoded_second_page: second pdf page
    :param fields_df: fields extracted for the pdf
    :return: div with the pdf and dashtable of the extracted information
    """
    df_transpose = fields_df.T
    df_transpose = df_transpose.reset_index().rename(columns={0: 'Value', 'index': 'Field'})

    return html.Div([
        html.Img(src=encoded_first_page.decode('utf-8'),
                 style={'width': '50%', 'display': 'inline-block'}),
        html.Div(children=[
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_transpose.columns],
                is_focused=True,
                data=df_transpose.to_dict('records'),
                style_cell={'textAlign': 'left'},
                style_as_list_view=True,
                style_data={
                    'whiteSpace': 'normal',
                    'height': 40,
                },
                style_data_conditional=[{
                    'if': {
                        'column_id': 'Value',
                    },
                    'color': '#C3082A',
                    },
                    {
                    "if": {"state": "selected"},  # 'active' | 'selected'
                    "backgroundColor": "inherit",
                    "border": "inherit",
                    },
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                editable=True
            ),  html.Div(
                [
                    dbc.Button("Submit",
                               id='submit-pos',
                               n_clicks=0,
                               outline=True,
                               color="black",
                               style={'width': '30%',
                                      'padding': '1em',
                                      'margin-bottom': '1em',
                                      "margin-top": "15px"}),
                    dcc.Loading(html.Div(id="submit-pos-loading"), type="circle"),
                    dbc.Alert('POS added to database',id='alert-pos-green',style={'width': '70%',"margin-top": "5px"},color='green',is_open=False),
                    dbc.Alert('POS already added to database',id='alert-pos-red', style={'width': '70%', "margin-top": "5px"},color='danger',is_open=False),
                ]
                ),
            ],
            style={'width': '50%',
                   'display': 'inline-block',
                   'vertical-align': 'top',
                   "margin-top": "30px"}),
        html.Img(src=encoded_second_page.decode('utf-8'),
                 style={'width': '50%',
                        'display': 'inline-block',
                        "margin-top": "30px"}),
    ])


@app.callback([Output('submit-pos-loading', 'children'),
               Output('alert-pos-green', 'is_open')],
              [Input('submit-pos', 'n_clicks')],)
def show_green_message(n_clicks):
    """

    :param n_clicks: on click submit the pdf
    :return: alert message
    """
    if n_clicks==1:
        time.sleep(2)
        return '', True
    else:
        return '', False


@app.callback(Output('alert-pos-red', 'is_open'),
              Input('submit-pos', 'n_clicks'),)
def show_red_message(n_clicks):
    """

    :param n_clicks: on click submit the pdf
    :return: alert message
    """
    if n_clicks>1:
        return True
    else:
        return False