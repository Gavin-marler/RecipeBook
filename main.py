import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def access():
    userName = input("Please Enter Your User Name: ")
    userAccount = db.collection("users").where(u'Name', u'==', userName)
    result = userAccount.get()

    if result:
        user = result[0]
        enterPassword(user, userName)
    else:
        newAccount = input("User Name does not exist. Would you like to create a new accout? (y/n)\n")
        if newAccount != 'y':
            print("Goodbye")
        else:
            newUser(userName)

def enterPassword(user, userName):
    password = input("Password: ")
    value = user.to_dict()
    if value["password"] != password:
        print("Password Incorrect. Goodbye")
    else:
        print("Welcome")
        options(userName)

def newUser(userName):
    password = input("Enter a Password: ")
    values = {"Name" : userName, "password" : password}
    newUser = db.collection("users").document(userName)
    newUser.set(values)

def options(userName):
    print("Select option:")
    select()
    option = ' '
    while option != 'q':
        option = input("> ")
        if option == 'a':
            addRecipe(userName)
        elif option == 'b':
            viewRecipe(userName)
        elif option == 'c':
            display(userName)
        elif option == 'd':
            editRecipe(userName)
        elif option == 'e':
            deleteRecipe(userName)
        elif option == 'q':
            print("Goodbye")
        else:
            print("Please try again.")

def select():
    print("a. Add Recipe")
    print("b. View Recipe")
    print("c. View All Recipes")
    print("d. Edit Recipe")
    print("e. Delete Recipe")
    print("q. Exit")
    print()

def addRecipe(userName):
    print("\nPlease enter the Name and Description of your recipe\n")
    name = input("Name: ")
    description = input("Description: ")
    value = {"name" : name, "description" : description}
    db.collection("users").document(userName).collection("description").document(name).set(value)

def viewRecipe(userName):
    name = input("Name: ")
    result =  db.collection("users").document(userName).collection("description")
    document = result.get()
    if document:
        found = result.where("name", "==", name).get()
        if found:
            for elements in found:
                description = elements.to_dict()
                print(f"Description: " + description["description"])
        else:
            add = input("Recipe doesn't exist. Add it? (y/n)")
            if add == 'y':
                addRecipe(userName)
    else:
        print("RecipeBook Empty")

def display(userName):
    snapshot = db.collection("users").document(userName).collection("description").get()
    for x in snapshot:
        info = x.to_dict()
        print(f"Name: " + info["name"])
        print(f"description: " + info["description"])
        print("")

def editRecipe(userName):
    name = input("Name: ")
    result =  db.collection("users").document(userName).collection("description")
    document = result.get()
    if document:
        password = input("Enter new description: ")
        found = result.document(name).update({"description" : description})
        if found:
            print("Recipe updated Successfully")
        else:
            add = input("Recipe doesn't exist. Add it? (y/n)")
            if add == 'y':
                addRecipe(userName)
    else:
        print("RecipeBook Empty")

def deleteRecipe(userName):
    name = input("Name: ")
    result =  db.collection("users").document(userName).collection("description")
    document = result.get()
    if document:
        found = result.document(name).delete()
        if found:
            print("Recipe deleted Successfully")
        else:
            print("Recipe doesn't exist.")
    else:
        print("RecipeBook Empty")

def main():
    print("Welcome to the RecipeBook\n")
    access()

if __name__ == "__main__":
    main()