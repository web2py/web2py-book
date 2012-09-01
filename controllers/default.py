# -*- coding: utf-8 -*-
import os, glob

response.title = 'web2py'
response.subtitle = 'Full Stack Web Framework, 4th Ed.\nwritten by Massimo Di Pierro in English'
response.menu = []

def splitter(x):
    a,b = x.split(':',1)
    return a.strip(),b.strip()

@cache('folders',None)
def get_folders():
    folder = os.path.join(request.folder,'sources')
    return folder, [f for f in os.listdir(folder) 
                    if os.path.isdir(os.path.join(folder,f))]
FOLDER, FOLDERS = get_folders()

def get_subfolder(book_id):
    subfolders = [f for f in FOLDERS if f.startswith(book_id)]
    return subfolders[0] if subfolders else redirect(URL('index'))

def get_info(subfolder):
    infofile = os.path.join(FOLDER,subfolder,'info.txt')
    if os.path.exists(infofile):
        info = dict(splitter(line)
                    for line in open(infofile).readlines()
                    if ':' in line)
        return info
    return {}

def get_chapters(subfolder):
    filename = os.path.join(FOLDER,subfolder,'chapters.txt')
    chapters = [splitter(line)
                for line in open(filename).readlines()
                if ':' in line]
    return chapters

@cache('menu',None)
def build_menu():
    menu = []
    submenu = []
    for subfolder in FOLDERS:
        info = get_info(subfolder)
        book_id = subfolder.split('-')[0]
        submenu.append((info['title']+' '+info['language'],None,URL('chapter',args=book_id)))
    menu.append(('Books',None,None,submenu))
    menu.append(('Contribute',None,'https://github.com/mdipierro/web2py-book'))
    return menu

response.menu = build_menu()

def convert2html(book_id,text):
    extra = {}
    def url2(*a,**b):
        b['args'] = [book_id]+b.get('args',[])
        return URL(*a,**b)
    def truncate(x): return x[:70]+'...' if len(x)>70 else x
    extra['verbatim'] = lambda code: cgi.escape(code)
    extra['cite'] = lambda key: TAG.sup(
        '[',A(key,_href=URL('reference',args=(book_id,key)),
              _target='_blank'),']').xml()
    extra['inxx'] = lambda code: '<div class="inxx">'+code+'</div>'
    extra['ref'] = lambda code: '[ref:'+code+']'
    # extra['code'] = lambda code: CODE(code,language='web2py').xml()
    return MARKMIN(text.replace('\r',''),extra=extra,url=url2)

def index():
    books = {}
    for subfolder in FOLDERS:        
        books[subfolder] = get_info(subfolder)
    return locals()

def chapter():
    book_id, chapter_id = request.args(0), request.args(1,cast=int,default='0')
    subfolder = get_subfolder(book_id)
    info = get_info(subfolder)
    chapters = get_chapters(subfolder)
    filename = os.path.join(FOLDER,subfolder,'%.2i.markmin' % chapter_id)
    content = open(filename).read()
    content = convert2html(book_id,content)
    return locals()

def search():
    book_id = request.args(0) or redirect(URL('index'))
    search = request.vars.search or redirect(URL('chapter',args=book_id))
    subfolder = get_subfolder(book_id)
    info = get_info(subfolder)
    chapters = get_chapters(subfolder)
    results = []
    for chapter in chapters:
        chapter_id = int(chapter[0])
        filename = os.path.join(FOLDER,subfolder,'%.2i.markmin' % chapter_id)
        data = open(filename).read().replace('\r','')
        k = data.find(search)
        if k>=0:
            snippet = data[data.rfind('\n\n',0,k)+1:data.find('\n\n',k)].strip()
            results.append((chapter[0],chapter[1],convert2html(book_id,snippet)))
        content = CAT(*[DIV(H2(A(chapter[1],_href=URL('chapter',args=(book_id,chapter[0])))),
                            chapter[2],BR(),
                            A('more',_href=URL('chapter',args=(book_id,chapter[0])),_class="btn"))
                        for chapter in results])
        if not results:
            response.flash = "no results"
    response.view = 'default/chapter.html'
    return locals()

def image():
    book_id = request.args(0)
    key = request.args(1)
    subfolder = get_subfolder(book_id)
    filename = os.path.join(FOLDER,subfolder,'images',key)
    if not os.path.exists(filename):
        raise HTTP(404)
    return response.stream(open(filename,'r'))


def reference():
    book_id = request.args(0)
    key = request.args(1)
    subfolder = get_subfolder(book_id)
    filename = os.path.join(FOLDER,subfolder,'references',key)
    if not os.path.exists(filename):
        raise HTTP(404)
    info = dict(splitter(line)
                for line in open(filename).readlines()
                if ':' in line)    
    if info['source_url']:
        redirect(info['source_url'])
    else:
        return repr(info)
