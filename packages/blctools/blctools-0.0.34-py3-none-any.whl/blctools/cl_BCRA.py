import numpy as np
import pandas as pd
import datetime as dt

import requests
from bs4 import BeautifulSoup as bs

from . import fechas

__all__ = ['BCRA',]
class BCRA():

    def __init__(self,
        cargar_tc = True,
        cargar_tc_minorista = False,
        cargar_rem = True,):
        
        self.__rem = None
        self.__tc_dia = None
        self.__tc_udh = None
        self.__tc_rem = None
        self.__tc_min = None
        
        if cargar_tc:
            self.cargar_tc_ultimo_dia_habil(devolver=False)
            
        if cargar_rem:
            self.cargar_rem()
            
        if cargar_tc_minorista:
            self.cargar_tc_minorista()
    
    @property
    def rem(self):
        return self.__rem
     
    @rem.setter
    def rem(self,val):
        raise Exception('El atributo .rem es de sólo lectura')

    @property
    def tc_dia(self):
        return self.__tc_dia
    
    @tc_dia.setter
    def tc_dia(self,val):
        raise Exception('El atributo .tc_dia es de sólo lectura')
    
    @property
    def tc_udh(self):
        return self.__tc_udh
    
    @tc_udh.setter
    def tc_udh(self,val):
        raise Exception('El atributo .tc_udh es de sólo lectura')
    
    @property
    def tc_rem(self):
        return self.__tc_rem
    
    @tc_rem.setter
    def tc_rem(self,val):
        raise Exception('El atributo .tc_rem es de sólo lectura')

    @property
    def tc_min(self):
        return self.__tc_min
    
    @tc_min.setter
    def tc_min(self,val):
        raise Exception('El atributo .tc_min es de sólo lectura')
    
    #
    # Funciones destinadas al Tipo de Cambio
    #
    def cargar_tc_diario(self,devolver=False):

        if self.tc_dia is None:
            try:
                self.__tc_dia = (pd
                    .read_excel('https://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/com3500.xls')
                    .pipe( lambda df_: df_.drop(columns=df_.iloc[:,[0,1,4,5]].columns))
                    .set_axis(['Fecha','TC'],axis=1)
                    .dropna(axis=0)
                    .drop(index=2)
                    .assign(
                        Fecha = lambda df_: pd.to_datetime(df_.Fecha),
                        TC = lambda df_: df_.TC.astype('float64')
                    )
                    .set_index('Fecha')
                )
            except:
                print('No se pudo cargar el Tipo de Cambio según la comunicación 3500 A del BRCRA.')
                self.__tc_dia = (pd.DataFrame(
                    data= pd.Series(data=[],dtype='float64',name='TC'),
                    index= pd.DatetimeIndex(pd.to_datetime([]),name='Fecha'))
                )
        
        if devolver:
            return self.tc_dia

    def cargar_tc_ultimo_dia_habil(self,devolver=False):
        
        if self.tc_dia is None:
            self.cargar_tc_diario(devolver=False)
        
        if self.tc_udh is None:
            self.__tc_udh = (self.tc_dia
                .groupby([self.tc_dia.index.year,self.tc_dia.index.month])
                .max()
                .pipe(lambda adf: adf.set_index(
                    pd.DatetimeIndex(
                        data = (dt.date(year=y,month=m,day=1) for y,m in adf.index),
                        name='Fecha'))
                )
            )
            
        if devolver:
            return self.tc_udh

    def cargar_tc_minorista(self,devolver=False):
        
        try:
            self.__tc_min = (pd
                .read_html(
                    bs(requests
                        .get('https://www.bcra.gob.ar/publicacionesestadisticas/' + 
                            'Planilla_cierre_de_cotizaciones.asp?dato=1&moneda=2')
                        .text,
                        features="lxml"
                    )
                    .find('table')
                    .prettify()
                )
                [0]
                .droplevel(0,axis=1) 
                .assign(
                    Fecha = lambda adf: pd.to_datetime(adf.Fecha,format='%d-%m-%Y'),
                    Año = lambda adf: adf.Fecha.dt.year,
                    Mes = lambda adf: adf.Fecha.dt.month
                )
                .rename(columns={'Comprador':'Comp','Vendedor':'Vend'})
                .assign(**(
                    {c: lambda adf, c=c: adf[c].div(1000) for c in ['Comp','Vend']} |
                    {f'{c}_Var': lambda adf, c=c: adf[c].div(adf[c].shift(-1)).sub(1) for c in ['Comp','Vend']}
                    )
                )
                .loc[:,['Fecha','Año','Mes','Comp','Vend','Comp_Var','Vend_Var',]]
            )
        except:
                print('No se pudo cargar el Tipo de Cambio según la comunicación 3500 A del BRCRA.')
                self.__tc_dia = (pd.DataFrame(
                    columns = ['Año','Mes','Comp','Vend','Comp_Var','Vend_Var'],
                    index = pd.DatetimeIndex(pd.to_datetime([]),name='Fecha'))
                )

    #
    # Funciones destinadas al Relevamiento de Expectativas del Mercado (REM)
    #
    def __consultar_rem_crudo(self,fecha=None,n=5):
        
        if fecha is None:
            fecha = fechas.mes_ant_ult_dia()
        else:
            fecha = fechas.mes_ult_dia(fecha) 
        
        for dia in range(31,20,-1):
            try:
                fecha = fecha.replace(day=dia)
                self.__rem = (pd
                    .read_excel(f'https://www.bcra.gob.ar/Pdfs/PublicacionesEstadisticas/REM{fecha.strftime("%y%m%d")}%20Tablas%20web.xlsx')
                    .dropna(axis=0,how='all')
                    .dropna(axis=1,how='all')
                    .drop(index=0)
                    .iloc[:-1,:]
                    .reset_index(drop=True)
                    .assign(Fecha = fecha)
                )
                break
            except:
                if n >0:
                    continue
                else:
                    print(f'Imposible recuperar archivos para los últimos meses')
                    self.__rem = pd.DataFrame()
            
        if self.rem is None:
            print(f'No se encontraron archivos para el año {fecha.year} mes {fecha.month}')
            print(f'Se intentará con el mes anterior')
            
            fecha = fechas.mes_ult_dia(fechas.restar_mes(fecha))
            self.__consultar_rem_crudo(fecha,n=(n-1))

    def __preprocesar_rem_crudo(self,fecha=None):
        
        self.__rem = (self.__rem
            .assign(Tabla = pd.NA)
            .assign(Tabla = lambda df_: df_
                .Tabla
                .mask(
                    cond = (df_.iloc[:,0].notna() & df_.iloc[:,1].isna()),
                    other = df_.iloc[:,0])
                .replace({
                        'Precios minoristas (IPC nivel general-Nacional; INDEC)':'IPC_Minorista',
                        'Precios minoristas (IPC núcleo-Nacional; INDEC)':'IPC_Nucleo',
                        'Tasa de interés (BADLAR)':'Tasa_Interes',
                        'Tipo de cambio nominal':'TC',
                        'Resultado Primario del SPNF':'RP_SPNF',
                        'Desocupación abierta':'Desocupacion',
                        'PIB a precios constantes':'PIB'})
                .ffill()
            )
            .set_axis(
                axis=1,
                labels= ['Periodo','Referencia','Mediana','Promedio','Desvío','Máximo','Mínimo',
                        'Q90','Q75','Q25','Q10','Participantes','Fecha_REM','Tabla'],)
            .pipe(lambda df_: df_[df_.Referencia.notna() & df_.Periodo.ne('Período')])
            .assign(
                Periodo = lambda df_: df_.Periodo.apply(fechas.convertir_año_a_fecha),
                Unidad = lambda df_: df_.Tabla.map({
                    'IPC_Minorista':'%',
                    'IPC_Nucleo':'%',
                    'Tasa_Interes':'%',
                    'TC':'ARS/USD',
                    'Exportaciones':'M USD',
                    'Importaciones':'M USD',
                    'RP_SPNF':'kM USD',
                    'Desocupacion':'%',
                    'PIB':'%'}),
                Referencia = lambda df_: df_.Referencia
                    .replace({v:'' for v in ['TNA; %','$/US$',
                            'millones de US$','miles de millones $',]},regex=False)
                    .str.replace(r'var. % ','',regex=False)
                    .str.replace(r'TNA; %; ','',regex=False)
                    .str.replace(r'% de la ','',regex=False)
                    .str.replace(r'$/US$; ','',regex=False)
                    .replace('','mensual',regex = True)
                )
            .loc[:,['Fecha_REM','Tabla','Unidad','Periodo','Referencia',
                    'Mediana','Promedio','Desvío','Máximo','Mínimo',
                    'Q90','Q75','Q25','Q10','Participantes',]]
        )

    def __explotar_proyeccion(self,fila_ini,fila_fin,n):

        if n == 12:
            n = 6; k = 12
        else:
            n = 12; k = 24
        
        data = {
            'Fecha_REM': [fila_fin.Fecha_REM]*n,
            'Tabla': [fila_fin.Tabla]*n,
            'Unidad': [fila_fin.Unidad]*n,
            'Periodo': fechas.lista_mensual(fila_ini.Periodo, k)[(1 if n == 6 else 13):(7 if n == 6 else None)],
            'Referencia': [f'Proy {"12" if n == 6 else "24"} meses']*n,
        }

        if 'IPC' in fila_ini.Tabla:
            data |= {c: np.full(
                    shape=n, 
                    fill_value= (np.power((1+fila_fin[c]/100),1/12) -1)*100) 
                for c in fila_ini['Mediana':].index}
        else:
            data |= {c: np.linspace(
                    start= fila_ini[c],
                    stop = fila_fin[c],
                    num=n+1)[1:] 
                for c in fila_ini['Mediana':].index}
        
        return pd.DataFrame(data)

    def __explotar_proyecciones(self):
        
        #Explotar proyecciones 12 meses
        dfs_12 = []
        for i, fila in self.rem.query('Periodo == "próx. 12 meses"').iterrows():
            dfs_12.append(self.__explotar_proyeccion(
                fila_ini=self.rem.loc[i-1,:],
                fila_fin=fila,
                n=12))
        
        dfs_24 = []
        for i, fila in self.rem.query('Periodo == "próx. 24 meses"').iterrows():
            dfs_24.append(self.__explotar_proyeccion(
                fila_ini=self.rem.loc[i-8,:],
                fila_fin=fila,
                n=24))
        
        self.__rem = (pd
            .concat([self.rem,] + dfs_12 + dfs_24)
            .sort_values(by=['Fecha_REM','Tabla','Periodo'])
            .query('Periodo != "próx. 12 meses" & Periodo != "próx. 24 meses"')
            .reset_index(drop=True)
        )

    def cargar_rem(self,fecha=None,devolver=False):
        
        self.__consultar_rem_crudo(fecha=fecha)
        self.__preprocesar_rem_crudo()
        self.__explotar_proyecciones()
        
        self.__tc_rem = self.rem[self.rem.Tabla.eq('TC') & self.rem.Referencia.str.contains('mensual')]
        
        if devolver:
            return self.rem
