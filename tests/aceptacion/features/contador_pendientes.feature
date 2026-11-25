# language: es
@PILOTO-4
Característica: Contador de tareas pendientes

  @PILOTO-4 @CA-1
  Escenario: CA-1 El contador inicial aparece bajo el formulario
    Dado la aplicación recién abierta con sus 3 tareas iniciales
    Cuando el usuario abre la aplicación
    Entonces hay exactamente un elemento visible con el texto "Pendientes: 2"
    Y ese elemento está situado bajo el formulario de alta

  @PILOTO-4 @CA-2
  Escenario: CA-2 Añadir una tarea actualiza el contador
    Dado la aplicación recién abierta con sus 3 tareas iniciales
    Cuando el usuario añade la tarea "Probar el contador" desde el formulario
    Entonces en menos de 1 segundo hay exactamente un elemento visible con el texto "Pendientes: 3"
    Y la lista muestra 4 tareas en el contador

  @PILOTO-4 @CA-3
  Escenario: CA-3 Dos altas seguidas actualizan el contador cada vez
    Dado la aplicación recién abierta con sus 3 tareas iniciales
    Cuando el usuario añade la tarea "Primera" desde el formulario
    Entonces en menos de 1 segundo hay exactamente un elemento visible con el texto "Pendientes: 3"
    Cuando el usuario añade la tarea "Segunda" desde el formulario
    Entonces en menos de 1 segundo hay exactamente un elemento visible con el texto "Pendientes: 4"
    Y la lista muestra 5 tareas en el contador

  @PILOTO-4 @CA-4
  Escenario: CA-4 Un título con HTML se muestra como texto literal
    Dado la aplicación recién abierta con sus 3 tareas iniciales
    Cuando el usuario añade la tarea "<b>negrita</b>" desde el formulario
    Entonces en menos de 1 segundo hay exactamente un elemento visible con el texto "Pendientes: 3"
    Y el título se muestra como texto literal "<b>negrita</b>"
    Y no hay ningún elemento b dentro de la lista
