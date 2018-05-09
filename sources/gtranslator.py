
"""adapted from https://github.com/kindlychung/translator"""


import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup

class Translator:
    #allowed_lang = ("nl", "fr", "de", "en")
    def __init__(self, from_lang, to_lang, orig_str = None, filename = None):
        """
        :type self: Translator
        :type from_lang: str
        :type to_lang: str
        :type orig_str: str
        :type filename: str
        :param from_lang:
        :param to_lang:
        :param orig_str:
        :param filename:
        :return:
        """
        self._from_lang = from_lang
        self._to_lang = to_lang
        self.agent = {'User-Agent': "Mozilla/4.0"}
        self.linkroot = "http://translate.google.com/m?sl=%s&hl=%s&q=" % (self.from_lang, self.to_lang)


        self.orig_str = str(orig_str)


    @property
    def from_lang(self):
        return self._from_lang
    @from_lang.setter
    def from_lang(self, new_lang):
        '''
        print("Setting from_lang")
        if new_lang not in self.allowed_lang:
            raise Exception("%s not valid language option" % new_lang)
        '''
        self._from_lang = new_lang
    @property
    def to_lang(self):
        return self._to_lang
    @to_lang.setter
    def to_lang(self, new_lang):
        '''
        print("Setting to_lang")
        if new_lang not in self.allowed_lang:
            raise Exception("%s not valid language option" % new_lang)
        '''
        self._to_lang = new_lang

    def translate(self, verbose=False):
        if len(self.orig_str) > 0:
            query = urllib.parse.quote(self.orig_str)
            link = self.linkroot + query
            try:
                request = urllib.request.Request(link, headers=self.agent)
                webpage = urllib.request.urlopen(request).read()
                soup = BeautifulSoup(webpage,'lxml')
                res = soup.find_all("div", class_="t0")[0].string
                if verbose:
                    print(res)
            except:
                print('error in translate',self.orig_str)
                return self.orig_str


            return res
        else:
            return ''









# mystring = """
# „Ik zal zoo beknopt mogelijk in mijn verhaal zijn,[A 9] zonder iets weg te laten, dat tot een goed begrip der zaak noodig is. Het kan wezen, dat gij reeds iets van de geschiedenis hebt gehoord, want ik heb een onderzoek op 't oog in den vermoedelijken moord, gepleegd op kolonel Barclay van de Royal Mallows te Aldershot.”
# „Ik heb daarvan nog niets gehoord.”
# „Dit voorval heeft, behalve in de naaste omgeving, nog weinig de aandacht getrokken. De feiten dateeren ook eerst van eergisteren. In 't kort is de zaak deze:
# Zooals gij weet, zijn de Royal Mallows een van de beroemdste Iersche regimenten van het Engelsche leger. Het verrichtte indertijd wonderen van dapperheid in den Krimoorlog en heeft zich sedert bij elke gelegenheid onderscheiden. Tot Maandagavond j.l. stond dit regiment onder commando van James Barclay, een dapper veteraan, die zijn militaire loopbaan als gewoon soldaat begon, wegens zijn dapperheid tot den rang van officier opklom en eindelijk het opperbevel verkreeg over het regiment, waarin hij eens als gewoon soldaat had gediend.
# Kolonel Barclay trouwde, toen hij nog sergeant was, en zijn vrouw, als meisje Miss Nancy Devoy geheeten, was een dochter van een officier uit hetzelfde regiment. Het is daarom best te begrijpen, dat de omgeving, waarin de jonggehuwden
# """
# translator = Translator("nl", "en", mystring)
# translator.translate()
# print(translator.prettify())


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser("Translate a file")
    parser.add_argument("--fromlang", "-f", default="nl", help="From language, default to nl")
    parser.add_argument("--tolang", "-t", default="en", help="To language, default to en")
    parser.add_argument("--inputfile", "-i", help="Input file, default to stdin")
    parser.add_argument("--outputfile", "-o", help="Output file, default to stdout")
    args = parser.parse_args()

    if not args.inputfile:
        input_string = sys.stdin.read(encoding)
    else:
        with open(args.inputfile, encoding="utf8", errors="replace") as fh:
            input_string = fh.read()

    trans = Translator(args.fromlang, args.tolang, input_string)
    trans.translate()
    output_string = trans.prettify()

    if not args.outputfile:
        print(output_string)
    else:
        with open(args.outputfile, "w", encoding="utf8", errors="replace") as fh:
            fh.write(output_string)


if __name__ == "__main__":
    main()
