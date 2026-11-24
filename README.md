# Piloto · lista de tareas

Proyecto piloto de Dorothy / Yellowway / Rubí. Una lista de tareas estática (HTML + JS, sin build) para
especificar y verificar funcionalidades sencillas.

- `web/`: la aplicación. Netlify publica este directorio.
- `tests/aceptacion/`: tests de aceptación en Gherkin (pytest-bdd + Playwright). Conjunto protegido.
- `.dorothy/proyecto.yaml`: ficha del proyecto para Dorothy.
- `.github/workflows/ci.yml`: secretos, tests y preview por pull request.

Ejecutar los tests en local:

```
pip install -r requirements-dev.txt
python -m playwright install chromium
pytest
```
