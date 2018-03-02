from flask import Blueprint, jsonify, request
from orycha import Orycha

servus = Blueprint('servus', __name__)


@servus.route('/login')
def login():
    return jsonify({'message': 'Under construction'}), 200


@servus.route('/create_node', methods=['POST'])
def create_node():
    node = Orycha.create(length=0, name='My Node')
    return jsonify({'result': 'success', 'user_action': node.__dict__}), 200


@servus.route('/delete', methods=['POST'])
def delete_node():
    data = request.get_json()
    _ = Orycha.delete(search_by=data)
    return jsonify({'result': 'success', 'message': 'Node deleted successfully'}), 200


@servus.route('/add_data/<string:node_id>', methods=['POST'])
def add_data_in_node(node_id):
    data = request.get_json()
    _ = Orycha.set_data(token_id=int(node_id), data=data)
    return jsonify({'result': 'success'}), 200


@servus.route('/get_node/<string:token_id>')
def get_node(token_id):
    node = Orycha.get(token_id=int(token_id))
    node['_id'] = str(node['_id'])
    return jsonify({'result': 'success', 'node': node}), 200


@servus.route('/get_all')
def get_all_nodes():
    nodes = Orycha.get_all()
    return jsonify({'result': 'success', 'nodes': nodes}), 200

