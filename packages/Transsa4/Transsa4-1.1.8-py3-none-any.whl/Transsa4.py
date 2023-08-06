#################################### Paquetes ##############################################
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
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, cross_val_predict
import joblib
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
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
import graphviz
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

############################### Funciones ##################################################
def InsertColumns(D): #(D es la tabla) 
    D=D.astype({'nro_dormitorios': 'uint8','nro_banos':'uint8','sup_util':'float64',
                'sup_total':'float64','valor_uf':'float64'})
    
    D.insert(D.shape[1],'ufm2(sup_util)',D.loc[:,'valor_uf']/D.loc[:,'sup_util'], True) 
    D.insert(D.shape[1],'ufm2(sup_total)',D.loc[:,'valor_uf']/D.loc[:,'sup_total'], True)
    D.insert(D.shape[1],'sup_total/sup_util',D.loc[:,'sup_total']/D.loc[:,'sup_util'], True) 
    return D
# Concatenación de tablas de ventas y tasaciones
def tabla_auxiliar(df1,variables): #df1 es la tabla de ofertas, variables son las columnas que se guardarán
    df1_aux=df1[variables]
    return df1_aux

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
    D_comuna=D1.loc[(D1.loc[:,'cve_comuna']==cve) & (D1.loc[:,'valor_uf']>=tol)]
    return D_comuna
def datosduplicados(tabla,T): #(tabla es la tabla, T es True entonces se muestra la cantidad de datos eliminados)
    n_inicial = tabla.shape[0];
    tabla2 = tabla.drop_duplicates(subset=['nro_dormitorios','nro_banos','longitud','latitud',
                                          'sup_util','sup_total'])
    
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

# Eliminar datos iguales a 0
def Del_DBcero(df):  #df:tabla de ofertas
    I1=df[(df['nro_dormitorios']<1)].index
    for x in I1.values:
            df.loc[x,'nro_dormitorios'] = np.nan;
            if not sys.warnoptions:
                import warnings
                warnings.simplefilter("ignore")
    I2=df[(df['nro_banos']<1)].index
    for x in I2.values:
        df.loc[x,'nro_banos'] = np.nan;
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")
    df=df.dropna(axis = 0);
    return df

def atypicals_be_gone(df,pars,T,metodo,limit,colors):
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

#########################################################################################################################
############################################# Funciones Nuevas ##########################################################
#########################################################################################################################

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
    df=df[['nro_dormitorios','nro_banos','latitud','longitud','sup_util','sup_total','valor_uf',
           'cve_comuna','ufm2(sup_util)','ufm2(sup_total)','sup_total/sup_util']]
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

#### subclusters ##########

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

#########################################################################################################################
#########################################################################################################################

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
def tam_muestra(ofertas_comuna1,confianza):
    alpha=1-confianza # Confianza del 90%=0.9
    N=ofertas_comuna1.shape[0]
    er=10/ofertas_comuna1['valor_uf'].mean()
    Z=stats.norm.ppf(1-alpha/2)
    COV=ofertas_comuna1['valor_uf'].std()/ofertas_comuna1['valor_uf'].mean()
    nmuestra=(N*(COV**2)*(Z**2))/((er**2)*(N-1)+(COV**2)*(Z**2))
    n_muestra=int(nmuestra)
    return n_muestra

def Muestra(df1,df2,cve,ant):
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
                        on=["cve_comuna",'nro_dormitorios','nro_banos',"longitud","latitud","sup_util","sup_total","valor_uf"])

    MuestraAVM=datosduplicados(MuestraAVM,False)
    nombre1='Muestra_Oferta_ML'+str(cve)+'.xlsx'
    nombre2='Muestra_Oferta_AVM'+str(cve)+'.xlsx'
    MuestraML.to_excel(nombre1)
    MuestraAVM.to_excel(nombre2)
    return MuestraML,MuestraAVM,nn

def Muestra_Total(A):
    if A=="ML":
        LR = pd.read_excel('Muestra_Oferta_ML19.xlsx');
        LC = pd.read_excel('Muestra_Oferta_ML21.xlsx');
        LB = pd.read_excel('Muestra_Oferta_ML22.xlsx');
        V = pd.read_excel('Muestra_Oferta_ML52.xlsx');
        Muestra = pd.concat([LR,LC,LB,V], ignore_index=True, sort=False)
        Muestra.to_excel('Muestra_Total_Oferta_ML.xlsx')
    elif A=="AVM":
        LR = pd.read_excel('Muestra_Oferta_AVM19.xlsx');
        LC = pd.read_excel('Muestra_Oferta_AVM21.xlsx');
        LB = pd.read_excel('Muestra_Oferta_AVM22.xlsx');
        V = pd.read_excel('Muestra_Oferta_AVM52.xlsx');
        Muestra = pd.concat([LR,LC,LB,V], ignore_index=True, sort=False)
        Muestra.to_excel('Muestra_Total_Oferta_AVM.xlsx')
    return Muestra
