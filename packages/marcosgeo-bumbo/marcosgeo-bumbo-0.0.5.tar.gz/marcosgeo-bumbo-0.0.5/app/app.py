# app.py

from bumbo.api import API
from bumbo.middleware import Middleware


app = API()


@app.route("/home")
def home(request, response):
    response.text = "\nHello from the HOME page\n\n"


@app.route("/about")
def about(request, response):
    response.text = "\nHello from the ABOUT page\n\n"


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"\nHello, {name}\n\n"


@app.route("/sum/{num_1:d}/{num_2:d}")
def sum(request, response, num_1, num_2):
    total = int(num_1) + int(num_2)
    response.text = f"\n{num_1} + {num_2} = {total}\n\n"


@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AssertionError("\nThis handler should not be used.\n\n")


@app.route("/template")
def template_handler(req, resp):
    resp.html = app.template(
        "index.html",
        context={"name": "Bumbo", "title": "Best Framework"}
    )


@app.route("/json")
def json_handler(req, resp):
    resp.json = {"name": "data", "type": "JSON"}


@app.route("/text")
def text_handler(req, resp):
    resp.text = "This is a simple text"



# class-based handler


@app.route("/book")
class BookResource:
    def get(self, request, response):
        response.text = "\nBooks Page\n\n"

    def post(self, request, response):
        response.text = "\nEndpoint to create a book\n\n"

    def put(self, request, response):
        response.text = "\nEndpoint to update a book\n\n"

    def delete(self, request, response):
        response.text = "\nEnpoint to delete a book\n\n"



# django-like handlers


def handler(req, resp):
    resp.text = "\nDjango-like handler\n\n"

app.add_route("/sample", handler)



# exception handler


def custom_exception_handler(request, response, exception_cls):
    response.text = str(exception_cls)

app.add_exception_handler(custom_exception_handler)



# custom middleware


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, resp):
        print("Processing response", req.url, resp)

app.add_middleware(SimpleCustomMiddleware)


