num_apps = int(input())
num_accepts = int(input())
students = []


def accepted_students(students):
    counter = 0
    while counter < num_accepts:
        print(students[counter][0])
        counter += 1


for n in range(num_apps):
    student = input()
    student = list(student.split())
    first_name = student[0]
    last_name = student[1]
    gpa = float(student[2])
    stu_name = first_name + ' ' + last_name
    student = [stu_name, gpa]
    students.append(student)
    sorted_students = sorted(students)

students = sorted(students, key=lambda students: (-students[1], students[0]))

print('Successful applicants:')
accepted_students(students)