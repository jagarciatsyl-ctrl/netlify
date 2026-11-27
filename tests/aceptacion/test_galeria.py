"""PISCI-3: acceptance tests of the image gallery with an enlarge overlay."""

import pytest
from pytest_bdd import given, scenarios, then, when

scenarios("features/galeria.feature")

JS_IMGS = """() => {
  const h = [...document.querySelectorAll('h2')].find(x => x.textContent.trim() === 'Galería');
  if (!h) return null;
  const s = h.closest('section') || h.parentElement;
  return [...s.querySelectorAll('img')].filter(i => !i.closest('[role=dialog]'));
}"""

JS_GRID = """() => {
  const h = [...document.querySelectorAll('h2')].find(x => x.textContent.trim() === 'Galería');
  if (!h) return null;
  const s = h.closest('section') || h.parentElement;
  const imgs = [...s.querySelectorAll('img')].filter(i => !i.closest('[role=dialog]'));
  const cont = imgs.length ? imgs[0].parentElement : null;
  return {
    n: imgs.length,
    alts: imgs.map(i => (i.getAttribute('alt') || '').trim()),
    display: cont ? getComputedStyle(cont).display : null,
    pos: imgs.map(i => { const r = i.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y)]; }),
  };
}"""

JS_CARGA = """() => {
  const h = [...document.querySelectorAll('h2')].find(x => x.textContent.trim() === 'Galería');
  if (!h) return null;
  const s = h.closest('section') || h.parentElement;
  const imgs = [...s.querySelectorAll('img')].filter(i => !i.closest('[role=dialog]'));
  return imgs.map(i => i.complete && i.naturalWidth > 0);
}"""


@pytest.fixture
def ctx():
    return {"respuestas": []}


@pytest.fixture
def galeria(navegador, base_url, ctx):
    contexto = navegador.new_context(viewport={"width": 1280, "height": 800})
    p = contexto.new_page()
    p.on("response", lambda r: ctx["respuestas"].append(r))
    p.goto(base_url)
    yield p
    contexto.close()


def seccion(p):
    return p.locator("section").filter(
        has=p.get_by_role("heading", name="Galería", exact=True)
    )


def miniaturas(p):
    return seccion(p).locator("img:not([role=dialog] img)")


def visor(p):
    return p.get_by_role("dialog")


@given("que la página está abierta con una ventana de 1280 px de ancho")
def _abierta(galeria):
    pass


@given("que la página está abierta con una ventana de 1280 px de ancho y la sección «Galería» está visible")
def _abierta_visible(galeria):
    seccion(galeria).scroll_into_view_if_needed(timeout=3000)


@given("que la sección «Galería» muestra las 6 imágenes")
def _seis(galeria):
    seccion(galeria).scroll_into_view_if_needed(timeout=3000)
    assert miniaturas(galeria).count() == 6


@given("que una imagen está ampliada en la ventana superpuesta")
def _ampliada(galeria):
    seccion(galeria).scroll_into_view_if_needed(timeout=3000)
    miniaturas(galeria).first.click(timeout=3000)
    assert visor(galeria).is_visible()


@when("la persona se desplaza hasta la sección con el título «Galería»")
def _scroll(galeria):
    seccion(galeria).scroll_into_view_if_needed(timeout=3000)


@when("la persona espera a que termine la carga de la página")
def _espera(galeria):
    galeria.wait_for_load_state("load")


@when("la persona hace clic en la primera imagen")
def _clic_primera(galeria):
    miniaturas(galeria).first.click(timeout=3000)


@when("la persona hace clic en el botón «Cerrar»")
def _clic_cerrar(galeria):
    visor(galeria).get_by_role("button", name="Cerrar").click(timeout=3000)


@then("ve 6 imágenes en cuadrícula de al menos 3 columnas, cada una con texto alternativo no vacío")
def _check_grid(galeria):
    info = galeria.evaluate(JS_GRID)
    assert info is not None, "No existe la sección con título «Galería»"
    assert info["n"] == 6, f"Se esperaban 6 imágenes y hay {info['n']}"
    assert all(info["alts"]), f"Alt vacío en alguna imagen: {info['alts']}"
    assert info["display"] == "grid", f"La galería no es una cuadrícula: {info['display']}"
    columnas = 0
    for y in {p[1] for p in info["pos"]}:
        fila = {p[0] for p in info["pos"] if p[1] == y}
        columnas = max(columnas, len(fila))
    assert columnas >= 3, f"Menos de 3 columnas: {info['pos']}"
    assert all(m.is_visible() for m in miniaturas(galeria).all())


@then("las 6 imágenes tienen ancho natural mayor que 0 y ninguna petición de imagen recibe un error")
def _check_carga(galeria, ctx):
    assert seccion(galeria).count() == 1, "No existe la sección con título «Galería»"
    galeria.wait_for_load_state("networkidle")
    estado = galeria.evaluate(JS_CARGA)
    assert estado is not None, "No existe la sección con título «Galería»"
    assert len(estado) == 6, f"Se esperaban 6 imágenes y hay {len(estado)}"
    assert all(estado), f"Imágenes sin cargar: {estado}"
    errores = [
        (r.url, r.status)
        for r in ctx["respuestas"]
        if r.status >= 400 and r.request.resource_type == "image"
    ]
    assert not errores, f"Peticiones de imagen con error: {errores}"


@then("ve una ventana superpuesta con la misma imagen a mayor tamaño y un botón «Cerrar»")
def _check_visor(galeria):
    mini = miniaturas(galeria).first
    src, alt = mini.get_attribute("src"), mini.get_attribute("alt")
    ancho_mini = mini.bounding_box()["width"]
    v = visor(galeria)
    assert v.is_visible(), "No aparece la ventana superpuesta"
    grande = v.locator("img").first
    assert grande.get_attribute("src") == src
    assert grande.get_attribute("alt") == alt
    assert grande.bounding_box()["width"] > ancho_mini
    assert v.get_by_role("button", name="Cerrar").is_visible()


@then("la ventana superpuesta desaparece y se ve la cuadrícula de 6 imágenes")
def _check_cerrado(galeria):
    assert not visor(galeria).is_visible(), "La ventana superpuesta sigue visible"
    m = miniaturas(galeria)
    assert m.count() == 6
    assert all(i.is_visible() for i in m.all())
