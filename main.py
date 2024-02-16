import re
from datetime import datetime
import json

DATABASE_FILE_NAME = "AddressBook.json"

data = {
    "Ivan":
        {
            "phone": ["1234567890"],
            "email": "ivan1990@gmail.com",
            "birthday": "01.01.1990",
            "address": "vul. Moya 155",
        }
}


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, KeyError, ValueError, IndexError) as e:
            return f"Error: {e}"

    return wrapper


def hello():
    return "How can I help you?"


@input_error
def add_name(name: str):
    if name in data:
        return "This name is already in the contact list!"
    else:
        data[name] = {"address": None, "phone": [], "email": None, "birthday": None}
        return f"{name} added to contacts"


@input_error
def add_phone(name: str, phone):
    if len(phone) != 10 and phone.isdigit():
        raise ValueError("The phone must have 10 digits.")
    if name not in data:
        return "Name not found in contacts!"
    else:
        record = data.get(name)
        list_phone = record.get("phone")
        list_phone.append(phone)

        record.update({"phone": list_phone})
        data.update({name: record})
        return f"Contact '{name}' with phone number '{phone}' added successfully."


@input_error
def add_birthday(name: str, str_birthday):
    def is_valid_birthday(str_birthday):
        if str_birthday is None:
            return True
        try:
            datetime.strptime(str_birthday, '%Y-%m-%d').date()
            return True
        except ValueError:
            return False

    # def convert_birthday(str_birthday):
    #     return datetime.strptime(str_birthday, '%Y-%m-%d').date()

    if name not in data:
        return "Name not found in contacts!"
    else:
        # birthday = convert_birthday(str_birthday)
        # print(birthday)
        # print(type(birthday))

        if is_valid_birthday(str_birthday):
            record = data.get(name)
            # record.update({"birthday": birthday})
            record.update({"birthday": str_birthday})
            data.update({name: record})
            return f"Date of birth added to {name} contact"
        else:
            return f"Incorrect date of birth format. Must be yyyy-mm-dd"


@input_error
def add_email(name: str, email):
    def is_valid_email(email):
        pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    if name not in data:
        return "Name not found in contacts!"
    else:
        if is_valid_email(email):
            record = data.get(name)
            print("record", record)
            record.update({"email": email})
            print("record", record)
            data.update({name: record})
            return f"Contact '{name}' with email '{email}' added successfully."
        else:
            return "Wrong email."


@input_error
def add_address(name: str, *address):
    print("add_address")
    if name not in data:
        return "Name not found in contacts!"
    else:
        record = data.get(name)
        record.update({"address": list(address)})
        data.update({name: record})

        return f"Address added to {name} contact list"


@input_error
def change_phone(name, phone):
    if name not in data:
        return "Name not found in contacts!"
    else:
        data[name] = phone
        return f"Phone number for '{name}' changed to '{phone}'."


@input_error
def get_phone(name):
    if name not in data:
        return "Name not found in contacts!"
    else:
        return f"The phone number for '{name}' is {data[name]}."


def show_all():
    if not data:
        return "No contacts available."

    result = "All contacts:\n"
    for name, record in data.items():
        result += f"{name}: {record}\n"
    return result


def good_bye():
    try:
        save_to_file(DATABASE_FILE_NAME)
        print("The address book is saved to disk.")
    except Exception as e:
        print(type(e).__name__, e)

    return "Good bye!"


def default_handler():
    return "Unknown command. Please try again."


def my_help():
    return ("You can use these commands:\n"
            "hello\n"
            # "add all Name phone birthday email address\n"

            "add name Name\n"
            "add adr street house apartment \n"
            "add phone 1234567890\n"
            "add email some-email@gmail.com\n"
            "add brd YYYY-MM-DD\n"

            # "change name phone\n"
            # "phone name\n"

            "show all\n"
            "good bye\n"
            "close\n"
            "exit\n"
            )


commands = {
    "hello": hello,
    "help": my_help,

    # "change ": change_phone,
    # "phone ": get_phone,
    "show all": show_all,
    "good bye": good_bye,
    "close": good_bye,
    "exit": good_bye,

    "add name": add_name,
    "add adr": add_address,
    "add phone": add_phone,
    "add email": add_email,
    "add brd": add_birthday,

}


@input_error
def parse_command(user_input: str):
    command, args = None, []
    user_input = user_input.lower()

    for cmd in commands:
        if user_input.startswith(cmd):
            command = cmd
            args = user_input.replace(cmd, "").split()
            if len(args) >= 1:
                args[0] = args[0].capitalize()  # name with a capital letter

    return command, args


@input_error
def handle_command(command, *args):
    return commands.get(command, default_handler)(*args)


def save_to_file(file_name: str):
    with open(file_name, "w") as file:
        json.dump(data, file)


def loading_from_file(file_name: str):
    # self.data = {}
    global data
    with open(file_name, "r") as file:
        data = json.load(file)


def main():
    try:
        loading_from_file(DATABASE_FILE_NAME)
        print("Loaded from file!")
    except Exception as e:
        print(type(e).__name__, e)

    while True:
        user_input = input("Enter command: ")

        command, args = parse_command(user_input)
        print("command: ", command)
        print("args: ", args)

        result = handle_command(command, *args)
        print(result)

        if result == "Good bye!":
            break


if __name__ == "__main__":
    main()
