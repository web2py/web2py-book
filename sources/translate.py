#!/usr/bin/env python3

from gtranslator import Translator
import os
import sqlite3
conn = sqlite3.connect("translations.sqlite") # ou use :memory: para botá-lo na memória RAM

cursor = conn.cursor()

def execute_sql(sql,parameters=None):
    cursor.execute(sql,parameters)
    conn.commit()
    return cursor.fetchone()
chuncks = []

#filename = "06.markmin"

def t(text,language='pt'):

    return call_translator_api(text,language)

def call_translator_api(text,language='pt'):
    '''TODO: # Implement a call to a real translator api, like google, bing, another
    using a experimental code from translator pip package

    '''

    trans = Translator('en', language, text)
    t = trans.translate(verbose=True)

    return t

def count_chars(filename):
    chars = []
    file = os.path.join("29-web2py-english/", filename)
    with open(file, "r") as f:
        for c in f.read():
            chars.append(c)
    #print(len(chars))
    return len(chars)


def check_markmin(chunck, language):
    # exceptions, need break down
    ignores_5 = [':inxx', ':code', ':cite']
    replaces = {" ** ":"**",
                " **,": "**,",
                '** "': '**"',
                ": **":":**",
                " / ":"/"}
    if language == 'pt':
        replaces["Chapter"] = "Capítulo"

    s = ''
    l = []
    row = execute_sql("""select translation 
            from translation 
            where original=?
            and language=?""",(chunck,language))
    if row:
        return row[0]
    else:
        original = chunck
        if chunck[:5] in ignores_5:
            s = chunck[:5]
            chunck = chunck[5:]
        lines = chunck.split('\n')
        for line in lines:
            if '[[' in line:
                cks = line.split(']]')
                tt = cks[0] + ']] ' + t(cks[1], language)
            else:
                tt = t(line,language)

            for b,a in replaces.items():
                tt = tt.replace(b,a)
            l.append(tt)
        brute = s + " " + "\n".join(l)
        execute_sql("""insert into translation 
                (language,original,translation)
                VALUES (?,?,?)""", (language, original, brute))
        return brute

def translate_file(filename, outputdir,language ='pt'):

        file = os.path.join("29-web2py-english/", filename)
        with open(file, "r") as f:
            text = f.read()
        tchars = len(text)
        chuncks = text.split('``')
        chars = 0
        cs = len(chuncks)
        l = 0

        fn = os.path.join(outputdir, filename)
        fh = open(fn, "w")
        for i in range(0,cs):
            #print(i)
            tt = chuncks[i]
            #print('test', tt[:5])
            if i%2 == 0: # text to translate

                if '\n###' in tt:
                    tt = tt.split('\n###')
                    brute = check_markmin(tt[0],language) + "\n### " + check_markmin(tt[1],language)
                else:
                    brute = check_markmin(tt,language)
                chars += len(brute)

                #print('translated:',brute)
                fh.write(brute)
                #translated = translated + '\n\n' + brute

                l +=1
            else:
                code = "``{}``".format(tt)

                print('escaped: ',code)
                chars +=len(code)
                fh.write("``{}``".format(tt))

            print('{:10.4f}'.format(chars / tchars*100),'%')


        fh.close()


        return chars
             



def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser("Translate the book files")
    #parser.add_argument("--fromlang", "-f", default="nl", help="From language, default to nl")
    parser.add_argument("--tolang", "-t", help="To language, default to pt")
    parser.add_argument("--file", "-f", default=None, help="file to translate, default to *.markmin + chapters.txt")
    parser.add_argument("--outputdir", "-d", default='99-web2py-test-translation/',help="Output dir, default to 99-web2py-test")
    args = parser.parse_args()

    if not args.tolang:
        print("""usage: Translate the book files [-h] [--tolang TOLANG] [--outputdir OUTPUTDIR]

optional arguments:
  -h, --help                            show this help message and exit
  --file FILE, -i FILE                  file to translate, default to *.markmin + chapters.txt
  --tolang TOLANG, -t TOLANG            To language code, like 'pt'
  --outputdir OUTPUTDIR, -d OUTPUTDIR   Output dir, default to 99-web2py-test-translation 
                        
REMINDER: the info.txt file still need to be altered manually""")
    else:
        #dir = args.outputdir if args.outputdir else '99-web2py-test-translation'
        import os
        """TODO: migrate to more secure subprocess module usage"""

        c = 0
        ct = 0
        if not args.file:
            os.system('cp -r 29-web2py-english {}'.format(args.outputdir))
            os.system('cp info.py {}/info.txt'.format(args.outputdir))
            for file in os.listdir(args.outputdir):
                if file.endswith(".markmin") or file == 'chapters.txt':
                    #print(os.path.join(".", file))
                    c += count_chars(file)
                    ct += translate_file(file,args.outputdir,language=args.tolang)
        else:
            if not os.path.isdir(args.outputdir):
                os.system('cp -r 29-web2py-english {}'.format(args.outputdir))
            c += count_chars(args.file)
            ct += translate_file(args.file,args.outputdir,language=args.tolang)
        #os.system('rm -rf __pycache__')
        print(c, 'characters in files > ', ct, 'translated')




if __name__ == "__main__":
    main()


