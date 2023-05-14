""" A module for the persistance layer """

import sys
import typing as t

from datetime import datetime
from pathlib import Path

from src.database import DatabaseManager

db = DatabaseManager("shipments.db")

CommandInput = t.Optional[t.Union[t.Dict[str, str], int]]
CommandResult = t.Optional[t.Union[t.List[str], str]]

class Command(t.Protocol):
    """A protocol class that will be an example for implementing Commands"""

    def execute(self, data: CommandInput) -> CommandResult:
        """The actual execution of the command"""
        pass

class CreateShipmentsTableCommand:
    """A Command class that creates the SQL table"""

    def execute(self):
        """The actual execution of the command"""

        db.create_table(
            table_name="shipments",
            columns={
                "id": "integer primary key autoincrement",
                "customer_name": "text not null",
                "customer_ship_to_address": "text not null",
                "contact_person": "text not null",
                "phone_number": "text not null",
                "cost_center": "text not null",
                "incoterm": "text not null",
                "item_description": "text not null",
                "purchase_order": "text",
                "tracking_number": "text",
                "notes": "text",
                "date_added": "text not null",
            },
        )

class AddShipmentCommand:
    """A Command class that inserts into the SQL table"""

    def execute(self, data: t.Dict[str, str], timestamp: t.Optional[str] = None) -> str:
        """The actual execution of the command"""

        date_added = timestamp or datetime.utcnow().isoformat()
        data.setdefault("date_added", date_added)
        db.add(table_name="shipments", data=data)
        return "Shipment added!"

class ListShipmentsCommand:
    """A Command class that will list all the shipments in the SQL table"""

    def __init__(self, order_by: str = "date_added"):
        self.order_by = order_by

    def execute(self) -> t.List[str]:
        """The actual execution of the command"""

        cursor = db.select(table_name="shipments", order_by=self.order_by)
        results = cursor.fetchall()
        return results

class DeleteShipmentCommand:
    """A Command class that will delete a shipment from the SQL table"""

    def execute(self, data: int) -> str:
        db.delete(table_name="shipments", criteria={"id": data})
        return "Shipment deleted!"

class QuitCommand:
    """A Command class that will quit the application"""

    def execute(self):
        sys.exit()