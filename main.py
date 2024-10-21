import pygame
from data_manager import CSVDataManager
from splash_screen import SplashScreen
from table_screen import TableScreen
from student import HonorStudent, RegularStudent
import math
from datetime import datetime

pygame.init()

clock_center = (410, 120)
second_hand_length = 35
minute_hand_length = 27
hour_hand_length = 23

clock_image = pygame.image.load('clock.png')
clock_image = pygame.transform.scale(clock_image, (100, 100))

def draw_clock(screen, time_now):
    screen.blit(clock_image, (360, 70)) 

    hours = time_now.hour
    minutes = time_now.minute
    seconds = time_now.second

    second_angle = math.radians(6 * seconds - 90)  # Секундная стрелка (6 градусов на секунду)
    minute_angle = math.radians(6 * minutes + seconds / 10 - 90)  # Минутная стрелка (6 градусов на минуту)
    hour_angle = math.radians(30 * (hours % 12) + minutes / 2 - 90)  # Часовая стрелка (30 градусов на час)

    second_x = clock_center[0] + second_hand_length * math.cos(second_angle)
    second_y = clock_center[1] + second_hand_length * math.sin(second_angle)

    minute_x = clock_center[0] + minute_hand_length * math.cos(minute_angle)
    minute_y = clock_center[1] + minute_hand_length * math.sin(minute_angle)

    hour_x = clock_center[0] + hour_hand_length * math.cos(hour_angle)
    hour_y = clock_center[1] + hour_hand_length * math.sin(hour_angle)

    pygame.draw.line(screen, (255, 0, 0), clock_center, (second_x, second_y), 1)  # Секундная стрелка (красная)
    pygame.draw.line(screen, (0, 0, 0), clock_center, (minute_x, minute_y), 2)    # Минутная стрелка (черная)
    pygame.draw.line(screen, (0, 0, 0), clock_center, (hour_x, hour_y), 4) 

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

class AttendanceApp:
    def __init__(self):
        self.window_size = (800, 700)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Student Attendance Tracker')
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.show_splash_screen = True
        self.data_manager = CSVDataManager('attendance.csv')
        self.students = self.data_manager.load_data()
        self.splash_screen = SplashScreen(self.screen, self.students)
        self.table_screen = TableScreen(self.screen, self.students, self.data_manager, self.add_student)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            if self.show_splash_screen:
                self.handle_splash_screen_events()
                self.splash_screen.display()
                time_now = datetime.now()
                draw_clock(self.screen, time_now)
            else:
                self.handle_table_screen_events()
                self.table_screen.display()

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()

    def handle_splash_screen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.show_splash_screen = False
                elif event.key == pygame.K_RIGHT:
                    self.splash_screen.next_student()
                elif event.key == pygame.K_LEFT:
                    self.splash_screen.previous_student()

    def handle_table_screen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.table_screen.handle_event(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for student in self.students:
                        student.calculate_attendance()
                        if student.attendance_percentage > 67:
                            self.students[self.students.index(student)] = HonorStudent(student.name, student.gender, student.avatar, student.attendance)
                        else:
                            self.students[self.students.index(student)] = RegularStudent(student.name, student.gender, student.avatar, student.attendance)
                    self.show_splash_screen = True
                else:
                    self.table_screen.handle_event(event)



    def add_student(self):
        name = self.get_input("Enter student name: ")
        gender = self.get_input("Enter student gender (male/female): ")

        if gender in ['male', 'female']:
            self.table_screen.add_student(name, gender)
        else:
            print("Invalid gender input. Please enter 'male' or 'female'.")

    def get_input(self, prompt):
        input_text = ""
        font = pygame.font.SysFont('Consolas', 18)
        active = True
        while active:
            self.screen.fill((255, 255, 255))
            draw_text(self.screen, prompt + input_text, font, (0, 0, 0), 150, 300)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
        return input_text

if __name__ == "__main__":
    app = AttendanceApp()
    app.run()