# Gráfica de boxplots #columna: 'nro dormitorios','nro banos','nro estacionamientos'
def grafico_boxplot_rcParams(df2,columna):
    plt.rcParams['figure.figsize'] = (9,6);
    sns.boxplot(data=df2.sort_values(by=[columna],
              ascending=True, inplace=False), 
              x=columna, y="valor_uf",
              showfliers=False,palette="Set2");
    sns.stripplot(data=df2.sort_values(by=[columna], 
              ascending=True, inplace=False), 
              x=columna, y="valor_uf",
              linewidth=1.0,palette="Set2");
    plt.xlabel(columna[4:])
    plt.ylabel('Valor UF')
    plt.title('Distribución valor UF por número de '+columna[4:])
    plt.grid(True, color='lightgrey',linestyle='--')
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

#################### Entrenamiento #################### 
def Entrenamiento(df2,independientes,dependiente, t_s):
    # si es para el valor, las independientes=['nro_dormitorios','nro_banos','longitud','latitud','sup_util','sup_total']
    Xrlinter = np.array(df2[independientes])
    # si es para el valor, dependiente='valor_uf'
    yrlinter = np.array(df2[[dependiente]])
    Xrlinter_train, Xrlinter_test, yrlinter_train, yrlinter_test = train_test_split(Xrlinter, yrlinter, test_size=t_s)
    return Xrlinter_train, Xrlinter_test, yrlinter_train, yrlinter_test

def Escalas(Xrlinter_train, Xrlinter_test):
    scl = StandardScaler().fit(Xrlinter_train)
    Xrlinter_train = scl.transform(Xrlinter_train)  
    Xrlinter_test = scl.transform(Xrlinter_test)  
    return Xrlinter_train, Xrlinter_test,scl


## Random Forest para un par de datos
def RForest(Xtrain,Xtest,ytrain,ytest,k,max_fe):
    rforest = RandomForestRegressor(max_features=max_fe,random_state=42)  
    params={'n_estimators':[300,400,550,800],
           'max_depth':[25,45,60,80]}  
    Search=GridSearchCV(estimator=rforest,
                       param_grid=params,
                       n_jobs=-1)
    rforest1=Search.fit(Xtrain,ytrain)
    rforest1.best_estimator_
    y_pred43 = cross_val_predict(rforest1, Xtest, np.ravel(ytest), cv=k)
    return rforest1,y_pred43

def RForestEleccion(df2,k,independientes,dependiente,max_fe):
    # Entrenamiento
    Xtodos_train, Xtodos_test, ytodos_train, ytodos_test=Entrenamiento(df2,independientes,dependiente,0.2)
    # Escala
    Xtodos_train, Xtodos_test,scl3 =Escalas(Xtodos_train, Xtodos_test)
    # Random Forest
    rforest1,y_pred43=RForest(Xtodos_train,Xtodos_test,ytodos_train,ytodos_test,k,max_fe)
    print("El método de Random Forest se ha ejecutado con éxito. Se procederá a guardar los resultados.")
    return scl3,ytodos_test,y_pred43,rforest1

def XGB(Xtrain,Xtest,ytrain,ytest,k):
    xg=xgb.XGBRegressor(objective="reg:squarederror",alpha=1)
    colsample= [0.4,0.6,0.8]
    lr=[0.05,0.1]
    max_d=[25,45,60,80]
    n_est=[400,550,700]
    params={"colsample_bytree":colsample,"learning_rate":lr,"max_depth":max_d,"n_estimators":n_est}
    search=GridSearchCV(estimator=xg,param_grid=params,n_jobs=-1)
    search_model=search.fit(Xtrain,ytrain)
    search_model.best_params_                    
    y_pred63 = cross_val_predict(search_model, Xtest, np.ravel(ytest), cv=k)
    return search_model,y_pred63

def XGB_Eleccion(df2,k,independientes,dependiente):
    # Entrenamientos
    Xtodos_train, Xtodos_test, ytodos_train, ytodos_test=Entrenamiento(df2,independientes,dependiente,0.2)
    # Escalas
    Xtodos_train, Xtodos_test,scl4 =Escalas(Xtodos_train, Xtodos_test)
    # XGBs
    xgb1,y_pred43=XGB(Xtodos_train,Xtodos_test,ytodos_train,ytodos_test,k)
    print("El método de Extreme Gradient Boosting se ha ejecutado con éxito. Se procederá a guardar los resultados.")
    return scl4,ytodos_test,y_pred43,xgb1

