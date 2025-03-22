import random
import mysql.connector
import Color_Treding as ct
class GameDatabase:
    """Handles database interactions for storing and updating user coins."""
    
    def __init__(self):
        """Initialize the database connection."""
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="game_zone"
        )
        self.cursor = self.conn.cursor()

    def update_coins(self, username, coins):
        """Update the user's coin balance in the database."""
        self.cursor.execute("UPDATE Users SET coins = coins + %s WHERE User_email = %s", (coins, username))
        self.conn.commit()

    def get_coins(self, username):
        """Retrieve the user's current coin balance."""
        self.cursor.execute("SELECT coins FROM Users WHERE User_email = %s", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else 0  # Return 0 if user not found

    def close(self):
        """Close the database connection."""
        self.conn.close()

def print_grid(grid):
    """Prints the game grid with colored backgrounds."""
    for i in range(5):
        for j in range(5):
            cell = grid[i][j]
            if cell == 'X':  # Mine detected, apply red background
                print(f"\033[41m\033[97m {cell} \033[0m", end="   ")
            elif cell == 'O':  # Safe cell, apply blue background
                print(f"\033[44m\033[97m {cell} \033[0m", end="   ")
            else:  # Default grid numbers with green background
                print(f"\033[42m\033[97m {cell:2} \033[0m", end="   ")
        print("\n")

def create_mines(num_mines):
    """Randomly selects mine positions."""
    return set(random.sample(range(25), num_mines))

def play_mine(username):
    """Handles the Mine Box game with database integration."""
    db = GameDatabase()

    # Get user balance
    current_coins = db.get_coins(username)
    print(f"\n🔹 {username}, Your current balance: {current_coins} coins.")

    try:
        bet = float(input("Enter your betting amount: $"))
        temp=bet
        if bet > current_coins:
            print("❌ Not enough coins! Lower your bet.")
            db.close()
            return
        num_mines = int(input("Select number of mines (1-24): "))
    except ValueError:
        print("Invalid input! Please enter numeric values.")
        db.close()
        return

    if num_mines < 1 or num_mines > 24:
        print("Invalid number of mines! Exiting...")
        db.close()
        return

    mine_positions = create_mines(num_mines)
    grid = [[f"{i * 5 + j:2}" for j in range(5)] for i in range(5)]
    revealed = set()

    while True:
        print("\nCurrent Grid:")
        print_grid(grid)
        choice = input("Enter box number to open (0-24) or 'cashout' to stop: ")

        if choice.lower() == 'cashout':
            print(f"You cashed out with ${bet:.2f}! 🎉")
            db.update_coins(username, int(bet - temp))  # Update balance
            db.close()
            break

        if not choice.isdigit() or int(choice) not in range(25):
            print("Invalid choice! Choose a number between 0-24.")
            continue

        box_num = int(choice)
        if box_num in revealed:
            print("Box already opened! Choose another.")
            continue

        revealed.add(box_num)
        row, col = divmod(box_num, 5)

        if box_num in mine_positions:
            grid[row][col] = 'X'  # Mark mine position
            print("\n💥 Boom! You hit a mine. You lose!")
            
            # Reveal all mines
            for mine in mine_positions:
                r, c = divmod(mine, 5)
                grid[r][c] = 'X'

            db.update_coins(username, -int(bet))  # Deduct coins on loss
            print_grid(grid)
            db.close()
            break
        else:
            grid[row][col] = 'O'
            bet *= 1.2  # Reward multiplier
            print(f"✅ Safe! Your new bet value is: ${bet:.2f}")

            if len(revealed) == (25 - num_mines):
                print("\n🎉 You cleared all safe boxes! You win!")
                db.update_coins(username, int(bet))  # Update balance on win
                db.close()
                break

def main(username):
    """Main menu for game selection."""
    while True:
        print("\n🔴 Welcome To Paid Game Zone 🔴")
        print(" 1. Mine Box  ")
        print(" 2. Color Trading   ")
        print(" 3. Exit  ")

        choice = input("Enter Your Choice: ")
        if choice == '1':
            play_mine(username)
        elif choice == '2':
            ct.ColorTrendingGame(username)
        elif choice == '3':
            print("Exiting game. See you next time!")
            break
        else:
            print("Enter a valid choice!")