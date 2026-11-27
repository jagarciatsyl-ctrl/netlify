# language: es
Característica: Galería de imágenes
  Para ver varias imágenes de un vistazo y ampliar la que interese

  @PISCI-3 @CA-7
  Escenario: CA-7 La galería muestra 6 imágenes en cuadrícula con texto alternativo
    Dado que la página está abierta con una ventana de 1280 px de ancho
    Cuando la persona se desplaza hasta la sección con el título «Galería»
    Entonces ve 6 imágenes en cuadrícula de al menos 3 columnas, cada una con texto alternativo no vacío

  @PISCI-3 @CA-8
  Escenario: CA-8 Las 6 imágenes se cargan sin errores
    Dado que la página está abierta con una ventana de 1280 px de ancho y la sección «Galería» está visible
    Cuando la persona espera a que termine la carga de la página
    Entonces las 6 imágenes tienen ancho natural mayor que 0 y ninguna petición de imagen recibe un error

  @PISCI-3 @CA-9
  Escenario: CA-9 Al hacer clic en la primera imagen se amplía en una ventana superpuesta
    Dado que la sección «Galería» muestra las 6 imágenes
    Cuando la persona hace clic en la primera imagen
    Entonces ve una ventana superpuesta con la misma imagen a mayor tamaño y un botón «Cerrar»

  @PISCI-3 @CA-10
  Escenario: CA-10 El botón Cerrar cierra la ventana superpuesta
    Dado que una imagen está ampliada en la ventana superpuesta
    Cuando la persona hace clic en el botón «Cerrar»
    Entonces la ventana superpuesta desaparece y se ve la cuadrícula de 6 imágenes
