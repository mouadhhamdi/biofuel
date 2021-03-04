import pdftotext
import os

pdf_data_path = os.path.join(os.path.curdir, '/pdf_data')
text_data_path = os.path.join(os.path.curdir, '/text_data')


def read_pdf(path):
    # Load your PDF
    with open(path, "rb") as f:
        return pdftotext.PDF(f)


def save_text_pdf(path):
    with open(path, "w") as f:
        f.write("\n\n".join(pdf))
        f.close()


def save_text_no_empty_pdf(path, pdf):
    with open(path, "w") as f:
        lines = "\n\n".join(pdf).split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]

        string_without_empty_lines = ""
        for line in non_empty_lines:
            string_without_empty_lines += line + "\n"
        f.write("".join(string_without_empty_lines))
        f.close()


pdf = read_pdf('pdf_data/POSM.pdf')
save_text_pdf("text_data/output.txt")
save_text_no_empty_pdf("text_data/POSM.txt", pdf)



