
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

#--- NOTE: mysql commands to create greytrust database and its tables
# CREATE DATABASE greytrust;
# CREATE TABLE customer_info ( id INT(10) AUTO_INCREMENT NOT NULL PRIMARY KEY, fullname VARCHAR(32) NOT NULL, gender VARCHAR(15) NOT NULL, residence VARCHAR(255) NOT NULL, dob VARCHAR(25) NOT NULL, pin VARCHAR(8) NOT NULL)
# CREATE TABLE transaction_info ( id INT(10) AUTO_INCREMENT NOT NULL PRIMARY KEY, cust_id INT(10), FOREIGN KEY transaction_info(cust_id) REFERENCES account_info(cust_id), type VARCHAR(6) NOT NULL, amount FLOAT(15, 2) NOT NULL, status VARCHAR(10) NOT NULL, datestamp DATETIME NOT NULL);
# CREATE TABLE account_info (id INT(10) AUTO_INCREMENT NOT NULL PRIMARY KEY, cust_id INT(10), FOREIGN KEY account_info(cust_id) REFERENCES customer_info(id), acc_number INT(10) NOT NULL, acc_balance FLOAT(15, 2) NOT NULL, acc_pin VARCHAR(8) NOT NULl )



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

    @property
    def get_accountNo(self):
        return self.account_num

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



#*** Functions In Menu
#--- making a deposit
def depAMT():
    with connection.cursor() as cursor:
        # getting amount and account number
        amount = int(input("Enter Deposit Amount: "))
        acc_num = int(input("Enter Account No: "))

        # requesting account balance from database
        data = (acc_num,)
        query = "SELECT * FROM account_info WHERE acc_number = %s";
        cursor.execute(query, data)
        result = cursor.fetchone()
        res = list(result.values())

        # updating account balance
        acc_bal = res[-2] + amount
        data1 = (acc_bal, acc_num)
        query1 = ("UPDATE account_info SET acc_balance = %s WHERE acc_number = %s");
        cursor.execute(query1, data1)
        connection.commit()

        # adding record to transaction table
        fk = res[1]
        trans_type = "CREDIT"
        trans_status = "Successful"
        trans_date = dt.now()
        data2 = (fk, trans_type, amount, trans_status, trans_date)
        query2 = ("INSERT INTO transaction_info(cust_id, type, amount, status, datestamp) VALUES (%s, %s, %s, %s, %s)");
        cursor.execute(query2, data2)
        connection.commit()

        # checking new balance
        data3 = (acc_num,)
        query3 = "SELECT acc_balance FROM account_info WHERE acc_number = %s";
        cursor.execute(query3, data3)
        result3 = cursor.fetchone()
        balance = list(result3.values())[0]
        print(f"Transaction Successful! Account Balance: {balance}")
        menu_gtb()


#--- withdrawing an amount
def widAMT():
    with connection.cursor() as cursor:
  # getting amount and account number
        amount = int(input("Enter Withdrawal Amount: "))
        acc_num = int(input("Enter Account No: "))

        # requesting account balance from database
        data = (acc_num,)
        query = "SELECT * FROM account_info WHERE acc_number = %s";
        cursor.execute(query, data)
        result = cursor.fetchone()
        res = list(result.values())

        # updating account balance
        if res[-2] > amount:
            a_bal = res[-2] - amount
            data1 = (a_bal, acc_num)
            query1 = ("UPDATE account_info SET acc_balance = %s WHERE acc_number = %s");
            cursor.execute(query1, data1)
            connection.commit()

            # adding record to transaction table
            fk = res[1]
            trans_type = "DEBIT"
            trans_status = "Successful"
            trans_date = dt.now()
            data2 = (fk, trans_type, amount, trans_status, trans_date)
            query2 = ("INSERT INTO transaction_info(cust_id, type, amount, status, datestamp) VALUES (%s, %s, %s, %s, %s)");
            cursor.execute(query2, data2)
            connection.commit()

            # checking new balance
            data3 = (acc_num,)
            query3 = "SELECT acc_balance FROM account_info WHERE acc_number = %s";
            cursor.execute(query3, data3)
            result3 = cursor.fetchone()
            balance = list(result3.values())[0] 
            print(f"Transaction Successful! Account Balance: {balance}")
            menu_gtb()
        
        else:
            # adding record to transaction table
            fk = res[1]
            trans_type = "DEBIT"
            trans_status = "Failed"
            trans_date = dt.now()
            data2 = (fk, trans_type, amount, trans_status, trans_date)
            query2 = ("INSERT INTO transaction_info(cust_id, type, amount, status, datestamp) VALUES (%s, %s, %s, %s, %s)");
            cursor.execute(query2, data2)
            connection.commit()

            # checking new balance
            data3 = (acc_num,)
            query3 = "SELECT acc_balance FROM account_info WHERE acc_number = %s";
            cursor.execute(query3, data3)
            result3 = cursor.fetchone()
            balance = list(result3.values())[0] 
            print(f"Transaction Failed! Account Balance: {balance}")
            menu_gtb()


