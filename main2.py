from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)
#Составим схему
class BookSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    author = fields.Str()
    year = fields.Int()

book_schema = BookSchema()
books_schema = BookSchema(many=True)
api=Api(app)
book_ns = api.namespace('')

b1 = Book(id =1, name = "Harry Potter", author = "Joan routing", year =1992)
b2 = Book(id =2, name = "monte-Cristo", author = "Alexandr Dumas", year =1852)

db.create_all()# создаем таблицы
with db.session.begin(): # открытие сессии
    db.session.add_all([b1, b2])

@book_ns.route('/books')
class BookView(Resource):
    def get(self):
        all_books = db.session.query(Book).all()
        return books_schema.dump(all_books), 200

    def post(self):
        req_json = request.json
        new_book =Book(**req_json)
        with db.session.begin():
            db.session.add(new_book)
        return "", 201
@book_ns.route('/books/<int:uid>')
class BookView(Resource):
    def get(self, uid:int):#получение данных
        try:
            book = db.session.query(Book).filter(Book.id == uid).one()
            return books_schema.dump(book), 200
        except Exception as e:
            return str(a), 404

    def put(self,uid):#Замена даннаых
        book = db.session.query(Book).get(uid)
        req_json = request.json

        book.name = req_json.get("name")
        book.author = req_json.get("author")
        book.year = req_json.get("year")
        db.session.add(book)
        db.session.commit()

        return "", 204
    def patch(self, uid):
        book= db.session.query(Book).get(uid)
        req_json = request.json

        if "name" in req_json:
            book.name = req_json.get("name")
        if "author" in req_json:
            book.author = req_json.get("author")
        if "year" in req_json:
            book.year = req_json.get("year")

        return "", 204

    def delete(self, uid, int):
         book = db.session.query(Book).get

         db.session.delete(book)
         db.session.commit()

         return "", 204

if __name__ == '__main__':
    app.run(debug=True)