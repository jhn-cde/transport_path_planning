var rutas = []
var select = document.getElementById("selectRuta"); 
var map = null
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
  obtenerRutas()
  initMap()
})

function initMap() {
  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer();
  
  map = new google.maps.Map(document.getElementById('map-markers'), {
    zoom: 13,
    center: { lat: -13.5279763, lng: -71.9406047 }
  });
  cargarGeoJson()
  
  directionsRenderer.setMap(map);

  select.addEventListener('change', (event) => {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
  });
  document.getElementById('map-markers').style.height = "80vh"
}

function cargarGeoJson()
{
  try {
    map.data.addGeoJson(geojson);
  } catch (e) {
    alert("Not a GeoJSON file!");
  }
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  let index = parseInt(select.value, 10)
  const waypts = [];
  if(index == 0)
  {
    console.log("showkml")
  }
  else{
    index = index - 1
    test_rutas = ""
    for (let i = 1; i < rutas[index].length - 1; i++) {
      waypts.push({
        location: rutas[index][i],
        stopover: true,
      });
      test_rutas += rutas[index][i] + " | "
    }
    console.log(rutas[index][0] + " | "+  test_rutas + rutas[index][(rutas[index].length-1)])
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

function displayVoronoi()
{
  
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
    var el = document.createElement("option")
    el.textContent = ruta_almacen
    el.value = i+1
    select.appendChild(el)
  }
  console.log(rutas)
}

