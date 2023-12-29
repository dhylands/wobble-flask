## wscat

wscat is a node utility that can be used to quickly test text based sockets.

```bash
sudo apt get install nodejs npm
sudo npm install -g wscat
```

Once installed it can be invoked:
```bash
wscat --connect http://localhost:5000/reverse
```

## gunicorn

For a production environement this can be run using gunicorn:

To install:
```bash
pip install gunicorn
```

To use:
```bash
gunicorn -b :5000 --workers 4 --threads 100 app:app
```
