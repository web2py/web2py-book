
if request.is_local:
    db = DAL('sqlite://translations.sqlite',
             #fake_migrate_all=True
             )

    db.define_table('translation',
        Field('language_code','integer',default=31),
        Field('filename'),
        Field('language', default=request.args(0), writable=False),
        Field('original', 'text', writable=False),
        Field('translation', 'text'),
        Field('last_checked','datetime',default=request.now)
        #migrate=False
        )