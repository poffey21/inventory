##
# take the json_data and create a set of items.
from . import models

class ReceiptSerializer(object):
    """ abstract class that implements receipt functions """
    
    def __init__(self, json_data):
        self.json_data = json_data


class Aldi(ReceiptSerializer):
    """ Receive a set of JSON Data """
    
    
    