def GraEstModels(a,b,c,d):
    xvec=list(a)
    xvec2=list(c)
    for k in range(0,len(xvec2)):
        xvec.append(xvec2[k])
    xmin,xmax=min(xvec)-1,max(xvec)+1
    yvec=list(b)
    yvec2=list(d)
    for k in range(0,len(yvec2)):
        yvec.append(yvec2[k])
    ymin,ymax=min(yvec)-1,max(yvec)+1
    puntos=[]
    for j in range(xmin[0],xmax[0]+1,1):
        puntos.append(j)
    
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(14,8))
    axs[0].scatter(a,b,color="#008080");
    axs[0].scatter(puntos,puntos,color="red",linewidth=3.5)
    axs[0].set_xlabel('Valor Observado',size=12)
    axs[0].set_ylabel('Valor Estimado',size=12)
    axs[0].grid(True)
    axs[0].set_xlim(xmin,xmax)
    axs[0].set_ylim(ymin,ymax)
    axs[0].set_title('Random Forest', size= 16)

    axs[1].scatter(c,d,color="#008080");
    axs[1].scatter(puntos,puntos,color="red",linewidth=3.5)
    axs[1].set_xlabel('Valor Observado',size=12)
    axs[1].set_ylabel('Valor Estimado',size=12)
    axs[1].grid(True)
    axs[1].set_xlim(xmin,xmax)
    axs[1].set_ylim(ymin,ymax)
    axs[1].set_title('Extreme Grandient Boosting', size= 16)
    plt.show()



##################### PARTE 3 #########################

def InsertColumnasAVM(reavm):
    reavm.insert(reavm.shape[1],'% de error',
             100*(reavm.loc[:,'Estimación AVM']-reavm.loc[:,'valor_uf'])/reavm.loc[:,'valor_uf'],
             True)
    reavm.insert(reavm.shape[1],'error AVM',reavm['Estimación AVM']-reavm['valor_uf'],True)
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
    sns.scatterplot(data=reavm2,x='valor_uf',y='Estimación AVM',color="#008080")
    plt.plot(reavm2['valor_uf'],reavm2['valor_uf'],color="red")
    plt.plot(reavm2['valor_uf'],reavm2['valor_uf']*(1.05),color="blue")
    plt.plot(reavm2['valor_uf'],reavm2['valor_uf']*(0.95),color="blue")
    plt.plot(reavm2['valor_uf'],reavm2['valor_uf']*(1.2),color="orange")
    plt.plot(reavm2['valor_uf'],reavm2['valor_uf']*(0.8),color="orange")
    plt.legend(["Datos","Recta ajustada a los datos","Error del +5%","Error del -5%","Error del +20%","Error del -20%"],bbox_to_anchor=(1, 1), loc='upper left')
    plt.title("Datos estimados por el AVM",size=16)
    plt.xlabel('Valor Observado');
    plt.ylabel('Valor Estimado AVM');
    plt.grid(True)
    plt.show()
    
# Selección de datos del AVM para escalar
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
def Xtodos(remL,variable_est): # variable_est es la variable a predecir, debe ser un strin
    reL=remL.drop([variable_est],axis=1)
    Xtodos_b = np.array(reL)
    return Xtodos_b
def SCL_model(scl,Xtodos,modelo):
    Xtodos=scl.transform(Xtodos)
    ValEst_mod=modelo.predict(Xtodos)
    return ValEst_mod
def InsertColumnsML(reml2,ValEst_RF,ValEst_XGB,variable_est):
    reml2.insert(reml2.shape[1],'ValEst_RF',ValEst_RF,True)
    reml2.insert(reml2.shape[1],'ValEst_XGB',ValEst_XGB,True)
    reml2.insert(reml2.shape[1],'% de error RF',100*(reml2['ValEst_RF']-reml2[variable_est])/reml2[variable_est],True)
    reml2.insert(reml2.shape[1],'error RF',reml2['ValEst_RF']-reml2[variable_est],True)

    reml2.insert(reml2.shape[1],'% de error XGB',100*(reml2['ValEst_XGB']-reml2[variable_est])/reml2[variable_est],True)
    reml2.insert(reml2.shape[1],'error XGB',reml2['ValEst_XGB']-reml2[variable_est],True)
    return reml2

