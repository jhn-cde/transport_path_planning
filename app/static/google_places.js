let map;
let markers = [];
let agregar = [];
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places") 
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", initAutocomplete())
    google.maps.event.addDomListener(window, "load", initMap)
})

let autocomplete;

function initAutocomplete() {

  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id-google-address'),
    {
      types: ['address'],
      componentRestrictions: {'country': ['pe']},
  })
}

function initMap() {
  map = new google.maps.Map(document.getElementById('map-markers'), {
      zoom: 13,
      center: { lat: -13.5279763, lng: -71.9406047 }
  });
  // This event listener will call addMarker() when the map is clicked.
  map.addListener("click", (event) => {
    deleteMarkers(agregar)
    title = event.latLng.toJSON()["lat"] + "," + event.latLng.toJSON()["lng"]
    addMarker(event.latLng, title, true, true);
    document.getElementById('id-google-address').value = title
  });

  addKnownMarkers()

  document.getElementById('map-markers').style.height = "80vh";
}

function addKnownMarkers()
{
  address_list = address_list.replace('[', '')
  address_list = address_list.replace(']', '')
  address_list = address_list.replace(/'/g, "")

  for (let address of address_list.split(", ")){
    address_info = address.split('()')
    address_info[0] = address_info[0].replace(/@/g, ', ')

    position =  {lat:parseFloat(address_info[1]), lng:parseFloat(address_info[2])}
    title = address_info[0]

    addMarker(position, title)
  }
}

function addMarker(position, title = "", seticon = false, nuevo_marker = false) {

  const marker = new google.maps.Marker({
    position: position,
    map: map,
    title: title,
  });
  if (seticon)
  {
    marker.setIcon("http://maps.google.com/mapfiles/kml/paddle/grn-blank.png")
  }
  if (nuevo_marker)
  {
    agregar.push(marker);
  }
  else{
    markers.push(marker);
  }
}

// Sets the map on all markers in the array.
function setMapOnAll(map, markers_list) {
  for (let i = 0; i < markers_list.length; i++) {
    markers_list[i].setMap(map);
  }
}
// Removes the markers from the map, but keeps them in the array.
function hideMarkers(markers_list) {
  setMapOnAll(null, markers_list);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers(markers_list) {
  hideMarkers(markers_list);
  markers_list = [];
}