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
    <input type="radio" name="state" value="off" {{relay_1_off}}> Off<br>
    <input type="radio" name="state" value="on" {{relay_1_on}}> On<br>
   </form>

   <button type="submit" form="form1" value="Submit">RELAY 1</button>
  </div>

  <div id="relay_panel_inner">
   <img src="images/relay_2.png" width="40" height=40"><br><br>
   <form action="/relayinput" method="POST" id="form2">
    <input type="hidden" name="relay" value="2">
    <input type="hidden" name="page" value="page_relay.html">
    <input type="radio" name="state" value="off" {{relay_2_off}}> Off<br>
    <input type="radio" name="state" value="on" {{relay_2_on}}> On<br>
   </form>

   <button type="submit" form="form2" value="Submit">RELAY 2</button>
  </div>

  <div id="relay_panel_inner">
   <img src="images/relay_3.png" width="40" height=40"><br><br>
   <form action="/relayinput" method="POST" id="form3">
    <input type="hidden" name="relay" value="3">
    <input type="hidden" name="page" value="page_relay.html">
    <input type="radio" name="state" value="off" {{relay_3_off}}> Off<br>
    <input type="radio" name="state" value="on" {{relay_3_on}}> On<br>
   </form>

   <button type="submit" form="form3" value="Submit">RELAY 3</button>
  </div>

  <div id="relay_panel_inner">
   <img src="images/relay_4.png" width="40" height=40"><br><br>
   <form action="/relayinput" method="POST" id="form4">
    <input type="hidden" name="relay" value="4">
    <input type="hidden" name="page" value="page_relay.html">
    <input type="radio" name="state" value="off" {{relay_4_off}}> Off<br>
    <input type="radio" name="state" value="on" {{relay_4_on}}> On<br>
   </form>

   <button type="submit" form="form4" value="Submit">RELAY 4</button>
  </div>

  </div>

</body>
</html>