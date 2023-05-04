from tkinter import *
from tkinter import ttk
import tkinter as tk
from helpers import connect

from Product import *


db = connect()


window = tk.Tk()
window.title("RiBazar")
window.geometry("1600x700")


def existsId(id):
    rows = db.find()
    for x in rows:
        if x.get("id") == int(id):
            return True
    return False


def getMaxId():
    rows = db.find().sort("id", -1).limit(1)
    maxId = 0
    for x in rows:
        maxId = x.get("id")

    return maxId + 1


def openInsertFrame():
    mainFrame.pack_forget()

    insertFrame.pack()
    insertTitle.pack()
    nameProductLabel.pack()
    nameProductEntry.pack()
    priceProductLabel.pack()
    priceProductEntry.pack()
    briefDescriptionProductLabel.pack()
    briefDescriptionProductEntry.pack()
    descriptionProductLabel.pack()
    descriptionProductText.pack()
    relevantProductLabel.pack()
    relevantProductCheckbutton.pack()
    valorationProductLabel.pack()
    valorationProductEntry.pack()
    imageUrlLabel.pack()
    imageUrlEntry.pack()
    statusSave.pack()
    insertProductButton.pack()
    backInsertToMainButton.pack()


def backInsertToMain():
    nameProductEntry.delete(0, tk.END)
    priceProductEntry.delete(0, tk.END)
    briefDescriptionProductEntry.delete(0, tk.END)
    descriptionProductText.delete('1.0', tk.END)
    valorationProductEntry.delete(0, tk.END)
    imageUrlEntry.delete(0, tk.END)
    statusSave.config(text="")

    insertFrame.pack_forget()
    mainFrame.pack()


def insertProduct():
    try:
        name = nameProductEntry.get()
        price = float(priceProductEntry.get())
        if price < 0:
            raise Exception
        briefDescription = briefDescriptionProductEntry.get()

        description = descriptionProductText.get(1.0, tk.END).replace("\n", "")
        if relevantVar.get() == 1:
            relevant = True
        else:
            relevant = False
        valoration = float(valorationProductEntry.get())
        if valoration < 0 or valoration > 5:
            raise Exception
        imageUrl = imageUrlEntry.get()
        p1 = Product(getMaxId(), name, price, briefDescription, description, relevant, valoration, imageUrl)
        db.insert_one(p1.__dict__)
        statusSave.config(text="Product created successfully")
        nameProductEntry.delete(0, tk.END)
        priceProductEntry.delete(0, tk.END)
        briefDescriptionProductEntry.delete(0, tk.END)
        descriptionProductText.delete(1.0, tk.END)
        relevantProductCheckbutton.deselect()
        valorationProductEntry.delete(0, tk.END)
        imageUrlEntry.delete(0, tk.END)
    except:
        statusSave.config(text="Some data is incorrect")


def openShowProductsFrame():
    mainFrame.pack_forget()

    try:
        productsTree.delete(*productsTree.get_children())
        for product in db.find():
            productsTree.insert('', 'end', text="1", values=(
                product.get("id"), product.get("name"), product.get("price"), product.get("briefDescription"),
                product.get("description"), product.get("relevant"), product.get("valoration"),
                product.get("imageUrl")))
        statusShow.config(text="")
    except:
        statusShow.config(text="Something gone wrong")

    showFrame.pack()
    showProductsTitle.pack()
    productsTree.pack()
    statusShow.pack()
    backShowToMainButton.pack()


def backShowToMain():
    productsTree.delete(*productsTree.get_children())
    showFrame.pack_forget()
    mainFrame.pack()


def openDeleteForm():
    mainFrame.pack_forget()

    deleteFrame.pack()
    idDeleteLabel.pack()
    idDeleteEntry.pack()
    deleteProductButton.pack()
    statusDelete.pack()
    backDeleteToMainButton.pack()


def backDeleteToMain():
    deleteFrame.pack_forget()

    idDeleteEntry.delete(0, tk.END)
    statusDelete.config(text="")

    mainFrame.pack()


def deleteProduct():
    try:
        idDelete = int(idDeleteEntry.get())
        if existsId(idDelete):
            deleteQuery = {"id": idDelete}

            db.delete_one(deleteQuery)
            statusDelete.config(text="Product deleted successfully")
            idDeleteEntry.delete(0, tk.END)
        else:
            statusDelete.config(text="No product with this ID")
    except:
        statusDelete.config(text="Something gone wrong")


