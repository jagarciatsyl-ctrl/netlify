"""PISCI-1: acceptance tests of the static pool website served at /piscinas/."""

import time

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("features/pisci_1_web_piscinas.feature")

MENUS = ["Quiénes somos", "Servicios", "Contacto"]

JS_LINK_INFO = """([scope, texto]) => {
  const ambito = document.querySelector(scope);
  if (!ambito) return null;
  const a = [...ambito.querySelectorAll('a')].find(x => x.textContent.trim() === texto);
  if (!a) return null;
  return {left: a.getBoundingClientRect().left, href: a.getAttribute('href'),
          target: a.getAttribute('target')};
}"""

JS_HEADER = """() => {
  const h = document.querySelector('header');
  if (!h) return null;
  const txt = (t) => [...h.querySelectorAll('a')].some(a => a.textContent.trim() === t);
  return {top: h.getBoundingClientRect().top,
          logo: !!h.querySelector('img#logo'),
          menus: ['Quiénes somos', 'Servicios', 'Contacto'].every(txt),
          wa: txt('WhatsApp')};
}"""

JS_SECCION = """(id) => {
  const s = document.getElementById(id);
  const h = document.querySelector('header');
  if (!s || !h) return null;
  const h2 = s.querySelector('h2');
  if (!h2) return null;
  const a = h2.getBoundingClientRect();
  return {h2Top: a.top, h2Bottom: a.bottom, secTop: s.getBoundingClientRect().top,
          headerBottom: h.getBoundingClientRect().bottom, vh: window.innerHeight};
}"""


@pytest.fixture
def piscina(navegador, base_url):
    contexto = navegador.new_context(viewport={"width": 1280, "height": 720})
    p = contexto.new_page()
    p.goto(base_url + "/piscinas/")
    yield p
    contexto.close()


@pytest.fixture
def ctx():
    return {}


def estabilizar(p):
    anterior, estables = None, 0
    limite = time.time() + 5
    while estables < 5 and time.time() < limite:
        actual = p.evaluate("window.scrollY")
        estables = estables + 1 if actual == anterior else 0
        anterior = actual
        time.sleep(0.05)


def scroll_a(p, y):
    p.evaluate("(y) => window.scrollTo(0, y)", y)
    estabilizar(p)


def posiciones(p):
    maximo = p.evaluate("Math.max(0, document.documentElement.scrollHeight - window.innerHeight)")
    return [0, maximo / 2, maximo]


# ---------- Given ----------

@given("que la página de piscinas está abierta en cualquier posición del scroll")
@given("que la página de piscinas se acaba de cargar")
@given("que la página de piscinas se acaba de cargar sin hacer scroll")
def _abierta(piscina):
    assert piscina.evaluate("document.querySelector('header') !== null"), "la página /piscinas/ no tiene header"


@given("que la persona ha llegado al final de la página de piscinas")
def _final(piscina):
    scroll_a(piscina, piscina.evaluate("document.documentElement.scrollHeight"))


# ---------- CA-55 ----------

@when("la persona se desplaza hacia abajo por la página")
def _desplaza(piscina, ctx):
    ctx["headers"] = []
    for y in posiciones(piscina):
        scroll_a(piscina, y)
        ctx["headers"].append(piscina.evaluate(JS_HEADER))


@then("el header sigue con su borde superior en y = 0 y contiene el logo, los menús y el botón WhatsApp")
def _header_fijo(ctx):
    assert len(ctx["headers"]) == 3
    for h in ctx["headers"]:
        assert h is not None, "no existe el elemento header"
        assert h["top"] == 0, f"el header no está en y = 0: {h['top']}"
        assert h["logo"], "el header no contiene #logo"
        assert h["menus"], "el header no contiene los tres menús"
        assert h["wa"], "el header no contiene el botón WhatsApp"


# ---------- CA-56 ----------

@when("se consulta el logo del encabezado")
def _consulta_logo(piscina, ctx):
    ctx["logo"] = piscina.evaluate(
        """() => {
          const e = document.querySelector('header #logo');
          if (!e) return null;
          return {tag: e.tagName, id: e.id, src: e.getAttribute('src'), alt: e.getAttribute('alt'),
                  left: e.getBoundingClientRect().left};
        }"""
    )
    ctx["enlaces"] = {t: piscina.evaluate(JS_LINK_INFO, ["header", t]) for t in MENUS + ["WhatsApp"]}


