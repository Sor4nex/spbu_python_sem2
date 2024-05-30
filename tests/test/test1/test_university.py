import pytest

from src.test.test1.university import *


class TestUni:
    uni1 = University()

    student1 = Student("Vasya", 20, 2)
    student2 = Student("Pupkin", 5, 0)

    professor1 = Professor("Oleg Pavlovich", 81)
    professor2 = Professor("Zinaida Dmitrievna", 30)

    course1 = Course("Programming na popkah pchelok")
    course2 = Course("IVE BECOME SO NUMB!!!")

    def test_add_student(self):
        self.uni1.add_student(self.student1)

        assert self.uni1.students == [self.student1]
        assert isinstance(self.uni1.students[0], Student)

        self.uni1.add_student(self.student2)

        assert self.uni1.students == [self.student1, self.student2]
        assert isinstance(self.uni1.students[1], Student)

        assert self.uni1.professors == []
        assert self.uni1.courses == []

    def test_add_professor(self):
        self.uni1.add_professor(self.professor1)

        assert self.uni1.professors == [self.professor1]
        assert isinstance(self.uni1.professors[0], Professor)

        self.uni1.add_professor(self.professor2)
        assert self.uni1.professors == [self.professor1, self.professor2]
        assert isinstance(self.uni1.professors[1], Professor)

        assert self.uni1.students == [self.student1, self.student2]
        assert self.uni1.courses == []

    def test_add_course(self):
        self.uni1.add_course(self.course1)

        assert self.uni1.courses == [self.course1]
        assert isinstance(self.uni1.courses[0], Course)

        self.uni1.add_course(self.course2)
        assert self.uni1.courses == [self.course1, self.course2]
        assert isinstance(self.uni1.courses[1], Course)

        assert self.uni1.professors == [self.professor1, self.professor2]
        assert self.uni1.students == [self.student1, self.student2]

    def test_student_add_course(self):
        student2 = Student("Leha Veter", 19, 12736)
        course2 = Course("БИБИ БУ БА)))")
        student2.add_course(course2, 999)

        assert student2.courses == [course2]
        assert len(course2.students) == 1
        assert isinstance(course2.students[0], StudentOnCourse)
        assert course2.students[0].student == student2
        assert course2.students[0].score == 999

    def test_professor_add_course(self):
        professor2 = Professor("Spirindonov", 23)
        course2 = Course("Prepodovanie matobesam progi na piton")
        professor2.add_course(course2)

        assert professor2.courses == [course2]
        assert course2.professors == [professor2]

    def test_get_student(self):
        assert self.uni1.get_student("Vasya") == self.student1
        assert self.uni1.get_student("Pupkin") == self.student2
        assert self.uni1.get_student("GOD OUR JESUS") is None

    def test_get_professor(self):
        assert self.uni1.get_professor("Oleg Pavlovich") == self.professor1
        assert self.uni1.get_professor("Zinaida Dmitrievna") == self.professor2
        assert self.uni1.get_professor("GOD OUR JESUS") is None

    def test_get_course(self):
        assert self.uni1.get_course("Programming na popkah pchelok") == self.course1
        assert self.uni1.get_course("IVE BECOME SO NUMB!!!") == self.course2
        assert self.uni1.get_course("действительно полезный курс, развивающий навыки, прогождающиеся в работе") is None

    def test_assign_student_course(self):
        self.uni1.assign_student_course("Vasya", "Programming na popkah pchelok", 4.23)

        assert self.student1.courses == [self.course1]
        assert isinstance(self.course1.students[0], StudentOnCourse)
        assert self.course1.students[0].student == self.student1
        assert self.course1.students[0].score == 4.23

        self.uni1.assign_student_course("Vasya", "IVE BECOME SO NUMB!!!", 3.3)

        assert self.student1.courses == [self.course1, self.course2]
        assert isinstance(self.course2.students[0], StudentOnCourse)
        assert self.course2.students[0].student == self.student1
        assert self.course2.students[0].score == 3.3

        self.uni1.assign_student_course("Pupkin", "Programming na popkah pchelok", 1.3)

        assert len(self.course1.students) == 2
        assert self.course1.students[1].student == self.student2
        assert self.course1.students[1].score == 1.3

    def test_assign_student_course_exception(self):
        with pytest.raises(KeyError):
            self.uni1.assign_student_course("GOD BLESS", "Programming na popkah pchelok", 23)

        with pytest.raises(KeyError):
            self.uni1.assign_student_course("Vasya", "teologia", 2)

    def test_assign_professor_course(self):
        self.uni1.assign_professor_course("Oleg Pavlovich", "Programming na popkah pchelok")

        assert self.professor1.courses == [self.course1]
        assert self.course1.professors == [self.professor1]

        self.uni1.assign_professor_course("Oleg Pavlovich", "IVE BECOME SO NUMB!!!")

        assert self.professor1.courses == [self.course1, self.course2]
        assert self.course2.professors == [self.professor1]

    def test_assign_professor_course_exception(self):
        with pytest.raises(KeyError):
            self.uni1.assign_professor_course("JAJA", "Programming na popkah pchelok")

        with pytest.raises(KeyError):
            self.uni1.assign_professor_course("Oleg Pavlovich", "teologia")

    def test_get_student_courses(self):
        assert self.uni1.get_student_courses("Vasya") == [self.course1, self.course2]
        assert self.uni1.get_student_courses("Pupkin") == [self.course1]

    def test_get_professor_courses(self):
        assert self.uni1.get_professor_courses("Oleg Pavlovich") == [self.course1, self.course2]

    def test_get_student_score(self):
        assert self.uni1.get_student_score("Vasya") == 3.765
        assert self.uni1.get_student_score("Pupkin") == 1.3