#--- balance enquiry
def balENQ():
    with connection.cursor() as cursor:
        # getting account number
        a_num = int(input("Enter Account No: "))
        a_pin = input("Enter PIN: ")

        # retrieving balance from database
        data = (a_num, a_pin)
        query = ("SELECT * FROM account_info WHERE acc_number = %s AND acc_pin = %s")
        cursor.execute(query, data)
        result = cursor.fetchone()
        balance = list(result.values())[-2]
        print(f"Account Balance for {a_num} is {balance}")
        menu_gtb()



#*** Menu 
def menu_gtb():
    while True:
        print("""
            ** HELLO, Goodday to you **
            > ENTER 1 to Make a Deposit
            > ENTER 2 to Withdraw an amount
            > ENTER 3 to Check Account Balance
            > ENTER 0 to Logout!
        """)
        option = input("Enter option: ")

        if option == '1':
            depAMT()
        elif option == '2':
            widAMT()
        elif option == '3':
            balENQ()
        elif option == '0':
            print("Thank you for banking with us!")
            break
        else:
            print("INVALID option entered.")



#*** Functions In Main
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

 
#--- open registered account
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
        res = list(result.values())
        fk = res[0]
        customer = GreyTrustBank(res[1], res[2], res[3], res[4], res[5])
        a_num, a_balance, a_pin = customer.get_accountNo, customer.account_bal, customer.get_pin;

        # adding to database
        data2 = (fk, a_num, a_balance, a_pin)
        query2 = ("INSERT INTO account_info(cust_id, acc_number, acc_balance, acc_pin) VALUES (%s, %s, %s, %s)");
        cursor.execute(query2, data2)
        connection.commit()

        print(f"""
            Data Entered Successfully! 
            Account Number: {a_num}, Account Pin: {a_pin}
            PLEASE SAVE credentials for future use!
        """)
        main_gtb()


#--- login to existing account
def loginAcc():
    with connection.cursor() as cursor:
        print("Please ENTER LOGIN details")
        num = int(input("Account Number: "))
        pin = input("Account PIN: ")

        # fetching account info from account_info table
        data = (num, pin)
        query = ("SELECT * FROM account_info WHERE acc_number = %s AND acc_pin = %s");
        cursor.execute(query, data)
        result = cursor.fetchone()
        res = list(result.values())

        # checking if account info is in account_info table
        if num not in res and pin not in res:
            print("Unable to LOGIN")
            main_gtb()
        else:
            print("LOGIN Succesful!")
            menu_gtb()



#*** MAIN
def main_gtb():
    while True:
        print("""
            *** WELCOME TO GREY TRUST BANK ***
            > ENTER 1 to REGISTER a new Account
            > ENTER 2 to OPEN Account
            > ENTER 3 to LOGIN your Account
            > ENTER 0 to exit
        """)
        option = input("Enter option: ")

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


#*** run program
main_gtb()




















































