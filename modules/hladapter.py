# -*- coding: utf-8 -*-

from gluon.contrib.markmin.markmin2html import make_dict
from gluon.html import PRE
from gluon._compat import to_native

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from ast import literal_eval
from traceback import format_exception_only
import sys


def hladapter(txt, clsid='',
              hlargs=dict(lexer='python', linenos=False)):
    """
    Pygments highlight() adapter for Markmin.

    This function let you fully customize the syntax highlighting
    of a verbatim block (i.e. something like ``...``:class[id]
    which is generally used to display source code) at markup level.

    Pass this callable using the extra argument of a markmin2html
    call to enable processing of a custom class, for example:

    html = markmin2html('<markup text>', extra=dict(code=hladapter))

    will enable syntax highlighting on  ``...``:code markup through
    a call to Pygments highlight() function, to be precise to

    highlight('...', get_lexer_by_name('python'),
                     HtmlFormatter(linenos=False))

    see http://pygments.org/docs/index.html for Pygments documentation.

    Thanks to this function you can now choose the lexer to use, pass
    arguments to the lexer and to the HtmlFormatter instances with the
    following markup syntax:

    ``...``:code[lexer='alias', lexer_opt1=val1, lexer_opt2=val2, opt3=val3, ...]

    Options to be passed to the lexer have to be prefixed by 'lexer_'
    (the prefix is stripped off from the option name before use),
    all remaining arguments are used as options for the formatter,
    the example above will result in the following call

    highlight('...', get_lexer_by_name('alias', opt1=val1, opt2=val2),
                     HtmlFormatter(linenos=False, opt3=val3))

    Default arguments passed to highlight (i.e. when no [...] syntax is
    used in markup) are those found in hlargs argument of this function.
    You can override any of the default arguments, other arguments are
    simply added to defaults.

    See http://pygments.org/docs/lexers/index.html for an up-to-date
    list of available lexers and their aliases (short names) and options.

    See http://pygments.org/docs/formatters/index.html#HtmlFormatter for
    available formatter options and their meaning.

    For example, to have line counting starting at 8, lines 2nd and 23th
    highlighted, and no syntax highlighting on a code block, use:

    ...``:code[lexer=None, linenos=True, linenostart=8, hl_lines=(2, 23)]

    Notice that due to a limit of the regex_code in markmin2html.py
    currently you need to use a tuple instead of a list for hl_lines,
    moreover Pygments always counts the lines to highlight starting at 1,
    no matter if a linenostart != 1 is present.
    """
    try:
        cidd = literal_eval(make_dict(clsid)) if clsid else {}
        kwargs = hlargs.copy()
        kwargs.update(cidd)
        # Pygments NULL lexer is TextLexer (text)
        lexer_alias = kwargs.pop('lexer', 'text') or 'text'
        lexer_opts = {}
        formatter_opts = {}
        for k in kwargs:
            if k.startswith('lexer_'):
                lexer_opts[k[6:]] = kwargs[k]
            elif k == 'hl_lines' and not isinstance(kwargs[k], tuple):
                # allow single value (not a tuple)
                formatter_opts[k] = (kwargs[k],)
            else:
                formatter_opts[k] = kwargs[k]
        lexer = get_lexer_by_name(lexer_alias, **lexer_opts)
        # NOTE: enabling linenos on HtmlFormatter lead to
        #       <div class="highlight_wrapper">
        #         <table class="highlighttable">
        #           <tr>
        #             <td class="linenos"><div class="linenodiv"><pre>
        #               ...
        #             </pre></div></td>
        #             <td class="code"><div class="highlight"><pre>
        #               ...
        #             </pre></div></td>
        #           </tr></table></div>
        #
        #       otherwise (disabled linenos)
        #       <div class="highlight_wrapper">
        #         <div class="highlight"><pre>
        #           ...
        #         </pre></div>
        formatter = HtmlFormatter(**formatter_opts)
        return ''.join(('<div class="highlight_wrapper">',
                        to_native(highlight(txt, lexer, formatter)),
                        '</div>'))
    except:
        return PRE(format_exception_only(*(sys.exc_info()[:2]))).xml()
