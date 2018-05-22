

def search():
    if not request.is_local:
        return 'not autorized'
    if request.args(0):
        try:
            session.language = int(request.args(0))
        except:
            pass
    else:
        session.language = '31'

    form = SQLFORM.factory(
        Field('search',default=request.post_vars.search),
        keepvalues=True

    )
    if form.process().accepted:
        q = db((db.translation.language_code == session.language)
               & (db.translation.translation.contains(form.vars.search)))
        #response.flash = 'form accepted'
        #print(form.vars.search)
    elif form.errors:
        response.flash = 'form has errors'
        #print('erro')
        q = db((db.translation.language == session.language))
    else:
        #print('nem tentei')
        q = db((db.translation.language == session.language))
    print(q)
    grid = SQLFORM.grid(q,
                        searchable=False,
                        maxtextlength=500,
                        csv=False,
                        user_signature=False
                        )
    return locals()