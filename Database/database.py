import mysql.connector

host = "localhost"
user = "root"
password = ""
database = "smart_ai_home_security"

# Connection to the database
data = mysql.connector.connect(host=host, user=user, password=password, database=database)
cursor = data.cursor()  

# connection querry database 
def __connectionCheck():

    try:

    # Test connection
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()

        if result:
            print("connected to database")
            print("MySQL Server version:", result[0])
        else:
            print("Connection failed!")

        # Closing the connection
        # cursor.close()
        # data.close()
        
        return cursor

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL:", error)


# __connection()

import mysql.connector

# create data in History table
def createHistory(images=None, name=None, time_in=None, date=None):

    try:
        # Create the HISTORY table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS HISTORY (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            Images LONGTEXT,
            Name VARCHAR(255),
            TimeIn VARCHAR(255),
            Date VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        data.commit()

        # Insert data into the HISTORY table
        insert_query = """
        INSERT INTO HISTORY (person, name, time, date)
        VALUES (%s, %s, %s, %s)
        """
        query = (images, name, time_in, date)
        cursor.execute(insert_query, query)
        data.commit()

        print("Data inserted successfully!")

    except mysql.connector.Error as err:
        print("Error:", err)

    # Close the cursor and connection
    cursor.close()
    data.close()

# read data from History table
def readHistory():
    try:
        # Select all rows from the HISTORY table
        select_query = "SELECT * FROM HISTORY"
        cursor.execute(select_query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Process the rows
        for row in rows:
            id = row[0]
            images = row[1]
            name = row[2]
            time_in = row[3]
            date = row[4]

            # Do something with the data
            print(f"ID: {id}, Images: {images}, Name: {name}, Time In: {time_in}, Date: {date}")

    except mysql.connector.Error as err:
        print("Error:", err)

    # Close the cursor and connection
    cursor.close()
    data.close()


# update data in History table
def updateHistory(ID=None,Images=None, new_name=None, new_time_in=None, new_date=None):
    try:
        # Update the specified record in the HISTORY table
        update_query = "UPDATE HISTORY SET person = %s, name = %s, time = %s, date = %s WHERE ID = %s"
        query = (Images,new_name, new_time_in, new_date, ID)
        cursor.execute(update_query, query)
        data.commit()

        if cursor.rowcount > 0:
            print("Data updated successfully!")
        else:
            print("No matching record found.")

    except mysql.connector.Error as err:
        print("Error:", err)

    # Close the cursor and connection
    cursor.close()
    data.close()


# delete data in History table
def deleteHistory(ID):

    try:
        # Delete the specified record from the HISTORY table
        delete_query = "DELETE FROM HISTORY WHERE ID = %s"
        query = (ID,)
        cursor.execute(delete_query, query)
        data.commit()

        if cursor.rowcount > 0:
            print("Data deleted successfully!")
        else:
            print("No matching record found.")

    except mysql.connector.Error as err:
        print("Error:", err)

    # Close the cursor and connection
    cursor.close()
    data.close()


# createHistory(
#     images="Hello Friend",
#     name="Elliot Alderson",
#     time_in="3:00pm",
#     date="June 8 2023"
# )

# readHistory()

# updateHistory(
#     ID=1,
#     Images="chek check",
#     new_name="Art Lisboa",
#     new_date="june 24 2023",
#     new_time_in="6:30"
# )

# deleteHistory(1)


