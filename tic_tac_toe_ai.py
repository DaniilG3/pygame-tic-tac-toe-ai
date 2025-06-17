import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
import random

class TicTacToeGame:
    def __init__(self, width=300, grid_size=3, status_height=50, button_height=50):
        # Initialize pygame modules
        pygame.display.init()
        pygame.font.init()

        # Dimensions
        self.WIDTH = width
        self.GRID_SIZE = grid_size
        self.CELL = self.WIDTH // self.GRID_SIZE
        self.STATUS_HEIGHT = status_height
        self.BUTTON_HEIGHT = button_height
        self.HEIGHT = self.CELL * self.GRID_SIZE + self.STATUS_HEIGHT + self.BUTTON_HEIGHT
        self.GRID_BOTTOM = self.CELL * self.GRID_SIZE

        # Colors & styling
        self.LINE_COLOR = (0, 0, 0)
        self.BG_COLOR = (255, 255, 255)
        self.CIRCLE_COLOR = (239, 231, 200)
        self.CROSS_COLOR = (66, 66, 66)
        self.STATUS_BG = (200, 200, 200)
        self.BUTTON_BG = (180, 180, 180)
        self.BUTTON_HOVER = (160, 160, 160)
        self.LINE_WIDTH = 5
        self.SPACE = self.CELL // 4
        self.FONT = pygame.font.SysFont(None, 32)
        self.BUTTON_FONT = pygame.font.SysFont(None, 28)

        # Play Again/Quit buttons
        self.PLAY_RECT = pygame.Rect(
            30,
            self.GRID_BOTTOM + self.STATUS_HEIGHT + (self.BUTTON_HEIGHT - 30) // 2,
            100, 30
        )
        self.QUIT_RECT = pygame.Rect(
            self.WIDTH - 130,
            self.GRID_BOTTOM + self.STATUS_HEIGHT + (self.BUTTON_HEIGHT - 30) // 2,
            100, 30
        )

        # Screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Tic-Tac-Toe with AI')

        # Game state
        self.board = self.reset_board()
        self.current = random.choice([1, 2])
        self.game_over = False

        # Draw initial state
        self.draw_lines()
        if self.current == 2:
            self.draw_status('O goes first!')
            self.ai_move()
            self.draw_figures()
            self.current = 1
            self.draw_status('Your turn!')
        else:
            self.draw_status('X goes first!')

    def reset_board(self):
        return [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]

    def draw_lines(self):
        self.screen.fill(self.BG_COLOR)
        for i in range(1, self.GRID_SIZE):
            y = i * self.CELL
            pygame.draw.line(self.screen, self.LINE_COLOR, (0, y), (self.WIDTH, y), self.LINE_WIDTH)
            x = i * self.CELL
            pygame.draw.line(self.screen, self.LINE_COLOR, (x, 0), (x, self.GRID_BOTTOM), self.LINE_WIDTH)

    def draw_figures(self):
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if self.board[r][c] == 1:
                    sx = c * self.CELL + self.SPACE
                    sy = r * self.CELL + self.SPACE
                    ex = (c + 1) * self.CELL - self.SPACE
                    ey = (r + 1) * self.CELL - self.SPACE
                    pygame.draw.line(self.screen, self.CROSS_COLOR, (sx, sy), (ex, ey), self.LINE_WIDTH)
                    pygame.draw.line(self.screen, self.CROSS_COLOR, (sx, ey), (ex, sy), self.LINE_WIDTH)
                elif self.board[r][c] == 2:
                    center = (c * self.CELL + self.CELL // 2, r * self.CELL + self.CELL // 2)
                    pygame.draw.circle(self.screen, self.CIRCLE_COLOR, center, self.CELL // 3, self.LINE_WIDTH)

    def draw_status(self, msg):
        pygame.draw.rect(self.screen, self.STATUS_BG, (0, self.GRID_BOTTOM, self.WIDTH, self.STATUS_HEIGHT))
        text = self.FONT.render(msg, True, self.LINE_COLOR)
        rect = text.get_rect(center=(self.WIDTH // 2, self.GRID_BOTTOM + self.STATUS_HEIGHT // 2))
        self.screen.blit(text, rect)

    def draw_buttons(self):
        mx, my = pygame.mouse.get_pos()
        # Play Again
        color = self.BUTTON_HOVER if self.PLAY_RECT.collidepoint(mx, my) else self.BUTTON_BG
        pygame.draw.rect(self.screen, color, self.PLAY_RECT)
        t = self.BUTTON_FONT.render('Play Again', True, self.LINE_COLOR)
        self.screen.blit(t, t.get_rect(center=self.PLAY_RECT.center))
        # Quit
        color = self.BUTTON_HOVER if self.QUIT_RECT.collidepoint(mx, my) else self.BUTTON_BG
        pygame.draw.rect(self.screen, color, self.QUIT_RECT)
        q = self.BUTTON_FONT.render('Quit', True, self.LINE_COLOR)
        self.screen.blit(q, q.get_rect(center=self.QUIT_RECT.center))

    def available(self, r, c):
        return self.board[r][c] == 0

    def full(self):
        return all(cell != 0 for row in self.board for cell in row)

    def win_line(self, p):
        for i in range(self.GRID_SIZE):
            if all(self.board[i][j] == p for j in range(self.GRID_SIZE)):
                y = i * self.CELL + self.CELL // 2
                return ((0, y), (self.WIDTH, y))
            if all(self.board[j][i] == p for j in range(self.GRID_SIZE)):
                x = i * self.CELL + self.CELL // 2
                return ((x, 0), (x, self.GRID_BOTTOM))
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == p:
            return ((0, 0), (self.WIDTH, self.GRID_BOTTOM))
        if self.board[2][0] == self.board[1][1] == self.board[0][2] == p:
            return ((0, self.GRID_BOTTOM), (self.WIDTH, 0))
        return None

    def minimax(self, depth, maxi):
        if self.win_line(2): return 1
        if self.win_line(1): return -1
        if self.full(): return 0
        best = -float('inf') if maxi else float('inf')
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if self.board[r][c] == 0:
                    self.board[r][c] = 2 if maxi else 1
                    score = self.minimax(depth + 1, not maxi)
                    self.board[r][c] = 0
                    if maxi:
                        best = max(best, score)
                    else:
                        best = min(best, score)
        return best

    def ai_move(self):
        best_score = -float('inf')
        moves = []
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if self.board[r][c] == 0:
                    self.board[r][c] = 2
                    score = self.minimax(0, False)
                    self.board[r][c] = 0
                    if score > best_score:
                        best_score = score
                        moves = [(r, c)]
                    elif score == best_score:
                        moves.append((r, c))
        if moves:
            move = random.choice(moves)
            self.board[move[0]][move[1]] = 2

    def restart(self):
        self.board = self.reset_board()
        self.game_over = False
        self.current = random.choice([1, 2])
        self.draw_lines()
        if self.current == 2:
            self.draw_status('O goes first!')
            self.ai_move()
            self.draw_figures()
            self.current = 1
            self.draw_status('Your turn!')
        else:
            self.draw_status('X goes first!')

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = ev.pos
                    if not self.game_over and my < self.GRID_BOTTOM:
                        r, c = my // self.CELL, mx // self.CELL
                        if self.available(r, c):
                            self.board[r][c] = self.current
                            self.draw_figures()
                            line = self.win_line(self.current)
                            if line:
                                pygame.draw.line(self.screen, (255, 0, 0), line[0], line[1], self.LINE_WIDTH)
                                self.game_over = True; self.draw_status(f"{'X' if self.current == 1 else 'O'} wins!")
                            elif self.full():
                                self.game_over = True; self.draw_status("It's a tie!")
                            else:
                                self.current = 2
                                self.ai_move(); self.draw_figures()
                                line = self.win_line(2)
                                if line:
                                    pygame.draw.line(self.screen, (255, 0, 0), line[0], line[1], self.LINE_WIDTH)
                                    self.game_over = True; self.draw_status('O (AI) wins!')
                                elif self.full():
                                    self.game_over = True; self.draw_status("It's a tie!")
                                else:
                                    self.current = 1; self.draw_status('Your turn!')
                    elif self.game_over and my >= self.GRID_BOTTOM + self.STATUS_HEIGHT:
                        if self.PLAY_RECT.collidepoint(mx, my):
                            self.restart()
                        elif self.QUIT_RECT.collidepoint(mx, my):
                            pygame.quit(); sys.exit()
            if self.game_over:
                self.draw_buttons()
            pygame.display.update()
            clock.tick(30)

if __name__ == '__main__':
    TicTacToeGame().run()

