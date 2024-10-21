class Student:
    def __init__(self, name, gender, avatar, attendance):
        self.name = name
        self.gender = gender
        self.avatar = avatar
        self.attendance = attendance
        self.attendance_percentage = self.calculate_attendance()

    def calculate_attendance(self):
        total_days = sum(self.attendance)
        return round((total_days / len(self.attendance)) * 100)

class HonorStudent(Student):
    def __init__(self, name, gender, avatar, attendance):
        super().__init__(name, gender, avatar, attendance)
        self.scholarship = True

class RegularStudent(Student):
    def __init__(self, name, gender, avatar, attendance):
        super().__init__(name, gender, avatar, attendance)
        self.scholarship = False