@then(parsers.parse('es una imagen con id "{ident}", src "{src}" y alt "{alt}"'))
def _logo_attrs(ctx, ident, src, alt):
    logo = ctx["logo"]
    assert logo is not None, "no existe header #logo"
    assert logo["tag"] == "IMG"
    assert logo["id"] == ident
    assert logo["src"] is not None and logo["src"].split("/")[-1] == src, logo["src"]
    assert logo["alt"] == alt


@then("su borde izquierdo queda a la izquierda de los tres menús y del botón WhatsApp")
def _logo_izquierda(ctx):
    assert ctx["logo"] is not None, "no existe header #logo"
    for t, r in ctx["enlaces"].items():
        assert r is not None, f"falta el enlace {t} en el header"
        assert ctx["logo"]["left"] < r["left"], f"el logo no está a la izquierda de {t}"


# ---------- CA-57 ----------

@when("la persona mira la primera pantalla")
def _primera(piscina, ctx):
    ctx["splash"] = piscina.evaluate(
        """() => {
          const s = document.querySelector('#splash');
          if (!s) return null;
          const hs = [...s.querySelectorAll('h1')];
          const r = hs.length ? hs[0].getBoundingClientRect() : null;
          return {n: hs.length, texto: hs.length ? hs[0].textContent.trim() : null,
                  rect: r && {top: r.top, bottom: r.bottom, left: r.left, right: r.right},
                  w: window.innerWidth, h: window.innerHeight};
        }"""
    )


@then(parsers.parse('el elemento splash contiene un único h1 con el texto "{texto}"'))
def _splash_h1(ctx, texto):
    assert ctx["splash"] is not None, "no existe #splash"
    assert ctx["splash"]["n"] == 1
    assert ctx["splash"]["texto"] == texto


@then("ese h1 está completamente dentro de la ventana")
def _h1_dentro(ctx):
    s = ctx["splash"]
    assert s is not None and s["rect"] is not None, "no hay h1 en #splash"
    r = s["rect"]
    assert r["top"] >= 0 and r["left"] >= 0 and r["bottom"] <= s["h"] and r["right"] <= s["w"], r


# ---------- CA-58 ----------

@when("la persona recorre la página hacia abajo tras el splash")
def _recorre(piscina, ctx):
    ctx["secciones"] = piscina.evaluate(
        """() => ['quienes-somos', 'servicios', 'contacto'].map(id => {
          const s = document.getElementById(id);
          if (!s) return null;
          const h = s.querySelector('h2');
          return {id, top: s.offsetTop, h2: h ? h.textContent.trim() : null};
        })"""
    )


@then(
    parsers.parse(
        'las secciones quienes-somos, servicios y contacto aparecen en ese orden con sus h2 "{a}", "{b}" y "{c}"'
    )
)
def _orden(ctx, a, b, c):
    s = ctx["secciones"]
    assert all(x is not None for x in s), "falta alguna de las secciones"
    assert s[0]["top"] < s[1]["top"] < s[2]["top"], "las secciones no están en orden"
    assert [x["h2"] for x in s] == [a, b, c]


# ---------- CA-59 a CA-61 ----------

@when(parsers.parse('la persona pulsa el menú "{menu}" desde arriba, el medio y el fondo'))
def _pulsa_menu(piscina, ctx, menu):
    ctx["medidas"] = []
    for y in posiciones(piscina):
        scroll_a(piscina, y)
        enlace = piscina.locator("header a", has_text=menu)
        if enlace.count() < 1:
            ctx["medidas"].append(("sin_menu", None))
            continue
        enlace.first.click()
        estabilizar(piscina)
        ctx["medidas"].append(("ok", piscina.evaluate(JS_SECCION, ctx_ident(menu))))


def ctx_ident(menu):
    return {"Quiénes somos": "quienes-somos", "Servicios": "servicios", "Contacto": "contacto"}[menu]


@then(
    parsers.parse(
        'la página se desplaza hasta la sección "{ident}" con su h2 visible y por debajo del header'
    )
)
def _llega(ctx, ident):
    assert len(ctx["medidas"]) == 3
    for estado, m in ctx["medidas"]:
        assert estado == "ok", "no existe el menú en el header"
        assert m is not None, f"no existe #{ident} con h2 o no hay header"
        assert m["h2Top"] >= 0 and m["h2Bottom"] <= m["vh"], f"h2 fuera de la ventana: {m}"
        assert m["secTop"] >= m["headerBottom"], f"la sección queda bajo el header: {m}"


