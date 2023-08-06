# Bumbo: Python Web Framework built for learning purposes

![purpose](https://img.shields.io/badge/purpose-learning-green.svg)
![Pypi](https://img.shields.io/pypi/v/bumbo.svg)

Bumbo is a Python web framework built for learnig purposes. You can learn this on [testdriven.io](https://testdriven.io/courses/python-web-framework/).

It's a WSGI framework and can be used with any WSGI application server such as Gunicorn.


## Installation
```shell
pip install marcosgeo-bumbo
```

## How to use it

### Basic usage

```python
from bumbo.api import API

app = API()


@app.route("/home")
def home(request, response):
    response.text = "Hello from HOME page"


@app.route("/hello/{name}")
def greeting(request, response, name):
    restponse.text = f"Hello, {name}"


@app.route("/book")
class BookResouce:
    def get(self, req, resp):
        resp.text = "Book Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template(
        "index.html", 
        context={"name": "Bumbo", "title": "Best Framework"}
    ).encode()

```

### Unit Tests

The recommended way of writing unit test is with [pytest](https://docs.pytest.org/en/latest/).  There are two built in fixtures that you may want to use when writing unit tests with Bumbo. The first one is `app` which is an instance of the main `API` class:

```python
def test_route_overlap_throws_exception(app):
    @app.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."

    with pytest.raises(AssertionError):
        @app.route("/")
        def home2(req, resp):
            resp.text = "Welcome Home 2."

```

The other ons is `client` that you can use to send HTTP requests to your handlers. It is based on the famous [requests](http://requests.readthedocs.io/) and should fell very familiar:

```python
def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(req, resp, name):
        rest.text = f"hey {name}"

    assert client.get("http://testserver/marcos").text == "hey marcos"

```

## Templates

The default folder for templates is `app/templates`. You can change it when initializing the main `API()` class:

```python
app = API(templates_dir="templates_dir_name")

```
Then you can use THML files in that folder like so in a handler:

```python
@app.route("/show/template")
def handler_with_template(req, resp):
    resp.html = app.template(
        "example.html",
        context={"title": "Awesome Framewokr", "body": "welcome to the future!"}
    )

```

## Static Files

Just like templates, the default folderfor static files is `static` and you can overwrite it:

```python
app = API(static_dir="static_dir_name")

```

Then you can use the files inside this folder as HTML templates:
```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>
  
  <link href="/static/main.css" rel="stylesheet" type="text/css">
</head>

<body>
  <h1>{{body}}</h1>
  <p>This is a praragrapha</p>
</body>
</html>
```

## Middleware
You can create custom middleware classes by inheriting from the `bumbo.middleware.Middleware` class and overriding ist two methods:

```python
from bumbo.api import API
from bumbo.middleware import Middleware


app = API()


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Before dispatch", req.url)

    def process_response(self, req, resp):
        print("After dispache, req.url)

add.add_middleware(SimpleCustomMiddleware)

```



