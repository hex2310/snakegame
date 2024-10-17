import sys
import random as rd
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPainter, QColor, QFont, QKeyEvent, QPaintEvent
from PyQt6.QtCore import QBasicTimer, QTimerEvent, Qt, QRect, QSize, QPoint

class SnakeGame(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self) -> None:        
        self.timer = QBasicTimer()
        
        # Starting position sanke body (head and 2 parts)
        #               x    y
        self.snake = [(100, 100), (90, 100), (80, 100)]
        
        # Initial direction of the snake
        self.snake_direction = 'right'
        
        # Place food on the gird
        self.food = self.place_food()
        
        self.score = 0
        
        self.setStyleSheet('background-color: #000000;')
        self.setWindowTitle('Snake Game')
        self.setGeometry(300, 300, 400, 400)
        
        # Game speed (lower faster)
        self.timer.start(100, self)
        
        self.show()
        
    def place_food(self) -> tuple[int, int]:
        x = rd.randint(0, 39) * 10
        y = rd.randint(0, 39) * 10
        return (x, y)
    
    def paintEvent(self, event: QPaintEvent | None) -> None:
        qp = QPainter()
        qp.begin(self)
        self.draw_game(qp)
        qp.end()
        return super().paintEvent(event)
    
    def draw_game(self, qp: QPainter):
        # Draw snake
        qp.setBrush(QColor(0, 255, 0)) # Green snake
        for pos in self.snake:
            qp.drawRect(pos[0], pos[1], 10, 10)
        
        # Draw food
        qp.setBrush(QColor(255, 0, 0)) # Red food
        qp.drawRect(self.food[0], self.food[1], 10, 10)
        
        # Display score
        qp.setPen(QColor(255, 255, 255))
        qp.setFont(QFont('Times New Roman', 10))
        qp.drawText(10, 10, f'Score: {self.score}')
        
    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        key = event.key()
        
        if key == Qt.Key.Key_W and self.snake_direction != 'down': # move up
            self.snake_direction = 'up'
        elif key == Qt.Key.Key_S and self.snake_direction != 'up': # move down
            self.snake_direction = 'down'
        elif key == Qt.Key.Key_A and self.snake_direction != 'right': # move left
            self.snake_direction = 'left'
        elif key == Qt.Key.Key_D and self.snake_direction != 'left': # move right
            self.snake_direction = 'right'
        elif key == Qt.Key.Key_Space:
            self.play_again()
        else: pass
            
        return super().keyPressEvent(event)
    
    def timerEvent(self, event: QTimerEvent | None) -> None:
        if event.timerId() == self.timer.timerId():
            self.move_snake()
            self.check_collisions()
            self.update()
        return super().timerEvent(event)
    
    def move_snake(self):
        head = self.snake[0]
        
        if self.snake_direction == 'up':
            new_head = (head[0], head[1] - 10)
        elif self.snake_direction == 'down':
            new_head = (head[0], head[1] + 10)
        elif self.snake_direction == 'right':
            new_head = (head[0] + 10, head[1])
        elif self.snake_direction == 'left':
            new_head = (head[0] - 10, head[1])
            
        # Update length of snake
        self.snake = [new_head] + self.snake[:-1]
        
        # Check is snake eats the food
        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1]) # Grow the snake
            self.score += 10
            self.food = self.place_food()
            
    def check_collisions(self):
        head = self.snake[0]
        
        # Check is snake hits the wall
        if (head[0] < 0 or
            head[0] >= self.width() or
            head[1] < 0 or
            head[1] >= self.height()):
                self.game_over()
            
        # Check if snake collides with itseft
        if head in self.snake[1:]:
            self.game_over()
            
    def game_over(self):
        self.result = QLabel(self)
        self.result.setFont(QFont('Times New Roman', 20))
        self.result.setStyleSheet('color: #ffffff;')
        self.result.setText(f'Your score: {self.score}\nPress space to play again')
        self.result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result.setGeometry(QRect(QPoint(50, 100), QSize(300, 60)))
        self.result.show()
        self.timer.stop()
        
    def play_again(self):
        try: 
            self.result.close()
        except: pass
        self.init_ui()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SnakeGame()
    sys.exit(app.exec())

