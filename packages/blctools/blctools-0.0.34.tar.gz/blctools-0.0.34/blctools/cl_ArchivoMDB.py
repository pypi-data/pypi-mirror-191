import pyodbc
import pandas as pd
from pathlib import Path

from . import dirs
from . import fechas

__all__ = ['ArchivoMDB',]


class ArchivoMDB():
    
    def __init__(self, archivo=None, abrir=True,consultas=None,tablas=None,mensajes=True):
        
        self.__ruta_archivo = None
        self.__archivo = None
        self.__conexion = None
        self.__cursor = None
        self.__tablas = None
        self.__datos = None
        
        if archivo is not None:
            self.archivo = dirs.check_archivo(archivo) 
            self.ruta_archivo = self.archivo.parent
    
            if abrir:
                
                if consultas is None and tablas is None:
                    self.abrir_archivo(mensajes=mensajes)
                    self.cerrar_archivo()
                elif consultas is not None:
                    tablas = None
                    self.ejecutar_consulta(consulta=consultas,cargar_tablas=True,mensajes=mensajes)
                elif tablas is not None:
                    self.consultar_tabla(tabla=tablas,cargar_tablas=True,mensajes=mensajes)
                else:
                    pass

    @property
    def ruta_archivo(self):
        return self.__ruta_archivo
    
    @ruta_archivo.setter
    def ruta_archivo(self,val):
        self.__ruta_archivo = val

    @property
    def archivo(self):
        return self.__archivo
    
    @archivo.setter
    def archivo(self,val):
        self.__archivo = val
    
    @property
    def conexion(self):
        return self.__conexion
    
    @conexion.setter
    def conexion(self,val):
        self.__conexion = val
    
    @property
    def cursor(self):
        return self.__cursor
    
    @cursor.setter
    def cursor(self,val):
        self.__cursor = val

    @property
    def tablas(self):
        return self.__tablas
    
    @tablas.setter
    def tablas(self,val):
        self.__tablas = val

    @property
    def datos(self):
        return self.__datos
    
    @datos.setter
    def datos(self,val):
        raise Exception('El atributo "datos" es de solo lectura.')
        
    def abrir_archivo(self,archivo=None,cargar_tablas=True,mensajes=False):
        
        if archivo is None:
            archivo = self.archivo
        else:
            archivo = dirs.check_archivo(archivo)
            
        if mensajes: print(f'Cargando .mdb en la memoria: {archivo}')
        #Preparando conexión con el archivo .mdb
        driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
        str_conexion = f"Driver={driver};DBQ={self.archivo};"
        
        self.conexion = pyodbc.connect(str_conexion)
        self.cursor = self.conexion.cursor()
        
        if cargar_tablas:
            self.tablas = (pd
                .DataFrame(
                    data = [tuple(x) for x in self.cursor.tables()],
                    columns = ['Catalog','Schema','Tabla','Tipo','Remarks']
                )
                .drop(columns = ['Catalog','Schema','Remarks'])
                .pipe(lambda adf: adf[adf.Tipo.ne('SYSTEM TABLE')])
                .reset_index(drop=True)
            )
        
    def cerrar_archivo(self):
        self.cursor.close()
        self.conexion.close()
    
    def __ejecutar_consulta(self,consulta):
        return pd.DataFrame(
            data = [tuple(x) for x in self.cursor.execute(consulta).fetchall()], 
            columns = [x[0] for x in self.cursor.description]
        )
        
    def ejecutar_consulta(self,consulta,cargar_tablas=False,mensajes=False,devolver=False):
        
        self.abrir_archivo(cargar_tablas=cargar_tablas,mensajes=mensajes)

        if isinstance(consulta,str):
            self.__datos = self.__ejecutar_consulta(consulta)
        
        elif isinstance(consulta,(tuple,list,set)):
            self.__datos = [self.__ejecutar_consulta(c) for c in consulta]
        else:
            raise Exception(f'Imposible preocesar la(s) consulta(s) {consulta}. Se esperaba un tipo de dato string, tuple, lista o set pero se recibió {type(consulta)}')

        self.cerrar_archivo()
        
        if devolver:
            return self.datos

    def consultar_tabla(self,tabla,cargar_tablas=False,mensajes=False,devolver=False):
        
        consultar = lambda x: self.ejecutar_consulta(
            consulta = f"SELECT * FROM {x};",
            cargar_tablas = cargar_tablas,
            mensajes = mensajes,
            devolver=True
        )
        
        if isinstance(tabla,str):
            self.__datos = consultar(tabla)
        elif isinstance(tabla,(list,tuple,set)):
            self.__datos = {t:consultar(t) for t in tabla}
        else:
            Exception(f'Imposible preocesar la(s) tabla(s) {tabla}. Se esperaba un tipo de dato string, tuple, lista o set pero se recibió {type(tabla)}')
            
        if devolver:
            return self.datos
            