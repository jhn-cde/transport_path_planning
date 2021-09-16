import requests
from urllib.parse import urlencode

# no views
def getlatlng(address, GOOGLE_API_KEY):
    # verificar si se tienen latlng
    tmp = address.split(",")
    try:
        lat = float(tmp[0])
        lng = float(tmp[1])
        return {"address":"" ,"lat":lat, "lng":lng}
    except Exception: # se tiene direccion
        try:
            # obtener latlng con la API de GOOGLE
            # paramteros
            data_type = 'json'
            endpoint = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/{data_type}"
            params = {"input":address.replace(', ', ',+'),
                "inputtype":"textquery", "fields":"formatted_address,name,rating,opening_hours,geometry",
                "key":GOOGLE_API_KEY}
            # juntar parametros
            url_params = urlencode(params)
            # generar url
            url = f"{endpoint}?{url_params}"
            # obtener informacion
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code not in range(200, 299):
                return {}
            # obtener latlng
            d = (response.json()['candidates'][0]["geometry"]['location'])
            d["address"] = address
            return d

        except (Exception):
            print("No se pudo obtener latlng", Exception)
            return {}

# Guardar modelo
def guardarObjeto(objeto, latlng, modelo):
    try:
        objeto.name = latlng['address']
        objeto.markermodel = modelo
        objeto.geom = {'type': 'Point', 'coordinates': [latlng["lng"], latlng["lat"]]}
        objeto.save()
    except Exception:
        print("No se pudo guardar el objeto2")

# obtener diccionario
def getDictCoords(json_dict):
    d = dict()
    for feature in json_dict["features"]:
        d[feature["properties"]["name"]] = feature["geometry"]["coordinates"]
    return d
    