import glob
import sys
import re
import shutil
import os


sys.path.append('/Users/massimodipierro/Dropbox/web2py')

HEADER = r"""
\documentclass[justified,sixbynine,notoc]{tufte-book}
\title{web2py\\{\small Complete Reference Manual, 5th Edition}}
\author{Massimo Di Pierro}
\publisher{Experts4Solutions}

% For nicely typeset tabular material
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{makeidx}
\usepackage{tocloft}
\usepackage{parskip}
\usepackage{upquote}

%\setlength\parskip{33pt}  % our strange value
%\usepackage{CJK}

\usepackage{natbib}
\setlength{\bibsep}{0.0pt}

\makeindex
\usepackage{listings}
\usepackage{url}
\usepackage[utf8x]{inputenc}

\sloppy\raggedbottom

\definecolor{lg}{rgb}{0.9,0.9,0.9}
\definecolor{dg}{rgb}{0.3,0.3,0.3}
\def\ft{\small\tt}
\def\inxx#1{\index{#1}}

\lstset{language=Python,
keywords={A,B,BEAUTIFY,BODY,BR,CAT,CENTER,CLEANUP,CODE,COL,COLGROUP,CRYPT,DAL,DIV,EM,EMBED,FIELDSET,FORM,Field,H1,H2,H3,H4,H5,H6,HEAD,HR,HTML,HTTP,I,IFRAME,IMG,INPUT,IS\_ALPHANUMERIC,IS\_DATE,IS\_DATETIME,IS\_DATETIME\_IN\_RANGE,IS\_DATE\_IN\_RANGE,IS\_DECIMAL\_IN\_RANGE,IS\_EMAIL,IS\_EMPTY\_OR,IS\_EQUAL\_TO,IS\_EXPR,IS\_FLOAT\_IN\_RANGE,IS\_IMAGE,IS\_INT\_IN\_RANGE,IS\_IN\_DB,IS\_IN\_SET,IS\_IPV4,IS\_LENGTH,IS\_LIST\_OF,IS\_LOWER,IS\_MATCH,IS\_NOT\_EMPTY,IS\_NOT\_IN\_DB,IS\_NULL\_OR,IS\_SLUG,IS\_STRONG,IS\_TIME,IS\_UPLOAD\_FILENAME,IS\_UPPER,IS\_URL,LABEL,LEGEND,LI,LINK,LOAD,MARKMIN,MENU,META,OBJECT,OL,ON,OPTGROUP,OPTION,P,PRE,SCRIPT,SELECT,SPAN,SQLDB,SQLFORM,SQLField,SQLTABLE,STYLE,T,TABLE,TAG,TBODY,TD,TEXTAREA,TFOOT,TH,THEAD,TITLE,TR,TT,UL,URL,XHTML,XML,embed64,local\_import,redirect,request,response,session,xmlescape,jQuery},
   breaklines=true, basicstyle=\ttfamily\color{black}\footnotesize,
   keywordstyle=\bf\ttfamily,
   commentstyle=\it\ttfamily,
   stringstyle=\color{dg}\it\ttfamily,
   numbers=left, numberstyle=\color{dg}\tiny, stepnumber=1, numbersep=5pt,
   % frame=lr,
   backgroundcolor=\color{lg},
   tabsize=4, showspaces=false,
   showstringspaces=false
   aboveskip=6pt,
   belowskip=-3pt
}
\setcounter{secnumdepth}{4}
\setcounter{tocdepth}{4}
% Generates the index
\begin{document}

\frontmatter

\maketitle
\thispagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{2mm}
{\footnotesize
\vskip 1in
Copyright 2008-2013 by Massimo Di Pierro. All rights reserved.
\vskip 1cm

THE CONTENT OF THIS BOOK IS PROVIDED UNDER THE TERMS OF THE CREATIVE COMMONS PUBLIC LICENSE BY-NC-ND 3.0.

\url{http://creativecommons.org/licenses/by-nc-nd/3.0/legalcode}

THE WORK IS PROTECTED BY COPYRIGHT AND/OR OTHER APPLICABLE LAW. ANY USE OF THE WORK OTHER THAN AS AUTHORIZED UNDER THIS LICENSE OR COPYRIGHT LAW IS PROHIBITED.

BY EXERCISING ANY RIGHTS TO THE WORK PROVIDED HERE, YOU ACCEPT AND AGREE TO BE BOUND BY THE TERMS OF THIS LICENSE. TO THE EXTENT THIS LICENSE MAY BE CONSIDERED TO BE A CONTRACT, THE LICENSOR GRANTS YOU THE RIGHTS CONTAINED HERE IN CONSIDERATION OF YOUR ACCEPTANCE OF SUCH TERMS AND CONDITIONS.

Limit of Liability/Disclaimer of Warranty: While the publisher and
author have used their best efforts in preparing this book, they
make no representations or warranties with respect to the accuracy
or completeness of the contents of this book and specifically
disclaim any implied warranties of merchantability or fitness for a
particular purpose.  No warranty may be created ore extended by
sales representatives or written sales materials.
The advice and strategies contained herein may not be
suitable for your situation. You should consult with a professional
where appropriate.  Neither the publisher nor author shall be liable
for any loss of profit or any other commercial damages, including
but not limited to special, incidental, consequential, or other damages. \\ \\

For more information about appropriate use of this material contact:

\begin{verbatim}
Massimo Di Pierro
School of Computing
DePaul University
243 S Wabash Ave
Chicago, IL 60604 (USA)
Email: massimo.dipierro@gmail.com
\end{verbatim}

Library of Congress Cataloging-in-Publication Data: \\ \\
ISBN: 978-0-578-12021-8 \\
Build Date: \today
}

\newpage
%\begin{center}
%\noindent\fontsize{12}{18}\selectfont\itshape
\nohyphenation
\thispagestyle{empty}
\phantom{placeholder}
\vspace{2in}
\hskip 3in
{\it to my family}
%\end{center}
\newpage
\thispagestyle{empty}
\phantom {a}
\newpage

\setlength{\cftparskip}{\baselineskip}
\tableofcontents

\mainmatter
\begin{fullwidth}
%\begin{CJK*}{UTF8}{min}


\chapter*{Preface}
"""

