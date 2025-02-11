import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, class_mapper
from datetime import datetime
import datetime as dt
from db import Base
from models.customers import Customer, CustomerOrder, CustomerOrderItems
from models.inventory import InventoryLocation, Inventory
from models.products import ProductCategory, Product, Supplier
from models.transactions import OrderProcess, ProcessedLineItems

CURRENT_DIR = os.getcwd()

load_dotenv(os.path.join(CURRENT_DIR, '.env'))

class DBManager:
    def __init__(self, db_url):
        # Initialize the connection to the database using SQLAlchemy
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)
        print("Connected to the database.")

    def create_record(self, table):
        if table == "customer":
            customer = Customer(
                customer_name=input("Enter customer name: "),
                customer_location=input("Enter customer location: "),
                customer_email=input("Enter customer email: "),
                customer_telephone=input("Enter customer telephone: ")
            )
            self.session.add(customer)
        elif table == "customer_order":
            customer_order = CustomerOrder(
                customer_id=int(input("Enter customer ID: ")),
                order_date=datetime.now(dt.UTC)
            )
            self.session.add(customer_order)
            self.session.flush()
            print("Enter line items for customer order.")
            while True:
                customer_order_items = CustomerOrderItems(
                    customer_order_id=customer_order.order_id,
                    # customer_order_id=int(input("Enter customer order ID: ")),
                    product_id=int(input("Enter product ID: ")),
                    request_quantity=int(input("Enter request quantity: "))
                )
                self.session.add(customer_order_items)
                more_items = input("Do you want to add another item? (yes/no): ").strip().lower()
                if more_items != "yes":
                    break
            # customer_order.children.append(customer_order_items)

        elif table == "inventory_location":
            inventory_location = InventoryLocation(
                aisle_number=input("Enter aisle number: "),
                bin_location=input("Enter bin location: ")
            )
            self.session.add(inventory_location)
        elif table == "inventory":
            inventory = Inventory(
                product_id=int(input("Enter product ID: ")),
                available_quantity=int(input("Enter available quantity: ")),
                reorder_trigger_quantity=int(input("Enter reorder trigger quantity: ")),
                inventory_status=bool(input("Enter inventory status (True/False): ")),
                inventory_location_id=int(input("Enter inventory location ID: "))
            )
            self.session.add(inventory)
        elif table == "product_category":
            product_category = ProductCategory(
                category_name=input("Enter category name: ")
            )
            self.session.add(product_category)
        elif table == "supplier":
            supplier = Supplier(
                supplier_name=input("Enter supplier name: "),
                supplier_contact_number=input("Enter supplier contact number: ")
            )
            self.session.add(supplier)
        elif table == "product":
            product = Product(
                serial_no=input("Enter serial number: "),
                product_name=input("Enter product name: "),
                product_weight=float(input("Enter product weight: ")),
                price_per_unit=float(input("Enter price per unit: ")),
                product_category_id=int(input("Enter product category ID: ")),
                product_supplier_id=int(input("Enter product supplier ID: "))
            )
            self.session.add(product)
        elif table == "order_process":
            order_process = OrderProcess(
                transaction_date=datetime.now(dt.UTC),
                sales_amount=float(input("Enter sales amount: ")),
                processed_by_id=int(input("Enter processed by ID: ")),
                customer_order_id=int(input("Enter customer order ID: ")),
                order_processed=bool(input("Enter order processed status (True/False): "))
            )
            self.session.add(order_process)
        elif table == "processed_line_items":
            processed_line_items = ProcessedLineItems(
                customer_line_item_id=int(input("Enter customer line item ID: ")),
                process_id_id=int(input("Enter process ID: ")),
                inventory_id=int(input("Enter inventory ID: ")),
                allocated_quantity=int(input("Enter allocated quantity: "))
            )
            self.session.add(processed_line_items)

        try:
            self.session.commit()
            print(f"Record created successfully in {table}.")
        except Exception as e:
            self.session.rollback()
            print(f"Error inserting record into {table}: {e}")

    def read_record(self, table):
        records = None
        if table == "customer": records = self.session.query(Customer).all()
        elif table == "customer_order": records = self.session.query(CustomerOrder).all()
        elif table == "customer_order_items": records = self.session.query(CustomerOrderItems).all()
        # elif table == "inventory_location": records = self.session.query(InventoryLocation).all()
        elif table == "inventory": records = self.session.query(Inventory).all()
        elif table == "product_category": records = self.session.query(ProductCategory).all()
        elif table == "supplier": records = self.session.query(Supplier).all()
        elif table == "product": records = self.session.query(Product).all()
        elif table == "order_process": records = self.session.query(OrderProcess).all()
        # elif table == "processed_line_items": records = self.session.query(ProcessedLineItems).all()

        if records:
            print(f"\nContents of the '{table}' table:")
            for record in records:
                print({c.key: getattr(record, c.key) for c in class_mapper(record.__class__).columns})
                if table == 'customer_order':
                     for item in record.order_items:
                         print("\t{}".format({c.key: getattr(item, c.key) for c in class_mapper(item.__class__).columns}))
                elif table == 'order_process':
                    for item in record.processed_line_items:
                         print("\t{}".format({c.key: getattr(item, c.key) for c in class_mapper(item.__class__).columns}))

                # print(record)
        else:
            print(f"\nNo records found in the '{table}' table.")

    def update_record(self, table):
        record = None
        if table == "customer":
            record_id = int(input("Enter customer ID: "))
            record = self.session.get(Customer, record_id)
            if record:
                record.customer_name = input("Enter new customer name: ")
                record.customer_location = input("Enter new customer location: ")
                record.customer_email = input("Enter new customer email: ")
                record.customer_telephone = input("Enter new customer telephone: ")
        elif table == "customer_order":
            record_id = int(input("Enter order ID: "))
            record = self.session.get(CustomerOrder, record_id)
            if record:
                print({c.key: getattr(record, c.key) for c in class_mapper(record.__class__).columns})
                for item in record.order_items:
                    print("\t{}".format({c.key: getattr(item, c.key) for c in class_mapper(item.__class__).columns}))

                record.customer_id = int(input("Enter new customer ID: "))
                record.order_date = datetime.now(dt.UTC)
                self.session.add(record)
                while True:
                    line_item = input("Do you want to change the line items? (yes/no): ").strip().lower()
                    if line_item == "yes":
                        line_item_id = input("Enter the line item ID: ")
                        line_item = self.session.query(CustomerOrderItems).filter_by(line_item_id=line_item_id).first()
                        if line_item:
                            # customer_order_id=int(input("Enter customer order ID: ")),
                            line_item.product_id=int(input("Enter product ID: ")),
                            line_item.request_quantity=int(input("Enter request quantity: "))
                    else:
                        break
        elif table == "product_category":
            record_id = int(input("Enter product category ID: "))
            record = self.session.get(ProductCategory, record_id)
            if record:
                record.category_name = input("Enter new category name: ")
            else:
                print("Product category not found.")

        elif table == "product":
            record_id = int(input("Enter product ID: "))
            record = self.session.get(Product, record_id)
            if record:
                record.product_name = input("Enter new product name: ")
                record.product_description = input("Enter new product description: ")
                record.category_id = int(input("Enter new category ID: "))
                record.supplier_id = int(input("Enter new supplier ID: "))
                record.price = float(input("Enter new product price: "))
            else:
                print("record not found.")

        elif table == "order_process":
            record_id = int(input("Enter order process ID: "))
            record = self.session.get(OrderProcess, record_id)
            if record:
                record.order_id = int(input("Enter new order ID: "))
                record.process_status = input("Enter new process status: ")
                record.processed_date = datetime.now(dt.timezone.utc)
            else:
                print("record not found.")

        elif table == "supplier":
            record_id = int(input("Enter supplier ID: "))
            record = self.session.get(Supplier, record_id)
            if record:
                record.supplier_name = input("Enter new supplier name: ")
                record.supplier_contact = input("Enter new supplier contact info: ")
            else:
                print("record not found.")


        elif table == "processed_line_items":
            record_id = int(input("Enter processed line item ID: "))
            record = self.session.get(ProcessedLineItems, record_id)
            if record:
                record.process_id = int(input("Enter new process ID: "))
                record.order_item_id = int(input("Enter new order item ID: "))


        # elif table == "customer_order_items":
        #     record_id = int(input("Enter order item ID: "))
        #     record = self.session.get(CustomerOrderItems, record_id)
        #     if record:
        #         record.order_id = int(input("Enter new order ID: "))
        #         record.product_id = int(input("Enter new product ID: "))
        #         record.quantity = int(input("Enter new quantity: "))
        # elif table == "inventory_location":
        #     record_id = int(input("Enter location ID: "))
        #     record = self.session.get(InventoryLocation, record_id)
        #     if record:
        #         record.customer_id = int(input("Enter new customer ID: "))
        #         record.order_date = datetime.now(dt.UTC)


        # Similar updates for other tables...

        try:
            if record:
                self.session.commit()
                print(f"Record updated successfully in {table}.")
                # print(f"Updated record ID: {record.pk}.")
                # print({c.key: getattr(record, c.key) for c in class_mapper(record.__class__).columns})
        except Exception as e:
            self.session.rollback()
            print(f"Error updating record in {table}: {e}")

    def delete_record(self, table):
        record = None
        if table == "customer":
            record_id = int(input("Enter customer ID: "))
            record = self.session.query(Customer).get(record_id)
        elif table == "customer_order":
            record_id = int(input("Enter order ID: "))
            record = self.session.query(CustomerOrder).get(record_id)
        # Similar deletions for other tables...

        if record:
            self.session.delete(record)
            try:
                self.session.commit()
                print(f"Record deleted successfully from {table}.")
            except Exception as e:
                self.session.rollback()
                print(f"Error deleting record from {table}: {e}")
        else:
            print("No matching record found.")

    def close_connection(self):
        self.session.close()
        print("Database connection closed.")


def main():
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    host = os.getenv("DATABASE_HOST")
    port = os.getenv("DATABASE_PORT")
    database = os.getenv("DATABASE_NAME")

    db_url = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
        user, password, host, port, database
    )
    db = DBManager(db_url)

    tables = ["customer", "customer_order", "inventory", "product",
              "product_category", "supplier",  "order_process"]

    while True:
        print("\nMenu:")
        print("1. Create a new record")
        print("2. Read a record")
        print("3. Update a record")
        print("4. Delete a record")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice in ['1', '2', '3', '4']:
            print("\nSelect a table:")
            for i, table in enumerate(tables, 1):
                print(f"{i}. {table}")
            table_choice = int(input("Enter table number: "))

            if 1 <= table_choice <= len(tables):
                selected_table = tables[table_choice - 1]
                if choice == '1':
                    db.create_record(selected_table)
                elif choice == '2':
                    db.read_record(selected_table)
                elif choice == '3':
                    db.update_record(selected_table)
                elif choice == '4':
                    db.delete_record(selected_table)
            else:
                print("Invalid table choice. Please try again.")
        elif choice == '5':
            db.close_connection()
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()