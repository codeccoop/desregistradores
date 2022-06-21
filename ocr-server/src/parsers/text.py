# BUILT-INS
import re
from spellchecker import SpellChecker

# from unidecode import unidecode
from src.parsers.numeric import Numeric


spell = SpellChecker(language="es")


class Parser(object):
    __text = None

    def __init__(self, text=""):
        self.text = text

    def __str__(self):
        return self.text

    def __add__(self, other):
        if other:
            if type(other) == type(self):
                return self.__class__(self.text + "\n" + other.text)
            elif type(other) == str:
                return self.__class__.match(self.text + "\n" + other)

        return self

    def __radd__(self, other):
        if other:
            if type(other) == type(self):
                return self.__class__(other.text + "\n" + self.text)
            elif type(other) == str:
                return self.__class__.match(other + "\n" + self.text)

        return self

    def __len__(self):
        return len(self.text)

    @staticmethod
    def decamelize(text):
        decamelized = text
        for capital in re.findall(r"(?<=[a-z])[A-Z]", text):
            decamelized = (
                decamelized[: decamelized.index(capital)]
                + " "
                + capital
                + decamelized[decamelized.index(capital) :]
            )

        return decamelized

    @staticmethod
    def spell(text):
        return " ".join([spell.correction(word) for word in text.split(" ")])

    @staticmethod
    def sanitize(text):
        return re.sub(
            r"(à|á|ä)",
            "a",
            re.sub(
                r"(è|é|ë)",
                "e",
                re.sub(
                    r"(ì|í|ï)",
                    "i",
                    re.sub(
                        r"(ò|ó|ö)",
                        "o",
                        re.sub(r"(ù|ú|ü)", "u", text, flags=re.IGNORECASE),
                        flags=re.IGNORECASE,
                    ),
                    flags=re.IGNORECASE,
                ),
                flags=re.IGNORECASE,
            ),
            flags=re.IGNORECASE,
        )

    @staticmethod
    def clean_text(text):
        try:
            return re.sub(
                r" +(?=(\,|\.|\:|\;))",
                "",
                re.sub(
                    r"(?<= ) +",
                    " ",
                    re.sub(
                        r"€+",
                        "",
                        re.sub(
                            r"(?<=\n) +",
                            "",
                            Parser.sanitize(text.strip()),
                            flags=re.IGNORECASE,
                        ),
                        flags=re.IGNORECASE,
                    ),
                    flags=re.IGNORECASE,
                ),
                flags=re.IGNORECASE,
            )
        except Exception as e:
            print(e)
            print("Error on Parser.clean_text()")
            return text

    @staticmethod
    def search(pattern, string):
        try:
            return re.search(pattern, string, flags=re.IGNORECASE)
        except Exception as e:
            print(e)
            print("Error on Parser.search()")
            return None

    @staticmethod
    def sub(pattern, replace, string):
        try:
            return re.sub(pattern, replace, string, count=0, flags=re.IGNORECASE)
        except Exception as e:
            print(e)
            print("Error on Parser.sub()")
            return string

    @staticmethod
    def findall(pattern, string):
        try:
            return re.findall(pattern, string, flags=re.IGNORECASE)
        except Exception as e:
            print(e)
            print("Error on Parser.findall()")
            return None

    @property
    def text(self):
        return self.__text or ""

    @text.setter
    def text(self, text):
        if text and type(text) == str:
            if self.__text:
                self.__text += "\n" + text
            else:
                self.__text = text

    @property
    def data(self):
        return self.text


class CoverParser(Parser):
    @staticmethod
    def match(text):
        match = Parser.search(r"((?!descripcion).)+", text)
        if match:
            cover_content = Parser.sub(r"descripcion.*", "", match.group())
            return CoverParser(cover_content)


