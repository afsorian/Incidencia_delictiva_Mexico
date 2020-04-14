#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 15:30:44 2020

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

#create dataframes
df1=pd.read_csv('/Users/apple/Documents/PA/Incidencia delictiva/IDM_NM.csv',encoding='latin-1')
df2=pd.read_csv('/Users/apple/Documents/PA/Incidencia delictiva/Poblacion.csv',encoding='latin-1')

#replace names for Entidad(es) with short versions
lst_df=[df1,df2]
for i in lst_df:
    i.replace('Veracruz de Ignacio de la Llave','Veracruz',inplace=True)
    i.replace('Michoacán de Ocampo','Michoacán',inplace=True)
    i.replace('Coahuila de Zaragoza','Coahuila',inplace=True)

#define 'Sum' column as the sum of all months for each row
lst_col=list(df1)
#lst_col=['Año', 'Clave_Ent', 'Entidad', 'Cve. Municipio', 'Municipio', 'Bien jurídico afectado', 'Tipo de delito', 'Subtipo de delito', 'Modalidad', Ene-Dic]
lst_rem=['Año','Clave_Ent','Cve. Municipio']
for i in lst_rem:
    lst_col.remove(i)
df1['Sum'] = df1[lst_col].sum(axis=1)

#df=df.fillna(0)
#df.head(10)/df.tail(10)

#define subcategories
#df1.groupby('Tipo de delito').count()
#subDelitos=pd.pivot_table(df1,index=['Tipo de delito','Subtipo de delito'])

#----------------
#define df's for crime categories
ID=df1
DCP = df1[(df1['Tipo de delito'].isin(['Aborto','Allanamiento de morada','Amenazas','Feminicidio','Homicidio','Lesiones','Otros delitos del Fuero Común','Otros delitos que atentan contra la libertad personal','Otros delitos que atentan contra la vida y la integridad corporal','Secuestro','Trata de personas','Tráfico de menores','Violencia de género en todas sus modalidades distinta a la violencia familiar','Violencia familiar']))]
DP = df1[(df1['Tipo de delito'].isin(['Abuso de confianza','Daño a la propiedad','Despojo','Extorsión','Fraude','Otros delitos contra el patrimonio','Robo']))]
DS = df1[(df1['Tipo de delito'].isin(['Abuso sexual','Acoso sexual','Corrupción de menores','Hostigamiento sexual','Incesto','Otros delitos que atentan contra la libertad y la seguridad sexual','Rapto','Violación equiparada','Violación simple']))]
DCS = df1[(df1['Tipo de delito'].isin(['Contra el medio ambiente','Incumplimiento de obligaciones de asistencia familiar','Narcomenudeo','Otros delitos contra la familia','Otros delitos contra la sociedad']))]
DCFE = df1[(df1['Tipo de delito'].isin(['Delitos cometidos por servidores públicos','Electorales','Evasión de presos','Falsedad','Falsificación']))]
AT = df1[(df1['Modalidad'].isin(['En accidente de tránsito']))]
#define list of categories
lst_sort=['sort_ID','sort_DCP','sort_DP','sort_DS','sort_DCS','sort_DCFE','sort_AT']

