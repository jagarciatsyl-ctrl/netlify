# language: es
@PILOT-0
Característica: Lista de tareas (comportamiento base del piloto)

  @CA-1
  Escenario: La lista muestra las tareas iniciales
    Dado la aplicación abierta
    Entonces la lista muestra 3 tareas

  @CA-2
  Escenario: Añadir una tarea la deja pendiente al final de la lista
    Dado la aplicación abierta
    Cuando la persona añade la tarea "Probar el piloto"
    Entonces la lista muestra 4 tareas
    Y la última tarea es "Probar el piloto" con estado "Pendiente"
