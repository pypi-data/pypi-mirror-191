#!/usr/bin/env python
# coding: utf-8

# In[1]:


############################### Paquetes ##############################################
import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
from tabulate import tabulate
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, cross_val_predict
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import sys
import xgboost as xgb
from IPython.display import display
from sklearn import metrics
from sklearn.cluster import KMeans 
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
from sklearn.decomposition import PCA
from sklearn.feature_selection import mutual_info_classif
import folium
import leafmap.foliumap as leafmap
import matplotlib.animation as animation


#################################### Funciones ##############################################



# Función para agregar columnas con indices (ufm2, etc) y cambiar el tipo de
# dato de ciertas columnas
def InsertColumns(D): #(D es la tabla) 
    D=D.astype({'ingreso':'float64','antiguedad':'float64','supCSII':'float64','supTSII':'float64',
                'valor':'float64','avaluofiscal' :'float64'})
    
    D.insert(D.shape[1],'ufm2(supCSII)',D.loc[:,'valor']/D.loc[:,'supCSII'], True) 
    D.insert(D.shape[1],'ufm2(supTSII)',D.loc[:,'valor']/D.loc[:,'supTSII'], True)
    D.insert(D.shape[1],'supTSII/supCSII',D.loc[:,'supTSII']/D.loc[:,'supCSII'], True) 
    return D

# Concatenación de tablas de ventas y tasaciones
def tabla_auxiliar(df1,df2,method): #(df1 es la tabla de ventas, df2 es la tabla de tasaciones, 
                                     #method: el proposito para el cual se genera la tabla: ML o AVM) #variables: nombres
    while (method!="ML" and method!="AVM"):
        print("El método seleccionado no es válido")
        method=input("Ingrese correctamente el método a utilizar (ML o AVM): ")
    ## Aquí hubo una modificación
    if method=="ML":
        variablesML=['ingreso','antiguedad','longitud','latitud','supCSII','supTSII','valor','avaluofiscal',
             'cve_comuna', 'ufm2(supCSII)','ufm2(supTSII)','supTSII/supCSII']
        df1_aux=df1[variablesML]
        df2_aux=df2[variablesML]
    else:
        variablesAVM=['num_','cve_propiedad','rol','cve_comuna','cve_region','ah','ah_hom','zona_eod',
             'zona_jjvv','materialidad','ingreso','antiguedad','longitud',
             'latitud','supCSII','supTSII','valor','avaluofiscal']
        df1_aux=df1[variablesAVM]
        df2_aux=df2[variablesAVM]
    df1_df2_aux=pd.concat([df1_aux,df2_aux], ignore_index=True, sort=False)
    return df1_df2_aux

# Selección de comuna
def Selec_Comuna(D1,cve): #(D1 es la tabla, cve: es el codigo de la comuna)
    comunas=[19,21,22,52]
    while cve not in comunas:
        print('Ingrese alguna de las siguientes comunas: La Reina (19), Las Condes (21), Lo Barnechea (22) o Vitacura (52):')
        cve=int(input())
    if cve==52:
        tol=5000
    else:
        tol=1000
    D_comuna=D1.loc[(D1.loc[:,'cve_comuna']==cve) & (D1.loc[:,'valor']>=tol)]
    return D_comuna

def etiqueta(mini,maxi):
    etiquetas=[]
    en='Index_antiguedad_10_'
    L=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","W","X","Y","Z"]
    k=0
    for j in range(mini,maxi,10):
        if j<maxi-10:
            p=L[k]+str(j)[2:]+'/'+str(j+9)[2:]
            etiquetas.append(en+p)
        if j>maxi-10:
            p=L[k]+str(j)[2:]+'/'+str(maxi)[2:]
            etiquetas.append(en+p)
        k+=1
    return etiquetas

# Eliminación de datos duplicados
def datosduplicados(tabla,T): #(tabla es la tabla, T es True entonces se muestra la cantidad de datos eliminados)
    n_inicial = tabla.shape[0];
    tabla2 = tabla.drop_duplicates(subset=['ingreso','longitud','latitud',
                                          'supCSII','supTSII','avaluofiscal'])
    
    if T==True:
        print(f'Hay {n_inicial-tabla2.shape[0]} datos duplicados')
        print(f'Al eliminarlos quedan {tabla2.shape[0]} datos')
    return tabla2

