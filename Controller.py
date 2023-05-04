from flask import Flask, request, redirect
from jinja2 import Environment, FileSystemLoader
from component import component
from Comanda import Comanda
from component.component import updateCommand

from helpers import connect, implementsApp

app = Flask(__name__)


@app.route("/")
def mostrarPerNom():
    p = connect()
    products = []

    for x in p.find().sort("name"):
        products.append(x)

    data = implementsApp(products)
    return f'{data}'


@app.route("/priceLessToMore")
def mostrarPriceLessToMore():
    p = connect()
    products = []

    for x in p.find().sort("price"):
        products.append(x)
    data = implementsApp(products)
    return f'{data}'


@app.route("/priceMoreToLess")
def mostrarPriceMoreToLess():
    p = connect()
    products = []

    for x in p.find().sort("price", -1):
        products.append(x)
    data = implementsApp(products)
    return f'{data}'


@app.route("/valorationLessToMore")
def mostrarValorationLessToMore():
    p = connect()
    products = []

    for x in p.find().sort("valoration"):
        products.append(x)
    data = implementsApp(products)
    return f'{data}'


@app.route("/valorationMoreToLess")
def mostrarValorationMoreToLess():
    p = connect()
    products = []

    for x in p.find().sort("valoration", -1):
        products.append(x)
    data = implementsApp(products)
    return f'{data}'


@app.route('/product/<productId>')
def showProduct(productId):
    p = connect()
    product = p.find_one({"id": int(productId)})
    commands = component.getAll("commands.bin")
    amount = 0
    for c in commands:
        if c.idProduct == productId:
            amount += int(c.quantity)

    environment = Environment(loader=FileSystemLoader("views/"))

    applayout = environment.get_template("product.html")
    info = {"product": product, "amount": amount}
    data = applayout.render(info)
    return f'{data}'


@app.route('/about')
def about():
    environment = Environment(loader=FileSystemLoader("views/"))

    applayout = environment.get_template("about.html")
    data = applayout.render()
    return f'{data}'


@app.route('/product/<productId>', methods=["POST"])
def addToCart(productId):
    p = connect()
    quantity = request.form['quantity']
    producte = p.find_one({"id": int(productId)})
    if component.restoreCommand(productId, "commands.bin") is None:
        c1 = Comanda(productId, quantity, producte.get('price'))
        component.saveObject(c1, "commands.bin")
    else:
        updateCommand("commands.bin",productId,quantity)

    return redirect('/product/' + productId)


@app.route('/cart')
def cart():
    environment = Environment(loader=FileSystemLoader("views/"))
    applayout = environment.get_template("cart.html")
    commands = component.getAll("commands.bin")
    totalPrice = 0.00
    for c in commands:
        totalPrice += c.price
    info = {"commands": commands, "totalPrice": totalPrice}
    data = applayout.render(info)
    return f'{data}'


@app.route('/cart/delete/<productId>')
def deleteCommand(productId):
    component.deleteObject("commands.bin", productId)

    return redirect('/cart')


@app.route('/cart/deleteAll')
def deleteAllCommands():
    component.deleteFileContent("commands.bin")
    return redirect('/cart')
