var rutas = []
var select = document.getElementById("selectRuta"); 
var map = null
let almacenes = []
let markers = []
let directionsService = null
let directionsRenderer = null
var center = { lat: -13.5279763, lng: -71.9406047 }


gjson = data = JSON.parse(ser);
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
  obtenerRutas()
  initMap()
})

function initMap() {
  
  map = new google.maps.Map(document.getElementById('map-markers'), {
    zoom: 13,
    center: center
  });
  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();

  cargarAlmacenes()

  cargarGeoJson()

  select.addEventListener('change', (event) => {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
  });
  document.getElementById('map-markers').style.height = "80vh"
}
function cargarAlmacenes()
{
  almacenes = get_list(almacenes_list)
  for (alm of almacenes)
  {
    addMarker({lat:parseFloat(alm[1]), lng:parseFloat(alm[2])})
  }
}
function cargarGeoJson()
{
  directionsRenderer.setMap(null);

  map.data.addGeoJson(gjson)
  map.data.setStyle({  
    fillColor: "#CCCCCC"
  })
  map.setZoom(13)
  map.setCenter(center)
}

function hideMarkers() {
  setMapOnAll(null);
}
function showMarkers() {
  setMapOnAll(map);
}
function deleteMarkers() {
  hideMarkers();
  markers = [];
}
function addMarker(position) {
  const marker = new google.maps.Marker({
    position,
    map,
  });

  markers.push(marker);
}
function setMapOnAll(map) {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  directionsRenderer.setMap(map);
  map.data.setStyle({  
    fillColor: "#FFFFFF"
  })

  let index = parseInt(select.value, 10)
  const waypts = [];
  if(index == 0)
  {
    showMarkers()
    cargarGeoJson()
  }
  else{
    hideMarkers()
    index = index - 1
    test_rutas = ""
    for (let i = 1; i < rutas[index].length - 1; i++) {
      waypts.push({
        location: rutas[index][i],
        stopover: true,
      });
      test_rutas += rutas[index][i] + " | "
    }
    //console.log(rutas[index][0] + " | "+  test_rutas + rutas[index][(rutas[index].length-1)])
    directionsService
      .route({
        origin: rutas[index][0],
        destination: rutas[index][(rutas[index].length-1)],
        waypoints: waypts,
        optimizeWaypoints: false,
        travelMode: google.maps.TravelMode.DRIVING,
      })
      .then((response) => {
        directionsRenderer.setDirections(response);

        const route = response.routes[0];
      })
      .catch((e) => window.alert("Directions request failed due to " + status));
  }
}

function obtenerRutas()
{
  rutas_list = rutas_list.replace('[', '')
  rutas_list = rutas_list.replace(']', '')
  rutas_list = rutas_list.replace(/'/g, "")

  for (let ruta of rutas_list.split(", ")){
    ruta_info = ruta.split('()')
    ruta_limpia = []
    for (let r of ruta_info){
      ruta_limpia.push(r.replace(/@/g, ', '))
    }
    rutas.push(ruta_limpia);
  }

  // Agregar opciones
  var el = document.createElement("option")
  el.textContent = "Regiones de Voronoi"
  el.value = 0
  select.appendChild(el)

  for (let i = 0; i < rutas.length; i++){
    ruta_almacen = rutas[i][0];
    almacenes.push(rutas[i]);
    var el = document.createElement("option")
    el.textContent = ruta_almacen
    el.value = i+1
    select.appendChild(el)
  }
  //console.log(rutas)
}

function get_list(str)
{
  str = str.replace('[', '')
  str = str.replace(']', '')
  str = str.replace(/'/g, "")

  var lista = []
  for (let address of str.split(", ")){
    l = address.split('()')
    l[0] = l[0].replace(/@/g, ', ')
    lista.push(l)
  }
  return lista
}