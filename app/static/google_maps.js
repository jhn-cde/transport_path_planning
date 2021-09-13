var rutas = []
var select = document.getElementById("selectRuta"); 

$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
  obtenerRutas()
  initMap()
})

function initMap() {
  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer();
  var map = new google.maps.Map(document.getElementById('map-markers'), {
    zoom: 13,
    center: { lat: -13.5279763, lng: -71.9406047 }
  });

  directionsRenderer.setMap(map);
  
  calculateAndDisplayRoute(directionsService, directionsRenderer);

  select.addEventListener('change', (event) => {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
  });
  document.getElementById('map-markers').style.height = "80vh"
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  let index = parseInt(select.value, 10)
  const waypts = [];

  for (let i = 1; i < rutas[index].length - 1; i++) {
    waypts.push({
      location: rutas[index][i],
      stopover: true,
    });
  }
  console.log(rutas[index][0] + " | "+ waypts + " | " + rutas[index][(rutas[index].length-1)])
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

  for (let i = 0; i < rutas.length; i++){
    ruta_almacen = rutas[i][0];
    var el = document.createElement("option")
    el.textContent = ruta_almacen
    el.value = i
    select.appendChild(el)
  }
}

