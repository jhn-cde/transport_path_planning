// Variables
var markers = []
var rutas = []
var select = document.getElementById("selectRuta"); 
var map = null
let directionsService = null
let directionsRenderer = null
var center = { lat: -13.5279763, lng: -71.9406047 }

// parse variables serializadas a json
gjson = JSON.parse(ser);
tiegjson =  JSON.parse(tieSer);
almgjson =  JSON.parse(almSer);
rutasjson =  JSON.parse(rutasSer);

cargarOpciones()
// cargaropciones
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
  google.maps.event.addDomListener(window, "load", initMap)
})
function initMap() {
  // Iniciarlizar mapa
  map = new google.maps.Map(document.getElementById('map-markers'), {
    zoom: 13,
    center: center
  });
  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();

  // cargar almacenes y regiones
  cargarAlmacenes()
  cargarRegiones()

  // evento cambio de opcion select
  select.addEventListener('change', (event) => {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
  });

  // estilos: haltura 80vh
  document.getElementById('map-markers').style.height = "80vh"
}

// Agregar opciones en select
function cargarOpciones()
{
  // primera opcion - regiones de voronoi
  var el = document.createElement("option")
  el.textContent = "Regiones de Voronoi"
  el.value = 0
  select.appendChild(el)
  let i = 0
  // otras opciones - rutas
  for (var [k, v] of Object.entries(rutasjson))
  {
    rutas.push(v);
    var el = document.createElement("option")
    el.textContent = k
    el.value = i+1
    select.appendChild(el)
    i++
  }
}

// cargar almacenes
function cargarAlmacenes()
{
  cargarGJSON(map, almgjson)
  try{
    map.data.forEach(function (feature) {
      if (feature.getProperty("markermodel") == "Almacen") {
        LatLng = feature.getGeometry().get();
        var marker = new google.maps.Marker({
             position: LatLng,
             map: map,
             title: feature.getProperty("name")
        });
        markers.push(marker);
        map.data.remove(feature);
      }
    });
  }catch (e){
    console.log("no se pudo agregar titulo almacen" + e)
  }
}

// cargar regiones de voronoi
function cargarRegiones()
{
  // limpiar rutas
  directionsRenderer.setMap(null);

  //cargar regiones
  cargarGJSON(map, gjson)

  // aumentar sombreado
  map.data.setStyle({ fillColor: "#CCCCCC" })

  // reestablecer zoom y centro
  map.setZoom(13)
  map.setCenter(center)
}

// Mostrar ruta
function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  directionsRenderer.setMap(map);

  let index = parseInt(select.value, 10)
  const waypts = [];
  if(index == 0)
  {
    // mostrar almacenes y aumentar sombreado
    cargarRegiones()
    showMarkers()
  }
  else{
    // quitar sombreado
    map.data.setStyle({  
      fillColor: "#FFFFFF"
    })

    // añadir puntos intermedios
    index = index - 1
    for (let i = 1; i < rutas[index].length - 1; i++) {
      waypts.push({
        location: new google.maps.LatLng(rutas[index][i][1], rutas[index][i][0]),
        stopover: true,
      });
    }

    // ultimo elemento de lista
    l_val = rutas[index].length-1
    // añadir ruta
    directionsService
      .route({
        origin: new google.maps.LatLng(rutas[index][0][1], rutas[index][0][0]),
        destination: new google.maps.LatLng(rutas[index][l_val][1], rutas[index][l_val][0]),
        waypoints: waypts,
        optimizeWaypoints: false,
        travelMode: google.maps.TravelMode.WALKING,
      })
      .then((response) => {
        directionsRenderer.setDirections(response);
        const route = response.routes[0];
      })
      .catch((e) => console.log("Solicitud de direccion falló debido a " + e));
    
    hideMarkers()
  }
}

// carga geojson
function cargarGJSON(map, gjson)
{
  try{
    map.data.addGeoJson(gjson)
  }catch (e){
    console.log("no se pudo cargar gjson" + e)
  }
}

// asigna map a todos los markers
function setMapOnAll(map) {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Quita los markers del mapa pero no los borra
function hideMarkers() {
  setMapOnAll(null);
}

// Muestra los markers del array
function showMarkers() {
  setMapOnAll(map);
}

// Borra todos los markers del array
function deleteMarkers() {
  hideMarkers();
  markers = [];
}