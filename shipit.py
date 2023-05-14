from src import commands as c
from src import presentation as p

if __name__ == "__main__":
    c.CreateShipmentsTableCommand().execute()
    print("Welcome to SHIPIT!")

def loop():
    options = {
        "A": p.Option(
            name="Add a shipment",
            command=c.AddShipmentCommand(),
        ),
        "B": p.Option(
            name="List shipments by date", 
            command=c.ListShipmentsCommand()),
        "C": p.Option(
            name="List shipments by customer name",
            command=c.ListShipmentsCommand(order_by="customer_name"),
        ),
        "D": p.Option(
            name="Delete a shipment",
            command=c.DeleteShipmentCommand(),
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