class DescriptionParser(Parser):
    @staticmethod
    def match(text):
        match = Parser.search(
            r"descripcion *\: *((?!(titulo|titulares|titularidades)).)+", text
        )
        if match:
            description_body = Parser.sub(r"^descripcion\:? *", "", match.group())
            return DescriptionParser(description_body)

    @property
    def data(self):
        data = dict()
        data["qualification"] = self.qualification
        data["type"] = self.type
        data["town"] = self.town
        data["street"] = self.street
        data["number"] = self.number
        data["surface"] = self.surface
        return data

    @property
    def qualification(self):
        match = Parser.search(r"(rustica|urbana)", self.text)
        if match:
            return match.group()

        type = self.type
        type = type and type.lower() or type
        if type and "terreno" not in type:
            return "urbana"

    @property
    def type(self):
        match = Parser.search(r"(porcion de terreno|vivienda|casa)", self.text)
        if match:
            return match.group()

    @property
    def town(self):
        match = Parser.search(
            r"(?:sita|sito|situado|situada) en (((?!(?:\.|\,|\;)).)+)", self.text
        )
        if match:
            return Parser.sub(r" *calle.*", "", match.groups()[0])

        match = Parser.search(
            r"(?:porcion de terreno|vivienda) en (((?!(?:\.|\,|\;)).)+)", self.text
        )
        if match:
            return Parser.sub(r" *calle.*", "", match.groups()[0])

    @property
    def street(self):
        if self.qualification and self.qualification.lower() == "rustica":
            return None

        match = Parser.search(r"(calle|plaza|camino) *(((?!,).)+)", self.text)
        if match:
            return (
                Parser.decamelize(match.groups()[0])
                + " "
                + Parser.sub(r" *numero.*", "", match.groups()[1])
            )

    @property
    def number(self):
        if self.qualification and self.qualification.lower() == "rustica":
            return None

        match = Parser.search(r"(?:numero) * (((?!(?:\.|\,|\;)).)+)", self.text)
        if match:
            return match.groups()[0]

    @property
    def surface(self):
        # match = Parser.search(r"(?:(?!superficie.*)superficie) *(?:total)? *(?:construida|edificada)? * (?:de)? *(((?!(?:\.|\,|\;)).)+)", self.text)
        match = Parser.search(
            r"(?<=superficie) ?(?:(?!(metro|area)).)*(metro|area)", self.text
        )
        if match:
            tokens = [token for token in Numeric.tokens() if token != "un"]
            sentence = " ".join(
                [Parser.spell(word) for word in match.group().split(" ")]
            )
            pos = None
            for token in tokens:
                if token in sentence:
                    new_pos = sentence.index(token)
                    if not pos or pos > new_pos:
                        pos = new_pos
            if pos is None:
                return pos
            pattern = re.compile("(" + "|".join(tokens) + ").*")
            return (
                pattern.match(Parser.sub(r" *(area|metro) *", "", sentence), pos=pos)
                .group()
                .strip()
                + " ("
                + match.groups()[1]
                + ")"
            )


class OwnershipParser(Parser):
    @staticmethod
    def match(text):
        match = Parser.search(r"titulo *\: *((?!cargas).)+", text)
        if match:
            ownership_body = Parser.sub(r"^titulo *\: *", "", match.group())
            return OwnershipParser(ownership_body)

    @property
    def data(self):
        data = dict()
        data["owner"] = self.owner
        data["nie"] = self.nie
        data["participation"] = self.participation
        data["adjudication"] = self.adjudication
        data["notary"] = self.notary
        data["town"] = self.town
        data["date"] = self.date
        return data

    @property
    def owner(self):
        match = Parser.search(r"titular\/es\:? *(((?!,).)+)", self.text)
        if match:
            return match.groups()[0].strip()

    @property
    def nie(self):
        match = Parser.search(
            r"(dni|cif).* (?:-)?([a-zA-Z]?[0-9]{8}[a-zA-Z]?) *", self.text
        )
        if match:
            return match.groups()[1].strip()

    @property
    def participation(self):
        match = Parser.search(r"participacion *\: *(((?!Titulo).)+)", self.text)
        if match:
            return match.groups()[0].strip()

    @property
    def adjudication(self):
        match = Parser.search(r"titulo *: *(((?!notario).)+)", self.text)
        if match:
            return match.groups()[0].strip()

    @property
    def notary(self):
        match = Parser.search(
            r"notario(?:\/autoridad)? *: *(((?!poblacion).)+) ", self.text
        )
        if match:
            return match.groups()[0].strip()

    @property
    def town(self):
        match = Parser.search(r"poblacion *: *(((?!fecha).)+)", self.text)
        if match:
            return match.groups()[0].strip()

    @property
    def date(self):
        match = Parser.search(
            r"fecha (?:documento|escritura) *: *((?!protocolo)[0-9]{2}\/[0-9]{2}\/[0-9]{4})",
            self.text,
        )
        if match:
            return match.groups()[0].strip()


