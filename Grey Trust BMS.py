
#*** Database setup
import pymysql
from pymysql import cursors
from datetime import datetime as dt

connection = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    db = 'greytrust',
    charset = 'utf8mb4',
    cursorclass = pymysql.cursors.DictCursor
)


#*** Bank App logic
import random as rd

#--- creating bank object
class GreyTrustBank():
    def __init__(self, name, gender, residence, dob, pin):
        self.name = name
        self.gender = gender
        self.residence = residence
        self.dob = dob
        self.pin = pin
        self.account_num = rd.randrange(0000000000, 9999999999)
        self.account_bal = 0 

    #- accessing class attributes
    @property
    def get_name(self):
        return self.name

    @property
    def get_gender(self):
        return self.gender

    @property
    def get_residence(self):
        return self.residence

    @property
    def get_dob(self):
        return self.dob
    
    @property
    def get_pin(self):
        return self.pin

    #- handling balance, deposit and withdraw
    def balance(self):
        return f"Your account balance is: ${self.account_bal}\n"

    def deposit(self, value):
        self.account_bal += int(value)
        print(f"Transaction Sucessful!\nBalance: ${self.account_bal}\n")

    def withdraw(self, value):
        if self.account_bal >= int(value):
            self.account_bal -= int(value)
            print(f"Transaction Successful!\nBalance: ${self.account_bal}\n")
        else:
            print(f"Insufficient Funds!\nCurrent Balance: ${self.account_bal}\n")




#--- NOTE: functions in menu_gtb()
#--- making a deposit
def depAMT():
    with connection.cursor() as cursor:
        # getting amount and account number
        amount = int(input("Enter Deposit Amount: "))
        a_num = int(input("Enter Account No: "))

        # requesting account balance from database
        data = (a_num,)
        query = "SELECT acc_balance FROM account_info WHERE acc_number = %s";
        cursor.execute(query, data)
        result = cursor.fetchone()

        # updating account balance
        a_bal = result[0] + amount
        data1 = (a_bal, a_num)
        query1 = ("UPDATE account_info SET acc_balance = %s WHERE acc_number = %s");
        cursor.execute(query1, data1)
        connection.commit()

        # adding record to transaction table
        fk = f"SELECT cust_id FROM account_info WHERE acc_number = {a_num}"
        trans_type = "CREDIT"
        trans_status = "Successful"
        trans_date = dt.now()
        data2 = (fk, trans_type, amount, trans_status, trans_date)
        query2 = ("INSERT INTO transaction_info(cust_id, type, amount, status, datestamp) VALUES (%s, %s, %s, %s, %s)");
        cursor.execute(query2, data2)
        connection.commit()

        # checking new balance
        data3 = (a_num,)
        query3 = "SELECT acc_balance FROM account_info WHERE acc_number = %s";
        cursor.execute(query3, data3)
        balance = cursor.fetchone()
        print(f"Transaction Successful! Account Balance: {balance}")
        menu_gtb()


