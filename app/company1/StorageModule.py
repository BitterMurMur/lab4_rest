import pickle
import sqlite3
import uuid
from datetime import datetime
from sqlite3 import Connection
import app.company1.CompanyModule as CompanyModule
import app.company1.DB as DB


class Storage:

    def __init__(self, company):
        self.company = company
        try:
            self.load()
        except:
            self.company.director = CompanyModule.ConcreteEmployee()
            self.company.leadEngineers:list[CompanyModule.ConcreteEmployee]  = []
            self.company.engineers:list[CompanyModule.LeafEmployee] = []

    def save(self):
        pickle.dump((self.company.director, self.company.leadEngineers, self.company.engineers), open("data/company1/data.dat", "wb"))
        
    def load(self):
        (self.company.director, self.company.leadEngineers, self.company.engineers) = pickle.load(open("data/company1/data.dat", "rb"))

    def getItems(self):
        company = CompanyModule.Company()
        company.director = self.company.director
        company.leadsEngineers = self.company.leadEngineers
        company.engineers = self.company.engineers
        return company

    def delete(self, id):
        if self.company.director.id == id:
            import CompanyModule
            self.company.director = CompanyModule.ConcreteEmployee()
        if len(self.company.director.childs) > 0:
            for child in self.company.director.childs:
                if child.id == id:
                    self.company.director.removeChild(child)
        if len(self.company.leadEngineers) > 0:
            for emp in self.company.leadEngineers:
                if emp.id == id:
                    self.company.leadEngineers.remove(emp)
                if len(emp.childs) > 0:
                    for child in emp.childs:
                        if child.id == id:
                            emp.removeChild(child)
        if len(self.company.engineers) > 0:
            for emp in self.company.engineers:
                if emp.id == id:
                    self.company.engineers.remove(emp)

    def getItem(self, id):
        if id == '0':
            return CompanyModule.Company()
        if self.company.director.id == id:
             return self.company.director
        if len(self.company.leadEngineers) > 0:
            for emp in self.company.leadEngineers:
                if emp.id == id:
                    return emp
        if len(self.company.engineers) > 0:
            for emp in self.company.engineers:
                if emp.id == id:
                    return emp
        raise Exception("Сотрудника с таким Id не существует")

    def add(self, fullName, position):
        if position == "Директор":
            self.company.director.fullName = fullName
            self.company.director.position = "Директор"
            if len( self.company.leadEngineers) > 0:
                for emp in  self.company.leadEngineers:
                    self.company.director.addChild(emp)
            if len( self.company.engineers) > 0:
                for emp in  self.company.engineers:
                    self.company.director.addChild(emp)

        elif position == "Ведущий инженер":
            leadEngineer = CompanyModule.ConcreteEmployee()
            leadEngineer.fullName = fullName
            leadEngineer.position = "Ведущий инженер"
            if len( self.company.engineers) > 0:
                for emp in  self.company.engineers:
                    leadEngineer.addChild(emp)
            self.company.leadEngineers.append(leadEngineer)

        elif position == "Инженер":
            engineer = CompanyModule.LeafEmployee()
            engineer.fullName = fullName
            engineer.position = "Инженер"
            self.company.engineers.append(engineer)

class DBStorage:

    con: Connection

    def __init__(self, company):
        self.company = company
        self.companyId = '35779ccf-a666-4596-9f44-15445f77e0e0'
        # self.company.director:CompanyModule.ConcreteEmployee
        # self.company.leadEngineers: list[CompanyModule.ConcreteEmployee]
        # self.company.engineers: list[CompanyModule.LeafEmployee]
        self.connect()


    def connect(self):
            self.con = sqlite3.connect('data/company1/Companies.db', detect_types=sqlite3.PARSE_DECLTYPES)
            self.cursor = self.con.cursor()

    def save(self):
        self.con.commit()
        self.con.close()

    def load(self):
        DB.createDB()

    def getItems(self):
        company = CompanyModule.Company()
        self.cursor.execute("select * from Employees where Position = 'Директор'")
        data = self.cursor.fetchone()
        self.cursor.execute("""select * from Employees""")
        dataChilds = self.cursor.fetchall()
        if data is not None:
            company.director.mapFields(data)
            self.setChilds(dataChilds, company.director)
        self.cursor.execute("select * from Employees where Position = 'Ведущий инженер'")
        data = self.cursor.fetchall()
        for item in data:
            tmpLead = CompanyModule.ConcreteEmployee()
            tmpLead.mapFields(item)
            self.setChilds(dataChilds, tmpLead)
            company.leadEngineers.append(tmpLead)
        self.cursor.execute("select * from Employees where Position = 'Инженер'")
        data = self.cursor.fetchall()
        for item in data:
            tmpEng = CompanyModule.LeafEmployee()
            tmpEng.mapFields(item)
            company.engineers.append(tmpEng)
        return company

    def delete(self, id):
        self.cursor.execute("delete from Employees where Id = ?", (id,))

    def getItem(self, id):
        self.cursor.execute("""select * from Employees  
        where Id =?""", (id,))
        data = self.cursor.fetchone()
        self.cursor.execute("select * from Employees")
        childData = self.cursor.fetchall()
        if id == '0':
            return CompanyModule.Company()
        if data[2] == 'Директор':
            director = CompanyModule.ConcreteEmployee()
            director.mapFields(data)
            self.setChilds(childData, director)
            return director
        if data[2] == 'Ведущий инженер':
            leadEngineer = CompanyModule.ConcreteEmployee()
            leadEngineer.mapFields(data)
            self.setChilds(childData, leadEngineer)
            return leadEngineer
        if data[2] == 'Инженер':
            eng = CompanyModule.LeafEmployee()
            eng.mapFields(data)
            return eng

    def setChilds(self, data, employee):
        if employee.position == 'Директор':
            for item in data:
                if item[2] == 'Ведущий инженер':
                    child = CompanyModule.ConcreteEmployee()
                    child.mapFields(item)
                    employee.addChild(child)
                if item[2] == 'Инженер':
                    child = CompanyModule.LeafEmployee()
                    child.mapFields(item)
                    employee.addChild(child)
        if employee.position == 'Ведущий инженер':
            for item in data:
                if item[2] == 'Инженер':
                    child = CompanyModule.LeafEmployee()
                    child.mapFields(item)
                    employee.addChild(child)

    def add(self, id, fullName, position):
            self.cursor.execute("select * from Employees where Id=?", (id,))
            addedEmployee = self.cursor.fetchone()
            if addedEmployee is not None:
                self.update(id, fullName, position)
            else:
                self.cursor.execute("""insert into Employees 
                values(?,?,?,?,?)""", (uuid.uuid4().__str__(), fullName, position, datetime.now(), self.companyId))

    def update(self,id, fullName, position):
        self.cursor.execute("update Employees set FullName=?, Position=? where id=?", (fullName, position, id))