#Identificación de atípicos dada una columna
def outliers_col(df,columna,n,a,T,n_i,limit):  #(df:tabla, columna, n: cantidad de datos inicial,
                                               # a: zscore o IQR, T es True entonces se muestran los resultados
                                               # n_i: cantidad de datos inicial, limit: limite del zscore)
    tabla= pd.DataFrame.from_dict({
    'Variable': [],'Cantidad de Atípicos': [],
    'Type': []});
    col = ['Variable','Cantidad de Atípicos','Type'];
    k=0;
    if (a=='zscore'):
        n_outliers = len(df[np.abs(stats.zscore(df[columna])) > limit])
        k=k+n_outliers;
        tablaux = pd.DataFrame([[df[columna].name,n_outliers,df[columna].dtype]],
                                    columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
        
    if (a=='IQR'):
        Q1,Q3 = np.percentile(df[columna], [25,75])
        iqr = Q3 - Q1
        ul = Q3+1.5*iqr
        ll = Q1-1.5*iqr
        n_outliers = len(df[(df[columna] > ul) | (df[columna] < ll)])
        k=k+n_outliers;
        tablaux = pd.DataFrame([[df[columna].name,n_outliers,df[columna].dtype]],
                                    columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    if T==True:
        print(tabulate(tabla, headers=col, tablefmt="fancy_grid"))  
        print('\nSe eliminarán:',k,'datos, y quedarán al menos:',n-k)
        print('en porcentaje con respecto a la cantidad inicial:',(n-k)*100/n_i,'%.\n')     
    return k,tabla
#Eliminación de atípicos dada una columna
def outliers_col_eliminacion(df,columna,a,limit):  #(df:tabla, columna, a: zscore o IQR, limit: limite del zscore)
    if a=='zscore':
        l=df[np.abs(stats.zscore(df[columna])) > limit].index;
        for x in l.values:
            df.loc[x,columna] = np.nan;
                
    if a=='IQR':
        Q1,Q3 = np.percentile(df[columna], [25,75])
        iqr = Q3 - Q1
        ul = Q3+1.5*iqr
        ll = Q1-1.5*iqr
        l=df[(df[columna] > ul) | (df[columna] < ll)].index;
        for x in l.values:
            df.loc[x,columna] = np.nan;
    
    df=df.dropna(axis = 0);
    return df

# Gráficas
def grafico_histograma_sns(df,columna,option1,option2):   #(df:tabla, columna, option1: kde True or False
                                                          #,option2: discrete True or False)
    plt.figure(figsize = (9,4))
    #sns.set_style("whitegrid")
    sns.histplot(data=df[columna],color="#008080",
                 kde=option1,discrete=option2,bins=100);
    plt.xlabel(None)
    plt.title(columna);
    plt.ylabel('Cantidad')
    plt.grid(True, color='lightgrey',linestyle='--')
    plt.show() 
def grafico_hyb_sns(df,columna,option1,option2,binss,col):   #(df:tabla, columna, option1: kde True or False
                                                             #,option2: discrete True or False, binss: numero de bins,
                                                             # col: color)
    #plt.rcParams['figure.figsize'] = (6,4)
    f, (ax_box, ax_hist) = plt.subplots(2,sharex=True,gridspec_kw={"height_ratios": (.25, .95)})
    red_cir = dict(markerfacecolor='maroon',marker='o',markersize=6)
    #sns.set_style("whitegrid")
    plt.grid(True, color='lightgrey',linestyle='--')
    sns.boxplot(x=df[columna],ax=ax_box,color=col,
                flierprops=red_cir).set_title(columna)
    
    sns.stripplot(x=df[columna],ax=ax_box,color="lightsalmon",jitter=0.15, size=2.5)
    sns.histplot(data=df[columna],color=col,ax=ax_hist,
                 kde=option1,discrete=option2,bins=binss)   
    ax_box.set(xlabel='')
    ax_box.grid(True, color='lightgrey',linestyle='--')
    ax_hist.set(xlabel='')
    ax_hist.set(ylabel='Cantidad')
    ax_hist.grid(True, color='lightgrey',linestyle='--')
    plt.show()
def grafico_boxplot_jitted(df,columna,jit):              #(df:tabla, columna, jit: si o no)
    plt.rcParams['figure.figsize'] = (9,12)
    red_cir = dict(markerfacecolor='maroon',marker='o',markersize=6)
    #sns.set_style("whitegrid")
    plt.grid(True, color='lightgrey',linestyle='--')
    if(jit=='no'):
        sns.boxplot(y=df[columna],color="#008080",
                     flierprops=red_cir).set_title(columna);  
    else:
        ax=sns.boxplot(x=df[columna],data=df,color="#008080",
                flierprops=red_cir).set_title(columna); 
        ax=sns.stripplot(x=df[columna], data=df, color="lightsalmon", jitter=0.15, size=2.5)

    plt.xlabel(None)   
    plt.grid(True, color='lightgrey',linestyle='--')
    plt.show()
    
def atypicals_be_gone(df,pars,colors,T,metodo,limit):
    ## Gráficos antes de la eliminación
    # Histogramas 1
    print('Histogramas (con atípicos)')
    for j in range(0,len(pars)):
        grafico_hyb_sns(df,pars[j],True,False,100,colors[j])
        plt.show()
    ## Eliminación de atípicos  
    n_i=df.shape[0]
    for j in range(0,len(pars)):
        w=1
        if T==True:
            print(f'Eliminación de atípicos considerando: {pars[j]}')
        while (w!=0):
            [w,resum]=outliers_col(df,pars[j],df.shape[0],metodo,T,n_i,limit);
            df=outliers_col_eliminacion(df,pars[j],metodo,limit);
    ## Gráficos después de la eliminación
    # Histogramas 2
    print('Histogramas (sin atípicos)')
    for j in range(0,len(pars)):
        grafico_hyb_sns(df,pars[j],True,False,100,colors[j])
        plt.show()

    return df

# Matriz de correlación
def matriz_correlacion(df):
    matriz = df.corr(method='kendall')
    plt.rcParams['figure.figsize'] = (7,7);
    plt.matshow(matriz, cmap='BrBG', vmin=-1, vmax=1)
    plt.xticks(range(df.shape[1]), df.columns, rotation=90)
    plt.yticks(range(df.shape[1]), df.columns)

    for i in range(len(matriz.columns)):
          for j in range(len(matriz.columns)):
                 plt.text(i, j, round(matriz.iloc[i, j], 2),
                 ha="center", va="center")

    plt.colorbar()
    plt.grid(False)
    plt.show()
# Cálcular el tamaño de la muestra
def tam_muestra(ven_tas_comuna1,confianza):
    alpha=1-confianza # Confianza del 90%=0.9
    N=ven_tas_comuna1.shape[0]
    er=10/ven_tas_comuna1['valor'].mean()
    Z=stats.norm.ppf(1-alpha/2)
    COV=ven_tas_comuna1['valor'].std()/ven_tas_comuna1['valor'].mean()
    nmuestra=(N*(COV**2)*(Z**2))/((er**2)*(N-1)+(COV**2)*(Z**2))
    n_muestra=int(nmuestra)
    return n_muestra

def Muestra_uni(df1,df2,cve,ant):
    nn=tam_muestra(df1,0.9) 
    n1=int(nn/10) 
    N=df1.shape[0] 
    n2=int(N/10) 
    df3=df1.sort_values(by=ant, ascending= True)
    Muestras=[]
    for i in range(0,2):
        a1=df3.iloc[0:n2,:]
        b1=df3.iloc[n2:2*n2,:]
        c1=df3.iloc[2*n2:3*n2,:]
        d1=df3.iloc[3*n2:4*n2,:]
        e1=df3.iloc[4*n2:5*n2,:]
        f1=df3.iloc[5*n2:6*n2,:]
        g1=df3.iloc[6*n2:7*n2,:]
        h1=df3.iloc[7*n2:8*n2,:]
        i1=df3.iloc[8*n2:9*n2,:]
        j1=df3.iloc[9*n2:N+1,:]
        if n1==n2:
            A1=a1.sample(n=n1)
            B1=b1.sample(n=n1)
            C1=c1.sample(n=n1)
            D1=d1.sample(n=n1)
            E1=e1.sample(n=n1)
            F1=f1.sample(n=n1)
            G1=g1.sample(n=n1)
            H1=h1.sample(n=n1)
            I1=i1.sample(n=n1)
            J1=j1.sample(n=nn-9*n1)
        else:
            k,n3=0,n1 
            while 10*n1+k<=nn:
                if 10*n1+k==nn:
                    A1=a1.sample(n=n1)
                    B1=b1.sample(n=n1)
                    C1=c1.sample(n=n1)
                    D1=d1.sample(n=n1)
                    E1=e1.sample(n=n1)
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break   
                k=k+1 
                n3=n3+1
                A1=a1.sample(n=n3)
                if 10*n1+k==nn:
                    B1=b1.sample(n=n1)
                    C1=c1.sample(n=n1)
                    D1=d1.sample(n=n1)
                    E1=e1.sample(n=n1)
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break
                k=k+1
                B1=b1.sample(n=n3) 
                if 10*n1+k==nn:
                    C1=c1.sample(n=n1)
                    D1=d1.sample(n=n1)
                    E1=e1.sample(n=n1)
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break
                k=k+1
                C1=c1.sample(n=n3)
                if 10*n1+k==nn:    
                    D1=d1.sample(n=n1)
                    E1=e1.sample(n=n1)
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break  
                k=k+1
                D1=d1.sample(n=n3) 
                if 10*n1+k==nn:
                    E1=e1.sample(n=n1)
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break 
                k=k+1
                E1=e1.sample(n=n3)
                if 10*n1+k==nn:
                    F1=f1.sample(n=n1)
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break 
                k=k+1
                F1=f1.sample(n=n3)
                if 10*n1+k==nn:
                    G1=g1.sample(n=n1)
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break
                k=k+1
                G1=g1.sample(n=n3)
                if 10*n1+k==nn:
                    H1=h1.sample(n=n1)
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break 
                k=k+1
                H1=h1.sample(n=n3)
                if 10*n1+k==nn:
                    I1=i1.sample(n=n1)
                    J1=j1.sample(n=n1)
                    break 
                k=k+1
                I1=i1.sample(n=n3)
                if 10*n1+k==nn:
                    J1=j1.sample(n=n1)
                    break 
                k=k+1
                J1=j1.sample(n=n3)
        MuestraML=pd.concat([A1,B1,C1,D1,E1,F1,G1,H1,I1,J1],sort=False)
        MuestraML=datosduplicados(MuestraML,False)
        Muestras.append(MuestraML)
    MuestraML=Muestras[0]
    MuestraAVM=pd.merge(df2,Muestras[1], how="right", 
                        on=["ingreso","antiguedad","longitud","latitud","supCSII","supTSII","valor","avaluofiscal"])
    MuestraAVM=datosduplicados(MuestraAVM,False)
    return MuestraML,MuestraAVM

def DelUbicaciones(df):
    L=df.loc[:,'longitud'].tolist()
    L2=df.loc[:,'latitud'].tolist()
    # Contar y guardar decimales de longitud
    digitosLongitud=[]
    for k in range(len(L)):
        c=1
        sLk=str(L[k])
        for s in range(len(sLk)):
            if sLk[s]!='.':
                c=c+1
            else:
                break
        dk=len(str(L[k]))-c
        digitosLongitud.append(dk)
    df.insert(df.shape[1],'D_longitud',digitosLongitud, True)
    # Contar y guardar decimales de latitud
    digitosLatitud=[]
    for k in range(len(L2)):
        c=1
        sLk=str(L2[k])
        for s in range(len(sLk)):
            if sLk[s]!='.':
                c=c+1
            else:
                break
        dk=len(str(L2[k]))-c
        digitosLatitud.append(dk)
    df.insert(df.shape[1],'D_latitud',digitosLatitud, True)
    # quedarnos solo con las ubicaciones con más de 6 decimales
    df=df[(df['D_longitud']>=6)&(df['D_latitud']>=6)]
    df=df[['ingreso','antiguedad','longitud','latitud','supCSII','supTSII','avaluofiscal','valor','supTSII/supCSII',
           'cve_comuna','ufm2(supCSII)','ufm2(supTSII)']]
    return df
def grafico_geografico_leafmap(df,df1,df2,defcolor1,defcolor2,defcolor3,ancho,alto):
    map_geo = leafmap.Map(center=[df['latitud'].mean(),df['longitud'].mean()],zoom=8,
                         width=ancho, height=alto)
    
    map_geo.add_circle_markers_from_xy(df,x="longitud", y="latitud",radius=5, color=defcolor1, fill_color=defcolor1,
                                           popup=["longitud","latitud","valor"])
    
    map_geo.add_circle_markers_from_xy(df1,x="longitud", y="latitud",radius=5, color=defcolor2, fill_color=defcolor2,
                                           popup=["longitud","latitud","valor"])
    
    map_geo.add_circle_markers_from_xy(df2,x="longitud", y="latitud",radius=1, color=defcolor3, fill_color=defcolor3,
                                          popup=["longitud","latitud","valor"])
    
    return display(map_geo)
def agrupamiento_dbscan(X,pdf,R,Min):
    # Compute DBSCAN
    db = DBSCAN(eps=R, min_samples=Min).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    new_pdf=pdf.assign(Clus_Db=labels)

    realClusterNum=len(set(labels)) - (1 if -1 in labels else 0)
    clusterNum = len(set(labels)) 

    # Number of data in a cluster
    Number_of_data=[];
    for clust_number in set(labels):
        if (clust_number!=-1):
                clust_set = new_pdf[new_pdf.Clus_Db == clust_number];
                Number_of_data.append(clust_set.shape[0]);

    return [labels,realClusterNum,Number_of_data,new_pdf]
#### Función para hacer los gráficos ##########
def graficosns(df,columna,option1,option2,binss,colore):   #(df:tabla, columna, option1: kde True or False
                                                             #,option2: discrete True or False, binss: numero de bins,
                                                            # col: color)
    f, ax= plt.subplots(2,1,figsize=(10,7),sharex=True,gridspec_kw={"height_ratios": (.35, .55)})
    sns.set_style("whitegrid")
    red_cir = dict(markerfacecolor='maroon',marker='o',markersize=6)
    sns.boxplot(y="Tipo",x=df[columna],data=df,ax=ax[0],
                flierprops=red_cir,palette=colore).set_title(columna)
    sns.stripplot(y="Tipo",x=df[columna],data=df,ax=ax[0],jitter=0.15,size=2.5,palette=colore)
    ax[0].grid(True, color='lightgrey',linestyle='--')
    ax[0].set(xlabel='')
    ax[0].set(ylabel='')
    

    sns.histplot(data=df,x=columna,hue='Tipo',element='bars',palette=colore,
                 ax=ax[1],kde=option1,discrete=option2,bins=binss)     
    ax[1].set(xlabel='')
    ax[1].set(ylabel='Cantidad')
    #ax[1].set_title(columna)
    ax[1].grid(True, color='lightgrey',linestyle='--')
    plt.show()
    
def sub_clusters(df):
    # Hacemos una lista con las etiquetas de los clusters
    L_C=df['cluster_elbow'].unique()
    L_C=L_C.tolist()
    L_C.sort()
    # lista para guardar cada data frame nuevo:
    List_data=[]
    # Empezamos a realizar el k-means a cada cluster:
    for P in L_C:
        df_p=df[df['cluster_elbow']==P]
        df_P=df_p.drop(['cluster_elbow'],axis=1)
        X = StandardScaler().fit_transform(df_P)
        kmeans_kwargs = {"init": "k-means++","n_init": 10,"max_iter": 300,"random_state": 42,}
        sse = []
        for k in range(1, 11):
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
            kmeans.fit(X)
            sse.append(kmeans.inertia_)

        fig = plt.figure(figsize=(3,3))
        plt.plot(range(1, 11),sse,color="blue",marker='o')
        plt.xticks(range(1, 11))
        plt.xlabel("Número de Clusters")
        plt.ylabel("SSE")
        plt.show()
        kl = KneeLocator(range(1, 11), sse, curve="convex", direction="decreasing")
        el=kl.elbow
        print(f"El número de clusters apropiados es: {el}")
        kmeanss=KMeans(n_clusters=el,**kmeans_kwargs)
        kmeanss.fit(X)
        df_P.loc[:,'subcluster']=kmeanss.labels_
        df_P.insert(df_P.shape[1]-1,'cluster_elbow',df_p.loc[:,'cluster_elbow'], True)
        List_data.append(df_P)
        display(df_P)
        fig = plt.figure(figsize=(6,4))
        sns.scatterplot(x='longitud',y='latitud',data=df_P,hue="subcluster",palette="Set2",edgecolor="black",linewidth=0.3)
        plt.legend(labels=((df_P['subcluster'].unique()).tolist()).sort(),
                   bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        plt.show()
    DF_P=pd.concat(List_data, ignore_index=True, sort=False)
    C_e=DF_P.loc[:,'cluster_elbow'].tolist()
    S_c=DF_P.loc[:,'subcluster'].tolist()
    L_CF=[]
    for num in range(len(C_e)):
        L_CF.append(str(C_e[num])+'.'+str(S_c[num]))
    DF_P.insert(DF_P.shape[1],'cluster',L_CF, True)
    return DF_P

def indexacion(df1,mini,maxi):
    df=df1.copy()
    years1=[]
    for i in range(mini,maxi,10):
        years1.append(i)
    if maxi not in years1:
        years1.append(maxi)
    conditionlist1=[]
    for k in range(0,(len(years1))-2): 
        c=(df['antiguedad'] >=years1[k]) & (df['antiguedad'] <years1[k+1])
        conditionlist1.append(c)
    c=(df['antiguedad'] >=years1[(len(years1))-2]) & (df['antiguedad'] <=years1[(len(years1))-1])
    conditionlist1.append(c)
    L=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","W","X","Y","Z"]
    vectorS1=[]
    for i in range(0,len(years1)-2):
        vectorS1.append(L[i]+str(years1[i])+"/"+str(years1[i+1]-1))
    vectorS1.append(L[len(years1)-2]+str(years1[len(years1)-2])+"/"+str(years1[len(years1)-1]))
    choicelist1=[]
    for i in range(0,len(vectorS1)):
        choicelist1.append(vectorS1[i][0]+vectorS1[i][3:6]+vectorS1[i][8:10])
    df.insert(df.shape[1],'Index_antiguedad_10',np.select(conditionlist1, choicelist1, default=0))
    df2=df.astype({"ingreso":"float64",'antiguedad':'float64','supCSII':'float64','supTSII':'float64','valor':'float64',"avaluofiscal": "float64"})
    return df2

# Gráfica de boxplots
def grafico_boxplot_rcParams(df2):
    plt.rcParams['figure.figsize'] = (7,5);
    sns.boxplot(data=df2.sort_values(by=['Index_antiguedad_10'],
              ascending=True, inplace=False), 
              x="Index_antiguedad_10", y="valor",
              showfliers=False,palette="Set2");
    sns.stripplot(data=df2.sort_values(by=['Index_antiguedad_10'], 
              ascending=True, inplace=False), 
              x="Index_antiguedad_10", y="valor",
              linewidth=1.0,palette="Set2");
    plt.xlabel('Década')
    plt.ylabel('Valor UF')
    plt.title('Distribución valor UF por década')
    plt.grid(True, color='lightgrey',linestyle='--')
    plt.show()

def GraEstModels(e,f,g,h): ##### MODIFICADA POR TENER REGRESION Y ENET #####
    xvec=list(e)
    xvec2=list(g)
    for k in range(0,len(xvec2)):
        xvec.append(xvec2[k])  
    xmin,xmax=min(xvec)-250,max(xvec)+250
    yvec=list(f)
    yvec2=list(h)
    for k in range(0,len(yvec2)):
        yvec.append(yvec2[k])
    ymin,ymax=min(yvec)-250,max(yvec)+250
    red=[xmin,xmax]
    
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(14,5))
    axs[0].scatter(e,f,color="#008080",edgecolor="c");
    axs[0].plot(red,red,color="red")
    axs[0].set_xlabel('Valor Observado',size=12)
    axs[0].set_ylabel('Valor Estimado',size=12)
    axs[0].grid(True)
    axs[0].set_xlim(xmin,xmax)
    axs[0].set_ylim(ymin,ymax)
    axs[0].set_title('Random Forest', size= 16)

    axs[1].scatter(g,h,color="#008080",edgecolor="c");
    axs[1].plot(red,red,color="red")
    axs[1].set_xlabel('Valor Observado',size=12)
    axs[1].set_ylabel('Valor Estimado',size=12)
    axs[1].grid(True)
    axs[1].set_xlim(xmin,xmax)
    axs[1].set_ylim(ymin,ymax)
    axs[1].set_title('Extreme Gradient Boosting', size= 16)

    plt.show()

def porcentajeerror(a,b): # a: y_test, b: y_pred
    r1=100*(b-a)/a;
    rr1=r1.tolist();
    tabla= pd.DataFrame.from_dict({'Intervalo':[],'%_Est_Acumulado': [],'Cantidad_Est_Relativa': []});
    col = ['Intervalo','%_Est_Acumulado','Cantidad_Est_Relativa'];
    cant=0
    k=[5,10,15,20,25,50]
    for lim in range(0,len(k)):
        if k[lim]==5:
            inter=f"|Error|<={k[lim]} %"
        else: 
            inter=f"{k[lim-1]}% <|Error|<={k[lim]}%"
        porcentaje1=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))/len(rr1)
        cantidad1=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr1))-cant
        cant=cant+cantidad1

        tablaux = pd.DataFrame([[inter,porcentaje1,cantidad1]], columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

def Entrenamiento(df2, t_s):
    df3=df2.drop(['valor'],axis=1)
    Xrlinter = np.array(df3)
    yrlinter = np.array(df2.valor)
    Xrlinter_train, Xrlinter_test, yrlinter_train, yrlinter_test = train_test_split(Xrlinter, yrlinter, test_size=t_s)
    return Xrlinter_train, Xrlinter_test, yrlinter_train, yrlinter_test, Xrlinter


def Escalas(Xrlinter_train, Xrlinter_test):
    scl = StandardScaler().fit(Xrlinter_train)
    Xrlinter_train = scl.transform(Xrlinter_train)  
    Xrlinter_test = scl.transform(Xrlinter_test)  
    return Xrlinter_train, Xrlinter_test,scl


## Random Forest para un par de datos
def RForest(Xtrain,Xtest,ytrain,ytest,k,maxfeat):
    rforest = RandomForestRegressor(max_features=maxfeat,random_state=42)  
    params={'n_estimators':[300,500,800],
           'max_depth':[30,50,80]}  
    Search=GridSearchCV(estimator=rforest,
                       param_grid=params,
                       n_jobs=-1)
    rforest1=Search.fit(Xtrain,ytrain)
    rforest1.best_estimator_
    y_pred43 = cross_val_predict(rforest1, Xtest, np.ravel(ytest), cv=k)
    return rforest1,y_pred43

def RForestEleccion(df2,k,maxfeat):
    # Entrenamiento
    Xtodos_train_inicial, Xtodos_test, ytodos_train, ytodos_test,Xtodos=Entrenamiento(df2,0.2)
    # Escala
    Xtodos_train, Xtodos_test,scl1 =Escalas(Xtodos_train_inicial, Xtodos_test)
    # Random Forest
    rforest1,y_pred43=RForest(Xtodos_train,Xtodos_test,ytodos_train,ytodos_test,k,maxfeat)
    return scl1,ytodos_test,y_pred43,rforest1,Xtodos_train_inicial

# XGB para un par de datos
def XGB(Xtrain,Xtest,ytrain,ytest,k):
    xg=xgb.XGBRegressor(objective="reg:squarederror",alpha=1)
    colsample= [0.3,0.5,0.7]
    lr=[0.05,0.2,0.5]
    max_d=[30,50,80]
    n_est=[300,500,800]
    params={"colsample_bytree":colsample,"learning_rate":lr,"max_depth":max_d,"n_estimators":n_est}
    search=GridSearchCV(estimator=xg,param_grid=params,n_jobs=-1)
    search_model=search.fit(Xtrain,ytrain)
    search_model.best_params_                    
    y_pred63 = cross_val_predict(search_model, Xtest, np.ravel(ytest), cv=k)
    return search_model,y_pred63

def XGB_Eleccion(df2,k):
    # Entrenamientos
    Xtodos_train_inicial, Xtodos_test, ytodos_train, ytodos_test,Xtodos=Entrenamiento(df2,0.2)
    # Escalas
    Xtodos_train, Xtodos_test,scl1 =Escalas(Xtodos_train_inicial, Xtodos_test)
    # XGBs
    xgb1,y_pred43=XGB(Xtodos_train,Xtodos_test,ytodos_train,ytodos_test,k)

    #scaler1_file = "escalaXGB_"+str(cve)+".save"
    #joblib.dump(scl1, scaler1_file)
    #print("El método de Extreme Gradient Boosting se ha ejecutado con éxito. Se procederá a guardar los resultados.")
    #joblib.dump(xgb1,"XGB_"+str(cve)+".joblib")
    # (Se hace aparte)
    return scl1,ytodos_test,y_pred43,xgb1,Xtodos_train_inicial

# Error para los 4 modelos
def porcentajeerror2(e,f,g,h):  ##### MODIFICADA POR TENER RL Y ENET #####
    r3=100*(f-e)/e;
    rr3=r3.tolist();
    r4=100*(h-g)/g;
    rr4=r4.tolist();
    
    tabla= pd.DataFrame.from_dict({'Intervalo':[],
                                '%_Est_RandomForest': [],'Cantidad_Est_RandomForest': [],
                                 '%_Est_XGboosting': [],'Cantidad_Est_XGboosting':[]});
    
    col = ['Intervalo','%_Est_RandomForest','Cantidad_Est_RandomForest', '%_Est_XGboosting','Cantidad_Est_XGboosting'];
    cant=[0,0]
    k=[5,10,15,20,25,50]
    for lim in range(0,len(k)):
        if k[lim]==5:
            inter=f"|Error|<={k[lim]} %"
        else: 
            inter=f"{k[lim-1]}% <|Error|<={k[lim]}%"
        porcentaje3=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))/len(rr3)
        cantidad3=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))-cant[0]
        porcentaje4=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))/len(rr4)
        cantidad4=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))-cant[1]
        cant=[cant[0]+cantidad3,cant[1]+cantidad4]
      
        tablaux = pd.DataFrame([[inter,porcentaje3,cantidad3,porcentaje4,cantidad4]],
                              columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

# Estadisticas de los errores de los 4 modelos
def Tabla_Estadistica_Error(y31,y32,y41,y42): #### MOD POR TENER RL Y ENET
    E_RForest=[]
    E_XGB=[]
    Sobreestimados3=0
    Sobreestimados4=0
    Subestimados3=0
    Subestimados4=0
    Estimados3=0
    Estimados4=0
    for i in range(0,len(y31)):
        E_RForest.append(y31[i]-y32[i])
        if y31[i]-y32[i]<0:
            Sobreestimados3+=1
        elif y31[i]-y32[i]>0:
            Subestimados3+=1
        Estimados3+=1
    for i in range(0,len(y41)):
        E_XGB.append(y41[i]-y42[i])
        if y41[i]-y42[i]<0:
            Sobreestimados4+=1
        elif y41[i]-y42[i]>0:
            Subestimados4+=1
        Estimados4+=1
        
    Sobreestimados=[Sobreestimados3,Sobreestimados4]
    Subestimados=[Subestimados3,Subestimados4]
    Estimados=[Estimados3,Estimados4]
    tabla= pd.DataFrame.from_dict({'Método':[],
                                'Media': [],'Desviación estándar': [],
                                'Mediana': [], "Datos sobreestimados":[], "Datos subestimados":[],"Datos Estimados":[]});
    col = ['Método','Media','Desviación estándar','Mediana',"Datos sobreestimados","Datos subestimados","Datos Estimados"];
    inter=["Random Forest", "Xtreme Gradient Boosting"]
    media=[np.mean(E_RForest),np.mean(E_XGB)]
    ds=[np.std(E_RForest),np.std(E_XGB)] 
    med=[np.percentile(E_RForest,50),np.percentile(E_XGB,50)]
    for i in range(0,2):
        tablaux = pd.DataFrame([[inter[i],media[i],ds[i],med[i],Sobreestimados[i],Subestimados[i],Estimados[i]]],
                                  columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla



##################### PARTE 3 #########################

def InsertColumnasAVM(reavm):
    reavm.insert(reavm.shape[1],'% de error',
             100*(reavm.loc[:,'Estimación AVM']-reavm.loc[:,'valor'])/reavm.loc[:,'valor'],
             True)
    reavm.insert(reavm.shape[1],'error AVM',reavm['Estimación AVM']-reavm['valor'],True)
    return reavm

def Is_estimated_by_AVM(reavm):
    reavm1=reavm.loc[reavm.loc[:,'Estimación AVM']<=0]
    print(f"La cantidad de datos no estimados por AVM es de: {len(reavm[reavm['Estimación AVM']<=0])}")
    print(f"Cuyo porcentaje equivale a: {(len(reavm[reavm['Estimación AVM']<=0])*100)/reavm.shape[0]: .2f}%")
    reavm2=reavm.loc[reavm.loc[:,'Estimación AVM']>0]
    print(f"La cantidad de datos estimados por AVM es de: {len(reavm[reavm['Estimación AVM']>0])}")
    print(f"Cuyo porcentaje equivale a: {(len(reavm[reavm['Estimación AVM']>0])*100)/reavm.shape[0]: .2f}%")
    return reavm1,reavm2

def Rend_Est_AVM(reavm2):
    plt.rcParams['figure.figsize'] = (9,5);
    sns.scatterplot(data=reavm2,x='valor',y='Estimación AVM',color="#008080")
    plt.plot(reavm2['valor'],reavm2['valor'],color="red")
    plt.plot(reavm2['valor'],reavm2['valor']*(1.05),color="blue")
    plt.plot(reavm2['valor'],reavm2['valor']*(0.95),color="blue")
    plt.plot(reavm2['valor'],reavm2['valor']*(1.2),color="orange")
    plt.plot(reavm2['valor'],reavm2['valor']*(0.8),color="orange")
    plt.legend(["Datos","Recta ajustada a los datos","Error del +5%","Error del -5%","Error del +20%","Error del -20%"],bbox_to_anchor=(1, 1), loc='upper left')
    plt.title("Datos estimados por el AVM",size=16)
    plt.xlabel('Valor Observado');
    plt.ylabel('Valor Estimado AVM');
    plt.grid(True)
    plt.show()
    
# Selección de datos del AVM para escalar
def Xrl_inter(remL):
    reL=remL.drop(['valor'],axis=1)
    Xrlinter = np.array(reL)
    return Xrlinter

def SCL_model(scl,Xtodos,modelo):
    Xtodos=scl.transform(Xtodos)
    ValEst_mod=modelo.predict(Xtodos)
    return ValEst_mod

def InsertColumnsML(reml2,ValEst_RF,ValEst_XGB): ###### MOD X TENER RL Y ENET
    
    reml2.insert(reml2.shape[1],'ValEst_RF',ValEst_RF,True)
    reml2.insert(reml2.shape[1],'ValEst_XGB',ValEst_XGB,True)

    reml2.insert(reml2.shape[1],'% de error RF',100*(reml2['ValEst_RF']-reml2['valor'])/reml2['valor'],True)
    reml2.insert(reml2.shape[1],'error RF',reml2['ValEst_RF']-reml2['valor'],True)

    reml2.insert(reml2.shape[1],'% de error XGB',100*(reml2['ValEst_XGB']-reml2['valor'])/reml2['valor'],True)
    reml2.insert(reml2.shape[1],'error XGB',reml2['ValEst_XGB']-reml2['valor'],True)
    return reml2

def Rend_Est_ML(reml2): #### MOD X TENER RL Y ENET
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))

    axs[0].scatter(reml2['valor'],reml2['ValEst_RF'],color="#008080",edgecolor="c")
    axs[0].plot(reml2['valor'],reml2['valor'],color="red")
    axs[0].plot(reml2['valor'],reml2['valor']*(1.05),color="blue")
    axs[0].plot(reml2['valor'],reml2['valor']*(0.95),color="blue")
    axs[0].plot(reml2['valor'],reml2['valor']*(1.2),color="orange")
    axs[0].plot(reml2['valor'],reml2['valor']*(0.8),color="orange")
    axs[0].set_xlabel('Valor Observado')
    axs[0].set_ylabel('Valor Estimado')
    axs[0].set_title('Random Forest')
    axs[0].grid(True)

    axs[1].scatter(reml2['valor'],reml2['ValEst_XGB'],color="#008080",edgecolor="c")
    axs[1].plot(reml2['valor'],reml2['valor'],color="red")
    axs[1].plot(reml2['valor'],reml2['valor']*(1.05),color="blue")
    axs[1].plot(reml2['valor'],reml2['valor']*(0.95),color="blue")
    axs[1].plot(reml2['valor'],reml2['valor']*(1.2),color="orange")
    axs[1].plot(reml2['valor'],reml2['valor']*(0.8),color="orange")
    axs[1].set_xlabel('Valor Observado')
    axs[1].set_ylabel('Valor Estimado')
    axs[1].set_title('Extreme Gradient Boosting')
    axs[1].grid(True)

    plt.show()

