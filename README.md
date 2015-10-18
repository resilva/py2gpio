PY2GPio
=======

This software let you configure GPIO channels and send each new state to an API.

Installation
------------

Installation process is really simple, the program needs the following dependencies :

- python
- pip
- python-virtualenv

To install them on raspbian :

```bash
sudo aptitude install python python-virtualenv python-pip
```

After that, you can install PY2GPio :

```bash
cd /opt

git clone 
cd py2gpio

virtualenv .
source bin/activate
pip install -r requirements.txt
```

To run the program you need, to activate the virtualenv and to run run.py :

```bash
source bin/activate
python run.py
```

to exit the virtualenv just type ``deactivate`` in your console.

For a real environnement you probably need to let the script running, I advise you to use [supervisord](http://supervisord.org/).

You can use the following configuration file (put in : /etc/supervisord/conf.d/) :

```conf
[program:py2gpio]
autorestart = true
autostart = true
startsecs = 0
command = /opt/py2gpio/bin/python /opt/py2gpio/run.py
startretries = 1
environment=PY2GPIO_CONFIG="/opt/py2gpio/config.ini",PY2GPIO_CHANNEL="/opt/py2gpio/channels.ini"
```

and run supervisorctl ``supervisorctl start py2gpio``

Configuration
-------------

Two config file, need to be present :

- config.ini (which define global settings)
- channels.ini (for the gpio to monitor)

### config.ini

This file contain only two sections with one key for each one.

The ``general`` section contain a ``debug`` key which can bet set to ``on`` or ``off`` to enable or disable debug logging.

The ``api`` section contain a ``url`` key with the url of the API endpoint where the status will be pushed. You can specify a ``$id`` which will be replaced by the id key of the channel when the event will be triggered and a ``$value`` which will be replaced by the value on the gpio when triggered.

You can take a look at the ``config.ini.dist`` to have a real working example.

### channels.ini

Each section of this file represent a gpio pin. The pin numbering schema used is the BCM one (take a look [here](http://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/) for more informations).

Each section can have the following keys :
- id (will replace the ``$id`` in the api url)
- mode (default: IN)
- pull_up_down (default: off)
- event (default: RISING)

Take a look at the ``channels.ini.dist`` for a real working example.
