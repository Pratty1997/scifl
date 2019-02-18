import bottle
import users
import banks_hospitals
import payments
import random

route = bottle.route
request = bottle.request
redirect = bottle.redirect

@route('/login', method='POST')
def login():

    # Get credentails from the front-end
    email = request.forms.get('email')
    password = request.forms.get('password')

    user = users.User()
    status = user.login(email, password)

    if(status == 'User has been blocked by us'):
        return status
    
    elif(status == 'Please register to continue'):
        return status

    elif(status == 201):
        page = '/profile/' + email
        redirect(page)

    elif(status == 202):
        return 'password or email incorrect'

    else:
        return status

@route('/register', method='POST')
def regitser():

    user = users.User()

    name = request.forms.get('name')
    email = request.forms.get('email')
    password = request.forms.get('password')
    phone_number = request.forms.get('phone_number')
    role = request.forms.get('role')

    status = user.register(email, name, password, phone_number, role)

    if(status == True):
        return 'User successfully registered'
    
    else:
        return 'User registration failed. Please try again.'

@route('/changepassword', method='POST')
def change_password():

    email = request.forms.get('email')
    password = request.forms.get('password')

    user = users.User()

    status = user.change_password(email, password)

    if(status):
        return 'Password successfully changed'
    
    else:
        return 'Password cound not be changed. Please try again'

@route('/verify/<user_account>')
def verify_user(user_account):

    user = users.User()
    email = user_account.split(':')[1]

    status = user.verify_user(email)

    if(status == True):
        return ' User has been verified'
    
    elif(status == False):
        return 'User verification failed. Try again.'

    elif(status == 'User is already verified'):
        return status
    
    elif(status == 'User not found'):
        return status

    else:
        return (status + ' . Please reactivate the user and try again')
    
@route('/block/<user_account>')
def block_account(user_account, method='POST'):

    user = users.User()

    email = user_account.split(':')[1]

    reason = request.forms.get('reason')

    status = user.block_user(email, reason)

    if(status):
        return status
    
    else:
        return 'Error occurred. Please try again.'

@route('/reactivate/<user_account>')
def reactivate(user_account):

    user = users.User()

    email = user_account.split(':')[1]

    status = user.reactivate_user(email)

    if(status == 'User is not blocked'):
        return status
    
    elif(status == 'User has been successfully reactivated'):
        return status

    else:
        return 'Reactivation failed. Please try again.'

@route('/new/<role>', method='POST')
def new_entry(role):

    hospitals = banks_hospitals.Hospitals()
    banks = banks_hospitals.Banks()

    name = request.forms.get('name')
    phone_number = request.forms.get('phone_number')
    pin = request.forms/get('pin')
    city = request.forms.get('city')
    state = request.forms.get('state')

    if(role == 'hospitals'):
        available_facilities = request.forms.get('available_facilities')
        status = hospitals.add_hospital(name, phone_number, pin, city, state , available_facilities)
        if(status):
            return 'Added successfully'
        else:
            return 'Error occurred.'
    
    else:
        status = banks.add_bank(name, phone_number, pin, city, state)
        if(status):
            return 'Added successfully'
        else:
            return 'Error occurred.'

@route('/find/<role>/<method>/<query>')
def find(role, method, query):

    if(role == 'hospital'):
        hospital = banks_hospitals.Hospitals()

        found = hospital.find_hospital(method, query)
        
        return found

    else:
        banks = banks_hospitals.Banks()

        found = banks.find_bank(method, query)

        return found

@route('/newpayment/<user>')
def new_payment(user):

    payment = payments.Payments()

    email = user.split(':')[1]
    method = request.forms.get('method')
    amount = request.forms.get('amount')
    card_number = request.forms.get('card')
    
    # If payment is successful
    # If payment is unsuccessful

    rand_int = random.randint(0,1)

    if(rand_int == 0):
        payment_status = 'Successful'
    else:
        payment_status = 'Unsuccessful'
    
    status = payment.new_payment(email, method, amount, card_number, payment_status)

    if(status):
        return 'Added.'
    
    else:
        while(status == False):
            status = payment.new_payment(email, method, amount, card_number, payment_status)

        return 'Added.'
    