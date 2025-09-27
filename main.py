import json
import random
import string
from pathlib import Path


class Bank:
    database = 'data.json'
    data = []

    # Load data if file exists
    try:
        if Path(database).exists():
            with open(database, 'r') as file:
                data = json.load(file)
    except Exception as e:
        print(f"An exception occurred: {e}")

    @classmethod
    def __update(cls):
        """Update the JSON file with latest bank data"""
        with open(cls.database, 'w') as file:
            json.dump(cls.data, file, indent=4)

    @classmethod
    def _find_user(cls, accnumber, pin):
        """Helper method to find a user by account number and pin"""
        return [u for u in cls.data if u['account_number'] == accnumber and u['pin'] == pin]

    def create_account(self):
        info = {
            "name": input("Enter your name: "),
            "age": int(input("Enter your age: ")),
            "email": input("Enter your email: "),
            "pin": input("Enter your 4-digit pin: "),
            "account_number": ''.join(random.choices(string.digits, k=10)),
            "balance": 0
        }

        if info['age'] < 18 or info['age'] > 65:
            print("❌ You are not eligible to create an account")
        elif len(info['pin']) != 4 or not info['pin'].isdigit():
            print("❌ Pin must be a 4-digit number")
        else:
            print("\n✅ Account created successfully!\n")
            for k, v in info.items():
                print(f"{k}: {v}")
            print("\nPlease note down your account number for future reference\n")

            Bank.data.append(info)
            Bank.__update()

    def deposit_money(self):
        accnumber = input("Enter your account number: ")
        pin = input("Enter your pin: ")

        user = self._find_user(accnumber, pin)
        if not user:
            print("❌ No account found")
            return

        amount = int(input("Enter amount to deposit: "))
        if amount <= 0:
            print("❌ Amount must be greater than zero")
        elif amount > 100000:
            print("❌ Amount exceeds deposit limit (100000)")
        else:
            user[0]['balance'] += amount
            print(f"✅ Dear {user[0]['name']}, your deposit was successful!")
            print(f"💰 New Balance: {user[0]['balance']}")
            Bank.__update()

    def withdraw(self):
        accnumber = input("Enter your account number: ")
        pin = input("Enter your pin: ")

        user = self._find_user(accnumber, pin)
        if not user:
            print("❌ No account found")
            return

        amount = int(input("Enter amount to withdraw: "))
        if user[0]['balance'] < amount:
            print("❌ Insufficient balance")
        else:
            user[0]['balance'] -= amount
            print(f"✅ Withdrawal successful, {user[0]['name']}!")
            print(f"💰 New Balance: {user[0]['balance']}")
            Bank.__update()

    def balance_enquiry(self):
        accnumber = input("Enter your account number: ")
        pin = input("Enter your pin: ")

        user = self._find_user(accnumber, pin)
        if not user:
            print("❌ No account found")
        else:
            print("\n📋 Your account details:")
            for k, v in user[0].items():
                print(f"{k}: {v}")

    def update_account(self):
        accnumber = input("Enter your account number: ")
        pin = input("Enter your pin: ")

        user = self._find_user(accnumber, pin)
        if not user:
            print("❌ No account found")
            return

        u = user[0]
        print("\nFill details to update (leave empty to keep current value):")

        newdata = {
            "name": input(f"Name ({u['name']}): ") or u['name'],
            "email": input(f"Email ({u['email']}): ") or u['email'],
            "pin": input(f"Pin ({u['pin']}): ") or u['pin'],
            "age": u['age'],
            "account_number": u['account_number'],
            "balance": u['balance']
        }

        u.update(newdata)
        Bank.__update()
        print(f"✅ Dear {u['name']}, your account has been updated successfully!")

    def close_account(self):
        accnumber = input("Enter your account number: ")
        pin = input("Enter your pin: ")

        user = self._find_user(accnumber, pin)
        if not user:
            print("❌ No account found")
            return

        confirmation = input("Are you sure you want to close your account? (yes/no): ")
        if confirmation.lower() == 'yes':
            Bank.data.remove(user[0])
            Bank.__update()
            print(f"✅ Dear {user[0]['name']}, your account has been closed successfully!")
        else:
            print("❌ Account closure cancelled.")