import pdftotext
from extract_data_text import YellowTextScrapper
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


def extract_info_pdf(filename_text, filename_pdf):
    import pandas as pd
    import pprint
    pd.set_option('display.max_rows', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('max_colwidth', False)

    pdfParseObject = PdfParser(path_to_pdf=filename_pdf, path_to_text=filename_text)
    pdfParseObject.save_text_no_empty_lines_pdf()
    textScrapperObject = YellowTextScrapper(path_to_text=filename_text)
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



