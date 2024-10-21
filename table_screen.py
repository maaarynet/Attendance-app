from student import Student, HonorStudent, RegularStudent
from screen_interface import ScreenInterface
import pygame

class TableScreen(ScreenInterface):
    def __init__(self, screen, students, data_manager, add_student_callback):
        self.screen = screen
        self.students = students
        self.data_manager = data_manager
        self.add_student_callback = add_student_callback
        self.current_row = 0
        self.current_col = 0
        self.font = pygame.font.SysFont('Consolas', 18)
        self.colors = {'WHITE': (255, 255, 255), 'BLACK': (0, 0, 0), 'BLUE': (0, 0, 255)}
        self.button_rect = pygame.Rect(650, 600, 100, 50)

    def display(self):
        self.screen.fill(self.colors['WHITE'])
        header = ['Name', 'Date 1', 'Date 2', 'Date 3']

        for col, text in enumerate(header):
            text_surface = self.font.render(text, True, self.colors['BLACK'])
            self.screen.blit(text_surface, (150 + col * 150, 50))

        for row, student in enumerate(self.students):
            name_surface = self.font.render(student.name, True, self.colors['BLACK'])
            self.screen.blit(name_surface, (150, 100 + row * 50))
            for col in range(3):
                color = self.colors['BLUE'] if (row, col) == (self.current_row, self.current_col) else self.colors['BLACK']
                date_surface = self.font.render(str(student.attendance[col]), True, color)
                self.screen.blit(date_surface, (150 + (col + 1) * 150, 100 + row * 50))

        self.plus_icon = pygame.image.load('plus.png')
        self.plus_icon = pygame.transform.scale(self.plus_icon, (50, 50))

        self.screen.blit(self.plus_icon, self.plus_icon.get_rect(center=self.button_rect.center))


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.add_student_callback()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.current_row = (self.current_row + 1) % len(self.students)
            elif event.key == pygame.K_UP:
                self.current_row = (self.current_row - 1) % len(self.students)
            elif event.key == pygame.K_RIGHT:
                self.current_col = min(self.current_col + 1, 2)
            elif event.key == pygame.K_LEFT:
                self.current_col = max(self.current_col - 1, 0)
            elif event.key == pygame.K_SPACE:
                self.toggle_attendance()

    def toggle_attendance(self):
        student = self.students[self.current_row]
        current_value = student.attendance[self.current_col]
        student.attendance[self.current_col] = 0 if current_value == 1 else 1
        self.data_manager.save_data(self.students)

        student.calculate_attendance()
        if student.attendance_percentage > 67:
            self.students[self.current_row] = HonorStudent(student.name, student.gender, student.avatar, student.attendance)
        else:
            self.students[self.current_row] = RegularStudent(student.name, student.gender, student.avatar, student.attendance)

    def add_student(self, name, gender):
        avatar = self.data_manager.choose_avatar(gender)
        new_student = Student(name, gender, avatar, [0, 0, 0])
        self.students.append(new_student)
        self.data_manager.save_data(self.students)
        print(f"Студент {name} був успішно додатий.")

