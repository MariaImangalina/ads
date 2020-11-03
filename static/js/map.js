
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
    polygonCoordinates = layer._latlngs;
    console.log(polygonCoordinates);

  }

  editableLayers.addLayer(layer);
});

  mymap.addEventListener('draw:created', function openForm() {
    document.getElementById("polygon_form").style.display = "block";  
  });

// popup window

function closeForm() {
    document.getElementById("polygon_form").style.display = "none";
  };

// ajax request

  pol_form = document.getElementById("polygon_form");
  pol_form.addEventListener('submit', (e) => {
    e.preventDefault()
    console.log('submitted')

    $.ajax({
      type: 'POST',
      url: "{% url 'add_polygon' %}",
      data: {
        'name': name.value,
        'coordinates': polygonCoordinates,
      },
      success: function(response) {
        console.log(response)
      },
      error: function(error) {
        console.log(error)
      },

    })
  })
