if Redis is not installed, need to install it first.
The method is dependent on your os.
e.g.install Redis by 
```
    sudo apt update -y
    sudo apt upgrade -y
    sudo apt install redis-server
    sudo systemctl status redis-server
    redis-cli
```

initialize the virtual environment for the first time. Only need to be done once. 
```python3 -m venv venv```

activate the venv
```source venv/bin/activate```

install all whatever things. only need to be done for the first time.
```pip install -r requirements.txt```

run this app.
```python3 run.py```


