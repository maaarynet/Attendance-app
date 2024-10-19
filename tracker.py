class AttendanceTracker:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.students = self.data_manager.load_data()

    def add_student(self, name, gender, avatar):
        new_student = Student(name, gender, avatar)
        self.students.append(new_student)

    def save_data(self):
        self.data_manager.save_data(self.students)

    def calculate_attendance(self):
        for student in self.students:
            student.calculate_attendance()