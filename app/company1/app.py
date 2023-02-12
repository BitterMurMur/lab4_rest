
from flask import Flask,  g
from app.company1.CompanyModule import Company
from app.company1 import bp

app = Flask(__name__)

def getCompany():
    if 'company' not in g:
        g.company = Company()
    return g.company

@bp.route("/")
def companyindex():
    return getCompany().show()

@bp.route("showform/<id>")
def showform(id):
    return getCompany().showFormId(id)

@bp.route("delete/<id>")
def delete(id):
    return getCompany().delete(id)

@bp.route("add/", methods=['POST'])
def add():
    return getCompany().add()

@bp.teardown_request
def teardown(ctx):
    getCompany().storage.save()

if __name__ == "__main__":
    app.run(debug=True)