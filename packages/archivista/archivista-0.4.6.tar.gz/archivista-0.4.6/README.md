# Archivista

Transformador de contenidos a la estructura y metadatos que requiere **Pelican;**
así puede mantenerse un depósito _sencillo_ en la nube con directorios y archivos
para generar los directorios y archivos en _content_.

Ofrece la ventaja de determinar los metadatos a falta de éstos; por ejemplo,
si no se tiene un _Title_ se toma el nombre del archivo MD. También destaca por
crear índices _automáticos_ cuando se colocan documentos PDF o páginas MD en directorios.

Además identifica archivos _descargables_ como PDF, XLSX, DOCX, etc. El propósito de esto
es que el conjunto de páginas, imágenes y archivos web (JPG, PNG, GIF, etc.)
se suban a un servicio de hospedaje gratuito (por ejemplo GitHub) y lo más pesado
a un _almacén frío_ como **Google Storage**.

## Historial de versiones

- 0.4.6 Metadatos JavaScripts Stylesheets
- 0.4.5 Mejor configuración y breadcrumb se puede deshabilitar
- 0.4.4 Marca error si la rama no está configurada
- 0.4.3 Metadato "Preview" para imágenes previas de artículos
- 0.4.2 Cuando hay un elemento se omite el breadcrumb
- 0.4.1 Breadcrumb
- 0.3.8 Los subdirectorios con fecha la pueden tener en cualquier parte
- 0.3.7 Los subdirectorios con fecha se ordenan del más reciente al más pasado
- 0.3.6 Al crear los mensajes son cuantitativos
- 0.3.5 Orden ascendente en subdirectorios e índices
- 0.3.4 Descarta metadatos desconocidos en los archivos md
- 0.3.3 Ya no necesita el archivo CSV, ahora puede obtener metadatos de los archivos md; también algunas configuraciones son opcionales
- 0.3.2 Comando con dos órdenes (mostrar y crear) y puede eliminar lo previo en content
- 0.3.1 Configuración en un archivo externo settings.ini
- 0.2.0 Obtener los metadatos desde un archivo CSV
- 0.1.0 Primeros experimentos

## Configuración

Debe crear un archivo `settings.ini` con las opciones

- almacen_frio: La ruta al depósito Google Storage donde van a estar los archivos descargables
- descargables_extensiones:
- eliminar_content_rama:
- fecha_por_defecto:
- imagenes_extensiones:
- indice_maximo_elementos_como_encabezado:
- nextcloud_ruta:
