Art17 – aplicație de consultare
===============================


Instalare
--------
Trebuie să fie deja instalate următoarele:

* Compilator C
* Python 2.7 (inclusiv header-ele pentru compilare)
* Biblioteca de client Oracle (`instantclient-basic`, `instantclient-sdk`)
  (instrucțiuni pentru MacOS: https://gist.github.com/mgax/6364125)
* Biblioteci XML (`libxml2-dev`, `libxslt1-dev`)

Download codul sursă::

    $ git clone https://github.com/eaudeweb/art17-consultation.git
    $ cd art17-consultation

Instalarea bibliotecilor Python::

    $ pip install -r requirements.txt

Crearea unui fișier de configurare (înlocuiți ``secret`` cu un șir de
caractere random)::

    $ mkdir -p instance
    $ echo > instance/settings.py <<EOF
    SQLALCHEMY_DATABASE_URI = 'oracle://user:pass@host:1521/XE'
    SECRET_KEY = 'secret'
    EOF

Rularea aplicației
------------------
Serverul de aplicație se pornește cu comanda::

    $ waitress-serve --call art17.app:create_consultation_app

Comanda primește următoarele argumente opționale (ultimul argument
trebuie să rămână numele aplicației):

* ``--port 5000`` portul pe care să asculte serverul http
* ``--url-prefix=/some/value`` prefixul de url unde este servită aplicația


Instalare offline
-----------------
În mod normal, instalarea dependențelor se face online, și pachetele vor
fi downloadate pe loc.  Instalarea se poate face și complet offline,
după cum urmează:

1. Pregătirea pachetelor::

    $ mkdir -p instance/dist
    $ pip install --download=instance/dist -r requirements.txt

2. Instalarea offline::

    $ pip install -f instance/dist -r requirements.txt


Configurație
------------
``DEBUG = False``
    Modul "debug", util pentru dezvoltare, a nu se folosi în producție,
    este complet nesecurizat.

``USE_LESS = False``
    Dacă este activ, fișierele ``.less`` se vor compila de către
    browser.

``SQL_DEBUG = False``
    Dacă este activ, se vor afișa query-urile SQL în consolă.

``AUTH_DEBUG = False``
    Activează o pagină de login unde se poate introduce orice `user_id`
    și set de roluri.

``AUTH_REVERSE_PROXY = False``
    Preia utilizatorul curent dintr-un header HTTP ``X-RP-AuthUser``.
    Acesta trebuie controlat de un reverse proxy în fața aplicației.

``AUTH_LOGIN_URL = ''``
    Stabilește URL-ul la care se face autentificarea, atunci când AUTH_DEBUG
    este False. După autentificare, se întoarce în aplicație, iar headerele
    HTTP sunt setate.

``AUTH_LOGIN_NEXT_PARAM = 'next'``
    Stabilește parametrul GET pe care îl primește AUTH_LOGIN_URL pentru a ști
    în ce pagină să se întoarcă (după autentificare).

``AUTH_LOGOUT_URL = ''``
    URL-ul la care se face deautentificarea, atunci când AUTH_DEBUG
    este False.

``LDAP_SERVER``
    Adresa serverului LDAP sau ActiveDirectory. De exemplu
    ``'ldap://192.168.2.3'``.

``LDAP_LOGIN``
    Date de autentificare pentru acces la LDAP. De exemplu
    ``('IBB\Administrator', 'admin')``.

``LDAP_BASE_DN``
    Directorul de bază pentru căutări în LDAP. De exemplu
    ``'OU=SharePoint,DC=ibb,DC=local'``.

``SQLALCHEMY_DATABASE_URI``
    Accesul la baza de date:
    ``'oracle://reportdata_owner:parola@localhost:1521/XE'``

``SPECIES_MAP_URL``, ``HABITAT_MAP_URL``
    Template-uri pentru generat link-uri la hărțile de specii și
    habitate, de exemplu:
    ``'http://example.com/map?species={species}&regions={regions}'``

``SENTRY_DSN``
    Adresă a unui server Sentry pentru logat erori.


Dezvoltare
----------
Instalarea pachetelor ajutătoare::

    $ pip install -r requirements-dev.txt

Rularea testelor::

    $ py.test

Actualizarea fișierelor `requirements`::

    $ pip-dump


Import baza de date
-------------------
Pentru importul inițial instrucțiunile de import sunt aici::

    https://gist.github.com/nico4/1f7524c51194fbebe14a

După aceea trebuie rulate migrările::

    $ ./manage.py db upgrade


Creare revizie
--------------
Pentru a crea un nou script de migrare::

    $ ./manage.py db revision

Apoi se editează din: `alembic/versions/revizie.py`

Pentru a aduce baza de date la zi: upgrade. Pentru a reveni la versiunea 
dinaintea migrării::

    $ ./manage.py db downgrade -1

Export date
-----------

Pentru exportul de date, folosim comanda export::
    
    $ ./manage.py export -h

Vor fi afișate tipurile de export disponibile.

