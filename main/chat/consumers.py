from channels.generic.websocket import JsonWebsocketConsumer
from ecomm.models import Good


class ChatConsumer(JsonWebsocketConsumer):
    """
    Consumer to work with json messages in chat
    """
    def connect(self):
        super().connect()
        self.user = self.scope['user']
        self.send_json({'message': '[Welcome %s!]' % self.user})

    def receive_json(self, data, **kwargs) -> None:
        message: str = data['message']
        response_message: str = get_response_message(message)
        self.send_json({'message': response_message})


def get_response_message(message: str) -> str:
    """
    Function takes good title and return good availability in stock
    :param message: Good name
    :return: Good in stock
    """
    dash_index: int = message.find('#')
    if dash_index == -1:
        return 'Please, enter good name after #'

    good_name: str = message[dash_index + 1:].strip()
    try:
        good_count: int = Good.objects.get(title__exact=good_name).quantity
    except Good.DoesNotExist:
        return good_name + '\nNothing found'
    if good_count == 0:
        return good_name + '\nGood out of stock'
    return f'{good_name}\nIn stock {good_count}'
