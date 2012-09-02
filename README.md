# The official web2py book

License: [Creative Commons  BY-NC-ND](http://creativecommons.org/licenses/by-nc-nd/3.0/legalcode)

[Read the book online](http://web2py.com/books)

The gitbub repo includes code and sources. The book sources are in the sources folder. You can contribute to the book by submitting patches.

## Notes to translators

Install GIT with

    git clone https://github.com/mdipierro/web2py-book.git

Check what has changed since verison 4 of the book:

    git diff -r 5a78edad03160fff97836b8a8d93d185b34d378d sources/29-web2py-english/

Implement the changes under the proper book source.
The book is in the markmin syntax. Images are incuded with the sytnax

    [[image @///image/key width:200px]]

where "image" is a label "key" is the name of a file under the sources/*/images/ folder.

References are added with

    ``key``:cite

Where "key" is the name of a file under the sources/*/references/ folder. Look at existing references for format.

Index entries are added with

    ``name``:inxx

They are used to build the printable book index.

Once done submit  patch as a pull request on github or email the author.

### Translator agreement

If you plan to help with the book translation please contact me we can reach an agreement about copyright and distribution.