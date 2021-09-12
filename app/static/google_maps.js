
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
  console.log("hola  munndo")
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
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  const waypts = [];
  const checkboxArray = document.getElementById("waypoints");
  
  rutas_list = rutas_list.replace('[', '')
  rutas_list = rutas_list.replace(']', '')
  rutas_list = rutas_list.replace(/'/g, "")

  for (let ruta of rutas_list.split(", ")){
    ruta_info = ruta.split('()')
    ruta_limpia = []
    for (let r of ruta_info){
      ruta_limpia.push(r.replace(/@/g, ', '))

    }
    console.log(ruta_limpia)
  }
}
