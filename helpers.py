import pymongo
from jinja2 import Environment, FileSystemLoader


def connect():
    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    mydb = myclient["riba"]
    mycol = mydb["products"]
    return mycol


def implementsApp(products):
    products = {"products": products}

    environment = Environment(loader=FileSystemLoader("views/"))

    applayout = environment.get_template("productsList.html")
    data = applayout.render(products)
    return data
