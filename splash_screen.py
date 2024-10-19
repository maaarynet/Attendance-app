from screen_interface import ScreenInterface
from student import HonorStudent, RegularStudent
import pygame

class SplashScreen(ScreenInterface):
    def __init__(self, screen, students):
        self.screen = screen
        self.students = students
        self.current_student_index = 0
        self.font = pygame.font.SysFont('Consolas', 18)
        self.colors = {'WHITE': (255, 255, 255), 'BLACK': (0, 0, 0)}
        # Загрузка фона
        self.background = pygame.image.load('classroom.png')
        self.background = pygame.transform.scale(self.background, (800, 700))

    def display(self):
        # Рисуем фон
        self.screen.blit(self.background, (0, 0))
        student = self.students[self.current_student_index]
        self.draw_student(student)

    def draw_student(self, student):
        # Отрисовка имени и посещаемости студента
        draw_text(self.screen, f"Name: {student.name}", self.font, self.colors['BLACK'], 550, 270)
        draw_text(self.screen, f"Attendance: {student.attendance_percentage}%", self.font, self.colors['BLACK'], 550, 300)
        
        # Проверяем, является ли студент отличником и выводим стипендию
        if isinstance(student, HonorStudent):
            draw_text(self.screen, f"Scholarship: YES", self.font, self.colors['BLACK'], 550, 330)
        else:
            draw_text(self.screen, f"Scholarship: NO", self.font, self.colors['BLACK'], 550, 330)

        # Отрисовка аватара студента
        student_image = student.avatar
        student_x = (800 - student_image.get_width()) // 2
        student_y = (700 - student_image.get_height()) // 2 - 30
        self.screen.blit(student_image, (student_x, student_y))

    def handle_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.next_student()
        elif event.key == pygame.K_LEFT:
            self.previous_student()

    def next_student(self):
        """ Переключение на следующего студента """
        self.current_student_index = (self.current_student_index + 1) % len(self.students)

    def previous_student(self):
        """ Переключение на предыдущего студента """
        self.current_student_index = (self.current_student_index - 1) % len(self.students)

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
