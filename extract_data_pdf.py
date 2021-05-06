import pdftotext
import base64
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table
from pdf2image import convert_from_bytes
from extract_data_text import TextScrapper
import io
import os
from pandas import json_normalize


class PdfParser:

    def __init__(self, path_to_pdf, path_to_text):
        self.path_to_pdf = path_to_pdf
        self.path_to_text = path_to_text

    def read_pdf(self):
        """

        :return: read pdf file
        """
        # Load your PDF
        with open(self.path_to_pdf, "rb") as f:
            return pdftotext.PDF(f)

    def save_text_pdf(self):
        """

        :return: write text from pdf
        """
        pdf = self.read_pdf()
        with open(self.path_to_text, "w") as f:
            f.write("\n\n".join(pdf))
        f.close()

    def save_text_no_empty_lines_pdf(self):
        """

        :return: write text file from pdf without empty lines
        """
        pdf = self.read_pdf()
        with open(self.path_to_text, "w") as f:
            lines = "\n\n".join(pdf).split("\n")
            non_empty_lines = [line for line in lines if line.strip() != ""]
            string_without_empty_lines = ""
            for line in non_empty_lines:
                string_without_empty_lines += line + "\n"
            f.write("".join(string_without_empty_lines))
            f.close()

    @staticmethod
    def pil_to_b64_dash(im):
        """

        :param im: images
        :return: images in byte format
        """
        buffered = io.BytesIO()
        im.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        return bytes("data:image/jpeg;base64,", encoding='utf-8') + img_str

    @staticmethod
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
                                   color="danger",
                                   style={'width': '30%',
                                          'padding': '1em',
                                          'margin-bottom': '1em'}),
                        dcc.Loading(html.Div(id="submit-pos-loading"), type="circle"),
                        dbc.Alert(id='alert-pos', style={'width': '70%',
                                                         'display': 'inline-block',
                                                         "margin-top": "10px",
                                                         "margin-left": "10em"}),
                    ]
                    ),
                ],
                style={'width': '50%',
                       'display': 'inline-block',
                       'vertical-align': 'top',
                       "margin-top": "30px"}),
            html.Img(src=encoded_second_page.decode('utf-8'),
                     style={'width': '50%',
                            'display': 'inline-block'}),
        ])

    @staticmethod
    def parse_pdf_content_dash(contents, filename, date):
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

        textScrapperObject = TextScrapper(path_to_text=text_file_path)
        fields_df = json_normalize(textScrapperObject.get_all_fields())

        images = convert_from_bytes(decoded)
        encoded_first_page = PdfParser.pil_to_b64_dash(images[0])
        encoded_second_page = PdfParser.pil_to_b64_dash(images[1])

        return pdfParseObject.render_pdf_extract_dash(encoded_first_page, encoded_second_page, fields_df)


def extract_info_pdf(filename_text, filename_pdf):
    import pandas as pd
    import pprint
    pd.set_option('display.max_rows', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('max_colwidth', False)

    pdfParseObject = PdfParser(path_to_pdf=filename_pdf, path_to_text=filename_text)
    pdfParseObject.save_text_no_empty_lines_pdf()
    textScrapperObject = TextScrapper(path_to_text=filename_text)
    # pprint.pprint(textScrapperObject.get_all_fields())
    fields_df = json_normalize(textScrapperObject.get_all_fields())
    df_transpose = fields_df.T
    df_transpose = df_transpose.reset_index().rename(columns={0: 'Value', 'index': 'Field'})
    # print(df_transpose)
    df_transpose.to_csv("pos.csv", index=False)
    return df_transpose

# extract_info_pdf('data/text_data/pos.txt', 'data/pdf_data/Type1.pdf')
# extract_info_pdf('data/text_data/pos.txt', 'data/pdf_data/Type2.pdf')
# extract_info_pdf('data/text_data/pos.txt', 'data/pdf_data/Type3.pdf')



