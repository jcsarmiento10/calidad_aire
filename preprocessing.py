# Santi
import pandas as pd
import numpy as np
import time

def read_data(filename = 'DATOS_DE_CALIDAD_DEL_AIRE_EN_COLOMBIA_2011-2017.csv'):
    print('> Reading data...')
    t0 = time.time()
    datos = pd.read_csv(filename, usecols = ['Fecha','Latitud','Longitud','Variable', 'Concentración', 'Unidades', 'Nombre de la estación', 'Tiempo de exposición'])
    print('> Read data in '+str(np.around(time.time()-t0, decimals = 3))+ ' seconds')
    #Filtra datos para quedarse solo con datos diarios
    datos = datos.loc[datos['Tiempo de exposición'] == 24]

    #Pasa las fechas de string a datetime
    datos.loc[:, 'Fecha'] = pd.to_datetime(datos['Fecha'])

    #Toma únicamente estaciones con número de días de mecición disponibles mayor a 500
    ser_avail_days = datos.groupby('Nombre de la estación').nunique()['Fecha']
    datos = datos.loc[datos.loc[:, 'Nombre de la estación'].isin(ser_avail_days[ser_avail_days.values >= 500].index), :]

    return datos


def df_variable(datos, key = 'PM10'):
    df = datos.loc[datos.Variable == key].copy()
    vars_to_drop = ['Tiempo de exposición', 'Unidades']
    df.drop(columns = vars_to_drop, axis = 'columns', inplace = True)
    fechas = list(pd.period_range(min(df.Fecha), max(df.Fecha), freq='D').values)
    samplingpoints = list(df.loc[:, 'Nombre de la estación'].unique())
    new_idx = []
    for sp in samplingpoints:
        for f in fechas:
            new_idx.append((sp, np.datetime64(f)))

    df.set_index(keys=['Nombre de la estación', 'Fecha'], inplace=True)
    df.sort_index(inplace=True)
    df = df.reindex(new_idx)
    #df['Concentración'] = df.groupby(level=0)['Concentración'].bfill().fillna(0)
    df = df.groupby(level=0).bfill().fillna(0)
    return df   

#data = read_data()
#df_variable = df_variable(data)