def atypicals_be_goneAVM(df,pars,T,metodo,limit): 
    ## Eliminación de atípicos  
    n_i=df.shape[0]
    for j in range(0,len(pars)):
        w=1
        if T==True:
            print(f'Eliminación de atípicos considerando: {pars[j]}')
        while (w!=0):
            [w,resum]=outliers_col(df,pars[j],df.shape[0],metodo,T,n_i,limit);
            df=outliers_col_eliminacion(df,pars[j],metodo,limit);
    return df

def Error_AVM_vs_ML(reml2): ### MOD X TENER RL Y ENET
    real=reml2['valor']
    estimado3=reml2['ValEst_RF']
    estimado4=reml2['ValEst_XGB']
    r3=100*(estimado3-real)/real;
    rr3=r3.tolist();
    r4=100*(estimado4-real)/real;
    rr4=r4.tolist();

    tabla= pd.DataFrame.from_dict({'Intervalo':[],
                                   '%_RF_Acumulado': [],'Cantidad_RF': [],
                                   '%_XGB_Acumulado': [],'Cantidad_XGB': []});

    col = ['Intervalo','%_RF_Acumulado','Cantidad_RF', "%_XGB_Acumulado",'Cantidad_XGB'];
    cant=[0,0]
    k=[5,10,15,20,25,50]
    for lim in range(0,len(k)):
        if k[lim]==5:
            inter=f"|Error|<={k[lim]} %"
        else: 
            inter=f"{k[lim-1]}% <|Error|<={k[lim]}%"
        porcentaje3=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))/len(rr3)
        cantidad3=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))-cant[0]
        porcentaje4=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))/len(rr4)
        cantidad4=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))-cant[1]
        cant=[cant[0]+cantidad3,cant[1]+cantidad4]


        tablaux = pd.DataFrame([[inter,porcentaje3,cantidad3,porcentaje4,cantidad4]],
                                columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    inter=f"|Error|>50%"
    porcentaje3=100*(reml2.shape[0]-cant[0])/reml2.shape[0]+porcentaje3
    cantidad3=reml2.shape[0]-cant[0]
    porcentaje4=100*(reml2.shape[0]-cant[1])/reml2.shape[0]+porcentaje4
    cantidad4=reml2.shape[0]-cant[1]
    cant=[cant[0]+cantidad3,cant[1]+cantidad4]


    tablaux = pd.DataFrame([[inter,porcentaje3,cantidad3,porcentaje4,cantidad4]],
                            columns=col);
    tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

def Tabla_Estadistica_Error2(df): ## MOD X TENER RL Y ENET ##
    E_RForest=df.loc[:,"error RF"]
    E_XGB=df.loc[:,"error XGB"]
    Sobreestimados4=len(E_RForest[E_RForest>0])
    Sobreestimados5=len(E_XGB[E_XGB>0])
    
    Subestimados4=len(E_RForest[E_RForest<0])
    Subestimados5=len(E_XGB[E_XGB<0])
    
    Estimados4=Sobreestimados4+Subestimados4+len(E_RForest[E_RForest==0])
    Estimados5=Sobreestimados5+Subestimados5+len(E_XGB[E_XGB==0])
    
    Sobreestimados=[Sobreestimados4,Sobreestimados5]
    Subestimados=[Subestimados4,Subestimados5]
    Estimados=[Estimados4,Estimados5]
    
    tabla= pd.DataFrame.from_dict({'Método':[],
                                'Media': [],'Desviación estándar': [],
                                'Mediana': [],"Datos sobreestimados":[], "Datos subestimados":[],"Datos estimados":[]});
    col = ['Método','Media','Desviación estándar','Mediana',"Datos sobreestimados",
        "Datos subestimados","Datos estimados"];
    inter=["Random Forest", "Xtreme Gradient Boosting"]
    media=[np.mean(E_RForest),np.mean(E_XGB)]
    ds=[np.std(E_RForest),np.std(E_XGB)] 
    med=[np.percentile(E_RForest,50),np.percentile(E_XGB,50)]

    for i in range(0,2):
        tablaux = pd.DataFrame([[inter[i],media[i],ds[i],med[i],Sobreestimados[i],Subestimados[i],
                                Estimados[i]]],
                                  columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

def ModeloFinal(reml2,scls,models,cve,Malerta1,Malerta2): ### MOD X TENER RL Y ENET
    RF_er=np.array(list(map(abs, reml2['% de error RF'].tolist())))
    XGB_er=np.array(list(map(abs, reml2['% de error XGB'].tolist())))
    L=[RF_er,XGB_er] #Lista 

    a3=len(RF_er[RF_er>17])
    a4=len(XGB_er[XGB_er>17])
    
    p=min(a3,a4)
    
    if p==a3: 
        print("El método escogido de manera definitiva será el de Random Forest. Se procede a guardarlo")
        scaler_file = "escala_Final_"+str(cve)+".save"
        joblib.dump(scls[0], scaler_file)
        joblib.dump(models[0],"Modelo_Final_"+str(cve)+".joblib")
        Malerta1.to_excel("Muestra_Alertas_"+str(cve)+".xlsx")
        return models[0],scls[0],Malerta1
    
    elif p==a4: 
        print("El método escogido de manera definitiva será el Extreme Gradient Boosting. Se procede a guardarlo")
        scaler_file = "escala_Final_"+str(cve)+".save"
        joblib.dump(scls[1], scaler_file)
        joblib.dump(models[1],"Modelo_Final_"+str(cve)+".joblib")
        Malerta2.to_excel("Muestra_Alertas_"+str(cve)+".xlsx")
        return models[1],scls[1],Malerta2

