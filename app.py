import dash
from dash.dependencies import Input, Output, State
from extract_data_pdf import PdfParser
from load_page_dash import load_layout
import dash_bootstrap_components as dbc
import dash_html_components as html

external_stylesheets = [dbc.themes.MATERIA]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.suppress_callback_exceptions = True
app.layout = load_layout


@app.callback(Output('output-pdf', 'children'),
              [Input('upload-pdf', 'contents')],
              [State('upload-pdf', 'filename'),
               State('upload-pdf', 'last_modified')])
def show_pdf(content, name, date):
    if content is not None:
        children = PdfParser.parse_pdf_content_dash(content, name, date)
        return children


@app.callback(Output('table-output', 'children'),
              [Input('submit-scrapping', 'n_clicks')])
def show_pdf(n_clicks):
    print(n_clicks)
    return


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=True)
