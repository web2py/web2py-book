# The official web2py book

License: [Creative Commons  BY-NC-ND](http://creativecommons.org/licenses/by-nc-nd/3.0/legalcode)

[Read the book online](http://web2py.com/books)

This web2py book github repository consists of:

 - the book sources (in English, translated in many languages), in the source folder
 - a full working web2py application (python 3 compatible) for generating the HTML output. This is the same one used for generating the web pages of the manual on the main web2py site
 - the python code used to produce the LaTeX output, in the private folder. This is used to obtain the PDF and also the printed version 

The web2py book application can also be installed locally for offline use, editing or testing. In this case you need the full web2py framework  (version 2.15.3 or higher) with the pygments Python module installed for HTML output.

You can easily contribute to the book by submitting patches related to the english version, or its translations.

## Notes to translators

Install with GIT:

    git clone https://github.com/web2py/web2py-book.git

Check what has changed since version 5 of the book:
    
    cd web2py-book
    git diff --relative 4b0feb3dac1c448c6752450d810b227fd325d454 sources/29-web2py-english/

(or git diff -r 5a78edad03160fff97836b8a8d93d185b34d378d sources/29-web2py-english/ for changes since version 4 of the book)

Implement the changes under the proper book source.

## Syntax

The book is in the markmin syntax. Images are included with the syntax

    [[image @///image/key width:200px]]

where "image" is a label "key" is the name of a file under the sources/*/images/ folder.

References are added with

    ``key``:cite

Where "key" is the name of a file under the sources/*/references/ folder. Look at existing references for format.

Index entries are added with

    ``name``:inxx

They are used to build the printable book index.

You can also add internal anchors (i.e. links) that will be automatically numbered and transformed to hyperlinks on the Web and PDF output.
You can find all the markmin syntax reference on this page http://web2py.com/examples/static/markmin.html

Once done submit  patch as a pull request on github, or email the author.

### Translator agreement

If you plan to help with the book translation please contact the author in order to reach an agreement about copyright and distribution.
