import mysql.connector
import hashlib
import re
import smtplib
import random
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ANSI color codes for text styling
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
flag=False

# Function to display title with colors
def print_title(title):
    print(f"{BOLD}{CYAN}{title.center(150)}{RESET}")

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to validate password
def validate_password(password):
    if len(password) < 8:
        return f"{RED}❌ Password must be at least 8 characters long!{RESET}"
    if not re.search(r'[A-Z]', password):
        return f"{RED}❌ Password must contain at least one uppercase letter!{RESET}"
    if not re.search(r'[a-z]', password):
        return f"{RED}❌ Password must contain at least one lowercase letter!{RESET}"
    if not re.search(r'\d', password):
        return f"{RED}❌ Password must contain at least one digit!{RESET}"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return f"{RED}❌ Password must contain at least one special character!{RESET}"
    return None

# Function to send OTP via Gmail
def send_otp(email):
    otp = str(random.randint(100000, 999999))
    
    sender_email = "yagneshsuthar251@gmail.com"  # Replace with your Gmail
    sender_password = "etoe vogz auos goya"  # Replace with your App Password
    subject = "Your OTP for GameZone"
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    
    body = f"""
    <html>
        <body>
            <h2 style="color:blue; text-align:center;">GAME ZONE </h2>
            <p>Your OTP for registration is: <b style="color:red;">{otp}</b></p>
            <p>Do not share this OTP with anyone.</p>
        </body>
    </html>
    """
    
    message.attach(MIMEText(body, "html"))
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        
        print(f"{GREEN}✅ OTP sent successfully to {email}{RESET}")
    except Exception as e:
        print(f"{RED}❌ Error sending email: {e}{RESET}")
    
    return otp

# Function to register a user
def register_user():
    print_title("🔹 REGISTER USER 🔹")
    
    name = input(f"{BOLD}{WHITE}Enter Name: {RESET}")
    email = input(f"{BOLD}{WHITE}Enter Email (Gmail only): {RESET}")

    if not re.match(r'^[a-zA-Z0-9_.+-]+@gmail\.com$', email):
        print(f"{RED}❌ Only Gmail addresses are allowed!{RESET}")
        return

    password = input(f"{BOLD}{WHITE}Enter Password: {RESET}")
    password_error = validate_password(password)
    if password_error:
        print(password_error)
        return

    contact = input(f"{BOLD}{WHITE}Enter Contact: {RESET}")

    otp = send_otp(email)
    user_otp = input(f"{BOLD}{WHITE}Enter the OTP sent to your email: {RESET}")

    if user_otp != otp:
        print(f"{RED}❌ Invalid OTP! Registration failed.{RESET}")
        return

    print(f"{GREEN}✅ OTP verified successfully!{RESET}")

    conn = mysql.connector.connect(host="localhost", user="root", password="", database="game_zone")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (Name, User_email, Pass_Hash,coins) VALUES (%s, %s, %s, %s)",
                       (name, email, hash_password(password), 100))
        conn.commit()
        print(f"{GREEN}✅ Registration successful!{RESET}")
    except mysql.connector.IntegrityError:
        print(f"{RED}❌ Error: Email already exists!{RESET}")
    conn.close()

# Function to authenticate user
def login_user():
    print_title("🔹 USER LOGIN 🔹")
    global email
    email = input(f"{BOLD}{WHITE}Enter Email: {RESET}")
    password = input(f"{BOLD}{WHITE}Enter Password: {RESET}")

    conn = mysql.connector.connect(host="localhost", user="root", password="", database="game_zone")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE User_email = %s AND Pass_Hash = %s", (email, hash_password(password)))
    user = cursor.fetchone()
    conn.close()

    if user:
        global flag
        flag=True
        print(f"{GREEN}✅ Login successful! Welcome, {user[1]} ({user[2]}){RESET}")
    else:
        print(f"{RED}❌ Invalid credentials!{RESET}")

# Main function to display menu
def main():
    while True:
        print_title(f"{BOLD}{YELLOW}1. Register{RESET}")
        print_title(f"{BOLD}{BLUE}2. Login{RESET}")
        print_title(f"{BOLD}{RED}3. Exit{RESET}")

        choice = input(f"\n{BOLD}{WHITE}Choose an option: {RESET}")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
            if flag == True : 
                break
        elif choice == '3' : 
            break
        else:
            print(f"{RED}❌ Invalid choice! Please select a valid option.{RESET}")

