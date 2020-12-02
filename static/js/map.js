
 // map display

var mymap = L.map('mapid').setView([55.7522200, 37.6155600], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoibWFyaWFpbWFuZ2FsaW5hIiwiYSI6ImNrZ3J4anNiaDA2YncydHA5dndlNGdld3gifQ.NrO6QfrsJEyB26UP8delaw'
}).addTo(mymap);


var editableLayers = new L.FeatureGroup();
mymap.addLayer(editableLayers);

var drawPluginOptions = {
  position: 'topright',
  draw: {

    polygon: {
      allowIntersection: false, // Restricts shapes to simple polygons
      drawError: {
        color: '#e1e100', // Color the shape will turn when intersects
        message: '<strong>Polygon draw does not allow intersections!<strong> (allowIntersection: false)' // Message that will show when intersect
      },
      shapeOptions: {
        color: '#bada55'
      }
    },

    polyline: false,
    circle: false,
    rectangle: false,
    marker: false,

  },
  edit: {
    featureGroup: editableLayers, //REQUIRED!!
    remove: false
  }
};


// Initialise the draw control and pass it the FeatureGroup of editable layers
var drawControl = new L.Control.Draw(drawPluginOptions);
mymap.addControl(drawControl);

var editableLayers = new L.FeatureGroup();
mymap.addLayer(editableLayers);


// Get coordinates from polygon
var polygonCoordinates
mymap.on('draw:created', function(e) {
  var type = e.layerType,
    layer = e.layer;

  if (type === 'polygon') {
    polygonCoordinates = layer._latlngs.toString();
    console.log(polygonCoordinates);

  }

  editableLayers.addLayer(layer);
});


// popup window

mymap.addEventListener('draw:created', function openForm() {
  document.getElementById("polygon_form").style.display = "block";  
});


function closeForm() {
    document.getElementById("polygon_form").style.display = "none";
  };

// ajax request

$('#polygon_form').on('submit', (e) => {
  e.preventDefault()
  console.log('submitted')
  url = '/data/map/'
  var csrf = document.getElementsByName('csrfmiddlewaretoken')

  $.ajax({
    type: 'POST',
    url: url,
    data: {
      name : id_name.value,
      csrfmiddlewaretoken : csrf[0].value,
      ads_type : id_ads_type.value, 
      min_area : id_min_area.value,
      max_area : id_max_area.value,
      coordinates: polygonCoordinates,
    },
    success: function(response) {
      alert('Полигон сохранен!');
      $('#pol_form')[0].reset();
      editableLayers.clearLayers()

    },
    error: function(error) {
      console.log(error)
    },
  });
});



$('td.is_paid').each(function(){
  if ($(this).text() == 'False') {
      $(this).css({'color':'red'})
  }
})
  

