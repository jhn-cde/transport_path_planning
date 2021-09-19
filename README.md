# transport_path_planning
Planeamiento de rutas para el transporte de un sistema logístico

# Librerias usadas
```bash
## django
# django con conda (recomendado)
conda install -c anaconda django
# django con pip
pip install django
## geojson
pip install django-geojson
## fiona
pip install fiona
## geopandas
conda install geopandas
## goevoronoi
pip install geovoronoi
```

# Como usar
Para clonar y correr este repositorio necesitarás: Git, Python y Django<br>
Es recomendable usar anaconda <br>

Desde tu linea de comandos:<br>
```bash
# Clona este repositorio
git clone https://github.com/jhn-cde/transport_path_planning.git
# Ingresa a la carpeta principal
cd transport_path_planning
# makemigrations
python manage.py makemigrations
# migrate
python manage.py migrate
# Corre el servidor
python manage.py runserver
# Dentro de un navegador ingresa a 
# http://localhost:8000/app
```
