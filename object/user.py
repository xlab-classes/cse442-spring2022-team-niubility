from object.fixedTime import FixedTime
from object.task import Task


class User:
    __task = []
    __labels = []
    __schedules = None
    __fixedTimes = []
    __openHour = {"Monday": (0, 0),
                  "Tuesday": (0, 0),
                  "Wednesday": (0, 0),
                  "Thursday": (0, 0),
                  "Friday": (0, 0),
                  "Saturday": (0, 0),
                  "Sunday": (0, 0)}

    def __init__(self, email: str, password: str):
        self.__email = email
        self.__password = password

    def get_email(self):
        return self.__email

    def set_password(self, newPassword):
        self.__password = newPassword

    def get_task(self):
        return self.__task

    def get_schedules(self):
        return self.__schedules

    def get_openHour(self):
        return self.__openHour

    def get_fixedTimes(self):
        return self.__fixedTimes

    def add_task(self, task: Task):
        if task.get_label() not in self.__labels:
            self.__task.append(task)
            self.__labels.append(task.get_label())
            return 0
        else:
            return -1

    def add_fixedTime(self, fixedTime: FixedTime):
        if fixedTime.get_label() not in self.__labels:
            self.__fixedTimes.append(fixedTime)
            self.__labels.append(fixedTime.get_label())
            return 0
        else:
            return -1

    def edit_task(self, old_task: Task, new_task: Task):
        self.remove_task(old_task)
        self.add_task(new_task)

    def edit_fixedTime(self, old_fixedTime: FixedTime, new_fixedTime: FixedTime):
        self.remove_fixed(old_fixedTime)
        self.add_fixedTime(new_fixedTime)

    def remove_task(self, task: Task):
        self.__task.remove(task)
        self.__labels.remove(task.get_label())

    def remove_fixed(self, ft: FixedTime):
        self.__fixedTimes.remove(ft)
        self.__labels.remove(ft.get_label())

    #def deadline_compare(self, obj1: str, obj2: str):
    
    def sort_task(self):
        self.__task.sort()
        return


    def schedule(self):
        return