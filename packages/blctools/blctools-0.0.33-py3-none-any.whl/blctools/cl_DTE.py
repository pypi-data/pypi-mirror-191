from . import dirs
from . import fechas

from .cl_ReporteBase import *
from .cl_BCRA import *

__all__ = ['DTE',]

class DTE(ReporteBase,BCRA):

    def __init__(
        self,
        fecha_i = fechas.hoy(),
        fecha_f = fechas.hoy(),
        cargar=False,
        descargar=False,
        dolarizar=None,
        periodo=None,
        filtro = 'ultimos',
        parques = [],
        tabla_datos = 'Q_RepItems',
        col_filtro = 'NEMO',
        dir_salida = dirs.raiz,
        ):

        dir_descarga, dir_extraccion = self.__elegir_dirs(filtro=None)

        ReporteBase.__init__(self,
            fecha_i = fecha_i,
            fecha_f = fecha_f,
            periodo=periodo,
            nemo_rpt = 'DTE_UNIF',
            nombre = 'DTE',
            formato_nombre_archivo = 'DTE%y%m',
            parques = parques,
            extension = 'mdb',
            tabla_datos = tabla_datos,
            tabla_fecha = 'VALORES_PERIODO',
            col_filtro = col_filtro,
            dir_salida = dir_salida,
            dir_descarga = dir_descarga,
            dir_extraccion = dir_extraccion,
            funcion_archivos_necesarios = fechas.iterar_mensual,
            valores_custom_filtro= {'finales':self.__filtrar_dtes_finales}
            )
        
        BCRA.__init__(self,
            cargar_tc = True,
            cargar_rem = False 
            )
        
        self.filtro = filtro
        self.dolarizar = dolarizar        

        if cargar:
            self.cargar(descargar=descargar,filtro=filtro,exportar_consulta=False,dolarizar=self.dolarizar)
            
        if not cargar and descargar:
            self.descargar(filtro=filtro)
        
    #--------------------------
    #
    #Fin de la función __init__
    #
    #--------------------------
    def __filtrar_dtes_finales(self,df):
        #Toma un dataframe resultante de la funcion cl_ApiCammesa.ApiCammesa.consultar()
        flt = df['titulo'].str.upper().str.startswith('DTE EMISIÓN 08/')
        return df[~flt]
    
    def __get_dirs(self,funcion):
        try:
            dir_descarga = funcion() + '\\00 ZIP'
        except: 
            dir_descarga = dirs.raiz + '\\00 ZIP'

        try:
            dir_extraccion = funcion() + '\\01 MDB'
        except:
            dir_extraccion = dirs.raiz + '\\01 MDB'
            
        return dir_descarga, dir_extraccion
    
    def __elegir_dirs(self,filtro=None):
        
        if filtro is None or filtro =='ultimos':
            dir_descarga, dir_extraccion = self.__get_dirs(dirs.get_dc_dte)
                    
        elif filtro == 'iniciales':
            dir_descarga, dir_extraccion = self.__get_dirs(dirs.get_dc_dtei)
                    
        elif filtro == 'finales':
            dir_descarga, dir_extraccion = self.__get_dirs(dirs.get_dc_dtef)
        else:
            dir_descarga    = dirs.raiz + '\\00 ZIP'
            dir_extraccion  = dirs.raiz + '\\01 MDB'
            
        return  dir_descarga, dir_extraccion
    
    @property
    def filtro(self):
        return self._filtro
    
    @filtro.setter
    def filtro(self,val):
        if val != False:
            self._filtro = self.check_filtro(val)
            self.dir_descarga, self.dir_extraccion = self.__elegir_dirs(self.filtro)
            self._actualizar_archivos()

    # Agregado de funcionalidades a funciones de la clase superior
    def consultar(self,exportar_consulta=False,dir_consulta=None,filtro=None):
        
        if filtro is not None:
            self.filtro = filtro
        
        ReporteBase.consultar(self,
            exportar_consulta=exportar_consulta,
            dir_consulta=dir_consulta,
            filtro=self.filtro
            ) 
    
    def descargar(self,exportar_consulta=False,dir_consulta=None,filtro=None):
        
        if filtro is not None:
            self.filtro = filtro
        
        ReporteBase.descargar(self,
            exportar_consulta=exportar_consulta,
            dir_consulta=dir_consulta,
            filtro=self.filtro
            ) 
        
    def cargar(self,descargar=False,filtro=None,exportar_consulta=False,dolarizar=None):
        
        if filtro is not None:
            self.filtro = filtro
        
        if dolarizar is not None:
            self.dolarizar = dolarizar
        
        ReporteBase.cargar(self,
            descargar=descargar,
            filtro=self.filtro,
            exportar_consulta=exportar_consulta
            )
        
        if isinstance(self.dolarizar,str):
            self.dolarizar = [self.dolarizar,]
        
        if isinstance(self.dolarizar,(list,tuple,set)):
            
            #Chequeo de columnas
            for col in self.dolarizar:
                if not isinstance(col,str):
                    raise TypeError(f'El parámetro "dolarizar" debe contenir una lista de strings, pero {col} es del tipo {type(col)}')
                
                if col not in self.datos.columns:
                    raise ValueError(f'No se encontró la columna {col} entre {self.datos.columns.to_list()}')
  
            #Chequeo de que se pudo cargar el tipo de cambio
            
            if self.tc_udh.empty:
                print('No se pudo cargar el Tipo de Cambio según la comunicación 3500 A del BRCRA.')
                self.tc_udh = None
            else:
                self.datos = (self.datos
                    .merge(
                        right=self.tc_udh, 
                        left_on='Fecha', 
                        right_index=True, 
                        how='left')
                    .assign(**{f'{c}_USD':lambda df_, c=c: df_[c].div(df_.TC) for c in self.dolarizar})
                    .rename(columns={c:f'{c}_ARS' for c in self.dolarizar})
                )
    
    def a_excel(self,descargar=False,filtro=None,exportar_consulta=False):
        
        if filtro is not None:
            self.filtro = filtro
        
        ReporteBase.a_excel(self,
            descargar=descargar,
            filtro=self.filtro,
            exportar_consulta=exportar_consulta
            )