#----------------
#create pivot table for INCIDENCIA DELICTIVA
piv_ID=pd.pivot_table(df1,index=['Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum')   
#insert a column with the mean for all years (2015-...)
piv_ID['Media']=piv_ID.mean(axis=1)
#merge with df2 to obtain a column with Entidad population numbers
pob_ID=piv_ID.merge(df2,on='Entidad')
#calculate 'tasa de delitos' -> tasa = (media(2015-2020)/PobTotal)*100,000
pob_ID.insert(1,'Tasa',(pob_ID['Media']/pob_ID['Est.2020'])*100000)
#insert a row with the mean national values
pob_ID=pob_ID.append(pd.Series(['MEDIA NACIONAL',mean(pob_ID['Tasa']),mean(pob_ID[2015]),mean(pob_ID[2016]),mean(pob_ID[2017]),mean(pob_ID[2018]),mean(pob_ID[2019]),mean(pob_ID[2020]),mean(pob_ID['Media']),mean(pob_ID['Est.2020'])],index=pob_ID.columns),ignore_index=True)
#sort pivot table by the column 'Tasa'
sort_ID=pob_ID.sort_values(by=['Tasa'])
#insert column with the category_id name
sort_ID.insert(1,'Categoría','Panorama General')

#----------------
#repeat for DELITOS CONTRA LAS PERSONAS
piv_DCP=pd.pivot_table(DCP,index=['Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum')   
piv_DCP['Media']=piv_DCP.mean(axis=1)
pob_DCP=piv_DCP.merge(df2,on='Entidad')
pob_DCP.insert(1,'Tasa',(pob_DCP['Media']/pob_DCP['Est.2020'])*100000)
pob_DCP=pob_DCP.append(pd.Series(['MEDIA NACIONAL',mean(pob_DCP['Tasa']),mean(pob_DCP[2015]),mean(pob_DCP[2016]),mean(pob_DCP[2017]),mean(pob_DCP[2018]),mean(pob_DCP[2019]),mean(pob_DCP[2020]),mean(pob_DCP['Media']),mean(pob_DCP['Est.2020'])],index=pob_DCP.columns),ignore_index=True)
sort_DCP=pob_DCP.sort_values(by=['Tasa'])
sort_DCP.insert(1,'Categoría','Delitos contra las Personas')
#create pivot table for subcategories
sub_DCP=pd.pivot_table(DCP,index=['Tipo de delito','Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum')
#duplicate year columns using headers '15-20'
for i in range(15,15+len(sub_DCP.columns)):
    year=int('20'+str(i))
    sub_DCP[i]=sub_DCP[year]
#obtain list of top10 Entidad in the category
list_DCP=list(sort_DCP['Entidad'][-10:])
#create df with top10
top_DCP=DCP[(DCP['Entidad'].isin(list_DCP))]
#create pivot table for top10 in category
tsub_DCP=pd.pivot_table(top_DCP,index=['Entidad','Tipo de delito','Año'],aggfunc=np.sum,values='Sum')

#----------------
#repeat for DELITOS CONTRA EL PATRIMONIO
piv_DP=pd.pivot_table(DP,index=['Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum')   
piv_DP['Media']=piv_DP.mean(axis=1)
pob_DP=piv_DP.merge(df2,on='Entidad')
pob_DP.insert(1,'Tasa',(pob_DP['Media']/pob_DP['Est.2020'])*100000)
pob_DP=pob_DP.append(pd.Series(['MEDIA NACIONAL',mean(pob_DP['Tasa']),mean(pob_DP[2015]),mean(pob_DP[2016]),mean(pob_DP[2017]),mean(pob_DP[2018]),mean(pob_DP[2019]),mean(pob_DP[2020]),mean(pob_DP['Media']),mean(pob_DP['Est.2020'])],index=pob_DP.columns),ignore_index=True)
sort_DP=pob_DP.sort_values(by=['Tasa'])
sort_DP.insert(1,'Categoría','Delitos contra el Patrimonio')
sub_DP=pd.pivot_table(DP,index=['Tipo de delito','Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum')
for i in range(15,15+len(sub_DP.columns)):
    year=int('20'+str(i))
    sub_DP[i]=sub_DP[year]
list_DP=list(sort_DP['Entidad'][-10:])
top_DP=DP[(DP['Entidad'].isin(list_DP))]
tsub_DP=pd.pivot_table(top_DP,index=['Entidad','Tipo de delito','Año'],aggfunc=np.sum,values='Sum')

#----------------
#repeat for DELITOS SEXUALES
piv_DS=pd.pivot_table(DS,index=['Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum')   
piv_DS['Media']=piv_DS.mean(axis=1)
pob_DS=piv_DS.merge(df2,on='Entidad')
pob_DS.insert(1,'Tasa',(pob_DS['Media']/pob_DS['Est.2020'])*100000)
pob_DS=pob_DS.append(pd.Series(['MEDIA NACIONAL',mean(pob_DS['Tasa']),mean(pob_DS[2015]),mean(pob_DS[2016]),mean(pob_DS[2017]),mean(pob_DS[2018]),mean(pob_DS[2019]),mean(pob_DS[2020]),mean(pob_DS['Media']),mean(pob_DS['Est.2020'])],index=pob_DS.columns),ignore_index=True)
sort_DS=pob_DS.sort_values(by=['Tasa'])
sort_DS.insert(1,'Categoría','Delitos Sexuales')
sub_DS=pd.pivot_table(DS,index=['Tipo de delito','Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum')
for i in range(15,15+len(sub_DS.columns)):
    year=int('20'+str(i))
    sub_DS[i]=sub_DS[year]
list_DS=list(sort_DS['Entidad'][-10:])
top_DS=DS[(DS['Entidad'].isin(list_DS))]
tsub_DS=pd.pivot_table(top_DS,index=['Entidad','Tipo de delito','Año'],aggfunc=np.sum,values='Sum')

#----------------
#repeat for DELITOS CONTRA LA SOCIEDAD
piv_DCS=pd.pivot_table(DCS,index=['Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum')  
piv_DCS['Media']=piv_DCS.mean(axis=1)
pob_DCS=piv_DCS.merge(df2,on='Entidad')
pob_DCS.insert(1,'Tasa',(pob_DCS['Media']/pob_DCS['Est.2020'])*100000)
pob_DCS=pob_DCS.append(pd.Series(['MEDIA NACIONAL',mean(pob_DCS['Tasa']),mean(pob_DCS[2015]),mean(pob_DCS[2016]),mean(pob_DCS[2017]),mean(pob_DCS[2018]),mean(pob_DCS[2019]),mean(pob_DCS[2020]),mean(pob_DCS['Media']),mean(pob_DCS['Est.2020'])],index=pob_DCS.columns),ignore_index=True)
sort_DCS=pob_DCS.sort_values(by=['Tasa'])
sort_DCS.insert(1,'Categoría','Delitos contra la Sociedad')
sub_DCS=pd.pivot_table(DCS,index=['Tipo de delito','Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum')
for i in range(15,15+len(sub_DCS.columns)):
    year=int('20'+str(i))
    sub_DCS[i]=sub_DCS[year]
list_DCS=list(sort_DCS['Entidad'][-10:])
top_DCS=DCS[(DCS['Entidad'].isin(list_DCS))]
tsub_DCS=pd.pivot_table(top_DCS,index=['Entidad','Tipo de delito','Año'],aggfunc=np.sum,values='Sum')

#----------------
#repeat for DELITOS CONTRA LAS FUNCIONES DEL ESTADO
piv_DCFE=pd.pivot_table(DCFE,index=['Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum') 
piv_DCFE['Media']=piv_DCFE.mean(axis=1)
pob_DCFE=piv_DCFE.merge(df2,on='Entidad')
pob_DCFE.insert(1,'Tasa',(pob_DCFE['Media']/pob_DCFE['Est.2020'])*100000)
pob_DCFE=pob_DCFE.append(pd.Series(['MEDIA NACIONAL',mean(pob_DCFE['Tasa']),mean(pob_DCFE[2015]),mean(pob_DCFE[2016]),mean(pob_DCFE[2017]),mean(pob_DCFE[2018]),mean(pob_DCFE[2019]),mean(pob_DCFE[2020]),mean(pob_DCFE['Media']),mean(pob_DCFE['Est.2020'])],index=pob_DCFE.columns),ignore_index=True)
sort_DCFE=pob_DCFE.sort_values(by=['Tasa'])
sort_DCFE.insert(1,'Categoría','Delitos contra las Funciones del Estado y el Servicio Público')
sub_DCFE=pd.pivot_table(DCFE,index=['Tipo de delito','Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum')
for i in range(15,15+len(sub_DCFE.columns)):
    year=int('20'+str(i))
    sub_DCFE[i]=sub_DCFE[year]
list_DCFE=list(sort_DCFE['Entidad'][-10:])
top_DCFE=DCFE[(DCFE['Entidad'].isin(list_DCFE))]
tsub_DCFE=pd.pivot_table(top_DCFE,index=['Entidad','Tipo de delito','Año'],aggfunc=np.sum,values='Sum')

#----------------
#repeat for ACCIDENTES DE TRANSITO
piv_AT=pd.pivot_table(AT,index=['Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum') 
piv_AT['Media']=piv_AT.mean(axis=1)
pob_AT=piv_AT.merge(df2,on='Entidad')
pob_AT.insert(1,'Tasa',(pob_AT['Media']/pob_AT['Est.2020'])*100000)
pob_AT=pob_AT.append(pd.Series(['MEDIA NACIONAL',mean(pob_AT['Tasa']),mean(pob_AT[2015]),mean(pob_AT[2016]),mean(pob_AT[2017]),mean(pob_AT[2018]),mean(pob_AT[2019]),mean(pob_AT[2020]),mean(pob_AT['Media']),mean(pob_AT['Est.2020'])],index=pob_AT.columns),ignore_index=True)
sort_AT=pob_AT.sort_values(by=['Tasa'])
sort_AT.insert(1,'Categoría','Accidentes de Tránsito')
#definir pivot table por subcategoría
sub_AT=pd.pivot_table(AT,index=['Tipo de delito','Entidad'],columns=['Año'],aggfunc=np.sum, values='Sum')
for i in range(15,15+len(sub_AT.columns)):
    year=int('20'+str(i))
    sub_AT[i]=sub_AT[year]
list_AT=list(sort_AT['Entidad'][-10:])
top_AT=AT[(AT['Entidad'].isin(list_AT))]
tsub_AT=pd.pivot_table(top_AT,index=['Entidad','Tipo de delito','Año'],aggfunc=np.sum,values='Sum')

#----------------
#create df for 'Municipio'
mun_ID=pd.pivot_table(df1,index=['Entidad', 'Municipio'],columns=['Año'],aggfunc=np.sum, values='Sum')  
#duplicate year columns using headers '15-20'
for i in range(15,15+len(mun_ID.columns)):
    year=int('20'+str(i))
    mun_ID[i]=mun_ID[year]
mun_ID=mun_ID.reset_index()
#get list for all 'Entidad'
gr_Ent=df1.groupby('Entidad').count()
lst_Ent=gr_Ent.reset_index().Entidad.values
#array(['Aguascalientes', 'Baja California', 'Baja California Sur','Campeche', 'Chiapas', 'Chihuahua', 'Ciudad de México','Coahuila de Zaragoza', 'Colima', 'Durango', 'Guanajuato','Guerrero', 'Hidalgo', 'Jalisco', 'Michoacán de Ocampo', 'Morelos','México', 'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro','Quintana Roo', 'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco','Tamaulipas', 'Tlaxcala', 'Veracruz de Ignacio de la Llave','Yucatán', 'Zacatecas'], dtype=object)
#create a dictionary with key_values=elements from lst_Ent & empty dataframes
d1 = {}
for name in lst_Ent:
    d1[name] = pd.DataFrame()
#fill in each dataframe with the info from the corresponding Entidad
for name, df in d1.items():
    d1[name]=mun_ID[(mun_ID['Entidad'].isin([name]))]
#e.g.: Ags=mun_ID[(mun_ID['Entidad'].isin(['Aguascalientes']))]

#------------------
#determine number of Municipios in each Entidad
mun=[]
for name, df in d1.items():
    mun.append(len(d1[name]))
#convert dataframes into Series and merge to one file
mun=pd.Series(mun,name='No_mun')
ent=pd.Series(lst_Ent,name='Entidad')
no_mun=pd.concat([ent,mun],axis=1)
#mend number for Municipios with changes
lst_chgs=([4,124],[6,16],[13,125],[19,570],[21,18],[25,72],[29,212])
for i,j in lst_chgs:
    no_mun.loc[i,'No_mun']=j
#export to csv
no_mun.to_csv('/Users/apple/Documents/PA/Incidencia delictiva/Municipios.csv')

#------------------
#create top_del per Entidad
df_all=pd.pivot_table(df1,index=['Entidad','Tipo de delito'],columns=['Año'],aggfunc=np.sum, values='Sum').reset_index()
df_all['Total']=df_all.sum(axis=1)
df_all=df_all.sort_values(by='Total',ascending=False)
#create a list of index with highest values per Entidad
highest=[]
for i in lst_Ent:
    high=df_all[df_all['Entidad']==i].index.values[0]
    highest.append(high)
#create dataframe top_del with obtained indexes
top_del=pd.DataFrame()
for i in highest:
    top_del=top_del.append(df_all.loc[i],ignore_index=True)
cols_to_move=['Entidad','Tipo de delito']
top_del=top_del[cols_to_move+[col for col in top_del.columns if col not in cols_to_move]]
#export to csv
top_del.to_csv('/Users/apple/Documents/PA/Incidencia delictiva/Top_del.csv')

#----------------
#reset index for all dataframes made by pivoting
sub_DCP=sub_DCP.reset_index()
sub_DP=sub_DP.reset_index()
sub_DS=sub_DS.reset_index()
sub_DCS=sub_DCS.reset_index()
sub_DCFE=sub_DCFE.reset_index()
sub_AT=sub_AT.reset_index()
tsub_DCP=tsub_DCP.reset_index()
tsub_DP=tsub_DP.reset_index()
tsub_DS=tsub_DS.reset_index()
tsub_DCS=tsub_DCS.reset_index()
tsub_DCFE=tsub_DCFE.reset_index()
tsub_AT=tsub_AT.reset_index()

# Create a Pandas Excel writer using XlsxWriter as the engine
writer=pd.ExcelWriter('/Users/apple/Documents/PA/Incidencia delictiva/Delitos.xlsx',engine='xlsxwriter')
# Write each dataframe to a different worksheet
sort_ID.to_excel(writer, sheet_name='sort_ID',index=False)
sort_DCP.to_excel(writer, sheet_name='sort_DCP',index=False)
sort_DP.to_excel(writer, sheet_name='sort_DP',index=False)
sort_DS.to_excel(writer, sheet_name='sort_DS',index=False)
sort_DCS.to_excel(writer, sheet_name='sort_DCS',index=False)
sort_DCFE.to_excel(writer, sheet_name='sort_DCFE',index=False)
sort_AT.to_excel(writer, sheet_name='sort_AT',index=False)
sub_DCP.to_excel(writer, sheet_name='sub_DCP',index=False)
sub_DP.to_excel(writer, sheet_name='sub_DP',index=False)
sub_DS.to_excel(writer, sheet_name='sub_DS',index=False)
sub_DCS.to_excel(writer, sheet_name='sub_DCS',index=False)
sub_DCFE.to_excel(writer, sheet_name='sub_DCFE',index=False)
sub_AT.to_excel(writer, sheet_name='sub_AT',index=False)
tsub_DCP.to_excel(writer, sheet_name='tsub_DCP',index=False)
tsub_DP.to_excel(writer, sheet_name='tsub_DP',index=False)
tsub_DS.to_excel(writer, sheet_name='tsub_DS',index=False)
tsub_DCS.to_excel(writer, sheet_name='tsub_DCS',index=False)
tsub_DCFE.to_excel(writer, sheet_name='tsub_DCFE',index=False)
tsub_AT.to_excel(writer, sheet_name='tsub_AT',index=False)
for name, df in d1.items():
    d1[name].to_excel(writer, sheet_name=name,index=False)
# Close the Pandas Excel writer and output the Excel file.
writer.save()












