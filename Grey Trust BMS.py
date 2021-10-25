
#*** Database setup
import pymysql
from pymysql import cursors
from datetime import date as dt

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
    def __init__(self, name, gender, residence, dob, acc_pin):
        self.name = name
        self.gender = gender
        self.residence = residence
        self.dob = dob
        self.pin = acc_pin
        self.account_num = rd.randrange(0000000000, 9999999999)
        self.acc_bal = 0 

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
        return f"Your account balance is: ${self.acc_bal}\n"

    def deposit(self, value):
        self.acc_bal += int(value)
        print(f"Transaction Sucessful!\nBalance: ${self.acc_bal}\n")

    def withdraw(self, value):
        if self.acc_bal >= int(value):
            self.acc_bal -= int(value)
            print(f"Transaction Successful!\nBalance: ${self.acc_bal}\n")
        else:
            print(f"Insufficient Funds!\nCurrent Balance: ${self.acc_bal}\n")



#--- menu function
def menu_gtb():
    while True:
        print("""
            ** HELLO, Goodday to you **
            > ENTER 1 to Make a Deposit
            > ENTER 2 to Withdraw an amount
            > ENTER 3 to Check Account Balance
            > ENTER 0 to Logout!
        """)
        choice = int(input("Enter option here: "))

        if choice == 1:
            depAMT()
        elif choice == 2:
            widAMT()
        elif choice == 3:
            balENQ()
        elif choice == 0:
            print("Thank you for banking with us!")
            pass
        else:
            print("INVALID option entered.")



#*** main_gtb() functions
#--- register new account
def regAcc():
    with connection.cursor() as cursor:
        print("""
            *** Thank you for choosing Grey Trust Bank!
            > To open an account, please provide the following information...
        """)

        #--- creating customer instance with info
        user_id = input("Enter custom ID here: ")
        user_name = input("Enter name here: ")
        user_age = input("Enter age here: ")
        customer = GreyTrustBank(user_id, user_name, user_age)

 
#--- login to existing account
def loginAcc():
    with connection.cursor() as cursor:
        print("Please ENTER LOGIN details")
        acc_no = int(input("Account Number: "))
        acc_pin = int(input("Account PIN: "))

        # sql stuff
        myQuery = (acc_no, acc_pin)
        mySql = """SELECT * FROM account_info WHERE acc_number = %s AND acc_pin = %s"""
        cursor.execute(mySql, myQuery)

        if cursor.rowcount <= 0:
            print("Unable to LOGIN")
        else:
            print("LOGIN Succesful!")
            menu_gtb()



#*** admin functions
#--- admin session
def admin_sesh():
    print("""
        > 1. Register new account
        > 2. login existing account
        > 3. logout
    """)
    choice = int(input("Enter option here: "))

    if choice == 1:
        regAcc()
    elif choice == 2:
        loginAcc()
    elif choice == 3:
        print("Exiting...")
        pass
    else:
        print("INVALID option!")


#--- admin login
def auth_admin():
    print("""ADMIN LOGIN""")
    username = input("Username: ")
    password = input("Password: ")

    if username == "collins":
        if password == "reverent":
            admin_sesh()
        else:
            print("INCORRECT Password!")
    else:
        print("LOGIN not recognised")



#*** main function
def main_gtb():
    while True:
        print("""
            *** WELCOME TO GREY TRUST BANK ***
            > ENTER 1 to LOGIN your Account
            > ENTER 2 to REGISTER a new Account
            > LOGIN as ADMIN
            > ENTER 0 to exit
        """)
        choice = int(input("Enter option here: "))

        if choice == 1:
            loginAcc()
        elif choice == 2:
            regAcc()
        elif choice == 37:
            auth_admin()
        elif choice == 0:
            print("Have a nice day")
            pass
        else:
            print("INVALID option entered.")


#--- running program
main_gtb()






























#-------------------------
# def create_table():
#     with connection.cursor() as cursor:
#         add_table = """
#             CREATE TABLE IF NOT EXISTS e_data(      
#                 id INT(10) AUTO_INCREMENT NOT NULL PRIMARY KEY,
#                 name VARCHAR(20),
#                 sales BIGINT(15),
#                 `date` DATE
#             );     
#         """;
#         cursor.execute(add_table)
#         connection.commit()
        
# # "if not exists" helps to check if a table with that name doesn't already exist
# # create_table() is a static function, as it holds no args


# def write_data(curr_name, curr_amount, curr_date):
#     with connection.cursor() as cursor:
#         add_record = f"""
#             INSERT INTO e_data (name, sales, `date`)
#             VALUES ('{curr_name}', {curr_amount}, '{curr_date}');
#         """;
#         cursor.execute(add_record)
#         connection.commit()


# def just_queries():
#     with connection.cursor() as cursor:
#         my_query = """
#             SELECT name, SUM(sales) AS "total sales" FROM e_data GROUP BY name ORDER BY SUM(sales) DESC
#             LIMIT 10;
#         """
#         cursor.execute(my_query)
#         connection.commit()
#         return cursor.fetchall()


# #- calling create table NOTE: after creating migrations and called migrant function
# create_table()
# output = just_queries()
# print(output)