FOOTER = r"""
\end{fullwidth}

\backmatter
\printindex

\begin{thebibliography}{999}
@BIBITEMS
\end{thebibliography}
\end{document}
"""

from gluon.contrib.markmin.markmin2latex import render

def getreference(path):
    data = open(path).read().split('\n')
    d = {}
    for line in data:
        if ':' in line and not line.startswith('#'):
            items=line.split(':',1)
            d[items[0].strip()]=items[1].strip()
    return d

def assemble(path):
    path = os.path.abspath(path)
    path1 = os.path.join(path,'??.markmin')
    text = '\n\n'.join(open(f,'r').read() for f in glob.glob(path1))
    text = text.replace('@///image',os.path.join(path,'images'))

    body, title, authors = render(text)
    body = body.replace('\\section{','\\chapter{'
                        ).replace('subsection{','section{')
    bibitems = []
    for item in re.compile('\\cite\{(.*?)\}').findall(body):
        for part in item.split(','):
            if not part in bibitems: bibitems.append(part)
    bibliography = []
    for item in bibitems:
        reference = getreference(os.path.join(path,'references',item))
        bibliography.append((item,reference['source_url']))
    txtitems = '\n'.join('\\bibitem{%s} \\url{%s}' % item for item in bibliography)
    body = body.replace('\@/','@/')
    body = body.replace('{\\textbackslash}@/','@/')
    body = body.replace('\\begin{center}','\\goodbreak\\begin{center}')
    return HEADER + body + FOOTER.replace('@BIBITEMS',txtitems)

if __name__=='__main__':
    print assemble(sys.argv[1])
