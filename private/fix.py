a=raw_input('replace:')
b=raw_input('with   :')

import glob
files = glob.glob('../sources/*/*.markmin')
for file in files:
    d = open(file,'r').read()
    d = d.replace(a,b)
    open(file,'w').write(d)