def modifyProduct():
    try:
        newName = nameProductModifyEntry.get()
        newPrice = priceProductModifyEntry.get()
        newBriefDescription = briefDescriptionProductModifyEntry.get()
        newDescription = descriptionProductModifyText.get(1.0, tk.END).replace("\n", "")
        if relevantVarModify.get() == 1:
            newRelevant = True
        else:
            newRelevant = False
        newValoration = float(valorationProductModifyEntry.get())
        if newValoration < 0 or newValoration > 5:
            raise Exception
        newURLImage = imageUrlModifyEntry.get()

        modifiedProduct = Product(int(idModifyEntry.get()), newName, newPrice, newBriefDescription, newDescription,
                                  newRelevant, newValoration, newURLImage)

        modifyquery = {"id": int(idModifyEntry.get())}
        newProductValues = {"$set": modifiedProduct.__dict__}
        db.update_one(modifyquery, newProductValues)
        statusModify.config(text="Product updated successfully")
    except:
        statusModify.config(text="Something gone wrong")



def openModifyForm():
    mainFrame.pack_forget()

    modifyFrame.pack()
    modifyTitle.pack()
    idModifyLabel.pack()
    idModifyEntry.pack()
    statusSearchModify.pack()
    searchIdProductButton.pack(pady=10)
    nameProductModifyLabel.pack()
    nameProductModifyEntry.pack()
    priceProductModifyLabel.pack()
    priceProductModifyEntry.pack()
    briefDescriptionProductModifyLabel.pack()
    briefDescriptionProductModifyEntry.pack()
    descriptionProductModifyLabel.pack()
    descriptionProductModifyText.pack()
    relevantProductModifyLabel.pack()
    relevantProductModifyCheckbutton.pack()
    valorationProductModifyLabel.pack()
    valorationProductModifyEntry.pack()
    imageUrlModifyLabel.pack()
    imageUrlModifyEntry.pack()
    statusModify.pack()
    modifyProductButton.pack()
    backModifyToMainButton.pack()


def backModifyToMain():
    modifyFrame.pack_forget()

    idModifyEntry.delete(0, tk.END)
    statusSearchModify.config(text="")
    nameProductModifyEntry.delete(0, tk.END)
    priceProductModifyEntry.delete(0, tk.END)
    briefDescriptionProductModifyEntry.delete(0, tk.END)
    descriptionProductModifyText.delete('1.0', tk.END)
    valorationProductModifyEntry.delete(0, tk.END)
    imageUrlModifyEntry.delete(0, tk.END)
    statusModify.config(text="")

    mainFrame.pack()

def searchProductModify():
    nameProductModifyEntry.delete(0, tk.END)
    priceProductModifyEntry.delete(0, tk.END)
    briefDescriptionProductModifyEntry.delete(0, tk.END)
    descriptionProductModifyText.delete('1.0', tk.END)
    valorationProductModifyEntry.delete(0, tk.END)
    imageUrlModifyEntry.delete(0, tk.END)
    statusModify.config(text="")
    idSearch = idModifyEntry.get()

    if existsId(idSearch):
        try:
            query = {"id": int(idSearch)}
            row = db.find(query)
            for product in row:
                nameProductModifyEntry.insert(0, product.get("name"))
                priceProductModifyEntry.insert(0, product.get("price"))
                briefDescriptionProductModifyEntry.insert(0, product.get("briefDescription"))
                descriptionProductModifyText.insert('1.0', product.get("description"))
                valorationProductModifyEntry.insert(0, product.get("valoration"))
                imageUrlModifyEntry.insert(0, product.get("imageUrl"))
        except:
            statusSearchModify.config(text="Something gone wrong")
    else:
        statusSearchModify.config(text="No product with this ID")


def exitForm():
    window.destroy()


# MAIN FORM
mainFrame = tk.Frame(window, padx=10, pady=50)
mainFrameLabelTitle = tk.Label(mainFrame, text="RIBAZAR PRODUCT CONTROL PANEL", font="Helvetica 16 bold")
insertFormButton = tk.Button(mainFrame, text="INSERT PRODUCT", command=openInsertFrame)
showProductsFormButton = tk.Button(mainFrame, text="SHOW PRODUCTS", command=openShowProductsFrame)
deleteFormButton = tk.Button(mainFrame, text="DELETE PRODUCT", command=openDeleteForm)
modifyFormButton = tk.Button(mainFrame, text="MODIFY PRODUCT", command=openModifyForm)
exitFormButton = tk.Button(mainFrame, text="EXIT", command=exitForm)

mainFrame.pack()
mainFrameLabelTitle.pack(pady=20)
insertFormButton.pack()
showProductsFormButton.pack()
modifyFormButton.pack()
deleteFormButton.pack()
exitFormButton.pack(pady=10)

# INSERT FRAME
insertFrame = tk.Frame(window, padx=10, pady=30)

