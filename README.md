# Inventory Management Application

This project is a Python-based inventory management application that
allows users to interact with a MySQL database through a console
interface. It supports CRUD (Create, Read, Update, Delete) operations
for multiple tables within a schema. The application provides a
menu-driven interface to manage records across various tables and is
designed with error handling for enhanced user experience.

## Table of Contents

-   [Features](#features)

-   [Supported Tables](#supported-tables)

-   [Setup Instructions](#setup-instructions)

-   [Usage](#usage)

-   [Error Handling](#error-handling)

-   [Code Structure](#code-structure)

-   [Example Output](#example-output)

## Features

-   **Create Record**: Allows inserting new records into specified tables, ensuring the necessary constraints are met.

-   **Read Record**: Retrieves and displays all records from the selected table.

-   **Update Record**: Modifies existing records in the database using primary key(s) for identification.

-   **Delete Record**: Deletes specific records from a table based on primary key(s).

-   **Error Handling**: Includes error handling for invalid options, database connection issues, and constraint violations.

## Supported Tables

The application supports the following tables:

1.  customer

2.  customer_order

    1.  customer_order_items

3.  inventory

4.  product

5.  product\_ category

6.  supplier

7.  order_process

    1.  processed_line_items

8.  User

These tables are managed using primary keys, and relationships between them are enforced by the application logic.

## Setup Instructions

### Prerequisites

-   Python 3.x installed on your system.

-   MySQL server running with a valid database schema.

-   MySQL Connector for Python (pymsql, sqlalchemy, python-dotenv
    package).

### Installation

1.  Clone or download this repository to your local machine.

2.  Install the MySQL connector package if not already installed:
```bash
pip install pymysql sqlalchemy python-dotenv
```
3.  Update the database connection credentials in the .env file with the
    parameters below:
```bash
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_HOST=
DATABASE_PORT=
```
The database schema and the required tables and relationships will be
auto created if it does not exist at first run.

## Usage

1.  **Run the application**:
```bash
python run.py
```
2.  **Menu Options**:

-   The application will display a menu with five options:

    -   Create a new record

    -   Read a record

    -   Update a record

    -   Delete a record

    -   Exit

-   Choose an option by entering the corresponding number (1-5).

3.  **CRUD Operations**:

-   Create: Select a table, then provide the required fields. The
    application checks for constraints like foreign key relationships
    before insertion.

-   Read: Select a table to view all its records.

-   Update: Choose the table, specify the primary key(s), and update the
    desired column\'s value.

-   Delete: Choose the table and provide the primary key(s) to delete
    the record.

4.  **Exit**:

-   To exit the application, select option 5. The application will close
    the database connection.

## Error Handling

-   **Database Connection**: If the application fails to connect to the
    MySQL database, it displays an error message and exits gracefully.

-   **Invalid Menu Options**: If an invalid menu option is selected, the
    application prompts the user to try again.

-   **Table and Column Selection**:

    -   The application validates the user\'s choice when selecting
        tables and columns.

    -   If a non-existent or invalid option is chosen, the application
        provides feedback and asks the user to make a valid selection.

-   **Constraint Violations**: The application enforces foreign key
    constraints. If a user tries to insert a record with a non-existent
    ID in a referenced table, it displays an error message.

-   **Business Logic Validation**: The application enforces business
    logic while updating or deleting records (EX: if customer order
    already processed then it will not let you update or delete)

## Code Structure

### DBManager Class

This class is responsible for handling all database interactions and
operations. It contains the following methods:

-   init: Establishes a connection to the MySQL database.

-   create_record: Inserts new records into the specified table.

-   read_record: Retrieves and displays all records from the selected
    table.

-   update_record: Updates a record based on the specified primary key
    and column.

-   delete_record: Deletes a record using the primary key(s) for
    identification.

-   read_records_and_sub_records: Prints main records and its
    sub-records together (useful for viewing customer order/order
    processing)

-   close_connection: Closes the database connection when the
    application exits.

### main_crud_function Function

This function manages the application flow:

-   Displays the main menu.

-   Takes user input for various operations.

-   Calls the appropriate methods from the DBManager class based on the
    user's choice.

### Example Output

Here\'s a screenshot of the application running:

-   **Create Record** :

    -   Create record python :

>![Inventory Management System - Example Output](screenshots/image1.png)

-   Create record sql :

> ![Inventory Management System - Example Output](screenshots/image2.png)

-   **Read Record**

    -   Read record python :

> ![Inventory Management System - Example Output](screenshots/image3.png)

-   Read record sql :

> ![Inventory Management System - Example Output](screenshots/image4.png)

-   **Update Record**

    -   Update record python :

> ![Inventory Management System - Example Output](screenshots/image5.png)

-   Update record sql :

    -   Before:

> ![Inventory Management System - Example Output](screenshots/image6.png)

-   After:

> ![Inventory Management System - Example Output](screenshots/image7.png)

-   **Delete Record**

    -   Delete record python:

>![Inventory Management System - Example Output](screenshots/image8.png)

-   Delete record sql:

    -   Before:

>![Inventory Management System - Example Output](screenshots/image9.jpeg)

>![Inventory Management System - Example Output](screenshots/image10.png)

>![Database Manager Application - Example Output](screenshots/image11.png)

-   After:

>![Database Manager Application - Example Output](screenshots/image12.jpeg)

![Database Manager Application - Example Output](screenshots/image13.png)

-   **Error Handling**

-   Case 1:

![Database Manager Application - Example Output](screenshots/image14.jpeg)

![Database Manager Application - Example Output](screenshots/image15.png)

-   Case 2:

![Database Manager Application - Example Output](screenshots/image16.jpeg)

![Database Manager Application - Example Output](screenshots/image17.png)
