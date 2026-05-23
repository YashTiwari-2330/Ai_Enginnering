# Advanced student management system

students = {}


def input_marks(message):
    """Take space-separated marks and return them as a list of numbers."""
    while True:
        marks_text = input(message).strip()

        if not marks_text:
            print("Please enter at least one mark.")
            continue

        try:
            marks = list(map(float, marks_text.split()))
            return marks
        except ValueError:
            print("Marks should be numbers only. Example: 78 85.5 90")


# Add student
def add_student():
    sid = input("Enter student key (s1, s2, ...) : ").strip()

    if not sid:
        print("Student key cannot be empty!\n")
        return

    if sid in students:
        print("This student key already exists!\n")
        return

    name = input("Enter student name : ").strip()
    er_no = input("Enter enrollment number : ").strip()
    marks = input_marks("Enter marks (space separated) : ")

    students[sid] = {
        "name": name,
        "er_no": er_no,
        "marks": marks,
    }

    print("Student added!\n")


# View students
def view_students():
    if not students:
        print("No data found!\n")
        return

    print("\n--- Student Records ---")
    for sid, data in students.items():
        avg = calculate_average(data["marks"])
        print(
            f"{sid} | Er No: {data['er_no']} | Name: {data['name']} | "
            f"Marks: {data['marks']} | Average: {avg:.2f}"
        )
    print()


# Calculate average
def calculate_average(marks):
    if not marks:
        return 0
    return sum(marks) / len(marks)


# Show topper
def show_topper():
    if not students:
        print("No students available!\n")
        return

    topper_id = ""
    topper_name = ""
    topper_avg = -1

    for sid, data in students.items():
        avg = calculate_average(data["marks"])

        if avg > topper_avg:
            topper_avg = avg
            topper_id = sid
            topper_name = data["name"]

    print(f"Topper: {topper_name} ({topper_id}) with average: {topper_avg:.2f}\n")


# Search student
def search_student():
    sid = input("Enter student id to search : ").strip()

    if sid in students:
        data = students[sid]
        avg = calculate_average(data["marks"])
        print("\n--- Student Found ---")
        print(f"Id: {sid}")
        print(f"Name: {data['name']}")
        print(f"Enrollment No: {data['er_no']}")
        print(f"Marks: {data['marks']}")
        print(f"Average: {avg:.2f}\n")
    else:
        print("Student not found!\n")


# Add marks
def add_marks():
    sid = input("Enter student id : ").strip()

    if sid in students:
        new_marks = input_marks("Enter new marks : ")
        students[sid]["marks"].extend(new_marks)
        print("Marks updated!\n")
    else:
        print("Student not found!\n")


# Delete student
def delete_student():
    sid = input("Enter student id to delete record : ").strip()

    if sid in students:
        del students[sid]
        print("Student deleted!\n")
    else:
        print("Student not found!\n")


# Menu
def menu():
    while True:
        print("1. Add student")
        print("2. View students")
        print("3. Search student")
        print("4. Add marks")
        print("5. Show topper")
        print("6. Delete student")
        print("7. Exit")

        choice = input("Enter choice : ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            add_marks()
        elif choice == "5":
            show_topper()
        elif choice == "6":
            delete_student()
        elif choice == "7":
            print("Thank you!")
            break
        else:
            print("Please enter a valid choice from 1 to 7.\n")


if __name__ == "__main__":
    menu()
