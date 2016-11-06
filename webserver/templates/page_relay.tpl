<html>
<body>
  <head>
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>{{page_title}}</title>
  </head>

  <form action="/relayinput" method="POST" id="states">
  <input type="hidden" name="page" value="page_relay.html">
  Current State<br><br>
  <div id="relay_panel_outter">
  <div id="relay_panel_inner">
    <img src="images/relay_1.png" width="40" height=40"><br><br>
    <input type="radio" name="state_1" value="off" {{ 'checked' if relay_1 == "off" else "" }}> Off<br>
    <input type="radio" name="state_1" value="on" {{ 'checked' if relay_1 == "on" else "" }}> On<br>
  </div>

  <div id="relay_panel_inner">
    <img src="images/relay_2.png" width="40" height=40"><br><br>
    <input type="radio" name="state_2" value="off" {{ 'checked' if relay_2 == "off" else "" }}> Off<br>
    <input type="radio" name="state_2" value="on" {{ 'checked' if relay_2 == "on" else "" }}> On<br>
  </div>

  <div id="relay_panel_inner">
    <img src="images/relay_3.png" width="40" height=40"><br><br>
    <input type="radio" name="state_3" value="off" {{ 'checked' if relay_3 == "off" else "" }}> Off<br>
    <input type="radio" name="state_3" value="on" {{ 'checked' if relay_3 == "on" else "" }}> On<br>
  </div>

  <div id="relay_panel_inner">
    <img src="images/relay_4.png" width="40" height=40"><br><br>
    <input type="radio" name="state_4" value="off" {{ 'checked' if relay_4 == "off" else "" }}> Off<br>
    <input type="radio" name="state_4" value="on" {{ 'checked' if relay_4 == "on" else "" }}> On<br>
  </div>

  <div id="relay_button_panel_inner">
    <button type="submit" class="relay_button" form="states" value="Submit">SET</button>
  </div>
  </div>
  </form>

  <hr>

  <form action="/scheduleinput" method="POST" id="schedule">
  <input type="hidden" name="page" value="page_relay.html">
  Current Schedule<br><br>
  <div id="relay_panel_outter">
  <div id="relay_panel_inner">

    <!-- 1 -->
    <div id="relay_schedule_panel_line_inner_title">
      On:
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=23 name="on_hour_1" value=0 class="time_input">
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=45 step=15 name="on_min_1" value=0 class="time_input">
    </div>

    <br><br><br>

    <div id="relay_schedule_panel_line_inner_title">
      Off:
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=23 name="off_hour_1" value=12 class="time_input">
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=45 step=15 name="off_min_1" value=0 class="time_input">
    </div>

  </div>

  <!-- 2 -->
  <div id="relay_panel_inner">

    <div id="relay_schedule_panel_line_inner_title">
      On:
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=23 name="on_hour_2" value=0 class="time_input">
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=45 step=15 name="on_min_2" value=0 class="time_input">
    </div>

    <br><br><br>

    <div id="relay_schedule_panel_line_inner_title">
      Off:
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=23 name="off_hour_2" value=12 class="time_input">
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=45 step=15 name="off_min_2" value=0 class="time_input">
    </div>

  </div>


  <!-- 3 -->
  <div id="relay_panel_inner">

    <div id="relay_schedule_panel_line_inner_title">
      On:
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=23 name="on_hour_3" value=0 class="time_input">
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=45 step=15 name="on_min_3" value=0 class="time_input">
    </div>

    <br><br><br>

    <div id="relay_schedule_panel_line_inner_title">
      Off:
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=23 name="off_hour_3" value=12 class="time_input">
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=45 step=15 name="off_min_3" value=0 class="time_input">
    </div>

  </div>


  <!-- 4 -->
  <div id="relay_panel_inner">

    <div id="relay_schedule_panel_line_inner_title">
      On:
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=23 name="on_hour_4" value=0 class="time_input">
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=45 step=15 name="on_min_4" value=0 class="time_input">
    </div>

    <br><br><br>

    <div id="relay_schedule_panel_line_inner_title">
      Off:
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=23 name="off_hour_4" value=12 class="time_input">
    </div>
    <div id="relay_schedule_panel_line_inner">
      <input type="number" min=0 max=45 step=15 name="off_min_4" value=0 class="time_input">
    </div>

  </div>


  <div id="relay_button_panel_inner">
    <button type="submit" class="relay_button" form="schedule" value="Submit">SET</button>
  </div>

  </div>
  </form>



</body>
</html>
