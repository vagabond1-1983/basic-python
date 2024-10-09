class Person:
    def __init__(self, name) -> None:
        self.name = name

    def say_hello(self):
        print(f"Hi {self.name}")


class Student(Person):
    def __init__(self, name, school) -> None:
        super().__init__(name)
        self.school = school

    def say_hello(self):
        super().say_hello()
        print(f"{self.name} is in school: {self.school}")


zhangsan = Student("zhangsan", "US")
zhangsan.say_hello()
