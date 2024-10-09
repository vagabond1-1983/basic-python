class Person:
    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def name(self):
        print("in the getter")
        return self.__name

    @name.setter
    def name(self, value):
        print("in the setter")
        self.__name = value


person = Person("leo")
person.name = "devin"
print(person.name)
