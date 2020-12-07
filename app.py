from peewee import *
import csv
import datetime
import sys
import os
from collections import OrderedDict

db = SqliteDatabase('inventory.db')

class Product(Model):
    product_id = PrimaryKeyField()
    product_name = CharField(max_length=255, unique=True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta():
        database = db

if __name__ == '__main__':
    """ initialise sqlite database """
    db.connect()
    db.create_tables([Product], safe=True)
    db.close()

def start():
    read_csv()
    clear()
    welcome()

def read_csv():
    with open('inventory.csv', newline='') as csvfile:
        productreader = csv.DictReader(csvfile)
        rows = list(productreader)
        for row in rows:
            row['product_price'] = int(row['product_price'].replace('£', '').replace('.', ''))
            row['product_quantity'] = int(row['product_quantity'])
            row['date_updated'] = (datetime.datetime.strptime(row['date_updated'], '%m/%d/%Y').date())
            try:
                Product.create(
                    product_name = row['product_name'],
                    product_quantity = row['product_quantity'],
                    product_price = row['product_price'],
                    date_updated = row['date_updated'],
                ).save()
            except ValueError:
                add = Product.get(product_name = row['product_name'])
                add.product_name = row['product_name']
                add.product_quantity = row['product_name']
                add.product_price = row['product_price']
                add.date_updated = row['date_updated']
                add.save()

def menu_loop():
    """ main menu """
    start()
    option = None
    while option != 'e':
        for key, value in menu.items():
            print(f' {key} {value.__doc__}')
        print("\n Press 'e' to exit.\n")
        option = input("Choose an option: ").lower().strip()
        if option == 'e':
            print("Thanks for coming!")
            break
        if option not in menu and option != 'e':
            print("That is not an option.")
            continue
        elif option in menu:
            clear()
            menu[option]()

def view_product():
    select = input("Please enter the product id: ")
    if select.lower() == "all":
        all_products = Product.select()
        for selected_product in all_products:
            print(selected_product)
    else:
        try:
            selected_product = Product.get_by_id(select)
            print(selected_product)
        except ValueError:
            print("No product with that ID.")

def add_product():
    add = Product()
    try:
        while True:
            try:
                add.product_name = input("What is the name of the product?\n")
                if add.product_name == "":
                    raise ValueError("Please enter a name")
            except ValueError:
                print("Try again.")
                continue
            else:
                break

        while True:
            try:
                add.product_quantity = int(input(f"How many are there of this product?\n"))
                if add.product_quantity < 0:
                    raise ValueError("Invalid value. Try again.")
            except ValueError:
                print("Invalid value. Please enter a number.")
                continue
            else:
                break

        while True:
            try:
                add.product_price = float(input(f"What is the price of this product?\n> £"))
                add.product_price = int(add.product_price*100)
                break
            except ValueError:
                print("Invalid value. Try again.")
                continue

        add.date_updated = datetime.datetime.now().date()
        add.save()
        clear()
        print(f"{} is now in the inventory!".format(product_name))

def backup_database():
    clear()
    backup_file = "Inventory_Backup.csv"
    field_titles = [
        'product_name',
        'product_price',
        'product_quantity',
        'date_updated',
    ]

    with open(backup_file, 'w', newline='')as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_titles)
        writer.writeheader()
        products = Product.select()
        for product in products:
            writer.writerow({
                    'product_name': product.product_name,
                    'product_quantity': product.product_quantity,
                    'product_price': product.product_price,
                    'date_updated': product.date_updated
            })
    print("Backup Complete.")

def welcome():
    print("---------------------------------")
    print("Welcome to this shop's inventory.")
    print("---------------------------------")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


menu = OrderedDict([
        ('a', add_product),
        ('v', view_products),
        ('b', backup_data),
    ])

if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    db.close()
    menu_loop()
