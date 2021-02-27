import random
import sqlite3
import sys


def luhn(card_num):
    odd_digits = []
    even_digits = []
    all_digits = []
    total = 0
    num = card_num[0:15]
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


class Account:
    def __init__(self, card_num=None, pin=None):
        self.card_num = card_num
        self.pin = pin
        self.balance = 0

    def generate_card_num(self):
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
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
'''))
    menu_2_selection = input()
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()
    if menu_2_selection == '1':
        balance = get_balance(card_num)
        if balance == None:
            balance = '0'
        print('Balance: ' + str(balance))
        print('')
        menu_2_selection = menu_2(card_num)
    elif menu_2_selection == '2':
        # add income to current balance, update db with new balance
        income = input("Enter income:")
        c.execute("SELECT balance FROM card WHERE number = (?)", (card_num,))
        balance = c.fetchall()[0]
        balance = balance[0]
        new_balance = int(balance) + int(income)
        c.execute("UPDATE card SET balance = (?) WHERE number = (?)", (new_balance, card_num))
        conn.commit()
        print('Income was added!')
        menu_2_selection = menu_2(card_num)
    elif menu_2_selection == '3':
        # do transfer
        transfer_card = input('Enter card number:')
        if luhn(transfer_card) == int(transfer_card[-1]):
            pass
        else:
            print('Probably you made a mistake in the card number. Please try again!')
        c.execute("SELECT * FROM card WHERE number = (?)", (transfer_card,))
        transfer_acct = c.fetchall()
        if transfer_acct == []:
            print('Such a card does not exist.')
        elif transfer_card in transfer_acct[0][1]:
            ta_balance = transfer_acct[0][3]
            to_transfer = int(input('Enter how much money you want to transfer:'))
            main_balance = get_balance(card_num)
            if to_transfer <= main_balance:
                main_balance = main_balance - to_transfer
                c.execute("UPDATE card SET balance = (?) WHERE number = (?)", (main_balance, card_num))
                ta_balance = ta_balance + to_transfer
                c.execute("UPDATE card SET balance = (?) WHERE number = (?)", (ta_balance, transfer_card))
                conn.commit()
                print('Success!')
            else:
                print('Not enough money!')
        else:
            print('Probably you made a mistake in the card number. Please try again!')
        menu_2_selection = menu_2(card_num)
    elif menu_2_selection == '4':
        #close account
        c.execute("DELETE FROM card WHERE number = (?)", (card_num,))
        conn.commit()
        print('The account has been closed!')
    elif menu_2_selection == '5':
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


def get_balance(card_num):
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()
    c.execute("SELECT balance FROM card WHERE number = (?)", (card_num,))
    balance = c.fetchall()[0]
    balance = balance[0]
    return balance



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
