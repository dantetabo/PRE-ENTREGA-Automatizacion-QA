# pre-entrega-automation-testing-dante

## Propósito
Automatizar flujos básicos de navegación en el sitio de pruebas [saucedemo.com] usando Selenium WebDriver y Pytest como práctica del curso de Automatización (pre-entrega).

## Tecnologías
- Python 3.8+
- Selenium
- pytest
- webdriver-manager (opcional, facilita la gestión del driver)
- pytest-html (para generar reporte HTML)

## Estructura del proyecto
```
pre-entrega-automation-testing-dante/
├─ tests/
│  └─ test_saucedemo.py
├─ utils/
│  └─ helpers.py
├─ conftest.py
├─ requirements.txt
├─ pytest.ini
├─ README.md
└─ reports/ (generado por las ejecuciones)
```

## Instalación de dependencias
Se recomienda crear un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate   # mac/linux
.venv\Scripts\activate    # windows (PowerShell use `.\.venv\Scripts\Activate.ps1`)
pip install -r requirements.txt
```

## Ejecutar las pruebas
Para ejecutar todos los tests y generar un reporte HTML:
```bash
pytest -v --html=reports/reporte.html
```
Comando solicitado en la consigna:
```bash
pytest pre-entrega-final/test_saucedemo.py -v --html=reporte.html
```
(Nota: en este repositorio el archivo se encuentra en `tests/test_saucedemo.py`, adapte la ruta si suben a `pre-entrega-final/`.)

## Notas importantes
- Los tests usan `webdriver-manager` para obtener automáticamente el binary de ChromeDriver. Si preferís usar geckodriver o un driver local, cambiad la fixture en `conftest.py`.
- Si querés ejecutar los tests en modo no-headless (ver el navegador), comentar la opción `headless` en `conftest.py`.
- En caso de falla, se captura una captura de pantalla automática y se guarda en `reports/` con timestamp.
- Realizá commits frecuentes y con mensajes descriptivos, por ejemplo:
  - `init: project skeleton`
  - `feat(tests): add login test with explicit waits`
  - `test: add cart interaction test`
  - `chore: add pytest config and requirements`
