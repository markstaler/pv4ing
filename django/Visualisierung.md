# Visualisierung

Um entscheiden oder handeln zu können sind Infomationen notwendig. Z.B. Energiemonitoring um die Effizenz zu beurteilen oder ein Niederschlagradar um eine geeignete Tourenwahl zu treffen. Werden Berechnungen oder Modellierungen ausgeführt so helfen diese Informationen ebenfalls Entscheidungen zu fällen. Im Ingenieurwesen ist dies in der Regel ein Diagramm. In den beiden Tutorial auf [www.pv4ing.ch](https://www.pv4ing.ch) sind die für uns relevanten Diagramme dargestellt. Zusätzlich sollte bei einer Visualisierung noch ein erklärender Text hinzu, nicht zu viel aber ein bisschen macht Sinn.

Denken wir an Energiemonitoring, so sollte die Visualisierung günstig sein, d.h. kein zusätzlicher Bildschirm und PC um den Zählerstand darzustellen. Das günstigste Display ist dies welches wir bereits dabei haben, das Mobil oder ein PC.

Deshalb bauen wir nicht ein eigenes GUI (Graphical User Interface), sondern erstellen eine Webpage. Auf der Messeinheit läuft ein Server, welcher die Information als Webpage darstellt und durch ein Mobil oder PC "angesurft" wird, welches die Informationen als Webpage über einen Browser darstellt.

Dabei ist neben der eigentlichen Information, die Darstellung der Webpage wichtig um eine gute Lesbarkeit auf unterschiedlichen Geräten (PC, Notebook, Smartphone) zu erreichen. Dies wird als Responsiv Design bezeichnet.

![](pic1.png)

### Leistsatz

Das Bauen einer Website kann zu einer sehr aufwändigen Sache werden, vorallem wenn wir uns in der Gestaltung verlieren. Deshalb einige Leitsätze:

1. Konzentration auf das Wesentliche: Was ist die Kernaussage der Webpage? Desgin wird "zugekauft"

2. Effektiv

3. Für jeden Handgriff das richtige Werkzeug

Der erste Punkt hat nicht mit programmieren oder Webpage zu tun.  Hierfür nimmt man Papier und Bleistift um die Kernaussage zu skizziern.

Bei zweiten Punkt "Effektiv" geht es daraum in kurzer Zeit eine Webpage zu erstellen. dies heisst Einfachheit im Aufbau mit wenig Code. Dies wird durch Python unterstützt da Python selbst dieses Ziel verfolgt beschrieben als "The Zen of Python":

1. Beautiful is better than ugly. 

2. Explicit (ausdrücklich) is better than implicit (indirekt).

3. Simple is better than complex. 

4. Complex is better than complicated. 

5. Flat is better than nested (verschachtelt).

Es gibt noch weitere Punkte, gib auf der Python Konsole folgendes ein:

`import this`

Der dritte Punkt "die richtigen Werkzeuge" zu verwendet unterstützt ein effektives arbeit. Das heisst auch das wir nicht das Selbe zweimal machen. Ein geschriebener Code sollte mehrmals für unterschiedliche Webpages einsetzbar sein. Dieses Prinzpip wird als "Don't repeat yourself (DRY)" bezeichnet.

### Webframework

Zur Erstellung von Webpages wird deshalb ein Webframework verwendet. Dies ist ein Baukastensystem mit einer Vielzahl nützlicher Werkzeuge wie Benutzerverwaltung, Formulare, Upload von Dateien und voralllem ein integrierter Entwicklungsserver um die Webpage schnell und einfach darzustellen ohne dem Aufsetzten eines Servers.

Der erste Schritt hierzu ist die Auftrennung von *Information*  und der *Darstellung*, wodurch beide Blöcke wiederverwendbar sind. Selbe Darstellung mit anderen Informationen oder selbe Informationen bei unterschiedlichen Darstellungen.

![](pic2.png)

Als Webframework verwenden wir Djano basierend auf Python. Dies Framework wird bei hunderten Webpages eingesetzt wie Youtube, Dropbox, Google, Netflix, Spotify, Pinterest, NASA, uvm. Der Untertitel von Django heisst "The web framework for perfectionists with deadlines" und zeigt die Stärken von Django, wie:

- Schnell umsetzbar mit wenig Code

- Sicherheit inbegriffen

- Skalierbar 

- Vielfach erprobt und bewährt

Djanog ist benannt nach dem Gitaristen Django Reinhardt.

![](djangoReinhardt.jpg)

### Architektur Django

Die Architektur von Django teilt die *Darstellung (Template)* von den *Informationen (Model)*, welche, je nach Anfrage (request) unterschiedlich zusammengebaut (*View*) werden. Das Konzept wird als MTV bezeichnet für *Model, Template, View* und ist eine lose gekoppelte Struktur, sodass einzelne Teile wiederverwendet werden können.

![](pic3.png)

# 

#### View

Die View ist die Programmeinheit bei Django, welche die Webpage zusammenbaut und darstellt, deshalb view. Hier werden auch die Anfragen (request) behandelt und die Adresse geprüft.

In der allgemeinen Literatur wird das MTV-Modell häufiger als MVC-Modell verwedet für Model, View, Control. Hier entspricht View dem DjangoTemplate und Control der Django View.

#### Template

Das Template beinhaltet die Darstellung, das Design der Webpage. Dieses Template werden wir nicht bauen, sondern fertig beziehen. Beispeil für eine Quelle ist [www.html5up.net](http://www.html5up.net).

#### Model

Unter Model werden die Informationen verstanden. Diese werden als Daten in einer Datenbank abgelegt. Um auf die Daten zugreifen zu können sind Datenbankabfragen wie SQL notwendig, diese sind jedoch nicht einfach und Django soll einfach sein. Deshalb wird die Information als Model definiert um so auf die Daten zugreifen zu können unabhängig der Datenbankstruktur im Hintergrund. Modelle werden vorerst nicht behandelt.

# 1. Einrichten der Werkstatt

Zum Leitsatz 3 "Für jeden Handgriff das richtige Werkzeug" richten uns zuerst eine Arbeitsumgebung, ein *virtual enviroment* ein. 

### Virtuelle Umgebung

Dies legt ein Ordner an indem unsere Python, Django, Bokeh Programme mit definierter Verion abgelegt sind. Sollten wir auf dem PC später mal ein Update durchführen, so bleibt unser Projekt trotzdem auf dem Versionsstand auf dem wir es gebaut haben.

Dies ist jetzt ein Mehraufwand, genau jetzt wo so viel Neues auf uns zukommt, aber es macht sich bezahlt. Wenn du später auf ein Projekt zurückgreifen möchtst haben sich die Versionen weiterentwickelt und der ürspüngliche Projekt-Code läuft nicht mehr, was nicht nur ärgerlich, sondern sehr zeitaufwändig ist. Deshalb "frieren" wir den aktuelle Stand der Entwicklungsumgebung ein. 

Wir erstellen zuerst unser Projektverzeichnis `djangoProjekt`. In diesem Verzeichnis erstellen wir eine virtuelle Umgebung namens `.env`. Im Anaconda-Paket ist die notwendige Software 'venv 'enthalten. Wir starten Python und weisen dieses an (mit -m) das die Software 'venv' ausgeführt werden soll:

    python -m venv .env

Nun starten wir die virtuelle Umgebung in unserem Projektverzeichnis mit 

    D:\djangoProjekt> .env\Scripts\activate

Damit die verwendeten Versionen der auf dem gewünschten Stand sind und dieser dokumentiert ist, erstellen wir eine *neue* Textdatei `requirements.txt`. Darin listen wir die SW-Pakete mit den Versionen:

```text
bokeh==2.0.0
django==3.0.4
```

Nun aktualisieren:

     pip install -r requirements.txt

Nun sind wir eingerichtet. Mit `pip list`  kannst du die aktuell, installierten Versionen ansehen. 

### GitHub

Als zweiten Schritt installieren wir GitHub ein Tool zur Code-Ablage auf einem Server. [Info zu Git](https://rogerdudler.github.io/git-guide/index.de.html). Dies ermöglicht das mehrere an einem Code arbeiten können und die Änderungen mit geloggt werden. Ein weiterer Vorteil ist, dass wir lokal unser Django-Projekt erstellen können und später über GitHub den Code auf einen Produktionsserver ins Internet bringen, zur Veröffentlichung (deployment). GitHub Desktop findet man unter [https://git-scm.com/](https://git-scm.com/). Lege ein Username/Passwort an. Wir öffnen GitHub und legen ein neues Repository an mit dem Namen **djangoProjekt** als "Local path" geben wir den existierenden Ordner "D:\djangoProjekt" an. Das ist alles.
![](newRepGitHub.PNG)
Nun haben ein Repository angelegt, welches wir später mit dem Server synchronisieren können, jedoch gibt es einige Ordner und Dateien welche wir nicht auf den Server stellen möchten, wie z.B. die virtuelle Umgebung mit dem Ordner `.env` oder .bat-Datei, welche wir später erstellen. Dazu legen wir eine neue Datei `.gitignore` im Hauptordner (`djangoProjekt`) des Repos an. Trage mit dem Notepad++ (nicht Editor, weil der ein Dateinamen mit führendem Punkt und ohne Endung nicht speichern kann) die Dateien und Ordner ein, welche nicht synchronisiert werden sollen:

```
.env
*.bat
*.pyc
__pycache__
db.sqlite3
```

Das wars. Nun bauen wir die erste Seite. Dieses Tutorial baut auf dem sehr empfehlenswerten Tutorial von [DjangoGirls](https://djangogirls.org) auf, welches in vielen Sprachen verfügbar ist. Nach eigenem durcharbeiten von Videos, Bücher, Webpages bietet DjangoGirls den flüssigsten Einstieg in Django.

# 1. Lokales Django-Projekt erstellen

Erstellen eines Django-Projekt  `energieDigital` .

    (.env) > django-admin startproject energieDigital .

Der Punkt `.` ist sehr wichtig, weil er dem Skript mitteilt, dass Django in deinem aktuellen Verzeichnis installiert werden soll. (Der Punkt `.` ist eine Schnellreferenz dafür.)

### settings.py

Wir machen nun ein paar Änderungen in `settings.py`. 

```python
ALLOWED_HOSTS = [
    '127.0.0.1',
    'markstaler.pythonanywhere.com',
    ]
```

Wir werden später die Seite unter pythonanywhere.com veröffentlichen. Du kannst dann deinen eigenen Namen davorstellen, anstatt "markstaler".

```python
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages', 
'django.contrib.staticfiles',
'energieDigital',
]
```

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'energieDigital/static')
```

### urls.py

Öffne die `energieDigital/urls.py`-Datei und passe den Code an, wie folgt:

```python
from django.contrib import admin
from django.urls import path
from .views import chart # hier importieren wir unsere Funktion

urlpatterns = [
    path('', chart),
    path('admin/', admin.site.urls),
    ]
```

#### views.py

In der *Views* schreiben wir die Logik unserer Anwendung und erzeugen die Darstellung mit dem Diagramm. Wir fügen eine neue Datei  `energieDigital/views.py` hinzu. Hier schreiben wir den Code zur Darstellung einer Sinusfunktion als eigene Funktion 'makeChart(nCycle)' in welche der Sinus berechnet wird und das Bokeh-Diagramm erzeugt wird:

```python
from django.shortcuts import render

from bokeh.plotting import figure
from bokeh.embed import components

import numpy as np

def chart(request):
    if request.POST: # wenn button gedrückt
        dic = request.POST # Werte von Page übernehmen
        print('mal sehen was das ist: ' + str(dic))
        nCycle = int(dic['nCycle'])
    else:
        nCycle = int(1)   

    chart = makeChart(nCycle)        
    return render(request, 'home.html', {'nCycle': nCycle, 'chart': chart})


def makeChart(nCycle):
    x = np.linspace(0,100,100)
    y = np.sin(x/100*2*3.1415*nCycle)    
    p1 = figure(plot_width=460, plot_height=200)
    p1.line(x, y)
    p1.toolbar.logo = None    

    script, div = components(p1)
    chart = script + div
    return chart
```

### Templates

Wenn nicht genauer angegeben sucht Django das html-Template im Ordner `templates`. D.h. wir legen diesen Ordner an.

    energieDigital
    └───templates

Als nächstes erstellen wir eine Datei `home.html`:

```html
<!DOCTYPE HTML>
<!-- Eventually by HTML5 UP -->
{% load static %}
<html>
    <head>
        <title>Energie Digital</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="{% static "assets/css/main.css" %}" />
        <!-- BOKEH -->
        <script type="text/javascript" src="{% static "bokeh-2.0.0.min.js" %}"></script>    
    </head>
    <body class="is-preload">
        <!-- Header -->
            <header id="header">
                <h1>Energie Digital</h1>
                <p>Programmierbeispiel im CAS Energie digital zu Visualisierung mit Django</p>                                        
            </header>
                <div style="background-color:rgba(0,0,0,0.5);padding: 20px">
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        <input type="number" step = 1 min = 1 max = 20 name="nCycle" value={{ nCycle }} style = color:blue>    
                        {{ chart|safe }}
                    <form>        
                </div>
        <!-- Scripts -->
            <script src="{% static "assets/js/main.js" %}"></script>
    </body>
</html>
```

Dies ist ein reduziertes Template von www.html5up.com/eventually. Dieses referenziert auf css-Datein und js-Dateien. Diese werden im Ordner `static` abgelegt, dem Ort wo Django standardmässig diese Dateien sucht. Lade das Template "Eventually" und speichere die beiden Ordner `immages`und `assets` in einem neu angelegten Ordner `static`. Dies ist der Ordner bei dem Django css-Dateien, Bilder und weitere Dateien zur Darstellung sucht. Die Ordnersturktur sieht nun wir folgt aus:

```
energieDigital 
   ├── static 
   │     ├── images
   │     └── assets
   └── templates
```

Öffne die Dateil `static/assets/js/main.js` mit dem Editor. Dort siehst du den Verweis auf die Hintergrundbilder `'images/bg01.jpg': 'center',`. Passe den Verweis an, wie folgt, da Django vom Projektverzeichnis ausgeht und unter `static` suchen soll:

```js
images: {
    'static/images/bg01.jpg': 'center',
    'static/images/bg02.jpg': 'center',
    'static/images/bg03.jpg': 'center'
},
```

Speichere im images-Ordner deine gewünschten Hintergundbilder mit obigen Namen. 

Nun haben wir in views.py ein bokeh-Diagramm er stellt als html-Code. Zur Darstellung braucht es noch die js-Datein von Bokeh im `static`Ordner. Diese ist im Internet unter https://cdn.bokeh.org/bokeh/release/bokeh-2.0.0.min.js wobei die Versionsnummer zu beachten ist (oben bei der pip-Installation definiert in der requirements.txt Datei). Diese Seite im Bowser aufrufen und rechte Maustaste "speichern unter" um so die Datei im Ordner `static` abspeichern.

Um den Developmentserver von Django zu starten muss auf der Konsole das Kommando `python manage.py runserver` eingegeben werden. Um nicht zeitaufwändig mit in der Konsole zum Projektlordner zu navigieren, die virtuelle Umgebung zu starten und anschliessend der Developmentserver, kann eine bat-Datei angelegt werden mit folgendem Inhalt in der `start.bat` Datei, welche zukünftig das starten übernimmt: 

```dos
cd ablouterPfadProjektordnerWoManage.pyLiegt
start cmd /T:0E /K ".env\Scripts\activate&&python manage.py runserver"
```

# 3. Veröffentlichen

Zuerst laden wir unser Projekt auf GitHub laden (push). Wir veröffentlichen die Webpage auf [pythonannywhere.com](https://www.pythonanywhere.com). Hierfür registrieren wir uns und reservieren den Namen der Webpage.

??ganz oben recht: Account>API Token>Create a new API token??

Beim Start von pythonanywhere landen wir auf dem "Dashboard" wo rechts unten eine console geöffnet werden kann. Wir öffnen "Bash" und laden unser Projekt von Github mit:
`git clone https://github.com/markstaler/djangoProjekt.git`
Eingabe GitHub-Name und Passwort wird abgefragt. Falls du später ein Update machen möchtest lautet das Kommando:
`git pull`, jedoch muss du im djangoProjekt-Verzeichnis sein.

Unter dem Menüpunkt "Files" rechts oben, kann du die Ordnerstruktur auf dem Server ansehen, welche wie folgt aussieht:

```
/home 
   └─ markstaler
       ├── .virtualenvs/
       ├── djangoProjekt/
       ├── ...  
```

Als nächstes installieren wir die virtuelle Umgebung, dabei geben wir die Pythonversion an (3.7) und den Namen der virtuellen Umgebung (markstaler-env).
`mkvirtualenv --python=/usr/bin/python3.7 markstaler-env
Die Ornderstruktur sieht nun wie folgt aus:

```
/home 
   └─ markstaler
       ├── .virtualenvs/
       │       └─ markstaler-env
       ├── djangoProjekt/
       ├── ...
```

Auf der Konsole kann mit "ls" angezeigt werden wie "dir" bei Windows. Wir wechseln ins Verzeichnis `djangoProjekt` indem wir auf der Konsole "cd dj" eingeben und TABULATOR drücken. Der Verzeichnisname wird vervollständigt! Komfortabel. Nun installieren wir unsere Pakete, die Datei "requirements.txt" kommt von unserem Projekt:
`pip3.7 install -r requirements.txt`
(Achtung auf dem Server/Linux die Version angeben "pip3.7")

```
/home 
   └─ markstaler
       ├── .virtualenvs/
       │       └─ markstaler-env
       │             └─ lib
       │                  └─ python3.7
       │                       └─ site-packages
       │                            └─ *meine Pakete*      
       ├── djangoProjekt/
       ├── ...
```

Sollte was beim installieren nicht funktionieren, so können die Pakete gelöscht werden, durch Löschen des Paketordner unter `site-packages` . Navigieren mit oben rechts Menüpunkt "Files".

Wir wechseln von der Bash-Console auf "Web" oben links. "Add a new web app" und wählen **Manual Configuration**, Python3.7. 

Wir ergänzen: 

`Source code: /home/markstaler/djangoProjekt`

`Working directory: /home/markstaler`

Nun wird auf dem Server eine Datei ...wsgi.py angelegt. Diese Datei ist wichtig da hier unser Django mit dem Produktionsserver verbunden wird. wsgi = Python Web Server Gateway Interface. Die Datei enthält neben Django-Einstellungen auch anderes, welches wir löschen. Die Datei sieht dann wie folgt aus, inklusiv Anpassungen für unser Projekt:

```python
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

## assuming your django settings file is at '/home/markstaler/mysite/mysite/settings.py'
## and your manage.py is is at '/home/markstaler/mysite/manage.py'
path = '/home/djangoProjekt'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'energieDigital.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Wir geben noch den Ort der virtuellen Umgebung an und den URL für static files (/static/) und das Verzeichnis, das wars.

Neustart des Produktionsserver durch "Reload ..." oben.

## 3. Security

Bei pythonanywhere wird der Produktionsserver durch den Anbieter betrieben und Django liegt dahinter. 

Es soll unter Web unten "HTTP to HTTPS" aktivieren werden.

### login

Der Inhalt der Webseite kann zusätzlich durch ein login ergänzt werden. Hierfür muss zuerst ein superuser angelegt werden. Über dieser kann anschliessend bei Webpage user generiert werden. Anlegen des Superuser:

`python3.7 manage.py createsuperuser`

Anschliessend wird im Browser die Django administration geöffnet:

`markstaler.pythonanywhere/admin` und eingeloggen, als Superuser, anschliessend kann ein user angelegt werden.

Für den login ergänzen wir die Datei `settings.py` durch folgende Zeile:

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

Schliesslich erstellen wir einen Login/Logout Dialog im Template `home.html`:

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

Im Ordner `templates` legen wir einen Unterordner `registration` an. Dort sucht Django standardmässig das login.html, welches wir wie folgt anlegen:

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
![](pic4.png)

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
