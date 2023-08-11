import time
import os
import threading
import msvcrt 
import random

game_over = False
speed = 0.25

class Field:
    def __init__(self):
        self.size_y = 22
        self.size_x = 22
        self.curr_field =  [['+','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','+',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
                       ['+','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','+',],]
    def draw(self):
        field_drawing_string = ''
        for y in range(self.size_y):
            for x in range(self.size_x):
                field_drawing_string += self.curr_field[y][x]          
            field_drawing_string += '\n'

        os.system('cls')
        print(field_drawing_string)

    def set_field_by_coords(self,y,x, symbol):
        self.curr_field[y][x] = symbol
    def get_field_by_coords(self,y,x):
        return self.curr_field[y][x]

class Apple:
    def __init__(self, field):
        apple_was_placed = False
        while not apple_was_placed:
            x = random.randint(1,field.size_x-2)
            y = random.randint(1,field.size_y-2)
            if field.get_field_by_coords(y,x) not in ['O','#']:
                self.coords = [y,x]
                field.set_field_by_coords(y,x,'*')
                apple_was_placed = True

    def spawn_new_apple(self):
        apple_was_placed = False
        while not apple_was_placed:
            x = random.randint(1,field.size_x-2)
            y = random.randint(1,field.size_y-2)
            if field.get_field_by_coords(y,x) not in ['O','#']:
                self.coords = [y,x]
                field.set_field_by_coords(y,x,'*')
                apple_was_placed = True


class Snake:
    def __init__(self,field,apple):
        self.length = 3
        self.tail_coords = [[10,2],[10,3],[10,4]]
        self.my_field = field
        self.my_apple = apple
        self.curr_direction = 'd'

    def update(self):
        global game_over
        global speed
        grow = False
        last_y,last_x = self.tail_coords[-1]
        if self.curr_direction == 'w':
            self.tail_coords.append([last_y-1,last_x])
        elif self.curr_direction == 'a':
            self.tail_coords.append([last_y,last_x-1])
        elif self.curr_direction == 's':
            self.tail_coords.append([last_y+1,last_x])
        elif self.curr_direction == 'd':
            self.tail_coords.append([last_y,last_x+1])

        y,x = self.tail_coords[-1]
        if self.my_field.get_field_by_coords(y,x) == '*':
            grow = True
            self.my_apple.spawn_new_apple()
            if len(self.tail_coords) % 5 == 0 and speed > 0:
                speed -= 0.05

        if self.my_field.get_field_by_coords(y,x) in ['#','|','-']:
            game_over = True

        for point in self.tail_coords[1:-1]:
            y,x = point
            self.my_field.set_field_by_coords(y,x,'#')

        if not grow:
            y,x = self.tail_coords[0]
            self.my_field.set_field_by_coords(y,x,' ')
            self.tail_coords.remove([y,x])

        y,x = self.tail_coords[-1]
        self.my_field.set_field_by_coords(y,x,'O')

def player_threading(snake):
    while not game_over:
        player_input = msvcrt.getch()
        if player_input[0] == 119 and snake.curr_direction != 's':
            snake.curr_direction = 'w'
        elif player_input[0] == 97 and snake.curr_direction != 'd':
            snake.curr_direction = 'a'
        elif player_input[0] == 115 and snake.curr_direction != 'w':
            snake.curr_direction = 's'
        elif player_input[0] == 100 and snake.curr_direction != 'a':
            snake.curr_direction = 'd'
        time.sleep(speed)


field = Field()
apple = Apple(field)
snake = Snake(field, apple)
player_thread = threading.Thread(target=player_threading, args=(snake,))
player_thread.start()
while not game_over:
    field.draw()
    time.sleep(speed)
    snake.update()



