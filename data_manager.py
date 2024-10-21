import csv
import pygame
from student import HonorStudent, RegularStudent

class CSVDataManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.male_avatars = ['boy1.png', 'boy2.png', 'boy3.png', 'boy4.png']
        self.female_avatars = ['girl1.png', 'girl2.png', 'girl3.png']
        self.used_male_avatars = []
        self.used_female_avatars = []

    def load_data(self):
        students = []
        with open(self.file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                attendance = list(map(int, row['attendance'].split(',')))

                gender = row['gender']
                avatar = self.choose_avatar(gender)

                if sum(attendance) / len(attendance) > 0.67:
                    student = HonorStudent(row['name'], gender, avatar, attendance)
                else:
                    student = RegularStudent(row['name'], gender, avatar, attendance)

                students.append(student)
        return students

    def save_data(self, students):
        with open(self.file_path, mode='w', newline='') as csvfile:
            fieldnames = ['name', 'gender', 'attendance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for student in students:
                writer.writerow({
                    'name': student.name,
                    'gender': student.gender,
                    'attendance': ','.join(map(str, student.attendance))
                })

    def choose_avatar(self, gender):
        if gender == 'male':
            available_avatars = [avatar for avatar in self.male_avatars if avatar not in self.used_male_avatars]
            if not available_avatars:
                self.used_male_avatars.clear()
                available_avatars = self.male_avatars

            avatar = available_avatars[0]
            self.used_male_avatars.append(avatar)

        else:
            available_avatars = [avatar for avatar in self.female_avatars if avatar not in self.used_female_avatars]
            if not available_avatars:
                self.used_female_avatars.clear()
                available_avatars = self.female_avatars

            avatar = available_avatars[0]
            self.used_female_avatars.append(avatar)

        return pygame.transform.scale(pygame.image.load(avatar), (130, 205))
