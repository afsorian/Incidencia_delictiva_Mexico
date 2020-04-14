#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 16:30:05 2020

@author: afsorian
"""

import pandas as pd
import numpy as np
from statistics import mean

#setup pandas visualization
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',100)
pd.set_option('display.max_colwidth',100)
pd.set_option('display.width',None)

#--------------------
#create columns for output dataframe df_Delito
tipo_del=pd.Series(['Delitos contra las personas','Delitos contra el patrimonio','Delitos sexuales','Delitos contra la sociedad','Delitos contra las funciones del estado y el servicio público','Accidentes de tránsito'],name='Tipo_delito')

g_id=pd.read_csv('/Users/apple/Documents/PA/Incidencia delictiva/Grafico_tdel.csv',encoding='latin-1')
g_id=g_id.drop(['Tipo_delito'],axis=1)

no_sub=pd.Series([14,7,9,5,5,2],name='No_sub')

sub_del=pd.Series(['Aborto, Allanamiento de morada, Amenazas, Feminicidio, Homicidio, Lesiones, Otros delitos del Fuero Común, Otros delitos que atentan contra la libertad personal, Otros delitos que atentan contra la vida y la integridad corporal, Secuestro, Trata de personas, Tráfico de menores, Violencia de género en todas sus modalidades distinta a la violencia familiar, Violencia familiar','Robo, Abuso de confianza, Daño a la propiedad, Despojo, Extorsión, Fraude, Otros delitos contra el patrimonio','Abuso sexual, Acoso sexual, Corrupción de menores, Hostigamiento sexual, Incesto, Otros delitos que atentan contra la libertad y la seguridad sexual, Rapto, Violación equiparada, Violación simple','Contra el medio ambiente, Incumplimiento de obligaciones de asistencia familiar, Narcomenudeo, Otros delitos contra la familia, Otros delitos contra la sociedad','Delitos cometidos por servidores públicos, Electorales, Evasión de presos, Falsedad, Falsificación','Homicidio culposo, Lesiones culposas'],name='Subtipo_delito')

graphs_ID=pd.Series(['<div class="flourish-embed flourish-chart" data-src="visualisation/1860213" data-url="https://flo.uri.sh/visualisation/1860213/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-chart" data-src="visualisation/1860376" data-url="https://flo.uri.sh/visualisation/1860376/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-chart" data-src="visualisation/1860399" data-url="https://flo.uri.sh/visualisation/1860399/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-chart" data-src="visualisation/1860416" data-url="https://flo.uri.sh/visualisation/1860416/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-chart" data-src="visualisation/1860426" data-url="https://flo.uri.sh/visualisation/1860426/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-chart" data-src="visualisation/1860465" data-url="https://flo.uri.sh/visualisation/1860465/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>'],name='Graph_id')

graphs_sub=pd.Series(['<div class="flourish-embed flourish-table" data-src="visualisation/1867629" data-url="https://flo.uri.sh/visualisation/1867629/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1868033" data-url="https://flo.uri.sh/visualisation/1868033/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1868088" data-url="https://flo.uri.sh/visualisation/1868088/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1868140" data-url="https://flo.uri.sh/visualisation/1868140/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1868245" data-url="https://flo.uri.sh/visualisation/1868245/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1868273" data-url="https://flo.uri.sh/visualisation/1868273/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>'],name='Table_sub')

graphs_top=pd.Series(['<div class="flourish-embed flourish-scatter" data-src="visualisation/1856352" data-url="https://flo.uri.sh/visualisation/1856352/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-scatter" data-src="visualisation/1881708" data-url="https://flo.uri.sh/visualisation/1881708/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-scatter" data-src="visualisation/1881754" data-url="https://flo.uri.sh/visualisation/1881754/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-scatter" data-src="visualisation/1881773" data-url="https://flo.uri.sh/visualisation/1881773/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-scatter" data-src="visualisation/1881789" data-url="https://flo.uri.sh/visualisation/1881789/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-scatter" data-src="visualisation/1881809" data-url="https://flo.uri.sh/visualisation/1881809/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>'],name='Graph_top')

df_Delito=pd.DataFrame()
df_Delito=pd.concat([tipo_del,graphs_ID,g_id,no_sub,sub_del,graphs_sub,graphs_top],axis=1)

#----------------
#create columns for output dataframe df_Estado
pob=pd.read_csv('/Users/apple/Documents/PA/Incidencia delictiva/Poblacion.csv',encoding='latin-1')
pob.replace('Veracruz de Ignacio de la Llave','Veracruz',inplace=True)
pob.replace('Michoacán de Ocampo','Michoacán',inplace=True)
pob.replace('Coahuila de Zaragoza','Coahuila',inplace=True)
pob=pob.rename(columns={'Est.2020':'Población'})

cap_pob=pd.read_csv('/Users/apple/Documents/PA/Incidencia delictiva/Capitales.csv',encoding='UTF-8')
cap_pob=cap_pob.drop(['Index;Entidad;Capital;Cap_pob;Index'],axis=1)
cap_pob=cap_pob.rename(columns={'Población':'Cap_pob'})

mun=pd.read_csv('/Users/apple/Documents/PA/Incidencia delictiva/Municipios.csv',encoding='UTF-8')
mun=mun.drop(['Unnamed: 0'],axis=1)

sent=pd.read_excel('/Users/apple/Documents/PA/Incidencia delictiva/Delitos.xlsx',sheet_name='sort_ID')
sent=sent.drop(sent[sent['Entidad']=='MEDIA NACIONAL'].index.values)
sent=sent.iloc[::-1,:]
sent['Pos_Nac']=range(1,1+len(sent))
sent=sent[['Entidad','Pos_Nac','Tasa']]

top_del=pd.read_csv('/Users/apple/Documents/PA/Incidencia delictiva/Top_Del.csv',encoding='UTF-8')
top_del=top_del.drop(['Unnamed: 0','Total'],axis=1)

cat_del=pd.read_csv('/Users/apple/Documents/PA/Incidencia delictiva/clas_del.csv',encoding='UTF-8')

Entidad=pd.Series(['Aguascalientes','Baja California','Baja California Sur','Campeche','Chiapas','Chihuahua','Ciudad de México','Coahuila', 'Colima','Durango','Guanajuato','Guerrero','Hidalgo','Jalisco', 'Michoacán','Morelos','México','Nayarit','Nuevo León','Oaxaca','Puebla', 'Querétaro','Quintana Roo','San Luis Potosí','Sinaloa','Sonora', 'Tabasco','Tamaulipas','Tlaxcala','Veracruz','Yucatán', 'Zacatecas'],name='Entidad')

graphs_Ent=pd.Series(['<div class="flourish-embed flourish-table" data-src="visualisation/1882274" data-url="https://flo.uri.sh/visualisation/1882274/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907347" data-url="https://flo.uri.sh/visualisation/1907347/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907359" data-url="https://flo.uri.sh/visualisation/1907359/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907364" data-url="https://flo.uri.sh/visualisation/1907364/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907424" data-url="https://flo.uri.sh/visualisation/1907424/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907439" data-url="https://flo.uri.sh/visualisation/1907439/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907453" data-url="https://flo.uri.sh/visualisation/1907453/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907490" data-url="https://flo.uri.sh/visualisation/1907490/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907505" data-url="https://flo.uri.sh/visualisation/1907505/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907529" data-url="https://flo.uri.sh/visualisation/1907529/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907537" data-url="https://flo.uri.sh/visualisation/1907537/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907549" data-url="https://flo.uri.sh/visualisation/1907549/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907560" data-url="https://flo.uri.sh/visualisation/1907560/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907587" data-url="https://flo.uri.sh/visualisation/1907587/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907602" data-url="https://flo.uri.sh/visualisation/1907602/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907617" data-url="https://flo.uri.sh/visualisation/1907617/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907629" data-url="https://flo.uri.sh/visualisation/1907629/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907642" data-url="https://flo.uri.sh/visualisation/1907642/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907653" data-url="https://flo.uri.sh/visualisation/1907653/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907660" data-url="https://flo.uri.sh/visualisation/1907660/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907671" data-url="https://flo.uri.sh/visualisation/1907671/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907681" data-url="https://flo.uri.sh/visualisation/1907681/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907693" data-url="https://flo.uri.sh/visualisation/1907693/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907697" data-url="https://flo.uri.sh/visualisation/1907697/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907716" data-url="https://flo.uri.sh/visualisation/1907716/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907725" data-url="https://flo.uri.sh/visualisation/1907725/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907735" data-url="https://flo.uri.sh/visualisation/1907735/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907740" data-url="https://flo.uri.sh/visualisation/1907740/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907754" data-url="https://flo.uri.sh/visualisation/1907754/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907764" data-url="https://flo.uri.sh/visualisation/1907764/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907771" data-url="https://flo.uri.sh/visualisation/1907771/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>','<div class="flourish-embed flourish-table" data-src="visualisation/1907780" data-url="https://flo.uri.sh/visualisation/1907780/embed"><script src="https://public.flourish.studio/resources/embed.js"></script></div>'],name='Table')

df_Estado=pd.DataFrame()
df_Estado=pd.concat([Entidad,graphs_Ent],axis=1)
df_Estado=df_Estado.merge(mun,on='Entidad').merge(pob,on='Entidad').merge(cap_pob,on='Entidad').merge(sent,on='Entidad').merge(top_del,on='Entidad')
df_Estado=df_Estado.merge(cat_del,on='Tipo de delito',how='left')
df_Estado=df_Estado.rename(columns={'Tipo de delito':'Top_delito'})
def move_column_inplace(df, col, pos):
    col = df.pop(col)
    df.insert(pos, col.name, col)
move_column_inplace(df_Estado,'Table',len(df_Estado.columns)-1)
move_column_inplace(df_Estado,'Cat_del',8)
    
#---------------
# Create a Pandas Excel writer using XlsxWriter as the engine
writer=pd.ExcelWriter('/Users/apple/Documents/PA/Incidencia delictiva/Data_delitos.xlsx',engine='xlsxwriter')
# Write each dataframe to a different worksheet
df_Delito.to_excel(writer,sheet_name='data_Delito',index=False)
df_Estado.to_excel(writer, sheet_name='data_Estado',index=False)
# Close the Pandas Excel writer and output the Excel file.
writer.save()



