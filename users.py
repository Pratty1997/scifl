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
            },
            'verified': {
                'status': False,
                'action': 'Email verification'
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
            if(user['blocked']['flag'] == True):
                # User has been blocked by us.
                return 'User has been blocked by us'
            if(user['verified']['status'] == False):
                # User has done completed some verification action.
                return ('Please complete ' + user['verified']['action'] + ' to proceed')
            
            password_validation = self.validate_password(user, password)
            if(password_validation):
                # For security, return a token that will be used to monitor all authenticated activities. 
                return True
            else:
                return False
        else:
            return 'Please register to continue'
    
    def change_password(self, email, password):
        
        new_password = self.create_hashed_password(password)

        try:
            self.users.update_one({'email': email}, {'$set': {'password': new_password}})
        # Add a module to send an email alert to the user stating that their password has been changed.
        
        except Exception as e:
            return False
    
    def verify_user(self, email):

        user = self.find_user(email)

        if(user):
            match = {'email': email}
            update = {'$set': { "verified.status": True, 'verified.action': ''}}
            
            if(user['blocked']['flag'] == True):
                return 'User has been blocked for '+ user['blocked']['reason'] 
            
            if(user['verified']['status'] == True):
                return 'User is already verified'

            try:
                self.users.update_one(match, update)
                return True
            except Exception as e:
                print(e)
                return False

        else:
            return 'User not found'

    def block_user(self, email, reason):
        
        user = self.find_user(email)

        if(user):
            
            match = {'email' : email}
            update = {'$set': {'blocked.flag' : True, 'blocked.reason': reason}}

            try:
                self.users.update_one(match, update)
                return 'User has been successfully blocked'
            except Exception as e:
                return False

    def reactivate_user(self, email):

        user = self.find_user(email)

        if(user):

            match = {'email': email}
            update = {'$set': {'blocked.flag': False, 'blocked.reason': ''}}
            if(user['blocked']['flag'] == False):
                return 'User is not blocked'
            try:
                self.users.update_one(match, update)
                return 'User has been successfully reactivated'
            except Exception as e:
                return False
            
    def generate_otp(self, email, action, timestamp):

        OTP = self.create_otp()

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

user = User()
email = 'xyz@gmail.com'
name = 'XYZ'
password = 'abcd'
phone_number = 1234567890
role = 'patient'
reason= 'malpractice'

# if(user.register(email,name,password,phone_number,role)):
#     print("User created")

# print(user.login(email,password))

#print(user.verify_user(email))

# print(user.block_user(email))

# print(user.verify_user(email))

# print(user.reactivate_user(email))

# print(user.block_user(email,reason))