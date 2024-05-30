import abc
from dataclasses import dataclass
from typing import Optional


class UniversityPerson(metaclass=abc.ABCMeta):
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
        self.courses: list[Course] = []


class Student(UniversityPerson):
    def __init__(self, name: str, age: int, track_num: int) -> None:
        super().__init__(name, age)
        self.track_num = track_num

    def add_course(self, course: "Course", score: float) -> None:
        self.courses.append(course)
        course.students.append(StudentOnCourse(self, score))


class Professor(UniversityPerson):
    def add_course(self, course: "Course") -> None:
        self.courses.append(course)
        course.professors.append(self)


@dataclass
class StudentOnCourse:
    student: Student
    score: float


class Course:
    def __init__(self, name: str) -> None:
        self.name = name
        self.students: list[StudentOnCourse] = []
        self.professors: list[Professor] = []


class University:
    def __init__(self) -> None:
        self.students: list[Student] = []
        self.professors: list[Professor] = []
        self.courses: list[Course] = []

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    def add_professor(self, professor: Professor) -> None:
        self.professors.append(professor)

    def add_course(self, course: "Course") -> None:
        if course in self.courses:
            raise KeyError(f"course {course.name} already exists in university courses")
        self.courses.append(course)

    def assign_student_course(self, student_name: str, course_name: str, student_score: float) -> None:
        course = self.get_course(course_name)
        if course is None:
            raise KeyError(f"no course, named {course_name}")
        student = self.get_student(student_name)
        if student is None:
            raise KeyError(f"no student, named {student_name}")
        student.add_course(course, student_score)

    def assign_professor_course(self, professor_name: str, course_name: str) -> None:
        course = self.get_course(course_name)
        if course is None:
            raise KeyError(f"no course, named {course_name}")
        professor = self.get_professor(professor_name)
        if professor is None:
            raise KeyError(f"no professor, named {professor_name}")
        professor.add_course(course)

    def get_student(self, name: str) -> Optional[Student]:
        for student in self.students:
            if student.name == name:
                return student
        return None

    def get_professor(self, name: str) -> Optional[Professor]:
        for professor in self.professors:
            if professor.name == name:
                return professor
        return None

    def get_course(self, name: str) -> Optional[Course]:
        for course in self.courses:
            if course.name == name:
                return course
        return None

    def get_student_score(self, name: str) -> float:
        student = self.get_student(name)
        if student is None:
            raise KeyError(f"no student, named {name}")
        score_summary = 0.0
        for course in student.courses:
            for course_student in course.students:
                if course_student.student == student:
                    score_summary += course_student.score
                    break
        return score_summary / len(student.courses)

    def get_student_courses(self, name: str) -> list[Course]:
        student = self.get_student(name)
        if student is None:
            raise KeyError(f"no student, named {name}")
        return student.courses

    def get_professor_courses(self, name: str) -> list[Course]:
        professor = self.get_professor(name)
        if professor is None:
            raise KeyError(f"no professor, named {name}")
        return professor.courses
