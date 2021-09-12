
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
  var map = new google.maps.Map(document.getElementById('map-markers'), {
      zoom: 13,
      center: { lat: -13.5279763, lng: -71.9406047 }
  });
  
  address_list = address_list.replace('[', '')
  address_list = address_list.replace(']', '')
  address_list = address_list.replace(/'/g, "")

  for (let address of address_list.split(", ")){
    address_info = address.split('()')
    address_info[0] = address_info[0].replace(/@/g, ', ')

    new google.maps.Marker({
      position: {lat:parseFloat(address_info[1]), lng:parseFloat(address_info[2])},
      map,
      title: address_info[0],
    });
  }
  document.getElementById('map-markers').style.height = "80vh";
}