# Flask demo

This is a demo project for Flask framework. 

Base functionality is to add watch posts.

## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Flask Application Structure 
```
.
|──────/static
| |────-/css
| |────---styles.css
|──────/templates
| |────/FDataBase.py
| |────/flsite.py
| |────/sq_db.sql
```


## Flask Configuration

#### Example

```
app = Flask(__name__)
app.config['DEBUG'] = True
```
### Configuring From Files

#### Example Usage

```
app = Flask(__name__ )
app.config.from_pyfile('config.Development.cfg')
```

#### cfg example

```

##Flask settings
DEBUG = True  # True/False
TESTING = False
....


```
 
## Run Flask
### Run flask for develop
```
$ python webapp/run.py
```
In flask, Default port is `5000`


## Changelog

- Version 1.0 : basic flask-example
