balance = 5000
pin = "1234"


def login():
    user_pin = input("Enter PIN: ")

    if user_pin == pin:
        print("Login successful")
        return True
    else:
        print("Invalid PIN")
        return False


def balance_inquiry():
    print("Current Balance:", balance)


def withdraw():
    global balance

    amount = int(input("Enter withdrawal amount: "))

    if amount <= balance:
        balance -= amount
        print("Withdrawal successful")
        print("Remaining Balance:", balance)
    else:
        print("Insufficient balance")


def deposit():
    global balance

    amount = int(input("Enter deposit amount: "))
    balance += amount

    print("Deposit successful")
    print("Current Balance:", balance)


def change_pin():
    global pin

    new_pin = input("Enter new PIN: ")
    pin = new_pin

    print("PIN changed successfully")


def main():
    if not login():
        return

    while True:
        print("\n===== ATM SYSTEM =====")
        print("1. Balance Inquiry")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. Change PIN")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            balance_inquiry()
        elif choice == "2":
            withdraw()
        elif choice == "3":
            deposit()
        elif choice == "4":
            change_pin()
        elif choice == "5":
            print("Thank you")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
