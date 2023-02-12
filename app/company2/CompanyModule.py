
from dataclasses import dataclass
from app.company2.StorageModule import *
from abc import ABC, abstractmethod
from flask import render_template, request, jsonify
import datetime

from app.company2.StrategyModule import *


@dataclass
class Company:
    
    def __init__(self):
        self.name = "ООО \"Тестовая\""
        self.storage = DBStorage(self)
        self.io:IStrategy = SQLIOStrategy(self.storage)
        self.rest:IStrategy = RestStrategy(self.storage)
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
        return render_template('company2/form.tpl', it=self.storage.getItems())

    def apicompany(self):
        ids = []
        company = self.storage.getItems()
        ids.append([company.director.id, company.director.fullName,  company.director.childs])
        for item in company.leadEngineers:
            ids.append([item.id, item.fullName, item.childs])
        for item in company.engineers:
            ids.append([item.id, item.fullName])
        return jsonify({'ids': ids })

    def apiadd(self):
        print(request.json)
        item = self.storage.getItem(0)
        item.input(self.rest)
        self.storage.add(item.fullName, item.position)


    def apiget(self, id):
        item = self.storage.getItem(id)
        print(item.__dict__)
        return jsonify(item.__dict__)

    def apiset(self, id):
        item = self.storage.getItem(id)
        item.input(self.rest)
        self.storage.add(item.fullName, item.position)


    def apidelete(self, id):
        self.storage.delete(id)

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
        return render_template('company2/form.tpl', it=self)

    def show(self):
        return "Редактировать (руководители)"

    def mapFields(self, data):
        if data is not None:
            self.id = data[0]
            self.fullName = data[1]
            self.position = data[2]
            self.creationTime = data[3]
            self.childs = []

    def input(self, io):
        self.id = io.input('id', self.id)
        self.fullName = io.input('Имя')
        self.position = io.input('Должность')
        self.childs = []

    def output(self, io):
        return io.output(self)
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
        return render_template('company2/form.tpl', it=self)

    def show(self):
        return "Редактировать (младший персонал)"

    def mapFields(self, data):
        if data is not None:
            self.id = data[0]
            self.fullName = data[1]
            self.position = data[2]
            self.creationTime = data[3]

    def input(self, io):
        self.id = io.input('id', self.id)
        self.fullName = io.input('Имя')
        self.position = io.input('Должность')

    def output(self, io):
        return io.output(self)
