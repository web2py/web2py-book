# -*- coding: utf-8 -*-
import os, datetime
session.forget()

TIME_EXPIRE = 60*60*24
FORCE_RENDER = False

# this is for checking new content instantly in development
if request.is_local:
    TIME_EXPIRE = -1
    FORCE_RENDER = True

response.title = 'web2py'
response.subtitle = 'Full Stack Web Framework, 4th Ed.\nwritten by Massimo Di Pierro in English'
response.menu = []

def splitter(x):
    a,b = x.split(':',1)
    return a.strip(),b.strip()

@cache('folders',None)
def get_folders(dummy=None):
    folder = os.path.join(request.folder,'sources')
    return folder, [f for f in os.listdir(folder)
                    if os.path.isdir(os.path.join(folder,f))]
FOLDER, FOLDERS = get_folders()

def get_subfolder(book_id):
    if not book_id:
        redirect(URL('index'))
    for f in FOLDERS:
        if f.startswith(book_id):
            return f
    redirect(URL('index'))

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
def build_menu(dummy=None):
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
    rtn = MARKMIN(text.replace('\r',''),extra=extra,url=url2)
    return rtn

def index():
    books = {}
    for subfolder in FOLDERS:
        books[subfolder] = cache.ram('info_%s' % subfolder, lambda: get_info(subfolder), time_expire=TIME_EXPIRE)
    return locals()

def calc_date(now=request.utcnow.date()):
    # if you are changing sources often remove the
    # comment from the next 2 lines
    # import datetime
    # now = now + datetime.timedelta(days=1)
    format = '%a, %d %b %Y 23:59:59 GMT'
    return now.strftime(format)

def chapter():
    book_id, chapter_id = request.args(0), request.args(1,cast=int,default='0')
    subfolder = get_subfolder(book_id)
    info = cache.ram('info_%s' % subfolder, lambda: get_info(subfolder), time_expire=TIME_EXPIRE)
    chapters = cache.ram('chapters_%s' % subfolder, lambda: get_chapters(subfolder), time_expire=TIME_EXPIRE)
    filename = os.path.join(FOLDER,subfolder,'%.2i.markmin' % chapter_id)
    dest = os.path.join(request.folder, 'static_chaps', subfolder, '%.2i.html' % chapter_id)
    response.headers['Cache-Control'] = 'public, must-revalidate'
    response.headers['Expires'] = calc_date()
    response.headers['Pragma'] = None
    if (not os.path.isfile(dest)) or FORCE_RENDER:
        content = open(filename).read()
        content = convert2html(book_id,content).xml()
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        open(dest, 'w').write(content)
        content = XML(content)
        return locals()
    else:
        content = XML(open(dest).read())
        return locals()

def search():
    book_id = request.args(0) or redirect(URL('index'))
    search = request.vars.search or redirect(URL('chapter',args=book_id))
    subfolder = get_subfolder(book_id)
    info = cache.ram('info_%s' % subfolder, lambda: get_info(subfolder), time_expire=TIME_EXPIRE)
    chapters = cache.ram('chapters_%s' % subfolder, lambda: get_chapters(subfolder), time_expire=TIME_EXPIRE)
    results = []
    content = H2('No results for "%s"' % search)
    for chapter in chapters:
        chapter_id = int(chapter[0])
        filename = os.path.join(FOLDER,subfolder,'%.2i.markmin' % chapter_id)
        data = open(filename).read().replace('\r','')
        k = data.find(search)
        if k>=0:
            snippet = data[data.rfind('\n\n',0,k)+1:data.find('\n\n',k)].strip()
            results.append((chapter[0],chapter[1],convert2html(book_id,snippet)))
            content = CAT(*[DIV(H2(A(chapter[1],
                                     _href=URL('chapter',
                                               vars=dict(search=search),
                                               args=(book_id,chapter[0])))),
                            chapter[2],BR(),
                            A('more',_href=URL('chapter',
                                               vars=dict(search=search),
                                               args=(book_id,chapter[0])),_class="btn"))
                        for chapter in results])
    response.view = 'default/chapter.html'
    return locals()

def image():
    book_id = request.args(0)
    key = request.args(1)
    subfolder = get_subfolder(book_id)
    filename = os.path.join(FOLDER,subfolder,'images',key)
    if not os.path.isfile(filename):
        raise HTTP(404)
    response.headers['Cache-Control'] = 'public, must-revalidate'
    response.headers['Expires'] = calc_date()
    response.headers['Pragma'] = None
    return response.stream(filename)


def reference():
    book_id = request.args(0)
    key = request.args(1)
    subfolder = get_subfolder(book_id)
    filename = os.path.join(FOLDER,subfolder,'references',key)
    if not os.path.isfile(filename):
        raise HTTP(404)
    info = dict(splitter(line)
                for line in open(filename).readlines()
                if ':' in line)
    if info['source_url']:
        redirect(info['source_url'])
    else:
        return repr(info)
