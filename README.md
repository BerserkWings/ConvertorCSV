# ConvertorCSV
Esta es una herramienta que procesa datos predeterminados de archivos Fortinet, para convertirlos en archivos CSV, de acuerdo a las opciones que indique el programa.

El programa esta hecho unicamente para aceptar archivos Fortinet, que incluyen ciertos conjuntos de datos, por ejemplo:

```shell
edit "IP_10.10.10.10"
  set uuid asdasdas-asdasdasd-asdasdasd-asdasda
  set subnet 10.10.10.10 255.255.255.255
  set comment "Esto es un comentario"
next

edit "IP_10.10.10.11"
  set uuid asdasdas-asdasdasd-asdasdasd-asdasda
  set subnet 10.10.10.11 255.255.255.0
next

edit "sitioWeb.com"
  set type fqdn
  set comment "Comentario del fqdn"
  set fqdn "sitioWeb.com"
next
```

La idea es, obtener cualquiera de los datos que estan en los conjuntos de datos (salvo el "uuid"), para meterlos en forma de columnas dentro de un archivo CSV, con el fin de poder migrarlos a otro dispositivo Fortinet.

### Proceso de Obtención de Datos
El usuario debera escoger el archivo a tratar con el botón "Cargar archivo".

Despues, debe elegir la carpeta donde sera guardado el archivo con el botón "Guardar Archivo en".

Ahora el usuario, debera elegir los datos que se deberan buscar dentro de los conjuntos de datos que estan almacenados en el archivo cargado con el botón "Datos a buscar". Este botón va a desplegar las opciones que puede buscar el programa como lo son:
* edit -> Para obtener el dato entre parentesis
* fqdn -> Para obtener los datos que sean tipo fqdn, esta busqueda toma en cuenta que tengan el dato "set type fqdn" como una validación.
* ip-address -> Para obtener la IP que esta en el dato subnet
* subnet-mask -> Para obtener la mascara de red que esta en el dato subnet, unicamente toma en cuenta las que sean de 32 bits.
* subnet-mask(variado) -> Para obtener la mascara de red que esta en el dato subnet, pero que sea distinta a 32 bits
* color -> Esta opción agrega un color por defecto a los datos ingresados en el CSV, puedes cambiarlo desde el código, el color por defecto es "black".
* comments -> Para obtener los comentarios que estan entre parentesis dentro del dato comment, si no hay ningún comentario, se pondra una coma seguido de una cadena vacia.

Despues de esto, el usuario podra elegir que datos son los que quiere mostrar en el archivo CSV con el botón "Datos a mostrar". Este botón va a desplegar las opciones que se desean ser guardadas como lo son:
* edit
* fqdn
* ip-address
* subnet-mask
* color
* comments

Si el usuario se equivoca en alguna de las opciones que uso, puede usar el botón "Borrar opciones" que esta al inicio de cada etiqueta que almacena las opciones elegidas, para borrar todas las opciones que se eligieron y volver a escoger las que desea.

Por ultimo, el usuario dara al botón "Generar CSV" para asignarle el nombre al archivo CSV y con esto generara el archivo CSV esperado.

Este script puede ser modificado para que acepte más datos o tambien puedes cambiarlo para que analice archivos de otros dispositivos y que cumpla con sus conjuntos de datos.

### Errores
El programa puede que tenga un fallo en la obtención de datos, aunque es muy bajo, puede fallar en un 5% la obtención de los datos, por lo que se recomienda verificar que los datos obtenidos sean correctos.
El programa unicamente agiliza la obtención de estos datos.
Cuenta con algunos manejos de errores, estos son:
* Si el usuario no ha elegido un archivo a analizar o una carpeta donde se guardar el archivo CSV resultante, no procedera la busqueda de datos hasta que cumpla con estos requisitos.
* Si el usuario desea buscar el dato "FQDN", no puede usar las opciones "ip-address", "subnet-mask" y "subnet-mask(variado)", ya que el conjunto de datos que tenga un FQDN, no cuenta con estos datos especificos.
* Si ocurre un error inesperado random, el programa mostrara el tipo de error que este ocurriendo.
