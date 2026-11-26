"""Base smoke test of the pilot: the page is served and has its title and heading.
The tasks of the pilot add their own acceptance tests next to this one."""

from playwright.sync_api import expect


def test_la_pagina_se_sirve_con_su_titulo_y_su_encabezado(pagina):
    expect(pagina).to_have_title("Piscinas")
    expect(pagina.get_by_role("heading", level=1)).to_have_text("Piscinas")
