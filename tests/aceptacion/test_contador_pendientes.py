"""Step definitions for contador_pendientes.feature. PROTECTED SET: only Espantapájaros may change this file."""

from urllib.parse import urlparse

from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("features/contador_pendientes.feature")


def _contador(pagina, texto):
    return pagina.get_by_text(texto, exact=True)


@given("la aplicación recién abierta con sus 3 tareas iniciales")
def _inicial(pagina):
    assert pagina.title() == "Tareas"
    assert pagina.locator("#lista li").count() == 3


@when("el usuario abre la aplicación")
def _abre(pagina):
    pass  # the fixture already opened it; no reload allowed


@when(parsers.parse('el usuario añade la tarea "{titulo}" desde el formulario'))
def _anadir(pagina, titulo):
    pagina.fill("#titulo", titulo)
    pagina.click("text=Añadir")


@then(parsers.parse('hay exactamente un elemento visible con el texto "{texto}"'))
def _uno_visible(pagina, texto):
    loc = _contador(pagina, texto)
    assert loc.count() == 1
    assert loc.is_visible()


@then(parsers.parse('en menos de 1 segundo hay exactamente un elemento visible con el texto "{texto}"'))
def _uno_visible_rapido(pagina, texto):
    loc = _contador(pagina, texto)
    expect(loc).to_have_count(1, timeout=1000)
    expect(loc).to_be_visible(timeout=1000)


@then("ese elemento está situado bajo el formulario de alta")
def _bajo_form(pagina):
    caja = _contador(pagina, "Pendientes: 2").bounding_box()
    form = pagina.locator("form#nueva").bounding_box()
    assert caja is not None
    assert caja["y"] >= form["y"] + form["height"] - 1


@then(parsers.parse("la lista muestra {n:d} tareas en el contador"))
def _cuenta(pagina, n):
    expect(pagina.locator("#lista li")).to_have_count(n, timeout=1000)


@then(parsers.parse('el título se muestra como texto literal "{texto}"'))
def _literal(pagina, texto):
    ultimo = pagina.locator("#lista li").last
    assert ultimo.locator(".titulo").text_content() == texto


@then("no hay ningún elemento b dentro de la lista")
def _sin_b(pagina):
    assert pagina.locator("#lista b").count() == 0


def test_solo_recursos_locales(navegador, base_url):
    """Verification point 7: every request goes to the same origin as the app (web/ only)."""
    contexto = navegador.new_context()
    try:
        p = contexto.new_page()
        urls = []
        p.on("request", lambda r: urls.append(r.url))
        p.goto(base_url)
        p.wait_for_load_state("networkidle")
        origen = urlparse(base_url).netloc
        assert urls
        externas = [u for u in urls if urlparse(u).netloc != origen and not u.startswith("data:")]
        assert externas == []
    finally:
        contexto.close()
