import pymongo
import hashlib
import string
import random

# Create a db client, running on 

client = pymongo.MongoClient('localhost:27017')

# Database : MongoDB
# Database name : scifl
# collection name : users (for Doctors, Patients) 

class User:

    def __init__(self):
        self.db = client.scifl
        self.users = self.db.users
        self.otp = self.db.otp

    # Make salt for password
    def make_salt(self):
        salt_value = ''
        for i in range(12):
            salt_value += random.choice(string.ascii_letters)

        return salt_value

    # Create an OTP for various actions
    def create_otp(self):
        OTP = ''
        numeric_values = '0123456789'
        for i in range(6):
            OTP += random.choice(numeric_values)
        return OTP

    # Create a hashed password for security
    def create_hashed_password(self, password, salt_value = None):
        if(salt_value == None):
            salt_value = self.make_salt()

        encoded_string = (str(password) + salt_value).encode('UTF-8')
        digested_string = hashlib.blake2b(encoded_string).hexdigest()
        password = digested_string + ":" + salt_value

        return password

    def find_user(self, email):
        try:
            user = self.users.find_one({'email': email})
            return user
        except Exception as ex:
            return None

    def validate_password(self, user, password):
        
        actual_password = user['password']
        user_salt = actual_password.split(':')[1]
        entered_password = self.create_hashed_password(password, user_salt)
        if(entered_password == actual_password):
            return True
        else:
            return False

    def register(self, email, name, password, phone_number, role):

        password_for_user = self.create_hashed_password(password) 
        new_user = {
            'name': name,
            'email': email,
            'password': password_for_user,
            'phone_number': phone_number,
            'role': role,
            'blocked': {
                'flag': False,
                'reason': ''
            }
            'verfied': {
                'status': False,
                'action': 'Email verification pending'
            }
        }

        try:
            self.users.insert_one(new_user)
            # Add a module to send an email with an activation link.
            return True
        
        except pymongo.errors.DuplicateKeyError as e:
            return 'user already exists, please login'
        
        except Exception as ex:
            return False
    
    def login(self, email, password):

        # find if a user exists
        user = self.find_user(email)
        
        if(user):
            password_validation = self.validate_password(user, password)
            if(password_validation):
                # For security, return a token that will be used to monitor all authenticated activities. 
                return True
            else:
                return False
    
    def change_password(self, email, password):
        
        new_password = self.create_hashed_password(password)

        try:
            self.users.update_one({'email': email}, {'$set': {'password': new_password}})
        # Add a module to send an email alert to the user stating that their password has been changed.
        
        except Exception as e:
            return False

    def generate_otp(self, email, action, timestamp):

        OTP = self.generate_otp()

        new_action = {
            'email': email,
            'action': action,
            'otp': OTP,
            'time': timestamp
        }

        try:
            self.otp.insert_one(new_action)
            # A Module to send OTP via sms.
            # An OTP has been sent to your email/mobile number.
            return True
        except Exception as e:
            return False