insertTitle = tk.Label(insertFrame, text="INSERT PRODUCT", font="Helvetica 16 bold")
nameProductLabel = tk.Label(insertFrame, text="Name")
nameProductEntry = tk.Entry(insertFrame)
priceProductLabel = tk.Label(insertFrame, text="Price")
priceProductEntry = tk.Entry(insertFrame)
briefDescriptionProductLabel = tk.Label(insertFrame, text="Brief Description")
briefDescriptionProductEntry = tk.Entry(insertFrame)
descriptionProductLabel = tk.Label(insertFrame, text="Description")
descriptionProductText = tk.Text(insertFrame, width=20, height=6)
relevantVar = tk.IntVar()
relevantProductLabel = tk.Label(insertFrame, text="Relevant")
relevantProductCheckbutton = tk.Checkbutton(insertFrame, text="", variable=relevantVar)
valorationProductLabel = tk.Label(insertFrame, text="Valoration")
valorationProductEntry = tk.Entry(insertFrame)
imageUrlLabel = tk.Label(insertFrame, text="URL Image")
imageUrlEntry = tk.Entry(insertFrame)
statusSave = tk.Label(insertFrame, text="")
insertProductButton = tk.Button(insertFrame, text="INSERT PRODUCT", command=insertProduct)
backInsertToMainButton = tk.Button(insertFrame, text="MAIN MENU", command=backInsertToMain)

# SHOW PRODUCTS FRAME
showFrame = tk.Frame(window, padx=10, pady=30)

showProductsTitle = tk.Label(showFrame, text="PRODUCTS LIST", font="Helvetica 16 bold")
productsTree = ttk.Treeview(showFrame, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"), show='headings')
treeScrollY = ttk.Scrollbar(showFrame)
treeScrollY.configure(command=productsTree.yview)
productsTree.configure(yscrollcommand=treeScrollY.set)
treeScrollY.pack(side=RIGHT, fill=BOTH)
productsTree.column("# 1", anchor=CENTER)
productsTree.heading("# 1", text="ID")
productsTree.column("# 2", anchor=CENTER)
productsTree.heading("# 2", text="NAME")
productsTree.column("# 3", anchor=CENTER)
productsTree.heading("# 3", text="PRICE")
productsTree.column("# 4", anchor=CENTER)
productsTree.heading("# 4", text="BRIEF DESCRIPTION")
productsTree.column("# 5", anchor=CENTER)
productsTree.heading("# 5", text="DESCRIPTION")
productsTree.column("# 6", anchor=CENTER)
productsTree.heading("# 6", text="RELEVANT")
productsTree.column("# 7", anchor=CENTER)
productsTree.heading("# 7", text="VALORATION")
productsTree.column("# 8", anchor=CENTER)
productsTree.heading("# 8", text="IMAGE URL")
statusShow = tk.Label(showFrame, text="")
backShowToMainButton = tk.Button(showFrame, text="MAIN MENU", command=backShowToMain)

# DELETE FRAME
deleteFrame = tk.Frame(window, padx=10, pady=30)

deleteTitle = tk.Label(deleteFrame, text="DELETE PRODUCT", font="Helvetica 16 bold")
idDeleteLabel = tk.Label(deleteFrame, text="ID")
idDeleteEntry = tk.Entry(deleteFrame)
deleteProductButton = tk.Button(deleteFrame, text="DELETE", command=deleteProduct)
statusDelete = tk.Label(deleteFrame, text="")
backDeleteToMainButton = tk.Button(deleteFrame, text="MAIN MENU", command=backDeleteToMain)

# MODIFY FRAME
modifyFrame = tk.Frame(window, padx=10, pady=30)

modifyTitle = tk.Label(modifyFrame, text="MODIFY PRODUCT", font="Helvetica 16 bold")
idModifyLabel = tk.Label(modifyFrame, text="Product ID")
idModifyEntry = tk.Entry(modifyFrame)
statusSearchModify = tk.Label(modifyFrame, text="")
searchIdProductButton = tk.Button(modifyFrame, text="SEARCH", command=searchProductModify)
nameProductModifyLabel = tk.Label(modifyFrame, text="Name")
nameProductModifyEntry = tk.Entry(modifyFrame)
priceProductModifyLabel = tk.Label(modifyFrame, text="Price")
priceProductModifyEntry = tk.Entry(modifyFrame)
briefDescriptionProductModifyLabel = tk.Label(modifyFrame, text="Brief Description")
briefDescriptionProductModifyEntry = tk.Entry(modifyFrame)
descriptionProductModifyLabel = tk.Label(modifyFrame, text="Description")
descriptionProductModifyText = tk.Text(modifyFrame, width=20, height=6)
relevantVarModify = tk.IntVar()
relevantProductModifyLabel = tk.Label(modifyFrame, text="Relevant")
relevantProductModifyCheckbutton = tk.Checkbutton(modifyFrame, text="", variable=relevantVarModify)
valorationProductModifyLabel = tk.Label(modifyFrame, text="Valoration")
valorationProductModifyEntry = tk.Entry(modifyFrame)
imageUrlModifyLabel = tk.Label(modifyFrame, text="URL Image")
imageUrlModifyEntry = tk.Entry(modifyFrame)
statusModify = tk.Label(modifyFrame, text="")
modifyProductButton = tk.Button(modifyFrame, text="MODIFY PRODUCT", command=modifyProduct)
backModifyToMainButton = tk.Button(modifyFrame, text="MAIN MENU", command=backModifyToMain)

window.mainloop()
