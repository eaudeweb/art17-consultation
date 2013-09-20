Art17 – aplicație de consultare
===============================


Insalare
--------
Trebuie să fie deja instalate următoarele:

* Compilator C
* Python 2.7 (inclusiv header-ele pentru compilare)
* Biblioteca de client Oracle (`instantclient-basic`, `instantclient-sdk`)
  (instrucțiuni pentru MacOS: https://gist.github.com/mgax/6364125)
* Biblioteci XML (`libxml2-dev`, `libxslt1-dev`)

Download codul sursă::

    $ git clone https://github.com/eaudeweb/art17-consultation.git art17
    $ cd art17-consultation

Instalarea bibliotecilor Python::

    $ pip install -r requirements.txt

Crearea unui fișier de configurare (înlocuiți ``secret`` cu un șir de
caractere random)::

    $ mkdir -p instance
    $ echo > instance/settings.py <<EOF
    SQLALCHEMY_DATABASE_URI = 'oracle://user:pass@host:1521/XE'
    SECRET_KEY = 'secret'
    ART17_LISTEN_HOST = '127.0.0.1'
    ART17_LISTEN_PORT = 5000
    EOF

Rularea aplicației::

    $ ./manage.py waitress


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


Dezvoltare
----------
Instalarea pachetelor ajutătoare::

    $ pip install -r requirements-dev.txt

Rularea testelor::

    $ py.test

Actualizarea fișierelor `requirements`::

    $ pip-dump


Import baza de data
-------------------
Pentru importul inițial instrucțiunile de import sunt aici::

    https://gist.github.com/nico4/1f7524c51194fbebe14a

După aceea trebuie rulate migrările::

    $ ./manage.py db upgrade