def Rend_Est_ML(reml2,variable_est,T):
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(14, 8))
    axs[0].scatter(reml2[variable_est],reml2['ValEst_RF'],color="#008080");
    axs[0].plot(reml2[variable_est],reml2[variable_est],color="red")
    if T==True:
        axs[0].plot(reml2[variable_est],reml2[variable_est]*(1.05),color="blue")
        axs[0].plot(reml2[variable_est],reml2[variable_est]*(0.95),color="blue")
        axs[0].plot(reml2[variable_est],reml2[variable_est]*(1.2),color="orange")
        axs[0].plot(reml2[variable_est],reml2[variable_est]*(0.8),color="orange")
    axs[0].set_xlabel('Valor Observado')
    axs[0].set_ylabel('Valor Estimado')
    axs[0].set_title('Random Forest')
    axs[0].grid(True)

    axs[1].scatter(reml2[variable_est],reml2['ValEst_XGB'],color="#008080");
    axs[1].plot(reml2[variable_est],reml2[variable_est],color="red")
    if T==True:
        axs[1].plot(reml2[variable_est],reml2[variable_est]*(1.05),color="blue")
        axs[1].plot(reml2[variable_est],reml2[variable_est]*(0.95),color="blue")
        axs[1].plot(reml2[variable_est],reml2[variable_est]*(1.2),color="orange")
        axs[1].plot(reml2[variable_est],reml2[variable_est]*(0.8),color="orange")
    axs[1].set_xlabel('Valor Observado')
    axs[1].set_ylabel('Valor Estimado')
    axs[1].set_title('Extreme Gradient Boosting')
    axs[1].grid(True)

    plt.show()
def Error_banos(reml2): ### MOD X TENER RL Y ENET
    real=reml2['nro_banos']
    estimado3=reml2['ValEst_RF']
    estimado4=reml2['ValEst_XGB']
    r3=estimado3-real;
    rr3=r3.tolist();
    r4=estimado4-real;
    rr4=r4.tolist();

    tabla= pd.DataFrame.from_dict({'Error de baños':[],
                                   '%_RF_Acumulado': [],'Cantidad_RF': [],
                                   '%_XGB_Acumulado': [],'Cantidad_XGB': []});

    col = ['Error de baños','%_RF_Acumulado','Cantidad_RF', "%_XGB_Acumulado",'Cantidad_XGB'];
    cant=[0,0]
    porc=[0,0]
    k=[0,1,2]
    for lim in range(0,len(k)):
        if k[lim]==0:
            inter=f"|Error| = 0 "
        else: 
            inter=f"|Error| = {k[lim]}"
        porcentaje3=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))/len(rr3)+porc[0]
        cantidad3=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr3))-cant[0]
        porcentaje4=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))/len(rr4)+porc[1]
        cantidad4=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), rr4))-cant[1]
        cant=[cant[0]+cantidad3,cant[1]+cantidad4]


        tablaux = pd.DataFrame([[inter,porcentaje3,cantidad3,porcentaje4,cantidad4]],
                                columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    inter=f"|Error|>=3"
    porcentaje3=100*(reml2.shape[0]-cant[0])/reml2.shape[0]+porcentaje3
    cantidad3=reml2.shape[0]-cant[0]
    porcentaje4=100*(reml2.shape[0]-cant[1])/reml2.shape[0]+porcentaje4
    cantidad4=reml2.shape[0]-cant[1]
    cant=[cant[0]+cantidad3,cant[1]+cantidad4]


    tablaux = pd.DataFrame([[inter,porcentaje3,cantidad3,porcentaje4,cantidad4]],
                            columns=col);
    tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

def Error_banos_DT(reml2): ##
    real=reml2['nro_banos']
    estimado=reml2['Val_Est_banos']
    errores=reml2['Error Baños']
    tabla= pd.DataFrame.from_dict({'Error de baños':[],
                                   '%Acumulado': [],'Cantidad estimada': []});

    col = ['Error de baños','%Acumulado','Cantidad estimada'];
    cant=[0]
    porc=[0]
    k=[0,1,2]
    for lim in range(0,len(k)):
        if k[lim]==0:
            inter=f"|Error| = 0"
        else: 
            inter=f"|Error| = {k[lim]}"
        porcentaje=100*sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), errores))/reml2.shape[0]+porc[0]
        cantidad=sum(map(lambda x : (x>=-k[lim]) & (x<=k[lim]), errores))-cant[0]
        cant=[cant[0]+cantidad]


        tablaux = pd.DataFrame([[inter,porcentaje,cantidad]],columns=col);
        tabla=pd.concat([tabla, tablaux],ignore_index=True);
    inter=f"|Error|>=3"
    porcentaje3=100*(reml2.shape[0]-cant[0])/reml2.shape[0]+porcentaje
    cantidad=reml2.shape[0]-cant[0]
    cant=[cant[0]+cantidad]


    tablaux = pd.DataFrame([[inter,porcentaje,cantidad]],columns=col);
    tabla=pd.concat([tabla, tablaux],ignore_index=True);
    return tabla

