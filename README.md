# AIhome
AL Home web console

# Installation

mkdir AIhome
cd ALhome
git clone https://github.com/oziee/AIhome.git

this uses Python 3
so something like 
```
pip3 install -r requirements.txt
```
or 
```
python3 -m pip install -r requirements.txt
```

# Before starting
Edit the config.py file and enter in your MQTT server info
can config the port to use too in there

# Running
Either create a service to run on startup.. on macOS use something like Automator 

for testing.. run
```
flask run --host=0.0.0.0 --port=80
```

or 
```
./wsgi.py
```

To log in the default is **admin/admin**
You can change the password inside the web console

# Docker using docker-compose
To run this within a Docker container, ignore above installation and running, and instead:
- If docker-compose is not already installed, install docker-compose see: https://docs.docker.com/compose/install/
- Update docker-compose.yml
  - MQTT_BROKER_URL in docker-compose.yml to point at your broker.
  - optionally change which port you want this app to be served on your host in (default 9000)
- In this directory do: ```docker-compose up --build```
- In a browser on your host, go to http://localhost:9000 or whatever port you configured.

# Information

As you start using your devices around the house, the system will start to build a list of sites and the logs will start to grow