#--- withdrawing an amount
def widAMT():
    with connection.cursor as cursor:
  # getting amount and account number
        amount = int(input("Enter Withdrawal Amount: "))
        a_num = int(input("Enter Account No: "))

        # requesting account balance from database
        data = (a_num,)
        query = "SELECT acc_balance FROM account_info WHERE acc_number = %s";
        cursor.execute(query, data)
        result = cursor.fetchone()

        # updating account balance
        if result[0] > amount:
            a_bal = result[0] - amount
            data1 = (a_bal, a_num)
            query1 = ("UPDATE account_info SET acc_balance = %s WHERE acc_number = %s");
            cursor.execute(query1, data1)
            connection.commit()

            # adding record to transaction table
            fk = f"SELECT cust_id FROM account_info WHERE acc_number = {a_num}"
            trans_type = "DEBIT"
            trans_status = "Successful"
            trans_date = dt.now()
            data2 = (fk, trans_type, amount, trans_status, trans_date)
            query2 = ("INSERT INTO transaction_info(cust_id, type, amount, status, datestamp) VALUES (%s, %s, %s, %s, %s)");
            cursor.execute(query2, data2)
            connection.commit()

            # checking new balance
            data3 = (a_num,)
            query3 = "SELECT acc_balance FROM account_info WHERE acc_number = %s";
            cursor.execute(query3, data3)
            balance = cursor.fetchone()
            print(f"Transaction Successful! Account Balance: {balance}")
            menu_gtb()
        
        else:
            # adding record to transaction table
            fk = f"SELECT cust_id FROM account_info WHERE acc_number = {a_num}"
            trans_type = "DEBIT"
            trans_status = "Failed"
            trans_date = dt.now()
            data2 = (fk, trans_type, amount, trans_status, trans_date)
            query2 = ("INSERT INTO transaction_info(cust_id, type, amount, status, datestamp) VALUES (%s, %s, %s, %s, %s)");
            cursor.execute(query2, data2)
            connection.commit()

            # checking new balance
            data3 = (a_num,)
            query3 = "SELECT acc_balance FROM account_info WHERE acc_number = %s";
            cursor.execute(query3, data3)
            balance = cursor.fetchone()
            print(f"Transaction Failed! Account Balance: {balance}")
            menu_gtb()


#--- balance enquiry
def balENQ():
    with connection.cursor() as cursor:
        # getting account number
        a_num = int(input("Enter Account No: "))

        # retrieving balance from database
        data = (a_num,)
        query = ("SELECT * FROM account_info WHERE acc_number = %s")
        cursor.execute(query, data)
        result = cursor.fetchone()
        print(f"Account Balance for {a_num} is {result[-2]}")
        menu_gtb()



#*** menu function
def menu_gtb():
    while True:
        print("""
            ** HELLO, Goodday to you **
            > ENTER 1 to Make a Deposit
            > ENTER 2 to Withdraw an amount
            > ENTER 3 to Check Account Balance
            > ENTER 0 to Logout!
        """)
        option = int(input("Enter option: "))

        if option == 1:
            depAMT()
        elif option == 2:
            widAMT()
        elif option == 3:
            balENQ()
        elif option == 0:
            print("Thank you for banking with us!")
            break
        else:
            print("INVALID option entered.")



#--- NOTE: functions in main_gtb()
#--- register new account
def regAcc():
    with connection.cursor() as cursor:
        print("""
            *** Thank you for choosing Grey Trust Bank!
            > To register an account, please provide the following information...
        """)

        # collecting customer info
        name = input("Enter name: ")
        gender = input("Enter gender: ")
        residence = input("Enter address: ")
        dob = input("Enter date of birth: ")
        pin = input("Enter account pin, maxlength of 8 characters: ")

        # creating customer instance with info
        customer = GreyTrustBank(name, gender, residence, dob, pin)
        n, gd, r, db, p = customer.get_name, customer.get_gender, customer.get_residence, customer.get_dob, customer.get_pin;

        # adding to database and calling the main function afterwards
        data1 = (n, gd, r, db, p)
        query1 = ("INSERT INTO customer_info(fullname, gender, residence, dob, pin) VALUES (%s, %s, %s, %s, %s)");
        cursor.execute(query1, data1)
        connection.commit()

        print("Data Entered Successfully!")
        main_gtb()


 
#--- open account
def openAcc():
    with connection.cursor() as cursor:
        # requesting customer details
        print("""
            *** PLease confirm the following registration details...
        """)

        # collecting details
        name = input("Enter name: ")
        pin = input("Enter account pin, maxlength of 8 characters: ")

        # fetching customer_info and generating account number
        data = (name, pin)
        query = ("SELECT * FROM customer_info WHERE fullname = %s AND pin = %s");
        cursor.execute(query, data)
        result = cursor.fetchone()

        # init bank object
        customer = GreyTrustBank(result[1], result[2], result[3], result[4], result[5])
        a_num, a_balance, a_pin = customer.account_num, customer.account_bal, customer.get_pin;

        # inserting into account_info table
        fk = f"SELECT id FROM customer_info WHERE fullname = {result[1]} AND pin = {result[5]}"
        data2 = (fk, a_num, a_balance, a_pin)
        query2 = ("INSERT INTO account_info(cust_id, acc_number, acc_balance, acc_pin) VALUES (%s, %s, %s, %s)");
        cursor.execute(query2, data2)
        connection.commit()

        print(f"""
            Data Entered Successfully! Account Number: {a_num}, Account Pin: {a_pin}
            GUARD THIS INFORMATION JEALOUSLY!
        """)
        main_gtb()



