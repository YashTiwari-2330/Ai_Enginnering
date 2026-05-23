# Hear the example of the class and object in python with projects 
# We implement a topics with why ,how and when the use oops topcis in real life exmaples

import json
import os
from abc import ABC , abstractmethod

# Task classs with private access modifier(Encapsulation) with decorators

class Task:
    def __init__(self , title , discription , completed = False):
        self.title = title
        self._discription = discription
        self.completed = completed

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self , value):
        if not value.strip():
            raise ValueError("Title cannot be empty..")
        self._title = value.strip()

    @property
    def discription(self):
        return self._discription
    
    @discription.setter
    def discription(self , value):
        self._discription = value.strip()
        
    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "✔" if self.completed else "❌"
        return f"{self.title} - {self._discription} [{status}]"

    def to_dict(self):
        return {
            "title" : self._title,
            "discription" : self._discription,
            "completed" : self.completed
        }
    
    @staticmethod
    def from_dict(data):
        return Task(title=data['title'] , 
                    discription=data['discription'] ,
                     completed=data['completed'])


class TodoBase(ABC):

    @abstractmethod
    def add_task(self , title):
        pass

    @abstractmethod
    def save_tasks(self):
        pass

    @abstractmethod
    def mark_task_completed(self , index):
        pass

    @abstractmethod
    def delete_task(self , index):
        pass

    @abstractmethod
    def show_tasks(self):
        pass
    

class SmartTodo(TodoBase):
    def __init__(self , filename = "todo.json"):
        self._filename = filename
        self._tasks = []
        self.load_tasks()

    # Load tasks from the json file
    def load_tasks(self):
        try:
            if os.path.exists(self._filename):
                with open(self._filename , "r") as file:
                    data = json.load(file)
                    self._tasks = [Task.from_dict(t) for t in data]
            else:
                self._tasks = []

        except json.JSONDecodeError:
            print("File corrupted. Resetting data.")
            self._tasks = []

        except Exception as e:
            print(f"Unexpected error: {e}")

    # Save tasks

    def save_tasks(self):
        try:
                with open(self._filename , "w") as file:
                    json.dump([t.to_dict() for t in self._tasks], file , indent=4)
                print("Task saved")

        except Exception as e:
            print(f"Error solvig tasks: {e}")


    # Core Fetures

    def add_task(self , title , discription = ""):
        task = Task(title , discription)
        self._tasks.append(task)
        print("Task added successfully..")

    def delete_task(self , index):
        if 0 <= index < len(self._tasks):
            del self._tasks[index]
            print("Task Deleted successfully..")

        else:
            print("Invalid task")

    def show_tasks(self):
        if not self._tasks:
            print("No tasks found..")
            return
        
        for i , task in enumerate(self._tasks):
            print(f"{i + 1} . {task}")
            print(f"Discription : {task._discription}")
            print(f"show task completed : {task.__str__()}")

    def mark_task_completed(self , index):
        try:
            if 0 <= index < len(self._tasks):
                self._tasks[index].mark_completed()
                print("Task marked as completed..")

            else:
                raise IndexError("Invalid task index")
            
        except Exception as e:
            print(f"Error marking task completed: {e}")

    
    def update_task(self , index , new_title , new_discription = ""):
        try:
            if 0 <= index < len(self._tasks):
                self._tasks[index].title = new_title
                self._tasks[index].discription = new_discription
                print("Task updated successfully..")

            else:
                raise IndexError("Invalid task index")
        
        except Exception as e:
            print(f"Error updating task: {e}")



    def menu(self):
        while True:
            print("\n1. Add Task")
            print("2. Save Tasks")
            print("3. Show Tasks")
            print("4. Mark Task as completed")
            print("5. Update Task")
            print("6. Delete Task")
            print("7. Exit")

            choice = input("Enter number of choice :- ") 

            try:
                choice = int(choice)

                if choice == 1:
                    title = input("Enter task to add :- ")
                    discription = input("Enter discription for the task :- ")
                    self.add_task(title , discription)

                    

                elif choice == 2:
                    self.save_tasks()

                elif choice == 3:
                    self.show_tasks()

                elif choice == 4:
                    index = int(input("Enter task number to mark as completed :-"))
                    self.mark_task_completed(index - 1)

                elif choice == 5:
                    index = int(input("Enter task number to update :-")) 
                    new_title = input("Enter new title for the task :-")
                    new_discription = input("Enter new discription for the task :-")
                    self.update_task(index - 1 , new_title , new_discription) 

                elif choice == 6:
                    index = int(input("Enter task number to delete :-")) 
                    self.delete_task(index -1) 

                elif choice == 7:
                    print("Exiting the program..")
                    break

            
            except ValueError:
                print("Please enter a valid number")  


if __name__ == "__main__":
    todo = SmartTodo()
    todo.menu()
