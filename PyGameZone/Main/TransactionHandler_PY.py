import mysql.connector
import datetime

class GameDatabase:
    """Handles database interactions for storing and updating user coins."""
    
    def __init__(self):
        """Initialize the database connection."""
        try:
            self.conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="game_zone"
            )
            self.cursor = self.conn.cursor()
            print("✅ Database Connected Successfully!")
        except mysql.connector.Error as err:
            print(f"❌ Database Connection Error: {err}")

    def user_exists(self, username):
        """Check if the user exists in the database."""
        self.cursor.execute("SELECT user_id FROM Users WHERE User_email = %s", (username,))
        return self.cursor.fetchone()

    def update_coins(self, username, coins, transaction_type):
        """Update the user's coin balance in the database and log the transaction."""
        user = self.user_exists(username)
        if not user:
            print("❌ User not found!")
            return False

        user_id = user[0]

        # Update coin balance
        self.cursor.execute("UPDATE Users SET coins = coins + %s WHERE User_email = %s", (coins, username))
        self.conn.commit()
        
        # Log the transaction
        self.cursor.execute("""
            INSERT INTO Transactions (user_id, amount, transaction_type, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (user_id, coins, transaction_type, datetime.datetime.now()))
        self.conn.commit()
        return True

    def get_coins(self, username):
        """Retrieve the user's current coin balance."""
        self.cursor.execute("SELECT coins FROM Users WHERE User_email = %s", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else 0  # Return 0 if user not found

    def withdraw_coins(self, username, amount):
        """Withdraw coins from the user's account."""
        current_coins = self.get_coins(username)
        print(f"💰 Available Balance: {current_coins} coins")
        
        if amount > current_coins:
            print("❌ Insufficient coins to withdraw!")
            return False
        
        if self.update_coins(username, -amount, "withdraw"):
            print(f"✅ Successfully withdrew {amount} coins!")
            return True

        return False

    def deposit_coins(self, username, amount):
        """Deposit coins into the user's account by verifying UPI transaction."""
        upi_id = input("Enter your UPI ID for verification: ").strip()
        print(f"💸 Send {amount} coins to UPI ID: gamezone@upi and confirm transaction.")
        confirmation = input("Have you sent the money? (yes/no): ").strip().lower()
        
        if confirmation == 'yes':
            if self.update_coins(username, amount, "buy"):
                print(f"✅ Successfully deposited {amount} coins!")
            else:
                print("❌ Deposit failed due to an error.")
        else:
            print("❌ Transaction not confirmed. Deposit failed.")

    def close(self):
        """Close the database connection."""
        self.conn.close()


def main(username):
    db = GameDatabase()
    
    while True:
        print("\n🔹 1. Check Balance")
        print("🔹 2. Deposit Coins")
        print("🔹 3. Withdraw Coins")
        print("🔹 4. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            balance = db.get_coins(username)
            print(f"💰 Your current balance: {balance} coins")
        elif choice == "2":
            amount = int(input("Enter amount to deposit: "))
            db.deposit_coins(username, amount)
        elif choice == "3":
            amount = int(input("Enter amount to withdraw: "))
            db.withdraw_coins(username, amount)
        elif choice == "4":
            print("👋 Exiting... Goodbye!")
            db.close()
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    user_email = input("Enter your email to login: ").strip()
    main(user_email)
