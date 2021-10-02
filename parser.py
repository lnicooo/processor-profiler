#!/usr/bin/env python3
import re
import pandas as pd

df = pd.DataFrame(columns=['func','id','samp','perc','in','out'])

a=re.compile('^(?:FP:)(\d*) (\w*) (?:[^ ]*) (\d*) (\d*)$')
b=re.compile('^(?:FPC:)(\d*), (\d*), (\d*)$')

with open("app.iprof") as f:
    for line in f:
        m_a=a.match(line)
        m_b=b.match(line)
        if(m_a):
            x={'func':m_a.group(2), 'id':m_a.group(3),'samp':int(m_a.group(4)),'in':0}
            df=df.append(x,ignore_index=True)

        elif(m_b):
            #print(m_b.group(3))
            df.loc[df['id'] == m_b.group(3),['in']]+=int(m_b.group(1))

    df['out']  = df['in'] - df['samp']
    df['perc'] = (df['samp']/df['samp'].sum())*100
    df = df.sort_values(by=['perc'],ascending=False)
    print(df)
