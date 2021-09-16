// Variables
let map;
let markers = [];
let autocomplete;
// variables json
pointgjson = data = JSON.parse(pointsSer);

$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initAutocomplete())
    google.maps.event.addDomListener(window, "load", initMap)
})

// iniciar autocompletado - sugerencias de busqueda
function initAutocomplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id-google-address'), {
      types: ['address'],
      componentRestrictions: {'country': ['pe']},
  })
}

function initMap() {
  // Crear mapa
  map = new google.maps.Map(document.getElementById('map-markers'), {
      zoom: 13,
      center: { lat: -13.5279763, lng: -71.9406047 }
  });

  // Este Listener llama a addMaker cuando el mapa es clickeado
  map.addListener("click", (event) => {
    // Esto permite añadir solo un marcador a la vez
    deleteMarkers()
    // añade marcador al mapa
    title = event.latLng.toJSON()["lat"] + "," + event.latLng.toJSON()["lng"]
    addMarker(event.latLng, title, true, true);
    document.getElementById('id-google-address').value = title
  });

  // carga los puntos guardados anteriormente
  cargarGJSON(map, pointgjson)

  // define la altura del mapa
  document.getElementById('map-markers').style.height = "80vh";
}

// cargar geojson en el mapa
function cargarGJSON(map, gjson) {
  try{
    map.data.addGeoJson(gjson)
  }catch (e){
    console.log("no se pudo cargar gjson" + e)
  }
}

// añadir marcador
function addMarker(position, title = "") {
  // crear maker
  const marker = new google.maps.Marker({
    position: position,
    map: map,
    title: title,
  });
  marker.setIcon("http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png")

  // añadir maker a makers - esto permite ocultar, mostrar o eliminar los marcadores
  markers.push(marker);
}

// Elmina todos los marcadores de makers removiendo referencias
function deleteMarkers() {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
}