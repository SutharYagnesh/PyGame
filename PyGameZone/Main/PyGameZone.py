import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import random
import GameZone_Login as login
import Free_Game as free
import Paid_Game as paid
import TransactionHandler_PY as th
# ---------------- Database Class ----------------
class GameDatabase:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="game_zone"
        )
        self.cursor = self.conn.cursor()
        
    def update_coins(self, username, coins):
        self.cursor.execute("UPDATE Users SET coins = coins + %s WHERE Name = %s", (coins, username))
        self.conn.commit()

    def get_coins(self, username):
        self.cursor.execute("SELECT coins FROM Users WHERE Name = %s", (username,))
        return self.cursor.fetchone()[0]

    def close(self):
        self.conn.close()

# ---------------- Game Class ----------------
class Game:
    def __init__(self, username):
        self.username = username
        self.db = GameDatabase()

    def play_game(self, game_type):
        coins = self.db.get_coins(self.username)
        if game_type == "free" or (game_type == "paid" and coins >= 10):
            outcome = random.choice(["win", "lose"])
            reward = np.random.randint(5, 20) if outcome == "win" else -10
            self.db.update_coins(self.username, reward)
            print(f"🎮 Game Over! You {'won' if reward > 0 else 'lost'} {abs(reward)} coins!")
        else:
            print("❌ Not enough coins to play this game!")

    def withdraw_coins(self, amount):
        coins = self.db.get_coins(self.username)
        if amount <= coins:
            self.db.update_coins(self.username, -amount)
            print(f"✅ Successfully withdrew {amount} coins!")
        else:
            print("❌ Not enough coins to withdraw!")

# ---------------- Analytics ----------------
def show_analytics(username):
    db = GameDatabase()
    coins = db.get_coins(username)
    history = [coins + np.random.randint(-10, 20) for _ in range(10)]  # Simulating history
    plt.plot(history, marker='o', linestyle='-')
    plt.xlabel('Games Played')
    plt.ylabel('Coins')
    plt.title('Coin Trend')
    plt.show()

# ---------------- Main Page ----------------
def main():
    db = GameDatabase()
    print(f""" {login.BOLD}{login.YELLOW}
                                        ██████╗  ███████╗███╗   ███╗███████╗███████╗ ██████╗ ███╗   ██╗███████╗
                                        ██╔════╝ ██╔══██╗████╗ ████║██╔════╝╚══███╔╝██╔═══██╗████╗  ██║██╔════╝
                                        ██║  ███╗███████║██╔████╔██║█████╗    ███╔╝ ██║   ██║██╔██╗ ██║█████╗
                                        ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝   ███╔╝  ██║   ██║██║╚██╗██║██╔══╝
                                        ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗███████╗╚██████╔╝██║ ╚████║███████╗
                                        ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝{login.RESET}\n\n""")
    login.main()
    if login.flag :
        while True:
            print("1. Play Free Game (0 Coins)")
            print("2. Play Paid Game (10 Coins)")
            print("3. Transaction(check,Withdraw,deposit)")
            print("4. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
               free.main()
            elif choice == "2":
                paid.main(login.email)
                pass
            elif choice == "3":
                th.main(login.email)
                pass
            elif choice == "4":
                break
            else:
                print("❌ Invalid choice!")

    db.close()

if __name__ == "__main__":
    main()
