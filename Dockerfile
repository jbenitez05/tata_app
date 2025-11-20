# Instrucciones para la generación de imagen docker 
# Crear la siguiente estructura de carpetas:
# 
# /tata
#    ├── Dockerfile
#    └── /py4web
#        └── /apps
#            └── /tata_app
#
# Para crear su imagen, ejecute: 
#
# ```
# docker build -t tata_app:latest .
# ```
#
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev build-essential && rm -rf /var/lib/apt/lists/*

COPY py4web /opt/py4web
RUN touch /opt/py4web/apps/__init__.py

RUN ln -s /opt/py4web/apps/tata_app /opt/py4web/apps/_default
RUN pip install --upgrade pip && pip install --no-cache-dir -r /opt/py4web/apps/tata_app/requirements.txt

EXPOSE 8000

CMD py4web run /opt/py4web/apps --watch off --port 8000 --host 0.0.0.0