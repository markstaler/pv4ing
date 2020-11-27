# Visualisierung Teil 2

Im ersten Teil der Visualisierung haben wir die View-Model-Template Architektur von Django erstellt, welche wie folgt aussieht: 

![](pic4.png)

Umgesetzt sieht die Dateistruktur zeigt sich wie folgt aus:

```
D:/djangoProjekt 
   ├── .env
   ├── energieDigital   
   │     ├── static
   │     │      ├── assets...
   │     │      ├── images...
   │     │      └─bokeh-2.1.1.min.js
   │     ├── templates
   │     │      └─home.html
   │     ├─settings.py
   │     ├─urls.py
   │     └─views.py
   │
   ├─db.sqlite3
   ├─manage.py
   ├─requirments.txt
   └─start.bat 
```

Ein wesentlicher Teil fehlt noch, das "Model (Information)" mit den Daten. Dies sind die beiden Dateien  "models.py" und "db.sqlite". D.h. der Teil der Datenspeicherung und Informationsgenerierung. Dies ergänzen wir nun. Im Tutorial werden folgende Punkte implementiert:

- Änderung der Darstellung
- Änderbarer Textinhalt über Model und Admin
- Logbuch
- Login

# Änderung der Darstellung

Nun verwenden wir ein anderes Template, das Template [Dimension](https://html5up.net/dimension). Der Ordner `asset` speichern wir in unser Projekt unter `static` mit dem Namen `asset2`. Den Rest benötigen wir nicht. Unter `templates`erstellen wir eine neue Datei **index.html**, welches eine reduzierte Form des Dimension-Template ist. Darin ist die Sinus-Funktion enthalten aus dem ersten Teil.

```html
<!DOCTYPE HTML>
<!-- Dimension by HTML5 UP -->
{% load static %}
<html>
<head>
	<title>Energie digital</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
	<link rel="stylesheet" href="{% static "assets2/css/main.css" %}" />
	<!-- BOKEH -->
	<script type="text/javascript" src="{% static "bokeh-2.1.1.min.js" %}"></script>
</head>
<body class="is-preload">
<!-- Wrapper -->
<div id="wrapper">
	<!-- Header -->
	<header id="header">
		<div class="content">
			<div class="inner">
				<h1>Energie digital</h1>
				<p>Programmierbeispiel in Programmiertechnik zu Visualisierung mit Django</p>
			</div>
		</div>
		<nav>
			<ul>
				<li><a href="#0">Projekt</a></li>
				<li><a href="#1">Berechnung</a></li>
				<li><a href="#2">Logbuch</a></li>
				<li><a href="#3">Kontakt</a></li>
			</ul>
		</nav>
	</header>
	<!-- Main -->
	<div id="main">
		<!-- #0 -->
			<article id="0">
				<h2 class="major">Projekt</h2>
				<p>Projekttext</p>
			</article>

		<!-- #1 -->
			<article id="1">
				<h2 class="major">Berechnung</h2>
					<form method="post" enctype="multipart/form-data">
					{% csrf_token %}
					<input type="number" step = 1 min = 1 max = 20 name="nCycle" value={{ nCycle }} style = color:blue>    							    {{ chart|safe }}
					</form>
			</article>

		<!-- #2 -->
			<article id="2">
				<h2 class="major">Logbuch</h2>
				<p>Logbuchtext</p>
			</article>

		<!-- #3 -->
			<article id="3">
				<h2 class="major">Kontakt</h2>
			</article>
	</div>

	<!-- Footer -->
	<footer id="footer">
		<p class="copyright">&copy; Untitled. Design: <a href="https://html5up.net">HTML5 UP</a>.</p>
	</footer>
</div>

<!-- BG -->
	<div id="bg"></div>

<!-- Scripts -->
	<script src="{% static "assets2/js/jquery.min.js" %}"></script>
	<script src="{% static "assets2/js/browser.min.js" %}"></script>
	<script src="{% static "assets2/js/breakpoints.min.js" %}"></script>
	<script src="{% static "assets2/js/util.js" %}"></script>
	<script src="{% static "assets2/js/main.js" %}"></script>
</body>
</html>

```

In der Datei **main.css** wird das Hintergrundbild definiert mit **images/bg.jpg**. Suche diese Stelle und ändere diese auf **images/bg01.jpg**, dadurch kann das bestehende Bild verwendet werden.

 In **views.py** ändern wir noch den Template Name von home.html auf **index.html**. Wir starten den Entwicklungsserver und sehen uns das neue Design an:

```
python manage.py runserver
```

# Änderbarer Textinhalt

Nun setzen wir die Django-Datenbank ein. Diese müsste bereit definiert sein in  `settings.py`.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

Erstmalig müssen wir die Datenbank anlegen über den Befehl:

    python manage.py migrate

### models.py

Die Datenmodelle werden in models.py definiert, welche neu zu erstellen ist. Diese Datei liegt im Ordner der Applikation, dort wo views.py liegt. 

```python
from django.db import models

class Seitentext(models.Model):
    no    = models.SmallIntegerField()
    titel = models.CharField(max_length=20)
    text = models.TextField()
    
    def __str__(self):
        return self.title
```

Nun müssen wir die alle neuen oder später geänderten Modelle welche zur "energieDigital" gehören in der Datenbank anlegen. Dies erfolgt durch

```
python manage.py makemigrations energieDigital
```

Es wurde eine Migrationsdatei angelegt, welche wir nun auf die Datenbank anwenden:

```
python manage.py migrate
```



## Django Admin Dashboard

Die Eingabe des Seitentext, bzw. Eingabe ins Datenmodell führen wir mit dem Django Admin Dashboard durch, somit müssen wir nicht eine eigene Eingabe Webpage bauen. Dort können wir die Modelle nicht nur anlegen, sondern auch ändern oder löschen. Hier legen wir ebenfalls im Applikationsordner die Datei **admin.py** an, in der wir Django mitteilen, dass, das Model "Seitentext" ins Dashboard aufgenommen werden soll:

```python
from django.contrib import admin
from .models import Seitentext

admin.site.register(Seitentext)
```

Für den Zugriff auf das Django Admin Dashboard benötigen wir einen User mit Passwort. Dieser legen wir durch folgenden Konsolenbefehl an.

```
python manage.py createsuperuser
```

Als Beispiel wählen wir `user: web; e-mail: web@test.ch; pwd: web123456`.  Anschliessend starten wir die Webpage

```
python manage.py runserver
```

Der Zugriff auf das Django Admin Dashboar erfolgt durch die Adresse http://127.0.0.1:8000/admin/. Diese ist seit Anfang an definiert, in der Datei `urls.py`. Es erscheint die Anmeldeseite:

![](login_page2.png)

Nun erscheint das Django Admin Dashboard und hier kannst du einen Seitentexte anlegen. Erstelle eine Beschreibung zu **Projekt** und zu **Berechnung**.

Anpassen index.html

```html
...
<nav>
	<ul>
		<li><a href="#0">{{ seite.0.titel }}</a></li>
		<li><a href="#1">{{ seite.1.titel }}</a></li>
		<li><a href="#2">{{ seite.2.titel }}</a></li>
		<li><a href="#3">{{ seite.3.titel }}</a></li>
	</ul>
</nav>
...

<!-- Main -->
<div id="main">
	<!-- #1 -->
	<article id="0">
		<h2 class="major">{{ seite.0.titel }}</h2>
		{{ seite.0.text|safe }}	
	</article>
...
```

Anpassung views.py

```python
from .models import Seitentext
...
    seite = Seitentext.objects.order_by('no')
    
    return render(request, 'index.html', {'nCycle': nCycle, 'chart': chart, 'seite': seite})
```



# Logbuch

noch zu definieren

# Login

Der Inhalt der Webseite kann zusätzlich durch ein Login ergänzt werden. Im Django Admin Dashboard legen wir einen  user an (nicht der superuser). Z.B. user: "editor" mit pwd: "editor123456".

Für die Login Funktionalität ergänzen wir die Datei `settings.py` durch folgende Zeile:

```python
LOGIN_REDIRECT_URL = '/'
```

In der Datei `urls.py` ergänzen wir folgendes:

```python
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views
from .views import chart

urlpatterns = [
    path('', chart),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(), name='loginPage'),
    path('logout/', views.LogoutView.as_view(next_page = '/'), name='logoutPage'),
    ]
```

Schliesslich erstellen wir einen Login/Logout Dialog am unteren Rand im bestehendem Template **index.html**:

```html
<!-- Footer -->
<footer id="footer">
    {% if user.is_authenticated %}
        angemeldet als {{ user.get_username }}.
        <a href="{% url 'logoutPage' %}">hier abmelden</span></a>
    {% else %}
        bitte <a href="{% url 'loginPage' %}">hier anmelden</span></a>
    {% endif %}
</footer> 
```

Im Ordner `templates` legen wir einen Unterordner `registration` an. Dort sucht Django standardmässig das **login.html**, welches wir wie folgt anlegen:

```html
{% load static %}
<html>
    <head>
        <title>login - energieDigital</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="{% static "assets/css/main.css" %}"/>
    </head>
    <body>
    {% block content %}
        {% if form.errors %}
            <font color="white">
            <br>
            <p>Benutzername und Passwort stinmmt nicht überein. Versuche es nochmals.</p>
        {% endif %}

        <form method="post" action="{% url 'loginPage' %}">
        {% csrf_token %}               
            Benutzername
            {{ form.username }}
            Passwort
            {{ form.password }}
            <br>                
            <input type="submit" value="loginPage" />
        </form>
    {% endblock %}
    </body>
</html>
```

Mit der Autentifiezierung können unterschiedliche Aktionen durchgeführt werden. Im Folgenden eine Ergänzung im Code von `views.py`:

```python
    auth = request.user.is_authenticated # ist jemand angemeldet
    if not(auth):
        chart = '<br>Kein Diagramm, da nicht angemeldet'
```

# Zusammenfassung

Die View-Model-Template Architektur von Django sieht nun wie folgt aus:
![](C:/Dokumente/40_GitHub/pv4ing/visual2/pic4.png)

Die Dateistruktur zeigt sich wie folgt:

```
D:/djangoProjekt 
   ├── .env
   ├── energieDigital   
   │     ├── static
   │     │      ├── assets...
   │     │      ├── images...
   │     │      └─bokeh-1.4.0.min.js
   │     │
   │     ├── templates
   │     │      ├─home.html
   │     │      └── registration
   │     │              └─login.html
   │     │
   │     ├─settings.py
   │     ├─urls.py
   │     ├─views.py
   │     └─wsgi.py
   │
   ├─db.sqlite3
   ├─manage.py
   ├─requirments.txt
   └─start.bat 
```