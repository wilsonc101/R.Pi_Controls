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
    <a href="graph/TC_internal"><img src="images/sensor_2.png" width="40" height=40"></a><br><br>
    TC Internal<br>
    {{ sensor_2 }}
  </div>

  <div id="relay_panel_inner">
    <a href="graph/TC_external"><img src="images/sensor_3.png" width="40" height=40"></a><br><br>
    TC External<br>
    {{ sensor_3 }}
  </div>

  <div id="relay_panel_inner">
    <img src="images/sensor_4.png" width="40" height=40"><br><br>
    Uptime
<pre><span style="font-size: 16px; font-family: Arial, Helvetica, sans-serif;">{{ sensor_4 }}</span></pre>
  </div>

 </div>


</body>
</html>
