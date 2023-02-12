
from flask import Flask,  g
from app.company2.CompanyModule import Company
from app.company2 import bp

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def getCompany():
    if 'company' not in g:
        g.company = Company()
    return g.company

@bp.route("/")
def companyindex():
    return getCompany().show()

@bp.route("/showform/<id>")
def showform(id):
    return getCompany().showFormId(id)

@bp.route("/delete/<id>")
def delete(id):
    return getCompany().delete(id)

@bp.route("/add/", methods=['POST'])
def add():
    return getCompany().add()

@bp.teardown_request
def teardown(ctx):
    getCompany().storage.save()

if __name__ == "__main__":
    app.run(debug=True)


@bp.route("/api/", methods=['GET'])
def apicompany():
    return getCompany().apicompany()


@bp.route("/api/", methods=['POST'])
def apiadd():
    return getCompany().apiadd()


@bp.route("/api/<id>", methods=['GET'])
def apiget(id):
    return getCompany().apiget(id)


@bp.route("/api/<id>", methods=['PUT'])
def apiset(id):
    return getCompany().apiset(id)


@bp.route("/api/<id>", methods=['DELETE'])
def apidelete(id):
    return getCompany().apidelete(id)