# BUILT-INS
import os

# VENDOR
from PyPDF2 import PdfFileReader

# SOURCE
from src.parsers.text import TextParser
from src.parsers.image import ImageParser


class PdfParser(object):
    def __init__(self, file_path):
        if not file_path or type(file_path) != str:
            raise ValueError("file_path arguments is not a valid type")
        elif not os.path.isfile(file_path):
            raise FileExistsError("Can't find nothing at the end of the path")

        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.conn = open(file_path, "rb")
        self.parser = PdfFileReader(self.conn)
        self.pages = [self.parser.getPage(i) for i in range(self.parser.getNumPages())]

    @property
    def format(self):
        has_text = bool(self.pages[0].extractText())
        if has_text:
            return "str"
        else:
            return "img"

    @property
    def data(self):
        if self.format == "str":
            text = ""
            for page in self.pages:
                text += "\n" + page.extractText()

            return TextParser(text)
        else:
            return TextParser(ImageParser(self.file_path).text, spell=True)

    def __str__(self):
        return self.data.text

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    directory = os.path.relpath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "../pdfs/T1")
    )
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        parser = PdfParser(file_path)
        print(file_name.upper())
        print(parser.data.ownership.data)
        print()
