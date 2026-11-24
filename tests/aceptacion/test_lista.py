"""Step definitions for lista.feature. PROTECTED SET: only Espantapájaros may change this file."""

from pytest_bdd import given, parsers, scenarios, then, when

scenarios("features/lista.feature")


@given("la aplicación abierta")
def _abierta(pagina):
    assert pagina.title() == "Tareas"


@when(parsers.parse('la persona añade la tarea "{titulo}"'))
def _anadir(pagina, titulo):
    pagina.fill("#titulo", titulo)
    pagina.click("text=Añadir")


@then(parsers.parse("la lista muestra {n:d} tareas"))
def _cuenta(pagina, n):
    assert pagina.locator("#lista li").count() == n


@then(parsers.parse('la última tarea es "{titulo}" con estado "{estado}"'))
def _ultima(pagina, titulo, estado):
    ultima = pagina.locator("#lista li").last
    assert ultima.locator(".titulo").inner_text() == titulo
    assert ultima.get_attribute("data-estado") == estado
