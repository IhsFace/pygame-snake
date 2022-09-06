import pygame
import sys
import random


class Snake():
    def __init__(self):
        self.body = [pygame.math.Vector2(5, 10), pygame.math.Vector2(6, 10)]
        self.direction = pygame.math.Vector2(1, 0)
        self.new_block = False
        self.game_active = False
        self.score = 2

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(
                int(block.x * cell_size), int(block.y * cell_size), cell_size - 5, cell_size - 5)
            pygame.draw.rect(screen, (255, 255, 255), block_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def reset_snake(self):
        self.body = [pygame.math.Vector2(5, 10), pygame.math.Vector2(6, 10)]
        self.direction = pygame.math.Vector2(1, 0)
        self.new_block = False
        self.game_active = False
        self.draw_snake()


class Fruit():
    def __init__(self):
        self.randomise()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size - 5, cell_size - 5)
        pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

    def randomise(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x, self.y)


class Main():
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.eat_sound = pygame.mixer.Sound('assets/eat.wav')

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.eat_sound.play()
            self.snake.score += 1
            self.fruit.randomise()
            self.snake.new_block = True

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomise()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def display_score(self):
        score = font.render(
            f'Score: {str(self.snake.score)}', True, (255, 255, 255))
        score_rect = score.get_rect(
            center=((cell_size * cell_number) // 2, 250))
        screen.blit(score, score_rect)

    def game_over(self):
        self.snake.game_active = True


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode(
    (cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 150)
main_game = Main()
font = pygame.font.SysFont('PressStart2P-Regular.ttf', 50)
font_scaled = pygame.font.SysFont('PressStart2P-Regular.ttf', 25)
end = font.render('Game Over!', True, (255, 255, 255))
end_rect = end.get_rect(center=((cell_size * cell_number) // 2, 200))
message = font_scaled.render(
    'Press SPACE to play again', True, (255, 255, 255))
message_rect = message.get_rect(center=((cell_size * cell_number) // 2, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.USEREVENT:
            main_game.update()
        if main_game.snake.game_active == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and main_game.snake.direction != pygame.math.Vector2(0, 1) or event.key == pygame.K_w and main_game.snake.direction != pygame.math.Vector2(0, 1):
                    main_game.snake.direction = pygame.math.Vector2(0, -1)
                if event.key == pygame.K_LEFT and main_game.snake.direction != pygame.math.Vector2(1, 0) or event.key == pygame.K_a and main_game.snake.direction != pygame.math.Vector2(1, 0):
                    main_game.snake.direction = pygame.math.Vector2(-1, 0)
                if event.key == pygame.K_DOWN and main_game.snake.direction != pygame.math.Vector2(0, -1) or event.key == pygame.K_s and main_game.snake.direction != pygame.math.Vector2(0, -1):
                    main_game.snake.direction = pygame.math.Vector2(0, 1)
                if event.key == pygame.K_RIGHT and main_game.snake.direction != pygame.math.Vector2(-1, 0) or event.key == pygame.K_d and main_game.snake.direction != pygame.math.Vector2(-1, 0):
                    main_game.snake.direction = pygame.math.Vector2(1, 0)
            screen.fill((0, 0, 0))
            main_game.draw_elements()
        elif main_game.snake.game_active == True:
            screen.fill((0, 0, 0))
            screen.blit(end, end_rect)
            main_game.display_score()
            screen.blit(message, message_rect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_game.snake.reset_snake()
                    main_game.snake.game_active = False
    pygame.display.update()
    clock.tick(60)
