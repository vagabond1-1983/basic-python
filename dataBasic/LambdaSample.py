persons = [
    {"name": "devin", "age": 40},
    {"name": "leo", "age": 20}
]

persons.sort(key=lambda item: item['age'])
print(persons)
