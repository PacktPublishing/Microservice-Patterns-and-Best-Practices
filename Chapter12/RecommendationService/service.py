import json
import logging

from nameko.web.handlers import http
from nameko.events import event_handler

from user_client import UserClient

from models import (
    create_user_node,
    create_label_node,
    create_recommendation,
    get_labels_by_user_id,
    get_users_by_label,
)


class Recommendation:
    name = 'recommendation'

    # declaring the receiver method as a handler to message broker
    @event_handler('recommendation_sender', 'receiver')
    def receiver(self, data):
        try:
            # consuming data from UsersService using the requests lib
            with UserClient(data['user_id']) as response:
                user = response
            # creating user node on Neo4j
            create_user_node(user)
            # getting all tags read
            for label in data['news']['tags']:
                # creating label node on Neo4j
                create_label_node(label)
                # creating the recommendation on Neo4j
                create_recommendation(
                    user.id,
                    label,
                )
        except Exception as e:
            logging.error('RELATIONSHIP_ERROR: {}'.format(e))


class RecommendationApi:
    name = 'recommnedation_api'

    @http('GET', '/user/<int:user_id>')
    def get_recommendations_by_user(self, request, user_id):
        """Get recommendations by user_id"""
        try:
            relationship_response = get_labels_by_user_id(user_id)
            http_response = [
                rel.end_node()
                for rel in relationship_response
            ]
            return 200, {'Content-Type': 'application/json'}, json.dumps(http_response)
        except Exception as ex:
            error_response(500, ex)

    @http('GET', '/label/<string:label>')
    def get_users_recomendations_by_label(self, request, label):
        """Get users recommendations by label"""
        try:
            relationship_response = get_users_by_label(label)
            http_response = [
                rel.end_node()
                for rel in relationship_response
            ]
            return 200, {'Content-Type': 'application/json'}, json.dumps(http_response)
        except Exception as ex:
            error_response(500, ex)


def error_response(code, ex):
    response_object = {
        'status': 'fail',
        'message': str(ex),
    }
    return code, {'Content-Type': 'application/json'}, json.dumps(response_object)