#--- login to existing account
def loginAcc():
    with connection.cursor() as cursor:
        print("Please ENTER LOGIN details")
        num = int(input("Account Number: "))
        pin = int(input("Account PIN: "))

        # sql stuff
        data = (num, pin)
        query = ("SELECT * FROM account_info WHERE acc_number = %s AND acc_pin = %s");
        cursor.execute(query, data)

        if cursor.rowcount <= 0:
            print("Unable to LOGIN")
            main_gtb()
        else:
            print("LOGIN Succesful!")
            menu_gtb()



#*** main function
def main_gtb():
    while True:
        print("""
            *** WELCOME TO GREY TRUST BANK ***
            > ENTER 1 to REGISTER a new Account
            > ENTER 2 to OPEN Account
            > ENTER 3 to LOGIN your Account
            > ENTER 0 to exit
        """)
        option = str(input("Enter option: "))

        if option == '1':
            regAcc()
        elif option == '2':
            openAcc()
        elif option == '3':
            loginAcc()
        elif option == '0':
            print("Have a nice day")
            break
        else:
            print("INVALID option entered.")


#--- running program
main_gtb()





































# ? admin session
# def admin_sesh():
#     print("""
#         > 1. Register new account
#         > 2. Login existing account
#         > 3. Delete existing account
#         > 4. Logout
#     """)
#     option = str(input("Option: "))

#     if option == '1':
#         regAcc()
#     elif option == '2':
#         loginAcc()
#     elif option == '3':
#         print("delAcc function here...")
#     elif option == '4':
#         print("Exiting...")
#         pass
#     else:
#         print("INVALID option!")


# ? admin login
# def auth_admin():
#     print("""ADMIN LOGIN""")
#     username = input("Username: ")
#     password = input("Password: ")

#     if username == "collins":
#         if password == "reverent":
#             admin_sesh()
#         else:
#             print("INCORRECT Password!")
#     else:
#         print("LOGIN not recognised")
#
#
#
# def regAcc():
#     with connection.cursor() as cursor:
#         print("""
#             *** Thank you for choosing Grey Trust Bank!
#             > To register an account, please provide the following information...
#         """)

#         # collecting customer info
#         name = input("Enter name: ")
#         gender = input("Enter gender: ")
#         residence = input("Enter address: ")
#         dob = input("Enter date of birth: ")
#         pin = input("Enter account pin, 5 digits max: ")

#         # creating customer instance with info
#         customer = GreyTrustBank(name, gender, residence, dob, pin)
#         n, gd, r, db = customer.get_name, customer.get_gender, customer.get_residence, customer.get_dob;
#         a_num, a_balance, a_pin = customer.account_num, customer.account_bal, customer.get_pin;

#         # adding to database and calling the main function afterwards
#         data1 = (n, gd, r, db)
#         query1 = ("INSERT INTO customer_info(fullname, gender, residence, dob) VALUES (%s, %s, %s, %s)");
#         cursor.execute(query1, data1)
#         connection.commit()

#         fk = f"SELECT id FROM customer_info WHERE fullname = {n}"
#         data2 = (fk, a_num, a_balance, a_pin)
#         query2 = ("INSERT INTO account_info(cust_id, acc_number, acc_balance, acc_pin) VALUES (%s, %s, %s, %s)");
#         cursor.execute(query2, data2)
#         connection.commit()

#         print(f"""
#             Data Entered Successfully! Account Number: {a_num}, Account Pin: {a_pin}
#             GUARD THIS INFORMATION JEALOUSLY!
#         """)
#         main_gtb()


















