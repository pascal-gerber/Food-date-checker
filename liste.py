from tkinter import *
import time

amountVar = 1

def createWindow():
    global allFoodDates
    window = Tk()

    allFoodDates = Text(window, width=50)
    allFoodDates.grid(row=0, column=0, columnspan=3)

    createNewItem = Button(window, command=createNewObject, text="Create new", height = 5, width = 15, bg="Lime")
    createNewItem.grid(row=1, column=0)

    deleteItem = Button(window, command=deleteObject, text = "delete Item", height = 5, width = 15, bg="crimson")
    deleteItem.grid(row=1, column=1)

    searchItems = Button(window, command=searchItem,text="🔎", height = 5, width = 15, bg="grey")
    searchItems.grid(row=1, column=2)

    update()
    
    window.title("foods and expiration")
    window.geometry("500x500")
    window.mainloop()

def checkAllDates():
    pass

def createNewObject():
    global amountVar
    global amount
    
    itemCreation = Tk()

    gridding = Label(itemCreation, width = 50, height = 30, bg="yellow")
    gridding.grid(row = 0, column=0, rowspan = 20, columnspan = 5)

    objName = Label(itemCreation, text="Name", bg="yellow")
    objName.grid(row = 1, column=0)

    reqName = Entry(itemCreation)
    reqName.grid(row = 2, column=0)

    objDate = Label(itemCreation, text="Date\nDD.MM.YYYY or\nDD MM YYYY", bg="yellow")
    objDate.grid(row = 1, column=1)
    
    reqDate = Entry(itemCreation)
    reqDate.grid(row = 2, column=1)

    amount = Label(itemCreation, text=amountVar, bg="yellow")
    amount.grid(row = 2, column=3)

    more = Button(itemCreation, text = "🔺", command=lambda change = change: change(1), height = 5, width = 10, bg="cyan")
    more.grid(row = 1, column=3)
    
    less = Button(itemCreation, text = "🔻", command=lambda change = change: change(-1), height = 5, width = 10, bg="cyan")
    less.grid(row = 3, column=3)

    confirm = Button(itemCreation, text="Create", bg="Lime", width = 30, height = 5,
                     command = lambda reqName = reqName, reqDate = reqDate: addNewItem(reqName.get(), reqDate.get()))
    confirm.grid(row = 3, column=0, columnspan=2)

    itemCreation.configure(bg = "yellow")
    itemCreation.title("create New item")
    itemCreation.geometry("500x500")
    itemCreation.mainloop()

def deleteObject():
    with open("data.txt", "r") as info:
        allLines = info.read().split("\n")[:-1]

    deleteInterface = Tk()

    cordY = 0
    cordX = 0
    coords = -1

    for each in allLines:
        coords += 1
        cordY = coords // 3
        cordX = coords % 3
        deleteMe = Button(deleteInterface, text=each, width = 20, bg = "crimson")
        deleteMe.configure(command=lambda deleteMe = deleteMe, each = each:breakPiece(deleteMe, each))
        deleteMe.grid(row=cordY, column=cordX)

    deleteInterface.title("delete objects")
    deleteInterface.geometry("500x500")
    deleteInterface.mainloop()

def breakPiece(boutton, text):
    boutton.destroy()
    with open("data.txt", "r") as info:
        allLines = info.read().split("\n")[:-1]

    allLines.remove(text)
    
    changedList = "\n".join(allLines) + "\n"

    with open("data.txt", "w") as info:
        info.write(changedList)

    update()

def searchItem():
    pass

def addNewItem(name, date):
    global amountVar
    inputDate = date.replace(".", " ")
    
    configuredDate = time.strptime(inputDate, "%d %m %Y")

    seconds = int(time.mktime(configuredDate))
    
    with open("data.txt", "a") as note:
        lineOfFoods = (str(str(seconds)) + " " + name + "\n") * amountVar
        note.write(lineOfFoods)

    update()

def change(num):
    global amountVar
    global amount
    if amountVar + num != 0:
        amountVar += num
        amount.configure(text = str(amountVar))

def update():
    global allFoodDates

    endResult = ""
    
    with open("data.txt", "r") as info:
        allLines = info.read().split("\n")[:-1]

    if len(allLines) == 0:
        allFoodDates.insert('1.0', "No food")

    else:
        for each in allLines:
            timeTill = each.split(" ")
            now = int(time.time())
            daysLeft = int((int(timeTill[0]) - now) // 86400) + 1
            if daysLeft > 0:
                inDays = str(daysLeft) + " days left"
            elif daysLeft == 0:
                inDays = "Today"
            else:
                inDays = str(daysLeft) + " days over"
                
            endResult += inDays + " " + timeTill[1] + "\n"

    
        endResultSorted = endResult.split("\n")

        before = []
        now = []
        after = []
        
        for each in endResultSorted:
            if len(each) < 2:
                continue
            if each[0] == "-":
                before.append(each)
            elif each[0] == "T":
                now.append(each)
            else:
                after.append(each)

        before.sort()
        now.sort()
        after.sort()

        endResultSorted = before[::-1] + now + after
        
        endResultSorted = "\n".join(endResultSorted)

        while endResultSorted[0] == "\n":
            endResultSorted = endResultSorted[1:]
            
        allFoodDates.delete('1.0','end')

        allFoodDates.insert('1.0', endResultSorted)
    
    


createWindow()


