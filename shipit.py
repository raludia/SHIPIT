from src import commands as c
from src import presentation as p


def loop():
    options = {
        "A": p.Option(
            name="Add a shipment",
            command=c.AddShipmentCommand(),
            prep_call=p.get_new_shipment_data,
        ),
        "S": p.Option(
            name="Get shipment by ID",
            command=c.GetShipmentCommand(),
            prep_call=p.get_shipment_id,
        ),
        "B": p.Option(
            name="List shipments by date", 
            command=c.ListShipmentsCommand()
        ),
        "C": p.Option(
            name="List shipments by customer",
            command=c.ListShipmentsCommand(order_by="customer"),
        ),
        "E": p.Option(
            name="Edit a shipment",
            command=c.EditShipmentCommand(),
            prep_call=p.get_update_shipment_data,
        ),
        "D": p.Option(
            name="Delete a shipment",
            command=c.DeleteShipmentCommand(),
            prep_call=p.get_shipment_id
        ),
        "X": p.Option(
            name="Export to Excel",
            command=c.ExportToExcelCommand(),
            prep_call=p.get_file_name,
        ),
        "Q": p.Option(
            name="Quit", 
            command=c.QuitCommand()),
    }

    p.clear_screen()
    p.print_options(options)
    chosen_option = p.get_option_choice(options)
    p.clear_screen()
    chosen_option.choose()

    _ = input("Press ENTER to return to menu")


if __name__ == "__main__":
    c.CreateShipmentsTableCommand().execute()
    while True:
        loop()