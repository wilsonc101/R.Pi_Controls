<html>
<body>
  <head>
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>{{page_title}}</title>
  </head>


  <form action="/relayinput" method="POST" id="states">
  <div id="relay_panel_outter">
  <div id="relay_panel_inner">
   <img src="images/relay_1.png" width="40" height=40"><br><br>
    <input type="hidden" name="relay" value="1">
    <input type="hidden" name="page" value="page_relay.html">
    <input type="radio" name="state_1" value="off" {{ 'checked' if relay_1 == "off" else "" }}> Off<br>
    <input type="radio" name="state_1" value="on" {{ 'checked' if relay_1 == "on" else "" }}> On<br>

  </div>

  <div id="relay_panel_inner">
   <img src="images/relay_2.png" width="40" height=40"><br><br>
    <input type="hidden" name="relay" value="2">
    <input type="hidden" name="page" value="page_relay.html">
    <input type="radio" name="state_2" value="off" {{ 'checked' if relay_2 == "off" else "" }}> Off<br>
    <input type="radio" name="state_2" value="on" {{ 'checked' if relay_2 == "on" else "" }}> On<br>
  </div>

  <div id="relay_panel_inner">
   <img src="images/relay_3.png" width="40" height=40"><br><br>
    <input type="hidden" name="relay" value="3">
    <input type="hidden" name="page" value="page_relay.html">
    <input type="radio" name="state_3" value="off" {{ 'checked' if relay_3 == "off" else "" }}> Off<br>
    <input type="radio" name="state_3" value="on" {{ 'checked' if relay_3 == "on" else "" }}> On<br>
  </div>

  <div id="relay_panel_inner">
   <img src="images/relay_4.png" width="40" height=40"><br><br>
    <input type="hidden" name="relay" value="4">
    <input type="hidden" name="page" value="page_relay.html">
    <input type="radio" name="state_4" value="off" {{ 'checked' if relay_4 == "off" else "" }}> Off<br>
    <input type="radio" name="state_4" value="on" {{ 'checked' if relay_4 == "on" else "" }}> On<br>
  </div>

  <div id="relay_panel_inner">
    <button type="submit" form="states" value="Submit">SET</button>
  </div>


  </div>
  </form>


</body>
</html>