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
from models.user import User

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
        elif table == "inventory":
            inventory = Inventory(
                product_id=int(input("Enter product ID: ")),
                available_quantity=int(input("Enter available quantity: ")),
                reorder_trigger_quantity=int(input("Enter reorder trigger quantity: ")),
                inventory_status=bool(input("Enter inventory status (True/False): ")),
                inventory_location_id=int(input("Enter inventory location ID: "))
            )
            self.session.add(inventory)
        elif table == "inventory_location":
            inventory_location = InventoryLocation(
                aisle_number=input("Enter aisle number: "),
                bin_location=input("Enter bin location: ")
            )
            self.session.add(inventory_location)
        elif table == "product_category":
            product_category = ProductCategory(
                category_name=input("Enter category name: ")
            )
            self.session.add(product_category)
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
        elif table == "supplier":
            supplier = Supplier(
                supplier_name=input("Enter supplier name: "),
                supplier_contact_number=input("Enter supplier contact number: ")
            )
            self.session.add(supplier)
        elif table == "order_process":
            customer_order_id = int(input("Enter customer order ID: ")),
            customer_order = self.session.get(CustomerOrder, customer_order_id)
            if not customer_order:
                print("Customer order not found")
            elif customer_order.processed_order_info:
                print("processed info already exists for customer order")
            else:
                self.read_records_and_sub_records([customer_order,])

                order_process = OrderProcess(
                    transaction_date=datetime.now(dt.UTC),
                    sales_amount=0,
                    processed_by_id=int(input("Enter your user ID: ")),
                    customer_order_id=customer_order_id,
                )
                self.session.add(order_process)
                self.session.flush()

                for item in customer_order.order_items:
                    print(f"\nProcessing customer line item ID: {item.line_item_id}")

                    inventory_id = int(input("Enter new inventory ID: ")),
                    # request_quantity = int(input("Enter new allocation quantity: "))
                    inventory = self.session.get(Inventory, inventory_id)
                    processed_line_item = ProcessedLineItems(
                        customer_line_item_id=item.line_item_id,
                        process_id_id=order_process.transaction_id,
                    )
                    if inventory and inventory.product_id == item.product_id:
                        if item.request_quantity <= inventory.available_quantity:
                            processed_line_item.allocated_quantity = item.request_quantity
                            inventory.available_quantity -= item.request_quantity
                        else:
                            processed_line_item.allocated_quantity = inventory.available_quantity
                            inventory.available_quantity -= 0
                        processed_line_item.inventory_id = inventory_id
                        self.session.add(processed_line_item)
                        self.session.add(inventory)
                        # self.session.flush()
                    else:
                        print(f"The customer requested product ID doesn't match with the inventory product with the ID: {inventory_id}")

        elif table == "user":
            user = User(
                username=input("Enter new username: "),
                first_name=input("Enter new first name: "),
                last_name=input("Enter new last name: "),
                email=input("Enter new email: "),
                password=input("Enter new password: "),
            )
            self.session.add(user)

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
        elif table == "inventory": records = self.session.query(Inventory).all()
        elif table == "inventory_location": records = self.session.query(InventoryLocation).all()
        elif table == "product_category": records = self.session.query(ProductCategory).all()
        elif table == "supplier": records = self.session.query(Supplier).all()
        elif table == "product": records = self.session.query(Product).all()
        elif table == "order_process": records = self.session.query(OrderProcess).all()
        elif table == "user": records = self.session.query(User).all()

        if records:
            self.read_records_and_sub_records(records)
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
            record_id = int(input("Enter customer order ID: "))
            record = self.session.get(CustomerOrder, record_id)
            if record:
                if record.processed_order_info and record.processed_order_info.order_processed:
                    print(f"\nThis customer order has already been processed. Hence, editing is not allowed.")
                else:
                    self.read_records_and_sub_records([record,])
                    change_type = input("\nDo you want to update customer info or line item? "
                                        "\nPress 1 for customer info.\nPress 2 for line item.\nEnter your choice: ")
                    if change_type == "1":
                        record.customer_id = int(input("Enter new customer ID: "))
                        record.order_date = datetime.now(dt.UTC)
                        self.session.add(record)
                    elif change_type == "2":
                        while True:
                            line_item_id = input("Enter the line item ID: ")
                            line_item = self.session.query(CustomerOrderItems).filter_by(customer_order_id=record_id,
                                                                                         line_item_id=line_item_id).first()
                            if line_item:

                                # line_item.product_id=int(input("Enter product ID: ")),
                                line_item.request_quantity=int(input("Enter request quantity: "))
                                self.session.add(line_item)
                            new_update = input("Do you want to change another line items? (yes/no): ").strip().lower()
                            if new_update != "yes":
                                break
                    else:
                        print("Invalid input.")
            else:
                raise ValueError(f"\nNo records found in the '{table}' table with the ID: '{record_id}'.")
        elif table == "inventory":
            record_id = int(input("Enter Inventory ID: "))
            record = self.session.get(Inventory, record_id)
            if record:
                record.available_quantity = int(input("Enter new Quantity: "))
                location_change_required = input("\nDo you want to update inventory location? (yes/no): ")
                if location_change_required == "yes":
                    new_location = int(input("Enter new Location ID: "))
                    if  self.session.get(InventoryLocation, new_location):
                        record.inventory_location_id = new_location
            else:
                print(f"\nNo records found in the '{table}' table with the ID: '{record_id}'.")
        elif table == "inventory_location":
            record_id = int(input("Enter location ID: "))
            record = self.session.get(InventoryLocation, record_id)
            if record:
                record.aisle_number = input("Enter new Aisle Number: ")
                record.bin_location = input("Enter new Bin Location: ")
        elif table == "product_category":
            record_id = int(input("Enter product category ID: "))
            record = self.session.get(ProductCategory, record_id)
            if record:
                record.category_name = input("Enter new category name: ")
            else:
                print(f"\nNo records found in the '{table}' table with the ID: '{record_id}'.")
        elif table == "product":
            record_id = int(input("Enter product ID: "))
            record = self.session.get(Product, record_id)
            if record:
                record.product_name = input("Enter new product name: ")
                # record.product_description = input("Enter new product description: ")
                record.product_category_id = int(input("Enter new category ID: "))
                record.product_supplier_id = int(input("Enter new supplier ID: "))
                record.price_per_unit = float(input("Enter new product price: "))
                record.product_weight = float(input("Enter new product weight: "))
            else:
                print(f"\nNo records found in the '{table}' table with the ID: '{record_id}'.")
        elif table == "supplier":
            record_id = int(input("Enter supplier ID: "))
            record = self.session.get(Supplier, record_id)
            if record:
                record.supplier_name = input("Enter new supplier name: ")
                record.supplier_contact_number = input("Enter new supplier contact number: ")
            else:
                print(f"\nNo records found in the '{table}' table with the ID: '{record_id}'.")
        elif table == "order_process":
            record_id = int(input("Enter order process ID: "))
            record = self.session.get(OrderProcess, record_id)
            if not record:
                print("Order Process ID not found")
            elif record.order_processed:
                print("Order has already been processed. Hence, edit not allowed.")
            elif record:
                print("\nCustomer Order Info")
                self.read_records_and_sub_records([record.customer_order, ])
                print("\nOrder Process Info")
                self.read_records_and_sub_records([record,])
                while True:
                    line_item_id = input("\nEnter the process line item ID: ")
                    line_item = self.session.query(ProcessedLineItems).filter_by(process_id_id=record_id,
                                                                                 line_item_id=line_item_id).first()
                    customer_line_item = self.session.query(CustomerOrderItems).filter_by(line_item_id=\
                                                                            line_item.customer_line_item_id).first()
                    if line_item:
                        inventory_id = int(input("Enter new inventory ID: ")),
                        request_quantity = customer_line_item.request_quantity
                        inventory = self.session.get(Inventory, inventory_id)
                        if inventory:
                            if inventory.available_quantity <= request_quantity:
                                line_item.request_quantity = request_quantity
                                line_item.inventory_id = inventory_id
                                self.session.add(line_item)
                                inventory.available_quantity -= request_quantity
                                self.session.add(inventory)
                            else:
                                print(f"Not enough inventory for product ID {inventory.product_id}")

                        else: print(f"\nNo records found in the 'Inventory' table with the ID: '{inventory_id}'.")
                    else:
                        print("Line item not found.")
                    new_update = input("Do you want to update any other line items? (yes/no): ").strip().lower()
                    if new_update != "yes":
                        break

            else:
                print(f"\nNo records found in the '{table}' table with the ID: '{record_id}'.")
        elif table == "user":
            record_id = int(input("Enter user ID: "))
            record = self.session.get(User, record_id)
            if record:
                record.username = input("Enter new username: ")
                record.first_name = input("Enter new first name: ")
                record.last_name = input("Enter new last name: ")
                record.email = input("Enter new email: ")
                record.password = input("Enter new password: ")
                record.last_login = datetime.now(dt.UTC)

        try:
            if record:
                self.session.commit()
                print(f"Record updated successfully in {table}.")

        except Exception as e:
            self.session.rollback()
            print(f"Error updating record in {table}: {e}")
            print(f"Error updating record in {table}: {e}")

    def delete_record(self, table):
        record = None
        record_id = int(input(f"Enter the ID of the {table.replace('_', ' ')} to delete: "))
        if table == "customer":
            record = self.session.get(Customer, record_id)
        elif table == "customer_order":
            record = self.session.get(CustomerOrder, record_id)
        elif table == "inventory_location":
            record = self.session.get(InventoryLocation, record_id)
        elif table == "inventory":
            record = self.session.get(Inventory, record_id)
        elif table == "product_category":
            record = self.session.get(ProductCategory, record_id)
        elif table == "supplier":
            record = self.session.get(Supplier, record_id)
        elif table == "product":
            record = self.session.get(Product, record_id)
        elif table == "order_process":
            record = self.session.get(OrderProcess, record_id)
        elif table == "user":
            record = self.session.get(User, record_id)
        else:
            print(f"Invalid table name: {table}")

        if record:
            if (record.__table__.name == "order_process" and record.order_processed == True) \
                or (record.__table__.name == "customer_order" and record.processed_order_info and \
                    record.processed_order_info.order_processed == True):
                print(f"\nThe order has already been processed. Therefore, it is not allowed to remove this record.")

            else:
                # Ask for user confirmation before deletion
                confirm = input(
                    f"Are you sure you want to delete this {table.replace('_', ' ')}? (yes/no): ").strip().lower()
                if confirm == "yes":
                    self.session.delete(record)
                    self.session.commit()
                    print(f"{table.replace('_', ' ').capitalize()} with ID {record_id} deleted successfully.")
                else:
                    print("Deletion cancelled.")
        else:
            print(f"No {table.replace('_', ' ')} found with ID {record_id}.")

    @staticmethod
    def read_records_and_sub_records(records):
        for record in records:
            print({c.key: getattr(record, c.key) for c in class_mapper(record.__class__).columns})
            if record.__table__.name == 'customer_order':
                for item in record.order_items:
                    print("\t{}".format({c.key: getattr(item, c.key) for c in class_mapper(item.__class__).columns}))
            elif record.__table__.name == 'order_process':
                for item in record.processed_line_items:
                    print("\t{}".format({c.key: getattr(item, c.key) for c in class_mapper(item.__class__).columns}))

    def close_connection(self):
        self.session.close()
        print("Database connection closed.")


