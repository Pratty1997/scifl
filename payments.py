import pymongo
import hashlib
import string
import random

client = pymongo.MongoClient('localhost:27017')

class Payments:

    def __init__(self):

        self.db = client.scifl
        self.payments = self.db.payments
    
    def new_payment(self, user, method, amount, card, status):

        payment = {
            'user': user,
            'method': method,
            'amount': amount,
            'card_number': card,
            'status': status
        }

        try:
            self.payments.insert_one(payment)
            return True
        except Exception as e:
            return False