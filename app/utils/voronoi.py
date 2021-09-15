from shapely import geometry
import geopandas as gpd
import pandas as pd
from shapely.ops import cascaded_union
from geovoronoi import voronoi_regions_from_coords, points_to_coords
from shapely.geometry import Point
import fiona
import random

class DiagramaVoronoi():
  def __init__(self, puntos):
    self.puntos = puntos        # coordenadas(matriz [n][2])
    self.region_polys = None    # diccionario de regiones de voronoi (poligonos shapely)
    self.region_pts = None      # diccionario de puntos y region a la que pertenecen
    self.distritos_cusco = None
    self.distritos_shape = None # util para gráficas
    self.coords = None          # util para gráficas
    self.iniciar()              # generara regiones

  def iniciar(self):
    # obtener poligonos shape
    self.distritos_shape = self.obtener_poligonos()

    # obtener coords
    self.coords = self.obtener_coords(self.puntos)

    # calcular las regiones de voronoi
    self.region_polys, self.region_pts = voronoi_regions_from_coords(self.coords, self.distritos_shape)

    self.guardar_regiones()

  def obtener_coords(self, puntos):
    # Preparar puntos
    df = pd.DataFrame({'lng':[v[0] for k,v in puntos.items()], 'lat':[v[1] for k,v in puntos.items()]})
    geo_puntos = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lng, df.lat))
    geo_puntos.crs = "EPSG:4326"
    
    # ajustar la informacion (CRS)
    gdf_proj = geo_puntos.to_crs(epsg=3395)

    # convertir datos a formato utilizable por geovoronoi
    coords = points_to_coords(gdf_proj.geometry)
    return coords

  def obtener_poligonos(self):
    # importar poligonos
    distritos = gpd.read_file('app/utils/distritos/DISTRITOS.shp')
    # separar distritos de Cusco
    for_drop = [i for i in range(1873)] # nro distritos en Perú
    for_drop.pop(535) # santiago
    for_drop.pop(537) # wanchaq
    for_drop.pop(1013) # San sebastian
    for_drop.pop(1049) # San jeronimo
    for_drop.pop(1080) # Cusco
    self.distritos_cusco = distritos.drop(for_drop, axis=0)
    # ajustar la informacion (CRS)
    self.distritos_cusco = self.distritos_cusco.to_crs(epsg=3395)
    # convertir datos a formato utilizable por geovoronoi
    distritos_shape = cascaded_union(self.distritos_cusco.geometry)
    return distritos_shape

  def guardar_regiones(self):
    # praparar shapes
    # convertir a diccionario
    mi_d = dict()
    mi_d["id"]=[]
    mi_d["geometry"] = []
    colores = []
    for k,pol in self.region_polys.items():
      mi_d["id"] += [k]
      colores += ["#"+str(random.randint(0, 999999)).zfill(6)]
      mi_d["geometry"] += [pol]
    # convertir a dataframe
    df = pd.DataFrame(mi_d)
    # convertir a geodataframe
    gdf = gpd.GeoDataFrame(df, geometry = df.geometry)
    # crs
    gdf.crs = "EPSG:3395"
    gdf = gdf.to_crs(epsg=4326)
    gdf['colour'] = colores
    # guardar
    gdf.to_file('app/static/regiones.geojson', driver='GeoJSON')

  def puntos_por_region(self, puntos, region):
    regiones = list(self.puntos.keys())
    coords = self.obtener_coords(puntos)
    almacen = regiones[self.region_pts[region][0]]
    puntos_region = [almacen]
    i = 0
    for k, v in puntos.items():
      punto = Point((coords[i][0], coords[i][1]))
      if (self.region_polys[region].contains(punto)):
        puntos_region.append(k)
      i+=1
    return puntos_region

def test():
  almacenes = {
      'alm1': [-71.993247,-13.525835],
      'alm2': [-71.968925,-13.517197],
      'alm3': [-71.966753,-13.531635],
      'alm4': [-71.939824,-13.527277],
      'alm5': [-71.915907,-13.531228],
      'alm6': [-71.887626,-13.546890]
  }
  voro = DiagramaVoronoi(almacenes)
  for k in voro.region_pts.keys():
    puntos_por_region = voro.puntos_por_region(almacenes, k)
    #print(puntos_por_region)

if __name__ == "__main__":
  test()