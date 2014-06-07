<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Home Dashboard</title>

    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/dashboard.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
 <script type="text/javascript">
    var ws = new WebSocket("ws://" + location.host + "/ws");
    ws.onmessage = function (evt) {
	var msg = JSON.parse(evt.data);
	var elem = document.getElementById(msg.key);
	if (elem != null)
	{
        	elem.innerHTML = msg.value;
	}
    };
  </script>
  </head>
  <body>
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Home Dashboard</a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
            <li><a href="#">Dashboard</a></li>
            <li><a href="#">Settings</a></li>
            <li><a href="#">Profile</a></li>
            <li><a href="#">Help</a></li>
          </ul>
          <form class="navbar-form navbar-right">
            <input type="text" class="form-control" placeholder="Search...">
          </form>
        </div>
      </div>
    </div>

    <div class="container-fluid">
      <div class="row">
        <!--navbar may be here-->
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
          <h3 class="page-header">Температура</h3>
          <div class="row placeholders">
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Гостиная</h4>
              <span class="text-muted"><div id="home/temperature/Гостиная">---</div></span>
            </div>
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Спальня</h4>
              <span class="text-muted"><div id="home/temperature/Спальня">---</div></span>
            </div>
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Детская</h4>
              <span class="text-muted"><div id="home/temperature/Детская">---</div></span>
            </div>
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Кухня</h4>
              <span class="text-muted"><div id="home/temperature/Кухня">---</div></span>
            </div>
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Кладовая</h4>
              <span class="text-muted"><div id="home/temperature/Кладовая">---</div></span>
            </div>
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Ванная</h4>
              <span class="text-muted"><div id="home/temperature/Ванная">---</div></span>
            </div>
          </div>
          <h3 class="page-header">Входная дверь</h3>
          <div class="row placeholders">
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Дверь</h4>
              <span class="text-muted"><div id="home/front door/door">---</div></span>
            </div>
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Верхний замок</h4>
              <span class="text-muted"><div id="home/front door/lock/upper">---</div></span>
            </div>
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Нижний замок</h4>
              <span class="text-muted"><div id="home/front door/lock/lower">---</div></span>
            </div>
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Кнопка</h4>
              <span class="text-muted"><div id="home/front door/button">---</div></span>
            </div>
          </div>
          <h3 class="page-header">Ванная</h3>
          <div class="row placeholders">
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Свет</h4>
              <span class="text-muted"><div id="home/bathroom/light">---</div></span>
            </div>
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Протечка</h4>
              <span class="text-muted"><div id="home/bathroom/leak">---</div></span>
            </div>
          </div>
          <h3 class="page-header">Туалет</h3>
          <div class="row placeholders">
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Свет</h4>
              <span class="text-muted"><div id="home/restroom/light">---</div></span>
            </div>
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Вентилятор</h4>
              <span class="text-muted"><div id="home/restroom/fan">---</div></span>
            </div>
            <div class="col-xs-3 col-sm-3 placeholder">
              <h4>Протечка</h4>
              <span class="text-muted"><div id="home/restroom/leak">---</div></span>
            </div>
          </div>
        </div>
      </div>
    </div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
<script src="js/bootstrap.min.js"></script>

</body>
</html>