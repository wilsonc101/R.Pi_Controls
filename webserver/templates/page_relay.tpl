<html>
<body>
  <head>
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>{{page_title}}</title>
  </head>


  <div id="relay_panel_outter">
  <div id="relay_panel_inner">
   <img src="images/relay_1.png" width="40" height=40"><br><br>
   <form action="/relayinput" method="POST" id="form1">
    <input type="hidden" name="relay" value="1">
    <input type="hidden" name="page" value="page_relay.html">
    <input type="radio" name="state" value="off" {{ 'checked' if relay_1 == "off" else "" }}> Off<br>
    <input type="radio" name="state" value="on" {{ 'checked' if relay_1 == "on" else "" }}> On<br>
   </form>

   <button type="submit" form="form1" value="Submit">RELAY 1</button>
  </div>

  <div id="relay_panel_inner">
   <img src="images/relay_2.png" width="40" height=40"><br><br>
   <form action="/relayinput" method="POST" id="form2">
    <input type="hidden" name="relay" value="2">
    <input type="hidden" name="page" value="page_relay.html">
    <input type="radio" name="state" value="off" {{ 'checked' if relay_2 == "off" else "" }}> Off<br>
    <input type="radio" name="state" value="on" {{ 'checked' if relay_2 == "on" else "" }}> On<br>
   </form>

   <button type="submit" form="form2" value="Submit">RELAY 2</button>
  </div>

  <div id="relay_panel_inner">
   <img src="images/relay_3.png" width="40" height=40"><br><br>
   <form action="/relayinput" method="POST" id="form3">
    <input type="hidden" name="relay" value="3">
    <input type="hidden" name="page" value="page_relay.html">
    <input type="radio" name="state" value="off" {{ 'checked' if relay_3 == "off" else "" }}> Off<br>
    <input type="radio" name="state" value="on" {{ 'checked' if relay_3 == "on" else "" }}> On<br>
   </form>

   <button type="submit" form="form3" value="Submit">RELAY 3</button>
  </div>

  <div id="relay_panel_inner">
   <img src="images/relay_4.png" width="40" height=40"><br><br>
   <form action="/relayinput" method="POST" id="form4">
    <input type="hidden" name="relay" value="4">
    <input type="hidden" name="page" value="page_relay.html">
    <input type="radio" name="state" value="off" {{ 'checked' if relay_4 == "off" else "" }}> Off<br>
    <input type="radio" name="state" value="on" {{ 'checked' if relay_4 == "on" else "" }}> On<br>
   </form>

   <button type="submit" form="form4" value="Submit">RELAY 4</button>
  </div>


  </div>

</body>
</html>