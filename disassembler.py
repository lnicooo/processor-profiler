#!/usr/bin/env python3

dump =  "build/app.dump"
disas = "build/app.disas"

dump_f = open(dump)
disas_f = open(disas)

dump =  [x.split() for x in dump_f]
disas = [x.split() for x in disas_f]

dump = list(filter(None,dump))

dump = dump[2:]

func_addr={}
func=""

for line_dump in dump:

    if(len(line_dump)==2):
        func = line_dump[1]
        func_addr[func]=[]
    else:
        func_addr[func].append(line_dump[0][:-1])

disas_func={}


for line in disas:
    for func in func_addr:

        addr= hex(int(line[0]))[2:]
        if(addr in func_addr[func]):
            break

    func = func[1:-2]

    if(func not in disas_func):
        disas_func[func]=[]


    disas_func[func].append(line)


    print(line,func)

print(len(func_addr))
print(len(disas_func))

print("===============")
print(disas_func['__call_exitprocs'])

print(disas_func['__retarget_lock_init'])
