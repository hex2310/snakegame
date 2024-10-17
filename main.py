import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QColor, QFont, QKeyEvent
from PyQt6.QtCore import QBasicTimer, Qt, QRect

class SnakeGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.timer = QBasicTimer()
        self.snake = [(100, 100), (90, 100), (80, 100)]  # Starting snake body (head and 2 parts)
        self.snake_dir = 'RIGHT'  # Initial direction of the snake
        self.food = self.place_food()  # Place food on the grid
        self.score = 0
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle('Snake Game')
        self.setGeometry(300, 300, 400, 400)
        self.timer.start(100, self)  # Game speed (lower means faster)
        self.show()

    def place_food(self):
        x = random.randint(0, 39) * 10
        y = random.randint(0, 39) * 10
        return (x, y)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_game(qp)
        qp.end()

    def draw_game(self, qp):
        # Draw Snake
        qp.setBrush(QColor(0, 255, 0))  # Green snake
        for pos in self.snake:
            qp.drawRect(pos[0], pos[1], 10, 10)

        # Draw Food
        qp.setBrush(QColor(255, 0, 0))  # Red food
        qp.drawRect(self.food[0], self.food[1], 10, 10)

        # Display Score
        qp.setPen(QColor(255, 255, 255))
        qp.setFont(QFont('Arial', 10))
        qp.drawText(10, 10, f'Score: {self.score}')

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key.Key_W and self.snake_dir != 'DOWN':  # Move up
            self.snake_dir = 'UP'
        elif key == Qt.Key.Key_S and self.snake_dir != 'UP':  # Move down
            self.snake_dir = 'DOWN'
        elif key == Qt.Key.Key_A and self.snake_dir != 'RIGHT':  # Move left
            self.snake_dir = 'LEFT'
        elif key == Qt.Key.Key_D and self.snake_dir != 'LEFT':  # Move right
            self.snake_dir = 'RIGHT'

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.move_snake()
            self.check_collisions()
            self.update()

    def move_snake(self):
        head = self.snake[0]
        if self.snake_dir == 'UP':
            new_head = (head[0], head[1] - 10)
        elif self.snake_dir == 'DOWN':
            new_head = (head[0], head[1] + 10)
        elif self.snake_dir == 'LEFT':
            new_head = (head[0] - 10, head[1])
        elif self.snake_dir == 'RIGHT':
            new_head = (head[0] + 10, head[1])

        self.snake = [new_head] + self.snake[:-1]

        # Check if snake eats the food
        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1])  # Grow the snake
            self.score += 10
            self.food = self.place_food()

    def check_collisions(self):
        head = self.snake[0]

        # Check if snake hits the wall
        if head[0] < 0 or head[0] >= self.width() or head[1] < 0 or head[1] >= self.height():
            self.game_over()

        # Check if snake collides with itself
        if head in self.snake[1:]:
            self.game_over()

    def game_over(self):
        self.timer.stop()
        self.setWindowTitle(f'Game Over! Your score: {self.score}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SnakeGame()
    sys.exit(app.exec())
