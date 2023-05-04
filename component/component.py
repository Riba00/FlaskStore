import pickle


def saveObject(object1, filePath):
    with open(filePath, "ab") as file:
        pickle.dump(object1, file)
    file.close()


def restoreObject(index, filePath):
    with open(filePath, "rb") as file:
        while True:
            try:
                object1 = pickle.load(file)
            except EOFError:
                break
            if object1.id == index:
                return object1
    file.close()


def updateObject(filePath, id, newObject):
    objects = []
    with open(filePath, "rb") as file:
        while True:
            try:
                object1 = pickle.load(file)
                objects.append(object1)
            except EOFError:
                break
    file.close()
    for o in objects:
        if o.id == id:
            saveObject(newObject, filePath)
        else:
            saveObject(o, filePath)


def deleteObject(filePath, id):
    objects = []
    with open(filePath, "rb") as file:
        while True:
            try:
                object1 = pickle.load(file)
                objects.append(object1)

            except EOFError:
                break
    file.close()
    deleteFileContent(filePath)
    for o in objects:
        if o.idProduct != id:
            saveObject(o, filePath)
            print(o.__dict__)


def deleteFileContent(file):
    with open(file, "wb") as file:
        pass
    file.close()


def getAll(filePath):
    data = []
    with open(filePath, "rb") as file:
        while True:
            try:
                object1 = pickle.load(file)
                data.append(object1)
            except EOFError:
                break
        file.close()
        return data


def updateCommand(filePath, idProduct, quantity):
    objects = []
    with open(filePath, "rb") as file:
        while True:
            try:
                object1 = pickle.load(file)
                objects.append(object1)
            except EOFError:
                break
    file.close()
    deleteFileContent(filePath)
    for o in objects:
        if o.idProduct == idProduct:
            o.quantity = int(o.quantity) + int(quantity)
            deleteObject(filePath,idProduct)
            saveObject(o, filePath)
        else:
            saveObject(o, filePath)


def restoreCommand(index, filePath):
    with open(filePath, "rb") as file:
        while True:
            try:
                object1 = pickle.load(file)
            except EOFError:
                break
            if object1.idProduct == index:
                return object1
    file.close()
