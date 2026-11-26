# Piloto · web de piscinas

Proyecto piloto de Dorothy / Yellowway / Rubí. Una web estática (HTML, CSS y JS, sin build) sobre construcción
de piscinas: parte de una página mínima y cada funcionalidad la especifica el usuario y la construye el flujo.

- `web/`: la web. Netlify publica este directorio.
- `tests/aceptacion/`: tests de aceptación (pytest + Playwright). Conjunto protegido.
- `.dorothy/proyecto.yaml`: ficha del proyecto para Dorothy.
- `.github/workflows/ci.yml`: secretos, tests y preview por pull request.

Ejecutar los tests en local:

```
pip install -r requirements-dev.txt
python -m playwright install chromium
pytest
```
