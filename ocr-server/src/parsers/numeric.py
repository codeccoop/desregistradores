import re


class Numeric (object):
    decimals = {
        "uno": 1,
        "un": 1,
        "dos": 2,
        "tres": 3,
        "cuatro": 4,
        "quatre": 4,
        "cinco": 5,
        "cinc": 5,
        "seis": 6,
        "sis": 6,
        "siete": 7,
        "set": 7,
        "ocho": 8,
        "vuit": 8,
        "nueve": 9,
        "nou": 9
    }

    teens = {
        "once": 11,
        "onze": 11,
        "doce": 12,
        "dotze": 12,
        "trece": 13,
        "tretze": 13,
        "catorce": 14,
        "catorze": 14,
        "quince": 15,
        "quinze": 15,
        "dieziseis": 16,
        "setze": 16,
        "diezisiete": 17,
        "diset": 17,
        "dieziocho": 18,
        "divuit": 18,
        "diezinueve": 19,
        "dinou": 19
    }

    tenths = {
        "diez": 10,
        "deu": 10,
        "veinte": 20,
        "veint": 20,
        "vint": 20,
        "treinta": 30,
        "trenta": 30,
        "cuarenta": 40,
        "quaranta": 40,
        "cincuenta": 50,
        "cinquanta": 50,
        "sesenta": 60,
        "seixanta": 60,
        "setenta": 70,
        "ochenta": 80,
        "vuitanta": 80,
        "noventa": 90,
        "noranta": 90,
    }

    hundreds = {
        "cien": 100,
        "cent": 100,
    }

    thousands = {
        "mil": 1000
    }

    def __init__ (self, value=None):
        self.__raw = value or ""

    def __add__ (self, other):
        if other:
            if type(other) == int or type(other) == float:
                return Numeric(self.val + other)
            elif type(other) == str and other.isnumeric():
                return Numeric(self.val + float(other))
            else:
                return Numeric(self.val + Numeric(other))

        return self

    def __radd__ (self, other):
        if other:
            if type(other) == int or type(other) == float:
                return Numeric(self.val + other)
            elif type(other) == str and other.isnumeric():
                return Numeric(self.val + float(other))
            else:
                return Numeric(self.val + Numeric(other))

        return self

    def __str__ (self):
        val = ""
        try:
            val = str(int(self.val))
        except:
            try:
                val = str(self.val)
            except:
                pass
        finally:
            return val

    @property
    def val (self):
        return self.parse(self.__raw)

    @staticmethod
    def tokens ():
        num = Numeric()
        return list(num.decimals.keys()) \
            + list(num.teens.keys()) \
            + list(num.tenths.keys()) \
            + list(num.hundreds.keys()) \
            + list(num.thousands.keys())

    def parse (self, val):
        if type(val) == int or type(val) == float:
            return val
        elif type(val) == str:
            if val.isnumeric():
                return float(val)
            elif val.isalnum():
                return self.alnum_to_num(val)
        else:
            raise TypeError("Can't parse value")

    def alnum_to_num (self, chars):
        if not chars:
            return 0

        chars = chars.lower()

        number = 0
        for decimal in self.decimals:
            match = re.search(r"(?<![a-z])[yi-]? *(%s)(?![a-z])" % decimal, chars)
            if match:
                number += self.decimals.get(match.groups()[1])

        for teen in self.teens:
            match = re.search(r"(?<=[a-z])(%s)(?![a-z])" % teen, chars)
            if match:
                number += self.teens.get(match.groups()[0])

        for tenth in self.tenths:
            match = re.search(r"(?<![a-z])(%s) *[yi-]? *([a-z]+)?(?![a-z])? *" % tenth, chars)
            if match:
                number += self.tenths.get(match.groups()[0])

        for hundred in self.hundreds:
            match = re.search(r"(?<![a-z])([a-z]+)?%s(?:tos?|s?)?(?![a-z])" % hundred, chars)
            if match:
                number += (self.decimals.get(match.groups()[0])) or 1 * 100

        for thousand in self.thousands:
            match = re.search(r"(?<![a-z])([a-z]+)?%s(?![a-z])" % thousand, chars)
            if match:
                print("match thousands")
                number += (self.decimals.get(match.groups()[0])) or 1 * 1000

        return number
