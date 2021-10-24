#--- Database Functions
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


#--- Bank App logic
import random as rd

#--- creating bank object
class GreyTrustBank():
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age
        self.account_num = rd.randrange(0000000000, 9999999999)
        self.acc_bal = 0 

    #- accessing class attributes
    @property
    def get_id(self):
        return self.id

    @property
    def get_name(self):
        return self.name

    @property
    def get_age(self):
        return self.age

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


#--- creating customer instance
print("* Hello! To register an account, please provide;\n- A Custom ID, Full Name & Age.\n")
user_id = input("Enter custom ID here: ")
user_name = input("Enter name here: ")
user_age = input("Enter age here: ")
customer = GreyTrustBank(user_id, user_name, user_age)







def menu_gtb():
    print("""
        * Welcome to GreyTrust Bank!
        > ENTER 1 to view Account Details
        > ENTER 2 to Make a Deposit
        > ENTER 3 to Withdraw an amount
        > ENTER 4 to Check Account Balance
        > ENTER 0 to Exit!
    """)
    choice = int(input("Enter option here: "))

    if choice == 1:
        print(f"- {customer.get_name}, Account: {customer.account_num}\n")

    elif choice == 2:
        amount = input("Enter amount here: ")
        customer.deposit(amount)

    elif choice == 3:
        amount = input("Enter amount here: ")
        customer.withdraw(amount)

    elif choice == 4:
        print(customer.balance())

    elif choice == 0:
        print("Thank you for banking with us!")
        pass


#--- running program
menu_gtb()






























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