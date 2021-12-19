def message_create(message, link):
	text = r'''
	<!DOCTYPE html>
	<html lang="en">
	<head>
	  <meta charset="utf-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	  <link rel="stylesheet" href="{{ url_for('static', filename='assets/css/bootstrap.min.css')}}">
	  <link rel="stylesheet" href="{{ url_for('static', filename='assets/css/style.css')}}">
	  <link rel="icon" href="{{ url_for('static', filename='img/favicon.png')}}">
	  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,700,700i|Roboto:100,300,400,500,700|Philosopher:400,400i,700,700i" rel="stylesheet">
	  <link rel="stylesheet" href="{{ url_for('static', filename='lib/font-awesome/css/font-awesome.min.css')}}">
	  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css')}}">
	    <link rel="stylesheet" href="{{ url_for('static', filename='assets/css/main.css')}}" type="text/css" />
	  

	  <title>MOBILIT'CHI</title>
	</head>

	<body>
	  
	  <!-- Header -->
	      <header id="header" class="alt"; top: 0px">
	        <div class="logo"><a href="'''+link+'''"><img src="https://zupimages.net/up/20/29/wg55.png"></a></div>
	      </header>


	<center><h2>'''+message+'''</h2></center>

	  <footer class="footer">
	    <div class="container">
	      <div class="row">

	        <div class="col-md-12 col-lg-4">
	          <div class="footer-logo">
	            <p>“Facilitons notre vie !” </p>
	          </div>

	        </div>
	      </div>
	    </div>
	    <div class="copyrights">
	      <div class="container">
	        <p>&copy; Copyrights MOBILIT'chi. Tout les droits réservé</p>
	        </div>
	  </footer>

	</html>
	'''
	return text










