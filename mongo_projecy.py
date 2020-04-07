import pymongo
import os
import env as config

MONGO_URI = os.environ.get("MONGO_URI")
DBS_NAME = "myTestDB"
COLLECTION_NAME = "myFirstMDB"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


def show_menu():
    print('')
    print("1. Add a Record")
    print("2. Find a Record by Name")
    print("3. Edit a Record")
    print("4. Delete a Record")
    print("5. Exit")

    option = input("Enter an Option: ")
    return option


def get_record():
    print("")
    first = input("Please Enter First Name: ")
    last = input("Please Enter Last Name: ")

    try:
        doc = coll.find_one({'first': first.lower(), 'last': last.lower()})
    except:
        print("Error Accessing DB")

    if not doc:
        print('')
        print('Error! No Results Found.')

    return doc


def add_record():
    print("")
    first = input("Please Enter First Name: ")
    last = input("Please Enter Last Name: ")
    dob = input("Please Enter Date of Birth: ")
    gender = input("Please Enter Gender: ")
    hair_colour = input("Please Enter Hair Colour: ")
    occupation = input("Please Enter Occupation:  ")
    nationality = input("Please Enter Nationality: ")

    new_doc = {'first': first.lower(), 'last': last.lower(), 
    'dob': dob, 'gender': gender.upper(), 'hair_colour': hair_colour.lower(), 
    'occupation': occupation.lower(), 'nationality': nationality.lower()}

    try:
        coll.insert(new_doc)
        print('')
        print('Document Inserted')
    except:
        print("Error Accessing DB")


def find_record():
    doc = get_record()
    if doc:
        print('')
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ': ' + v.capitalize())


def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}
        print('')
        for k, v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + ' [' + v + ']: ')
                if update_doc[k] == "":
                    update_doc[k] = v

        try:
            coll.update_one(doc, {'$set': update_doc})
            print("")
            print("Document Updated!")
        except:
            print("Error Accessing DB")


def delete_record():
    doc = get_record()
    if doc:
        print('')
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())

        print('')
        confirmation = input("Is this the document you want to delete?\nY or N: ")
        print('')

        if confirmation.lower() == 'y':
            try:
                coll.remove(doc)
                print("Document Deleted!")
            except:
                print("Error Accessing Database")
        else:
            print("Document Not deleted!")


def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            # print("You have Selected Option 1")
            add_record()
        elif option == "2":
            # print("You have Selected Option 2")
            find_record()
        elif option == "3":
            # print("You have Selected Option 3")
            edit_record()
        elif option == "4":
            #print("You have Selected Option 4")
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid Option")


conn = mongo_connect(MONGO_URI)
coll = conn[DBS_NAME][COLLECTION_NAME]

main_loop()
