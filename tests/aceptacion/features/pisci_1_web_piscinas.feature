# language: es
Característica: Web estática de piscinas
  Para conocer el negocio de piscinas, navegar por sus secciones y contactar por WhatsApp

  @PISCI-1 @CA-55
  Escenario: CA-55 El encabezado permanece fijo arriba al hacer scroll
    Dado que la página de piscinas está abierta en cualquier posición del scroll
    Cuando la persona se desplaza hacia abajo por la página
    Entonces el header sigue con su borde superior en y = 0 y contiene el logo, los menús y el botón WhatsApp

  @PISCI-1 @CA-56
  Escenario: CA-56 El logo del encabezado es una imagen a la izquierda de todo
    Dado que la página de piscinas se acaba de cargar
    Cuando se consulta el logo del encabezado
    Entonces es una imagen con id "logo", src "logo.svg" y alt "Logo Piscinas"
    Y su borde izquierdo queda a la izquierda de los tres menús y del botón WhatsApp

  @PISCI-1 @CA-57
  Escenario: CA-57 El splash contiene el h1 visible en la primera pantalla
    Dado que la página de piscinas se acaba de cargar sin hacer scroll
    Cuando la persona mira la primera pantalla
    Entonces el elemento splash contiene un único h1 con el texto "Sumérgete en tu mejor verano"
    Y ese h1 está completamente dentro de la ventana

  @PISCI-1 @CA-58
  Escenario: CA-58 Las secciones aparecen en orden con sus h2
    Dado que la página de piscinas se acaba de cargar sin hacer scroll
    Cuando la persona recorre la página hacia abajo tras el splash
    Entonces las secciones quienes-somos, servicios y contacto aparecen en ese orden con sus h2 "Quiénes somos", "Servicios" y "Contacto"

  @PISCI-1 @CA-59
  Escenario: CA-59 El menú Quiénes somos lleva a su sección
    Dado que la página de piscinas está abierta en cualquier posición del scroll
    Cuando la persona pulsa el menú "Quiénes somos" desde arriba, el medio y el fondo
    Entonces la página se desplaza hasta la sección "quienes-somos" con su h2 visible y por debajo del header

  @PISCI-1 @CA-60
  Escenario: CA-60 El menú Servicios lleva a su sección
    Dado que la página de piscinas está abierta en cualquier posición del scroll
    Cuando la persona pulsa el menú "Servicios" desde arriba, el medio y el fondo
    Entonces la página se desplaza hasta la sección "servicios" con su h2 visible y por debajo del header

  @PISCI-1 @CA-61
  Escenario: CA-61 El menú Contacto lleva a su sección
    Dado que la página de piscinas está abierta en cualquier posición del scroll
    Cuando la persona pulsa el menú "Contacto" desde arriba, el medio y el fondo
    Entonces la página se desplaza hasta la sección "contacto" con su h2 visible y por debajo del header

  @PISCI-1 @CA-62
  Escenario: CA-62 El botón WhatsApp abre el enlace en una pestaña nueva
    Dado que la página de piscinas está abierta en cualquier posición del scroll
    Cuando la persona pulsa el botón WhatsApp del encabezado
    Entonces se abre en una pestaña nueva el enlace "https://wa.me/34600000000" y el href del botón es exactamente ese valor

  @PISCI-1 @CA-63
  Escenario: CA-63 El pie de página tiene logo y enlaces de marcador
    Dado que la persona ha llegado al final de la página de piscinas
    Cuando mira el elemento footer
    Entonces está debajo de todas las secciones
    Y contiene la imagen "logo-pie" con el mismo src que el logo y alt "Logo Piscinas"
    Y contiene los enlaces "Privacidad", "Cookies" y "Legal" con href "#"

  @PISCI-1 @CA-64
  Escenario: CA-64 Los siete elementos tienen el fondo exacto
    Dado que la página de piscinas se acaba de cargar
    Cuando se consulta el color de fondo calculado de body, header, footer, splash, quienes-somos, servicios y contacto
    Entonces los siete tienen exactamente el valor "rgb(10, 26, 47)" y ninguno es transparente
