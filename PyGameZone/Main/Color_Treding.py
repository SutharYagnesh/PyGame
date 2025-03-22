import random
import mysql.connector
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        return result[0] if result else None  # Return None if user not found
    
    def close(self):
        """Close the database connection."""
        self.conn.close()

class ColorTrendingGame:
    def __init__(self, username):
        self.username = username
        self.db = GameDatabase()
        self.history = []
        self.run_game()

    def generate_numbers(self):
        return [random.randint(0, 20) for _ in range(8)]

    def check_result(self, choice, numbers, bet_number):
        winning_number = random.choice(numbers)
        avg = sum(numbers) / len(numbers)
        result = "Big" if avg >= 5 else "Small"
        win = choice == result or bet_number == winning_number
        return win, result, winning_number

    def format_number(self, number, index):
        colors = [41, 42, 43, 44, 45, 46, 47, 100]  # Different background colors
        return f"\033[1;37;{colors[index % len(colors)]}m {number} \033[0m"

    def format_big(self):
        return "\033[1;37;41m [B] Big \033[0m"  # White text on red background

    def format_small(self):
        return "\033[1;37;42m [S] Small \033[0m"  # White text on green background

    def run_game(self):
        while True:
            clear_screen()
            print("\nGame Grid:")
            numbers = self.generate_numbers()
            for i in range(0, len(numbers), 4):
                print("  ".join(self.format_number(num, i + j) for j, num in enumerate(numbers[i:i+4])))
            
            print("\nChoose Big, Small or a Specific Number (0-10)")
            print(f"{self.format_big()}   {self.format_small()}")
            print(f"Coins: {self.db.get_coins(self.username)}")
            
            attempts = 0
            while attempts < 3:
                choice = input("Enter your choice (B/S/0-10) or Q to quit: ").strip().upper()
                if choice == 'Q':
                    self.db.close()
                    print("Game Over.")
                    return
                elif choice in ['B', 'S']:
                    bet_choice = "Big" if choice == 'B' else "Small"
                    bet_number = None
                    break
                elif choice.isdigit() and 0 <= int(choice) <= 10:
                    bet_number = int(choice)
                    if bet_number in numbers:
                        bet_choice = None
                        break
                    else:
                        print("Number not in generated list. You have one more attempt.")
                        attempts += 1
                else:
                    print("Invalid choice, please enter B, S, or a number between 0-10.")
                    attempts += 1
            else:
                print("You exceeded the allowed attempts. Try again in the next round.")
                continue
            
            bet_amount = int(input("Enter your bet amount: "))
            user_coins = self.db.get_coins(self.username)
            
            if bet_amount > user_coins:
                print("Insufficient coins! Try a lower bet.")
                continue
            
            win, result, winning_number = self.check_result(bet_choice, numbers, bet_number)
            if win:
                coins_won = int(bet_amount * 1.8)
                print(f"Congratulations! The winning number was {winning_number}. You won {coins_won} coins.")
            else:
                coins_won = -bet_amount
                print(f"You lost the bet! The winning number was {winning_number}.")
            
            self.db.update_coins(self.username, coins_won)
            result_text = f"You chose {bet_choice if bet_choice else bet_number}, result: {result}, winning number: {winning_number}, {'Win' if win else 'Lose'}!"
            self.history.append(result_text)
            
            print("Last 5 game results:")
            for entry in self.history[-5:]:
                print(entry)
            input("Press Enter to continue...")
