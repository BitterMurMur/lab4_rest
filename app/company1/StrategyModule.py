
from abc import ABC, abstractmethod
from flask import render_template


# абстрактный класс для стратегии
class IStrategy(ABC):

    @abstractmethod
    def input(self, name ):
        pass
    @abstractmethod  
    def output(self, title, field):
        pass
#конкретная стратегия для ввода вывода с консоли        
class ConsoleIOStrategy(IStrategy):
    
    def input(self,  field=None):
        return input(f"{field}: ")
    
    def output(self, title=None, field=None):
        print(f"{title}: {field}")

#конкретная стратегия для ввода вывода через веб форму
class WebIOStrategy(IStrategy):

    def __init__(self, storage):
        self.storage = storage

    def input(self,  field=None):
        return render_template('company1/form.tpl', it=self)

    def output(self, title=None, field=None):
        company = self.storage.getItems()
        if company is not None:
            return render_template('company1/company.tpl', it=company.director, leads=company.leadEngineers, engs=company.engineers)
        else:
            return render_template('company1/company.tpl', it="", leads="", engs="")

# конкретная стратегия для ввода вывода sql
class SQLIOStrategy(IStrategy):

    def __init__(self, storage):
        self.storage = storage

    def input(self, field=None):
        return render_template('company1/form.tpl', it=self)

    def output(self, title=None, field=None):
        company = self.storage.getItems()
        if company is not None:
            return render_template('company1/company.tpl', it=company.director, leads=company.leadEngineers,
                                   engs=company.engineers)
        else:
            return render_template('company1/company.tpl', it="", leads="", engs="")