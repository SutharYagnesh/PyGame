import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = ''

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY=(128,128,128)
# Game classes
class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.o_score = 0
        self.x_score = 0
        self.games_played = 0

    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                self.winner = row[0]
                return True
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                self.winner = self.board[0][col]
                return True
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            self.winner = self.board[0][0]
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            self.winner = self.board[0][2]
            return True
        # Check for tie
        if all([cell != ' ' for row in self.board for cell in row]):
            self.winner = 'Tie'
            return True
        return False

    def draw_board(self):
        screen.fill(GRAY)
        
        
        cell_size = SCREEN_HEIGHT // 3
        for row in range(3):
            for col in range(3):
                pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size), 3)
                font = pygame.font.Font(None, 120)
                text = font.render(self.board[row][col], True, BLACK)
                text_rect = text.get_rect(center=(col * cell_size + cell_size // 2, row * cell_size + cell_size // 2))
                screen.blit(text, text_rect)
                
    def play(self):
        while not self.check_winner():
            self.draw_board()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    # Calculate row and column indices based on mouse click position
                    row = None
                    col = None
                    cell_size = SCREEN_HEIGHT // 3
                    for i in range(3):
                        if i * cell_size <= y < (i + 1) * cell_size:
                            row = i
                    for j in range(3):
                        if j * cell_size <= x < (j + 1) * cell_size:
                            col = j
                    # Check if the click was inside the board and the cell is empty
                    if row is not None and col is not None and self.board[row][col] == ' ':
                        self.board[row][col] = self.current_player
                        if self.current_player == 'X':
                            self.current_player = 'O'
                        else:
                            self.current_player = 'X'
           
            if self.winner != 'Tie':
                if self.winner == 'X':
                    self.x_score += 1
                else:
                    self.o_score += 1

            self.games_played += 1

            if self.games_played == 5:
                if self.x_score > self.o_score:
                    print("X wins the match!")
                elif self.o_score > self.x_score:
                    print("O wins the match!")
                else:
                    print("It's a tie match!")
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # Reset current player

        self.draw_board()
        pygame.display.flip()

        self.draw_board()
        font = pygame.font.Font(None, 50)
        if self.winner == 'Tie':
            text = font.render("It's a tie!", True, RED)
        else:
            text = font.render(f"{self.winner} wins!", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH /1.15, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        self.display_end_game_menu()

    def display_end_game_menu(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 250 <= x <= 550 and 200 <= y <= 250:  # Play Again
                        self.__init__()  # Reset the game
                        self.play()
                    elif 250 <= x <= 550 and 275 <= y <= 325:  # Main Menu
                        return main()  # Return to the game menu

            # Draw end game menu
            screen.fill(GRAY)
            font = pygame.font.Font(None, 48)
            text = font.render("Game Over", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(text, text_rect)

            pygame.draw.rect(screen, BLACK, (250, 200, 300, 50))
            pygame.draw.rect(screen, BLACK, (250, 275, 300, 50))

            font = pygame.font.Font(None, 36)
            text = font.render("Play Again", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 225))
            screen.blit(text, text_rect)

            text = font.render("Main Menu", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300))
            screen.blit(text, text_rect)

            pygame.display.flip()
class BrickBreaker:
    def __init__(self):
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx = 10 
        self.ball_dy = 10 
        self.paddle_x = SCREEN_WIDTH // 2 - 50
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.game_over = False

        for row in range(5):
            for col in range(8):
                self.bricks.append(pygame.Rect(col * 100 + 10, row * 50 + 10, 80, 40))

    def move_ball(self):
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_x <= 0 or self.ball_x >= SCREEN_WIDTH - 10:
            self.ball_dx = -self.ball_dx

        if self.ball_y <= 0:
            self.ball_dy = -self.ball_dy

        if self.ball_y >= SCREEN_HEIGHT - 10:
            self.lives -= 1
            if self.lives == 0:
                self.game_over = True
            else:
                self.reset_ball()

        ball_rect = pygame.Rect(self.ball_x, self.ball_y, 10, 10)
        for brick in self.bricks:
            if ball_rect.colliderect(brick):
                self.bricks.remove(brick)
                self.score += 10
                if self.ball_dx > 0:
                    self.ball_dx = 1  # Increased sensitivity
                else:
                    self.ball_dx = -1  # Increased sensitivity
                self.ball_dy = -self.ball_dy

        paddle_rect = pygame.Rect(self.paddle_x, SCREEN_HEIGHT - 20, 100, 10)
        if ball_rect.colliderect(paddle_rect):
            self.ball_dy = -self.ball_dy

    def move_paddle(self, direction):
        if direction == 'LEFT' and self.paddle_x >= 0:
            self.paddle_x -= 100
        elif direction == 'RIGHT' and self.paddle_x <= SCREEN_WIDTH - 100:
            self.paddle_x += 100

    def reset_ball(self):
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_dx = 10
        self.ball_dy = 10

    def draw_objects(self):
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (self.paddle_x, SCREEN_HEIGHT - 20, 100, 10))
        pygame.draw.circle(screen, RED, (self.ball_x, self.ball_y), 10)
        for brick in self.bricks:
            pygame.draw.rect(screen, BLUE, brick)

        # Display score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

    def play(self):
        clock = pygame.time.Clock()
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_paddle('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        self.move_paddle('RIGHT')

            self.move_ball()
            self.draw_objects()
            pygame.display.flip()
            clock.tick(30)

        # Display end game menu
        self.display_end_game_menu()

    def display_end_game_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 250 <= x <= 550 and 200 <= y <= 250:  # Play Again
                        self.__init__()  # Reset the game
                        self.play()
                    elif 250 <= x <= 550 and 275 <= y <= 325:  # Main Menu
                        return main()  # Return to the game menu

            # Draw end game menu
            screen.fill(GRAY)
            font = pygame.font.Font(None, 48)
            text = font.render("Game Over", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(text, text_rect)

            pygame.draw.rect(screen, BLACK, (250, 200, 300, 50))
            pygame.draw.rect(screen, BLACK, (250, 275, 300, 50))

            font = pygame.font.Font(None, 36)
            text = font.render("Play Again", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 225))
            screen.blit(text, text_rect)

            text = font.render("Main Menu", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300))
            screen.blit(text, text_rect)

            pygame.display.flip()
class Snake:
    def __init__(self):
        self.snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.food = self.generate_food()
        self.direction = 'RIGHT'
        self.score = 0
        self.lives = 3

    def generate_food(self):
        while True:
            food = (random.randint(0, SCREEN_WIDTH // 20 - 1) * 20, random.randint(0, SCREEN_HEIGHT // 20 - 1) * 20)
            if food not in self.snake:
                return food

    def move_snake(self):
        head = self.snake[0]
        if self.direction == 'UP':
            new_head = (head[0], head[1] - 20)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + 20)
        elif self.direction == 'LEFT':
            new_head = (head[0] - 20, head[1])
        elif self.direction == 'RIGHT':
            new_head = (head[0] + 20, head[1])

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], 20, 20))
        pygame.draw.rect(screen, RED, (self.food[0], self.food[1], 20, 20))

    def play(self):
        clock = pygame.time.Clock()
        while self.lives > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != 'DOWN':
                        self.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.direction != 'UP':
                        self.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                        self.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                        self.direction = 'RIGHT'

            self.move_snake()
            if self.check_collision():
                self.lives -= 1
                self.reset_game()
            screen.fill(BLACK)
            self.draw_snake()
            self.display_stats()
            pygame.display.flip()
            clock.tick(10)

        # Display end game menu
        self.display_end_game_menu()

    def check_collision(self):
        head = self.snake[0]
        if (
            head[0] < 0 or
            head[0] >= SCREEN_WIDTH or
            head[1] < 0 or
            head[1] >= SCREEN_HEIGHT or
            head in self.snake[1:]
        ):
            return True
        return False

    def display_stats(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

    def reset_game(self):
        self.snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.food = self.generate_food()
    def display_end_game_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 250 <= x <= 550 and 200 <= y <= 250:  # Play Again
                        self.__init__()  # Reset the game
                        self.play()
                    elif 250 <= x <= 550 and 275 <= y <= 325:  # Main Menu
                        return main()  # Return to the game menu

            # Draw end game menu
            screen.fill(GRAY)
            font = pygame.font.Font(None, 48)
            text = font.render("Game Over", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(text, text_rect)

            pygame.draw.rect(screen, BLACK, (250, 200, 300, 50))
            pygame.draw.rect(screen, BLACK, (250, 275, 300, 50))

            font = pygame.font.Font(None, 36)
            text = font.render("Play Again", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 225))
            screen.blit(text, text_rect)

            text = font.render("Main Menu", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300))
            screen.blit(text, text_rect)

            pygame.display.flip()


def game_menu():
    input_rect = pygame.Rect(300, 435, 200, 30)
    user_text = ''
    font = pygame.font.Font(None, 24)
    active = False

    while True:
        screen.fill(GRAY)
        font = pygame.font.Font(None, 75)
        text = font.render("Select a game:", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, BLACK, (250, 200, 300, 50))
        pygame.draw.rect(screen, BLACK, (250, 275, 300, 50))
        pygame.draw.rect(screen, BLACK, (250, 350, 300, 50))
       
        font = pygame.font.Font(None, 48)
        text = font.render("Tic Tac Toe", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 225))
        screen.blit(text, text_rect)

        text = font.render("Snake", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(text, text_rect)
        
        text = font.render("BrickBreaker", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 375))
        screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 250 <= x <= 550 and 200 <= y <= 250:
                    return TicTacToe()
                elif 250 <= x <= 550 and 275 <= y <= 325:
                    return Snake()
                elif 250 <= x <= 550 and 350 <= y <= 400: 
                    return BrickBreaker()
              
        pygame.display.flip()

# Main function
def main():
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Zone")
    game = game_menu()
    game.play()