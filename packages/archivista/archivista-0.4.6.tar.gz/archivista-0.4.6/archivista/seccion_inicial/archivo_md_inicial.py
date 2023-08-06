"""
Archivista, Sección Inicial, ArchivoMdInicial
"""
from pathlib import Path

METADATOS_VALIDOS = ["title", "summary", "category", "tags", "date", "modified", "status", "preview", "javascripts", "stylesheets"]


class ArchivoMdInicial:
    """Archivo md inicial"""

    def __init__(self, config, ruta, nivel):
        self.config = config
        if isinstance(ruta, str):
            self.ruta = Path(ruta)
        else:
            self.ruta = ruta
        self.nivel = nivel
        self.ya_alimentado = False
        self.archivo_md_nombre = None
        self.archivo_md_ruta = None
        self.ya_procesado = False
        self.procesado_contenido = ""
        self.procesado_metadatos = {}

    def alimentar(self):
        """Alimentar"""
        if self.ya_alimentado is False:
            # La ruta puede ser un directorio o el archivo md
            if self.ruta.exists() and self.ruta.is_dir():
                # La ruta es un directorio
                posible_nombre = self.ruta.parts[-1] + ".md"
                posible_ruta = Path(self.ruta, posible_nombre)
                if posible_ruta.exists() and posible_ruta.is_file():
                    self.archivo_md_nombre = posible_nombre
                    self.archivo_md_ruta = posible_ruta
            elif self.ruta.exists() and self.ruta.is_file():
                # La ruta es un archivo
                self.archivo_md_nombre = posible_nombre
                self.archivo_md_ruta = posible_ruta
            # Levantar bandera
            self.ya_alimentado = True
        # Entregar verdadero si hay
        return self.archivo_md_ruta is not None

    def procesar(self):
        """Procesar el archivo md para separar el contenido y los metadatos"""
        if self.ya_procesado is False:
            if self.ya_alimentado is False:
                self.alimentar()
            if self.archivo_md_ruta is not None:
                with open(str(self.archivo_md_ruta), "r", encoding="utf8") as puntero:
                    renglones = puntero.readlines()
                    for numero, linea in enumerate(renglones):
                        pareja = linea.split(":", 1)
                        if len(pareja) == 2 and pareja[0].lower() in METADATOS_VALIDOS:
                            variable = pareja[0].lower()
                            valor = pareja[1].strip()
                            self.procesado_metadatos[variable] = valor
                        else:
                            self.procesado_contenido = "".join(renglones[numero:])
                            break
            self.ya_procesado = True

    def contenido(self):
        """Contenido entrega texto markdown"""
        if self.ya_procesado is False:
            self.procesar()
        return self.procesado_contenido

    def metadatos(self):
        """Metadatos entrega un diccionario si los tiene"""
        if self.ya_procesado is False:
            self.procesar()
        return self.procesado_metadatos

    def __repr__(self):
        """Representación"""
        return "  " * self.nivel + f"<ArchivoMdInicial> {self.archivo_md_nombre}"
