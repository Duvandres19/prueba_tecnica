from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tecnica:Tecnica@dev-priceshoes.cxzdtitkxlft.us-east-2.rds.amazonaws.com/PRUEBA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Tecnica(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    parent = db.Column(db.Integer)

    def __init__(self, id,nombre, parent):
        self.ID = id
        self.nombre = nombre
        self.parent = parent



class TecnicaSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'nombre', 'parent')


tecnica_schema = TecnicaSchema()
tecnicas_schema = TecnicaSchema(many=True)

@app.route('/tecnica/add', methods=['Post'])
def insertData():
  id = request.json['id']
  nombre = request.json['nombre']
  parent = request.json['parent']

  new_model= Tecnica(id, nombre,parent)

  db.session.add(new_model)
  db.session.commit()

  return tecnica_schema.jsonify(new_model)

@app.route('/tecnica/get', methods=['GET'])
def getData():
  all_data = Tecnica.query.all()
  result = tecnicas_schema.dump(all_data)
  return jsonify(result)

@app.route('/tecnica/get/<id>', methods=['GET'])
def get_task(id):
  tecnica = Tecnica.query.get(id)
  return tecnica_schema.jsonify(tecnica)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})



if __name__ == "__main__":
    app.run(debug=True)
