

      function showPosition() {
          if(navigator.geolocation) {
              navigator.geolocation.getCurrentPosition(function(position) {
                console.log(position.coords.latitude)
                console.log(position.coords.longitude)
                const lat_1 = position.coords.latitude;
           	    const lon_2 = position.coords.longitude;
                  document.getElementById("lat_url_1").value = position.coords.latitude;
                  document.getElementById("long_url_2").value = position.coords.longitude;
              });
          } else {
              alert("Sorry, your browser does not support HTML5 geolocation.");
          }
          // return lat_1, lat_2;
      }

      showPosition()


      // console.log(lat_1)
      // console.log(lat_2)
