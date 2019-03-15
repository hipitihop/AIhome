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

# Information

As you start using your devices around the house, the system will start to build a list of sites and the logs will start to grow