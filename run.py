import os

from data_operations import DBManager


def main_crud_function():
    user = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    host = os.getenv("DATABASE_HOST")
    port = os.getenv("DATABASE_PORT")
    database = os.getenv("DATABASE_NAME")

    db_url = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
        user, password, host, port, database
    )
    db = DBManager(db_url)

    tables = ["customer", "customer_order", "inventory", "inventory_location", "product",
              "product_category", "supplier",  "order_process", "user"]

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
    main_crud_function()