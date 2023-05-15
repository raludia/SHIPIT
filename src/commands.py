""" A module for the persistance layer """

import sys
import typing as t

from datetime import datetime
from pathlib import Path

import openpyxl

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
                "customer": "text not null",
                "address": "text not null",
                "contact": "text not null",
                "phone": "text not null",
                "cc": "text not null",
                "incoterm": "text not null",
                "description": "text not null",
                "PO": "text",
                "tracking": "text",
                "notes": "text",
                "date_added": "text not null"
            }
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

class GetShipmentCommand:
    """A Command class that will return a single shipment based on an ID"""

    def execute(self, data: int) -> t.Optional[tuple]:
        result = db.select(table_name="shipments", criteria={"id": data}).fetchone()
        return result

class EditShipmentCommand:
    """A Command class that will edit a shipment identified with an ID"""

    def execute(self, data: t.Dict[str, str]) -> str:
        db.update(
            table_name="shipments", criteria={"id": data["id"]}, data=data["update"]
        )
        return "Shipment updated!"
    
class DeleteShipmentCommand:
    """A Command class that will delete a shipment from the SQL table"""

    def execute(self, data: int) -> str:
        db.delete(table_name="shipments", criteria={"id": data})
        return "Shipment deleted!"

class ExportToExcelCommand:
    """A Command class used to export the data in an Excel format"""

    def execute(self, data: str) -> str:
        """data (str): the file name of the exported workbook"""

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        records = ListShipmentsCommand().execute()

        for row in records:
            sheet.append(row)

        export_folder_path = Path(f"./exports")
        export_folder_path.mkdir(parents=True, exist_ok=True)

        workbook.save(export_folder_path / f"{data}.xlsx")

        return f"Exported to file {data}"

class QuitCommand:
    """A Command class that will quit the application"""

    def execute(self):
        sys.exit()