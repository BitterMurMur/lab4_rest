from dataclasses import dataclass
from app.company1.StorageModule import *
from abc import ABC, abstractmethod
from flask import render_template, request
import datetime

from app.company1.StrategyModule import *


#фирма
@dataclass
class Company:
    
    def __init__(self):
        self.name = "ООО \"Тестовая\""
        self.storage = DBStorage(self)
        self.io:IStrategy = SQLIOStrategy(self.storage)
        self.director: ConcreteEmployee = ConcreteEmployee()
        self.leadEngineers: list[ConcreteEmployee] = []
        self.engineers: list[LeafEmployee]= []

    def add(self):
        self.setData(request.form)
        return self.io.output()

    def delete(self, id):
        self.storage.delete(id)
        return self.io.output()

    def show(self):
        return self.io.output()

    def setData(self, form):
        id = form.get('Id')
        fullName = form.get('fullName')
        position = form.get('position')
        self.storage.add(id, fullName, position)

    def showFormId(self, id):
        return self.storage.getItem(id).showForm()

    def showForm(self):
        return render_template('company1/form.tpl', it=self.storage.getItems())
        
#абстрактный класс для сотрудников фирмы
class Employee(ABC):
    
    @abstractmethod
    def addChild(self, employee):
        pass

    @abstractmethod
    def removeChild(self, employee):
        pass

    @abstractmethod
    def showForm(self):
       pass

    @abstractmethod
    def show(self):
       pass

@dataclass
class ConcreteEmployee(Employee):

    fullName: str = ""
    position: str = ""
    creationTime = 0
    childs = []
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.creationTime = datetime.datetime.now()

    def addChild(self, employee):
        self.childs.append(employee)
   
    def removeChild(self, employee):
        self.childs.remove(employee)

    def showForm(self):
        return render_template('company1/form.tpl', it=self)

    def show(self):
        return "Редактировать (руководители)"

    def mapFields(self, data):
        if data is not None:
            self.id = data[0]
            self.fullName = data[1]
            self.position = data[2]
            self.creationTime = data[3]
            self.childs = []
@dataclass
class LeafEmployee(Employee):

    fullName: str = ""
    position: str = ""
    creationTime = 0

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.creationTime = datetime.datetime.now()

    def addChild(self, employee):
        raise Exception("Подчиненных нет")

    def removeChild(self, employee):
        raise Exception("Подчиненных нет")

    def showForm(self):
        return render_template('company1/form.tpl', it=self)

    def show(self):
        return "Редактировать (младший персонал)"

    def mapFields(self, data):
        if data is not None:
            self.id = data[0]
            self.fullName = data[1]
            self.position = data[2]
            self.creationTime = data[3]

