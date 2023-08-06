"""
Archivista, Config, Config
"""
import configparser
from pathlib import Path
import click
from archivista.universales.funciones import validar_rama

SETTINGS_INI = 'settings.ini'


class Config():
    """ Configuración """

    def __init__(self):
        self.rama = None
        self.almacen_frio_url = None
        self.nextcloud_ruta = None
        self.pelican_ruta = None
        self.plantillas_ruta = None
        self.plantilla = None
        self.titulo = None
        self.eliminar_content_rama = True
        self.fecha_por_defecto = '2020-01-01 00:00:00'
        self.breadcrumb = True
        self.descargables_extensiones = ['pdf', 'gz', 'zip']
        self.imagenes_extensiones = ['gif', 'jpg', 'jpeg', 'png', 'svg']
        self.indice_maximo_elementos_como_encabezado = 8
        self.insumos_ruta = None
        self.salida_ruta = None

    def obtener_ramas(self):
        """ Obtener las ramas configuradas en settings.ini """
        settings = configparser.ConfigParser()
        settings.read(SETTINGS_INI)
        return settings.sections()

    def cargar(self, rama):
        """ Cargar configuraciones en settings.ini """
        settings = configparser.ConfigParser()
        settings.read(SETTINGS_INI)
        self.rama = validar_rama(rama)
        if self.rama not in settings.sections():
            raise Exception(f'ERROR: No se encuentra la rama {self.rama} en settings.ini')
        if 'almacen_frio' in settings[self.rama]:
            self.almacen_frio_url = settings[self.rama]['almacen_frio']
        if 'nextcloud_ruta' in settings[self.rama]:
            self.nextcloud_ruta = settings[self.rama]['nextcloud_ruta']
        if 'pelican_ruta' in settings[self.rama]:
            self.pelican_ruta = settings[self.rama]['pelican_ruta']
        if 'plantillas_ruta' in settings[self.rama]:
            self.plantillas_ruta = settings[self.rama]['plantillas_ruta']
        if 'plantilla' in settings[self.rama]:
            self.plantilla = settings[self.rama]['plantilla']
        if 'titulo' in settings[self.rama]:
            self.titulo = settings[self.rama]['titulo']
        if 'eliminar_content_rama' in settings[self.rama]:
            self.eliminar_content_rama = settings[self.rama].getboolean('eliminar_content_rama')
        if 'fecha_por_defecto' in settings[self.rama]:
            self.fecha_por_defecto = settings[self.rama]['fecha_por_defecto']
        if 'breadcrumb' in settings[self.rama]:
            self.breadcrumb = settings[self.rama].getboolean('breadcrumb')
        if 'descargables_extensiones' in settings[self.rama]:
            self.descargables_extensiones = settings[self.rama]['descargables_extensiones'].split(',')
        if 'imagenes_extensiones' in settings[self.rama]:
            self.imagenes_extensiones = settings[self.rama]['imagenes_extensiones'].split(',')
        if 'indice_maximo_elementos_como_encabezado' in settings[self.rama]:
            self.indice_maximo_elementos_como_encabezado = int(settings[self.rama]['indice_maximo_elementos_como_encabezado'])

    def validar(self):
        """ Validar configuraciones """
        if self.almacen_frio_url is None:
            raise Exception('FALTA: Configurar almacen_frio en settings.ini')
        if self.nextcloud_ruta is None:
            raise Exception('FALTA: Configurar nextcloud_ruta en settings.ini')
        if self.pelican_ruta is None:
            raise Exception('FALTA: Configurar pelican_ruta en settings.ini')
        if self.plantillas_ruta is None:
            raise Exception('FALTA: Configurar plantillas_ruta en settings.ini')
        if self.plantilla is None:
            raise Exception('FALTA: Configurar plantilla en settings.ini')
        if self.titulo is None:
            raise Exception('FALTA: Configurar titulo en settings.ini')
        # Validar URL almacen_frio_url
        # Validar nextcloud_ruta
        self.nextcloud_ruta = Path(self.nextcloud_ruta)
        if not self.nextcloud_ruta.exists() or not self.nextcloud_ruta.is_dir():
            raise Exception('ERROR: No existe el directorio nextcloud_ruta')
        # Validar pelican_ruta
        self.pelican_ruta = Path(self.pelican_ruta)
        if not self.pelican_ruta.exists() or not self.pelican_ruta.is_dir():
            raise Exception('ERROR: No existe el directorio pelican_ruta')
        # Validar plantillas_ruta
        self.plantillas_ruta = Path(self.plantillas_ruta)
        if not self.plantillas_ruta.exists() or not self.plantillas_ruta.is_dir():
            raise Exception('ERROR: No existe el directorio plantillas_ruta')
        # Validar plantilla
        plantilla = Path(self.plantillas_ruta, self.plantilla)
        if not plantilla.exists() or not plantilla.is_file():
            raise Exception('ERROR: No existe el archivo plantilla')
        # Validar insumos_ruta
        self.insumos_ruta = Path(self.nextcloud_ruta, self.titulo)
        if not self.insumos_ruta.exists() or not self.insumos_ruta.is_dir():
            raise Exception('ERROR: No existe el directorio de insumos {}'.format(str(self.insumos_ruta)))
        # Validar salida_ruta
        self.salida_ruta = Path(self.pelican_ruta, 'content')
        if not self.salida_ruta.exists() or not self.salida_ruta.is_dir():
            raise Exception('ERROR: No existe el directorio content {}'.format(str(self.salida_ruta)))


pass_config = click.make_pass_decorator(Config, ensure=True)