# ---------- CA-62 ----------

@when("la persona pulsa el botón WhatsApp del encabezado")
def _pulsa_wa(piscina, ctx):
    piscina.context.route(
        "https://wa.me/**", lambda r: r.fulfill(status=200, content_type="text/html", body="<html></html>")
    )
    ctx["wa"] = []
    for y in posiciones(piscina):
        scroll_a(piscina, y)
        info = piscina.evaluate(JS_LINK_INFO, ["header", "WhatsApp"])
        if info is None:
            ctx["wa"].append(None)
            continue
        with piscina.context.expect_page() as nueva:
            piscina.locator("header a", has_text="WhatsApp").first.click()
        popup = nueva.value
        popup.wait_for_load_state()
        info["popup_url"] = popup.url
        popup.close()
        ctx["wa"].append(info)


@then(
    parsers.parse(
        'se abre en una pestaña nueva el enlace "{url}" y el href del botón es exactamente ese valor'
    )
)
def _wa(ctx, url):
    assert len(ctx["wa"]) == 3
    for info in ctx["wa"]:
        assert info is not None, "no existe el botón WhatsApp en el header"
        assert info["href"] == url
        assert info["target"] == "_blank"
        assert info["popup_url"].startswith(url)


# ---------- CA-63 ----------

@when("mira el elemento footer")
def _mira_footer(piscina, ctx):
    ctx["footer"] = piscina.evaluate(
        """() => {
          const f = document.querySelector('footer');
          if (!f) return null;
          const pie = f.querySelector('img#logo-pie');
          const logo = document.querySelector('#logo');
          const links = {};
          for (const a of f.querySelectorAll('a')) links[a.textContent.trim()] = a.getAttribute('href');
          const ft = f.getBoundingClientRect().top + window.scrollY;
          const bajo = ['splash', 'quienes-somos', 'servicios', 'contacto'].map(id => {
            const s = document.getElementById(id);
            return s ? ft >= s.getBoundingClientRect().bottom + window.scrollY - 0.5 : false;
          });
          return {bajo,
                  pie: pie ? {src: pie.getAttribute('src'), alt: pie.getAttribute('alt')} : null,
                  logoSrc: logo ? logo.getAttribute('src') : null,
                  links};
        }"""
    )


@then("está debajo de todas las secciones")
def _footer_debajo(ctx):
    assert ctx["footer"] is not None, "no existe footer"
    assert all(ctx["footer"]["bajo"]), f"el footer no está debajo de todas las secciones: {ctx['footer']['bajo']}"


@then(parsers.parse('contiene la imagen "{ident}" con el mismo src que el logo y alt "{alt}"'))
def _footer_logo(ctx, ident, alt):
    f = ctx["footer"]
    assert f is not None and f["pie"] is not None, f"el footer no contiene #{ident}"
    assert f["logoSrc"] is not None and f["pie"]["src"] == f["logoSrc"]
    assert f["pie"]["alt"] == alt


@then(parsers.parse('contiene los enlaces "{a}", "{b}" y "{c}" con href "{href}"'))
def _footer_links(ctx, a, b, c, href):
    f = ctx["footer"]
    assert f is not None, "no existe footer"
    for t in (a, b, c):
        assert f["links"].get(t) == href, f"enlace {t} ausente o con href distinto"


# ---------- CA-64 ----------

@when(
    "se consulta el color de fondo calculado de body, header, footer, splash, quienes-somos, servicios y contacto"
)
def _fondos(piscina, ctx):
    ctx["fondos"] = piscina.evaluate(
        """() => ['body', 'header', 'footer', '#splash', '#quienes-somos', '#servicios', '#contacto'].map(sel => {
          const e = document.querySelector(sel);
          return [sel, e ? getComputedStyle(e).backgroundColor : null];
        })"""
    )


@then(parsers.parse('los siete tienen exactamente el valor "{valor}" y ninguno es transparente'))
def _fondos_ok(ctx, valor):
    assert len(ctx["fondos"]) == 7
    for sel, color in ctx["fondos"]:
        assert color is not None, f"no existe {sel}"
        assert color != "rgba(0, 0, 0, 0)", f"{sel} es transparente"
        assert color == valor, f"{sel}: {color}"
