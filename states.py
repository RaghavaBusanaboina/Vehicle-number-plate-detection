import re
with open('states','r+') as f:
    with open('update_states', 'w+') as f1:
        for i in f.readlines():
            line = i.replace(' ','')
            # l = line.replace('-',':')
            # l1 = l[1:]
            if not line.isspace():
                l1 = re.sub(pattern='^[0-9]*',repl='',string=line)
                l2 = l1.replace('\n',',')
                y = l2.split('—')
                out = f'"{y[0]}":"{y[1]}",'
                f1.write(out)