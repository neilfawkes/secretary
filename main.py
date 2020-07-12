from pprint import pprint


def people_func(document_number, documents):
    temp = []
    for i in documents:
        if i['number'] == document_number:
            print()
            print(i['name'])
        else:
            temp.append(1)
        if len(temp) == len(documents):
            print("Document number doesn't exist.")


def list_func(documents):
    print()
    for i in documents:
        print(f'{i["type"]}, {i["number"]}, {i["name"]}')


def shelf_func(document_number, directories):
    temp = []
    for shelf_number, doc_numbers in directories.items():
        if doc_numbers.count(document_number) > 0:
            print()
            print(f'This document is on the shelf №{shelf_number}.')
            temp.append(1)
    if len(temp) == 0:
        print("Document number doesn't exist.")


def add_func(documents, directories, new_number, new_type, new_name, new_shelf):
    if directories.get(new_shelf) == None:
        print("The desired shelf doesn't exist!")
        if input("Do you want to create the shelf with this number? y/n: ") == 'y':
            add_shelf_func(new_shelf, directories, documents)
        else:
            print("Document not added because the shelf doesn't exist.")
    else:
        documents.append({"type": new_type, "number": new_number, "name": new_name})
        directories[new_shelf].append(new_number)
        documents_rewrite(documents)
        directories_rewrite(directories)
        print('New document added successfully!')


def delete_func(document_number, documents, directories):
    temp = []
    counter = 0
    for i in documents:
        if i['number'] == document_number:
            del(documents[counter])
            for doc_numbers in directories.values():
                if doc_numbers.count(document_number) > 0:
                    doc_numbers.remove(document_number)
            documents_rewrite(documents)
            directories_rewrite(directories)
            print('Document deleted successfully!')
            temp = []
            break
        else:
            temp.append(1)
        counter += 1
    if len(temp) == len(documents):
        print("Document number doesn't exist.")


def move_func(document_number, shelf_number, directories, documents):
    temp = []
    if directories.get(shelf_number) == None:
        print("The desired shelf doesn't exist!")
        if input("Do you want to create the shelf with this number? y/n ") == 'y':
            add_shelf_func(shelf_number, directories, documents)
    else:
        for shelf_number, doc_numbers in directories.items():
            if doc_numbers.count(document_number) > 0:
                doc_numbers.remove(document_number)
                temp.append(1)
                directories[shelf_number].append(document_number)
                documents_rewrite(documents)
                directories_rewrite(directories)
        if len(temp) == 0:
            print("Document number doesn't exist.")
        else:
            print('Document moved successfully!')


def add_shelf_func(shelf_number, directories, documents):
    if directories.get(shelf_number) == None:
        directories[shelf_number] = list()
        directories_rewrite(directories)
        print(f'New shelf №{shelf_number} added successfully!')
        if input('Do you want to add new document to this shelf? y/n ') == 'y':
            add_func(documents, directories, new_number = input('Input document number: '),
                new_type = input('Input document type: '),
                new_name = input("Input owner's name: "),
                new_shelf = shelf_number)
    else:
        print('The shelf with this number already exists.')


def show_all(directories):
    pprint(directories)


def welcome():
    with open("welcome.txt") as welcome:
        print(welcome.read())
    user_input = input('Input a command or type "help" to see the list of commands: ').lower()
    return user_input


def help_func():
    print("", "'p' – people – search a person by inputting the document number",
    "'l' – list – prints the list of all existing documents",
    "'s' – shelf – search the shelf by inputting the document number",
    "'a' – add – add a new document (input the number, type, owner's name and the number of shelf)",
    "'d' – delete – delete a document by inputting a number",
    "'m' – move – move a document to a new shelf",
    "'as' – add shelf – add a new shelf to the list of directories",
    "'sa' – show all – prints all existing shelves",
    "'ol' - show all owners' names",
    "'q' - quit the program", "", sep = '\n')
    user_input = input("Do you want to exit the help section? y/n: ")
    if user_input == 'y':
        main()


def documents_function():
    with open("documents.txt") as doc_file:
        list_of_documents = list(doc_file.read().split("\n\n"))
        documents = []
        list_of_documents = [x for x in list_of_documents if x != ""]
        for document_lines in list_of_documents:
            documents_dict = {"name": document_lines.split("\n")[0],
            "type": document_lines.split("\n")[1],
            "number": document_lines.split("\n")[2]}
            documents.append(documents_dict)
    for dicts in documents:
        if dicts["name"] == "":
            del(dicts["name"])
    # pprint(documents)
    return documents


def directories_function():
    with open("directories.txt") as dir_file:
        list_of_directories = list(dir_file.read().split("\n\n"))
        directories = {}
        list_of_directories = [x for x in list_of_directories if x != ""]
        for directories_line in list_of_directories:
            directories_list = list(directories_line.split("\n")[1:])
            directories[directories_line[0]] = directories_list
    # pprint(directories)
    return directories


def documents_rewrite(documents):
    with open("documents.txt", "w") as doc_file:
        for doc_lines in documents:
            doc_file.write(doc_lines.get("name") + "\n")
            doc_file.write(doc_lines.get("type") + "\n")
            doc_file.write(doc_lines.get("number") + "\n")
            doc_file.write("\n")


def directories_rewrite(directories):
    with open("directories.txt", "w") as dir_file:
        for key, value in directories.items():
            dir_file.write(key + "\n")
            for line in value:
                dir_file.write(line + "\n")
            dir_file.write("\n")


def owners_list(documents):
    for names in documents:
        try:
            print(names["name"])
        except KeyError:
            print("Owner's name not found!")


def main():
    documents = documents_function()
    directories = directories_function()
    try:
        for lines in documents:
            lines["name"]
    except KeyError:
        print("Warning: some documents have no owner's name!")

    user_input = welcome()
    if user_input == 'help':
        help_func()
    elif user_input == 'p':
        people_func(input('Input the document number: '), documents)
    elif user_input == 'l':
        list_func(documents)
    elif user_input == 's':
        shelf_func(input('Input the document number: '), directories)
    elif user_input == 'a':
        add_func(documents, directories,
            new_number = input('Input document number: '),
            new_type = input('Input document type: '),
            new_name = input("Input owner's name: "),
            new_shelf = input('Input shelf number: '))
    elif user_input == 'd':
        delete_func(input('Input the document number: '), documents, directories)
    elif user_input == 'm':
        move_func(input("Input the document number: "), input('Input the number of the desired shelf: '), directories, documents)
    elif user_input == 'as':
        add_shelf_func(input('Input the number of the new shelf: '), directories, documents)
    elif user_input == 'sa':
        show_all(directories)
    elif user_input == 'ol':
        owners_list(documents)
    elif user_input == 'q':
        print("Goodbye!")
    else:
        print("Invalid command!")


if __name__ == '__main__':
    main()