class ChargesParser(Parser):
    @staticmethod
    def match(text):
        match = Parser.search(r"cargas *\: *((?!presentacion).)+", text)
        if match:
            charges_body = Parser.sub(r"^cargas\: *", "", match.group())
            return ChargesParser(charges_body)


# def get_presentation (text):
#     match = re.search(r"(PRESENTACION\:)?((?!-+).)+", text)
#     if match:
#         return re.sub("^PRESENTACION\: *", "", re.sub(r"€+", " ", match.group()))


class TextParser(object):

    __cover = CoverParser()
    __description = DescriptionParser()
    __ownership = OwnershipParser()
    __charges = ChargesParser()

    def __init__(self, text, spell=False):
        if spell is True:
            pass
            # text = Parser.spell(text)
        text = Parser.clean_text(text)
        self.cover = text
        text = Parser.sub(re.escape(self.cover.text), "", text)
        self.description = text
        text = Parser.sub(re.escape(self.cover.text), "", text)
        self.ownership = text
        text = Parser.sub(re.escape(self.ownership.text), "", text)
        self.charges = text

    @property
    def cover(self):
        return self.__cover

    @cover.setter
    def cover(self, cover):
        if cover:
            if type(cover) == CoverParser:
                self.__cover = self.cover + cover
            elif type(cover) == str:
                self.__cover = self.cover + CoverParser.match(cover)
            else:
                pass
                raise TypeError(
                    "Description property accepts string type values. "
                    + type(cover)
                    + " was found."
                )

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        if description:
            if type(description) == DescriptionParser:
                self.__description = self.description + description
            elif type(description) == str:
                self.__description = self.description + DescriptionParser.match(
                    description
                )
            else:
                pass
                raise TypeError(
                    "Description property accepts string type values. "
                    + type(description)
                    + " was found."
                )

    @property
    def ownership(self):
        return self.__ownership or OwnershipParser()

    @ownership.setter
    def ownership(self, ownership):
        if ownership:
            if type(ownership) == OwnershipParser:
                self.__ownership = self.ownership + ownership
            elif type(ownership) == str:
                self.__ownership = self.ownership + OwnershipParser.match(ownership)
            else:
                pass
                raise TypeError(
                    "Ownership property accepts string type value. "
                    + type(ownership)
                    + " was found."
                )

    @property
    def charges(self):
        return self.__charges or ChargesParser()

    @charges.setter
    def charges(self, charges):
        if charges:
            if type(charges) == ChargesParser:
                self.__charges = self.charges + charges
            elif type(charges) == str:
                self.__charges = self.charges + ChargesParser.match(charges)
            else:
                pass
                raise TypeError(
                    "Charges property accepts string type value. "
                    + type(charges)
                    + " was found."
                )

    @property
    def text(self):
        return (
            "Description:\r"
            + f"{self.description}\n"
            + "Ownership:\r"
            + f"{self.ownership}\n"
            + "Charges:\r"
            + f"{self.charges}\n"
        )

    @property
    def success(self):
        return len(self.description) or len(self.charges) or len(self.ownership)

    def __str__(self):
        return self.text


if __name__ == "__main__":
    import os

    directory = os.path.relpath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "../pdfs/T1")
    )
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        parser = TextParser(file_path)
        print(file_name.upper())
        print(parser.description)
        print(parser.description.data)
        print()
