<html>
<body>
  <head>
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>{{page_title}}</title>
  </head>

  Sensor Status<br><br>
 <div id="relay_panel_outter">
  <div id="relay_panel_inner">
    <img src="images/sensor_1.png" width="40" height=40"><br><br>
    Pi CPU<br>
    {{ sensor_1 }}
  </div>

  <div id="relay_panel_inner">
    <img src="images/sensor_2.png" width="40" height=40"><br><br>
    SENSOR 2<br>
    {{ sensor_2 }}
  </div>

  <div id="relay_panel_inner">
    <img src="images/sensor_3.png" width="40" height=40"><br><br>
    SENSOR 3<br>
    {{ sensor_3 }}
  </div>

  <div id="relay_panel_inner">
    <img src="images/sensor_4.png" width="40" height=40"><br><br>
    SENSOR 4<br>
    {{ sensor_4 }}
  </div>

 </div>


</body>
</html>
