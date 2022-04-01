from flask import Flask, request
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

@app.route('/test')
def test():
   print(request.args.get("param"))
   return 'Teste'

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
from sql_alchemy import banco
banco.init_app(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=27017)
