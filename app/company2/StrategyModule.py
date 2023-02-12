
from abc import ABC, abstractmethod
from flask import render_template


# абстрактный класс для стратегии
class IStrategy(ABC):

    @abstractmethod
    def input(self, field=None,  value=None ):
        pass
    @abstractmethod  
    def output(self, item ):
        pass
#конкретная стратегия для ввода вывода с консоли        
class ConsoleIOStrategy(IStrategy):
    
    def input(self,  field=None,  value=None):
        return input(f"{field}: ")
    
    def output(self, item):
        print(item)

#конкретная стратегия для ввода вывода через веб форму
class WebIOStrategy(IStrategy):

    def __init__(self, storage):
        self.storage = storage

    def input(self,  field=None,  value=None):
        return render_template('company2/form.tpl', it=self)

    def output(self, item):
        company = self.storage.getItems()
        if company is not None:
            return render_template('company2/company.tpl', it=company.director, leads=company.leadEngineers, engs=company.engineers)
        else:
            return render_template('company2/company.tpl', it="", leads="", engs="")

# конкретная стратегия для ввода вывода в sql
class SQLIOStrategy(IStrategy):

    def __init__(self, storage):
        self.storage = storage

    def input(self,  field=None,  value=None):
        return render_template('company2/form.tpl', it=self)

    def output(self, item=None):
        company = self.storage.getItems()
        if company is not None:
            return render_template('company2/company.tpl', it=company.director, leads=company.leadEngineers,
                                   engs=company.engineers)
        else:
            return render_template('company2/company.tpl', it="", leads="", engs="")

# конкретная стратегия для ввода вывода rest api
class RestStrategy(IStrategy):

    def __init__(self, io):
        self.io = io

    def input(self,  field=None,  value=None):
        return self.io.json.get(field)


    def output(self,item):
        print(item)
