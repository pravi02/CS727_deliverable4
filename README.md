#Inventory Management Application

This project is a Python-based inventory management application that
allows users to interact with a MySQL database through a console
interface. It supports CRUD (Create, Read, Update, Delete) operations
for multiple tables within a schema. The application provides a
menu-driven interface to manage records across various tables and is
designed with error handling for enhanced user experience.

**Table of Contents**

-   [Features](#features)

-   [Supported Tables](#supported-tables)

-   [Setup Instructions](#setup-instructions)

-   [Usage](#usage)

-   [Error Handling](#error-handling)

-   [Code Structure](#code-structure)

-   [Example Output](#example-output)

**Features**

-   **Create Record**: Allows inserting new records into specified
    tables, ensuring the necessary constraints are met.

-   **Read Record**: Retrieves and displays all records from the
    selected table.

-   **Update Record**: Modifies existing records in the database using
    primary key(s) for identification.

-   **Delete Record**: Deletes specific records from a table based on
    primary key(s).

-   **Error Handling**: Includes error handling for invalid options,
    database connection issues, and constraint violations.

**Supported Tables**

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

These tables are managed using primary keys, and relationships between
them are enforced by the application logic.

**Setup Instructions**

**Prerequisites**

-   Python 3.x installed on your system.

-   MySQL server running with a valid database schema.

-   MySQL Connector for Python (pymsql, sqlalchemy, python-dotenv
    package).

**Installation**

1.  Clone or download this repository to your local machine.

2.  Install the MySQL connector package if not already installed:

pip install pymysql sqlalchemy python-dotenv

3.  Update the database connection credentials in the .env file with the
    parameters below:

DATABASE_USER=\
DATABASE_PASSWORD=\
DATABASE_NAME=\
DATABASE_HOST=\
DATABASE_PORT=

The database schema and the required tables and relationships will be
auto created if it does not exist at first run.

**Usage**

1.  **Run the application**:

python run.py

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

**Error Handling**

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

**Code Structure**

**DBManager Class**

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

**main_crud_function Function**

This function manages the application flow:

-   Displays the main menu.

-   Takes user input for various operations.

-   Calls the appropriate methods from the DBManager class based on the
    user's choice.

**Example Output**

Here\'s a screenshot of the application running:

-   **Create Record** :

    -   Create record python :

![A screenshot of a computer program AI-generated content may be
incorrect.](screenshots/image1.png){width="6.5in"
height="6.093055555555556in"}

-   Create record sql :

> ![A table of names and numbers AI-generated content may be
> incorrect.](screenshots/image2.png){width="4.595608048993876in"
> height="5.200018591426072in"}

-   **Read Record**

    -   Read record python :

> ![A screen shot of a computer screen AI-generated content may be
> incorrect.](screenshots/image3.png){width="5.650943788276465in"
> height="3.2839260717410323in"}

-   Read record sql :

> ![A screenshot of a computer AI-generated content may be
> incorrect.](screenshots/image4.png){width="6.5in"
> height="4.404166666666667in"}

-   **Update Record**

    -   Update record python :

![A screenshot of a computer program AI-generated content may be
incorrect.](screenshots/image5.png){width="4.1012237532808395in"
height="5.359932195975503in"}

-   Update record sql :

    -   Before:

![A table with numbers and numbers on it AI-generated content may be
incorrect.](screenshots/image6.png){width="3.6663681102362204in"
height="4.470367454068241in"}

-   After:

![A table with numbers and numbers AI-generated content may be
incorrect.](screenshots/image7.png){width="3.395300743657043in"
height="4.398698600174978in"}

-   **Delete Record**

    -   Delete record python:

![A screenshot of a computer program AI-generated content may be
incorrect.](screenshots/image8.png){width="5.6859405074365705in"
height="4.248053368328959in"}

-   Delete record sql:

    -   Before:

![Database Manager Application - Example
Output](screenshots/image9.jpeg){width="5.34375in"
height="3.9375in"}

![A table with numbers and numbers AI-generated content may be
incorrect.](screenshots/image10.png){width="3.135025153105862in"
height="4.895220909886264in"}

![A screenshot of a computer AI-generated content may be
incorrect.](screenshots/image11.png){width="6.5in"
height="0.9131944444444444in"}

-   After:

![Database Manager Application - Example
Output](screenshots/image12.jpeg){width="5.479166666666667in"
height="4.15625in"}

![A table with numbers and numbers AI-generated content may be
incorrect.](screenshots/image13.png){width="3.209630358705162in"
height="4.564344925634296in"}

-   **Error Handling**

-   Case 1:

![Database Manager Application - Example
Output](screenshots/image14.jpeg){width="6.5in"
height="1.9333333333333333in"}

![A screenshot of a computer program AI-generated content may be
incorrect.](screenshots/image15.png){width="3.501415135608049in"
height="2.1258595800524933in"}

-   Case 2:

![Database Manager Application - Example
Output](screenshots/image16.jpeg){width="6.5in"
height="6.263888888888889in"}

![A screenshot of a computer program AI-generated content may be
incorrect.](screenshots/image17.png){width="3.3555227471566056in"
height="5.345910979877515in"}
