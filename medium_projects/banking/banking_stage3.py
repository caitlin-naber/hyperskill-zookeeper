import random
import sqlite3
import sys

class Account:
    def __init__(self, card_num=None, pin=None):
        self.card_num = card_num
        self.pin = pin
        self.balance = 0

    def generate_card_num(self):
        def luhn(num):
            odd_digits = []
            even_digits = []
            all_digits = []
            total = 0
            for x in range(len(num)):
                if x % 2 == 0:
                    odd_digits.append(int(num[x]))
                else:
                    even_digits.append(int(num[x]))
            for x in range(len(odd_digits)):
                odd_digits[x] = odd_digits[x] * 2
            for x in range(len(odd_digits)):
                if odd_digits[x] > 9:
                    odd_digits[x] -= 9
            for x in odd_digits:
                all_digits.append(x)
            for x in even_digits:
                all_digits.append(x)
            for x in all_digits:
                total += x
            if total % 10 == 0:
                checksum = 0
                return checksum
            else:
                i = str(total)
                i = i[-1]
                i = int(i)
                checksum = 10 - i
                return checksum

        iin = '400000'
        acc_id = random.randint(0, 999999999)
        acc_id = str(acc_id).zfill(9)
        num = str(iin) + acc_id
        num = num + str(luhn(num))
        return num


    def generate_pin(self):
        pin = random.randint(0, 9999)
        pin = str(pin).zfill(4)
        self.pin = pin
        return self.pin


def main_menu():
    print('''1. Create an account
2. Log into account
0. Exit''')
    menu_selection = input()
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()
    if menu_selection == '1':
        new_account = Account()
        card_num = new_account.generate_card_num()
        pin = new_account.generate_pin()
        c.execute("INSERT INTO card (number, pin) VALUES (?, ?)", (card_num, pin))
        c.execute("SELECT * FROM card;")
        conn.commit()
        print(f'''Your card has been created
Your card number:
{card_num}
Your card pin:
{pin}
''')
        print('')
        return card_num
    elif menu_selection == '2':
        card_num = input('Enter your card number:')
        pin = input('Enter your pin:')
        log_in(card_num, pin)
    else:
        print('Bye!')
        sys.exit()


def menu_2(card_num):
    print(('''1. Balance
2. Log out
0. Exit
'''))
    menu_2_selection = input()
    if menu_2_selection == '1':
        check_balance(card_num)
        print('')
        menu_2_selection = menu_2(card_num)
    elif menu_2_selection == '2':
        print('''You have successfully logged out!
        ''')
        menu_selection = main_menu()
        return menu_selection
    else:
        print('Bye!')
        sys.exit()
    return menu_2_selection


def log_in(card_num, pin):
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()
    c.execute("SELECT * FROM card WHERE number = (?)", (card_num,))
    cards = (c.fetchall())
    if cards == []:
        print("Wrong card or PIN!")
        menu_selection = main_menu()
        return menu_selection
    if card_num in cards[0][1]:
        query_pin = cards[0][2]
        if pin == query_pin:
            print("You have successfully logged in!")
            menu_selection = menu_2(card_num)
        else:
            print('''Wrong PIN!
            ''')
            menu_selection = main_menu()
    else:
        print('''Wrong card!
        ''')
        menu_selection = main_menu()
    return menu_selection


def check_balance(card_num):
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()
    c.execute("SELECT balance FROM card WHERE number = (?)", (card_num,))
    balance = c.fetchall()[0]
    balance_only = balance[0]
    if balance_only == None:
        balance_only = '0'
    print('Balance: ' + str(balance_only))

conn = sqlite3.connect('card.s3db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS card (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    );
    ''')


menu_selection = main_menu()

while menu_selection != '0':
    menu_selection = main_menu()
    