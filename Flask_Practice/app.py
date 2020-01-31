from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import identity, authenticate

app = Flask(__name__)
app.secret_key = 'rapol'
api = Api(app)

items = []

jwt = JWT(app, authenticate, identity)


class Item(Resource):
    @jwt_required()
    def get(self, name):
        """for item in items:
            if item['name'] == name:
                return item
            else:
                return {'item': None}, 404
                """
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 404 if item is None else 200  # or 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {'message': "item with name '{}' already exits.".format(name)}
        else:
            data = request.get_json()
            item = {'name': name, 'prince': data['price']}
            items.append(item)
            return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {
            'message': "item Deleted"
        }

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help="this is wrong keyword")
        data = parser.parse_args() #request.get_json()
        print(data)
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
            print(data)
            return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(debug=True)
