import pdftotext
import base64
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from pdf2image import convert_from_bytes
from extract_data_text import TextScrapper
import io
from pandas import json_normalize


class PdfParser:

    def __init__(self, path_to_pdf, path_to_text):
        self.path_to_pdf = path_to_pdf
        self.path_to_text = path_to_text

    def read_pdf(self):
        # Load your PDF
        with open(self.path_to_pdf, "rb") as f:
            return pdftotext.PDF(f)

    def save_text_pdf(self):
        pdf = self.read_pdf()
        with open(self.path_to_text, "w") as f:
            f.write("\n\n".join(pdf))
        f.close()

    def save_text_no_empty_pdf(self):
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
        buffered = io.BytesIO()
        im.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        return bytes("data:image/jpeg;base64,", encoding='utf-8') + img_str

    @staticmethod
    def render_pdf_extract_dash(encoded_first_page, encoded_second_page, fields_df):

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
                ), dbc.Button("Submit",
                              id='submit-scrapping',
                              n_clicks=0,
                              outline=True,
                              color="danger",
                              style={"margin-top": "30px"},
                              className="mr-1")],
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
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        if decoded[0:4] != b'%PDF':
            raise ValueError('Missing the PDF file signature')

        filename_pdf_save_time = "data_dash/data_dash_pdf/pos.pdf"  #+ str(date) + "_" + filename
        filename_text_save_time = "data_dash/data_dash_text/pos.txt"  #+ str(date) + "_" + filename.split('pdf')[0] + ".txt"

        with open(filename_pdf_save_time, 'wb') as f:
            f.write(decoded)
            f.close()

        pdfParseObject = PdfParser(path_to_pdf=filename_pdf_save_time, path_to_text=filename_text_save_time)
        pdfParseObject.save_text_no_empty_pdf()

        textScrapperObject = TextScrapper(path_to_text=filename_text_save_time)
        fields_df = json_normalize(textScrapperObject.get_all_fields())

        images = convert_from_bytes(decoded)
        encoded_first_page = PdfParser.pil_to_b64_dash(images[0])
        encoded_second_page = PdfParser.pil_to_b64_dash(images[1])

        return pdfParseObject.render_pdf_extract_dash(encoded_first_page, encoded_second_page, fields_df)


# PdfParse = PdfParser(path_to_pdf='pdf_data/POSM.pdf', path_to_text='text_data/output.txt')
# PdfParse.save_text_no_empty_pdf()
