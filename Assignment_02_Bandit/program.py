import os
import subprocess
import hashlib

username = "admin"
password = "admin123"

def check_user(user, pwd):
    if user == username and pwd == password:
        return True
    return False

def run_command(command):
    os.system(command)

def execute_command(command):
    subprocess.call(command, shell=True)

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def main():
    user = input("Username: ")
    pwd = input("Password: ")

    if check_user(user, pwd):
        print("Login successful")
    else:
        print("Login failed")

    command = input("Enter command: ")
    run_command(command)

    print("Password hash:", hash_password(pwd))


if __name__ == "__main__":
    main()
