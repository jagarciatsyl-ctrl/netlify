"""Acceptance-test fixtures. PROTECTED SET: only Espantapájaros may change this file.

By default the tests serve ./web locally; set BASE_URL to run them against a preview instead.
"""

import functools
import http.server
import os
import threading
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

WEB = Path(__file__).resolve().parents[2] / "web"


@pytest.fixture(scope="session")
def base_url():
    externa = os.environ.get("BASE_URL")
    if externa:
        yield externa.rstrip("/")
        return
    manejador = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(WEB))
    manejador.log_message = lambda *a, **k: None
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), manejador)
    hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
    hilo.start()
    yield f"http://127.0.0.1:{servidor.server_address[1]}"
    servidor.shutdown()


@pytest.fixture(scope="session")
def navegador():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture
def pagina(navegador, base_url):
    contexto = navegador.new_context()
    p = contexto.new_page()
    p.goto(base_url)
    yield p
    contexto.close()
