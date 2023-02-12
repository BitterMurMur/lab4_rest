import sqlite3

def createDB():
    with sqlite3.connect('data/Companies.db') as con:
        cursor = con.cursor()
        cursor.execute("""
        create table Companies 
        (
            Id text not null primary key,
            CreationDate datetime null,
            Name text not null
        )"""
        )
        cursor.execute("""
        create table Employees 
        (
            Id text not null primary key,
            FullName text not null,
            Position text not null,
            CreationDate datetime null,
            CompanyId text null,
            FOREIGN KEY (CompanyId) REFERENCES Companies(id)
        )"""
        )
        cursor.execute("""insert into "Companies"
    values
    ('35779ccf-a666-4596-9f44-15445f77e0e0',
    date('now'),
    'ООО Тестовая'
    )""")

