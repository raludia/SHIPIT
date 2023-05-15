""" A module for the presentation layer """

import os
import typing as t
from src.commands import Command

class Option:
    def __init__(
        self, name: str, command: Command, prep_call: t.Optional[t.Callable] = None
    ):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        result = self.command.execute(data) if data else self.command.execute()
        if isinstance(result, list):
            for line in result:
                print(line)
        else:
            print(result)

    def __str__(self):
        return self.name

def print_options(options: t.Dict[str, Option]) -> None:
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


def option_choice_is_valid(choice: str, options: t.Dict[str, Option]) -> bool:
    result = choice in options or choice.upper() in options
    return result


def get_option_choice(options: t.Dict[str, Option]) -> Option:
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")
        choice = input("Choose an option: ")
    return options[choice.upper()]

def get_user_input(label: str, required: bool = True) -> t.Optional[str]:
    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label}: ") or None
    return value

def get_new_shipment_data() -> t.Dict[str, t.Optional[str]]:
    result = {
        "customer": get_user_input("Customer Name"),
        "address": get_user_input("Customer address"),
        "contact": get_user_input("Contact Person"),
        "phone": get_user_input("Phone Number"),
        "cc": get_user_input("Cost Center"),
        "incoterm": get_user_input("Incoterm"),
        "description": get_user_input("Description"),
        "PO": get_user_input("Purchase Order (not mandatory)", required=False),
        "tracking": get_user_input("Tracking (not mandatory)", required=False),
        "notes": get_user_input("Notes (not mandatory)", required=False),
    }
    return result

def get_shipment_id() -> int:
    result = int(get_user_input("Enter a shipment ID"))  # type: ignore
    return result

def get_update_shipment_data() -> t.Dict[str, t.Union[int, t.Dict[str, str]]]:
    shipment_id = int(get_user_input("Enter a shipment ID to edit"))
    field = get_user_input("Choose a value to edit (customer, address, contact, phone, cc, incoterm, description, order, tracking, notes)")
    new_value = get_user_input(f"Enter a new value for {field}")
    return {"id": shipment_id, "update": {field: new_value}}

def get_file_name() -> str:
    file_name = get_user_input(
        "Please type in the name of the Excel file where you want to save"
    )
    return file_name

def get_email() -> t.Dict[str, str]:
    recipient = get_user_input("Enter an email")
    return {"recipient": recipient}

def clear_screen():
    clear_command = "cls" if os.name == "nt" else "clear"
    os.system(clear_command)