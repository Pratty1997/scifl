import pymongo

client = pymongo.MongoClient('localhost:27017')

class Hospitals:

    def __init__(self):
        self.db = client.scifl
        self.hospitals = self.db.hospitals

    def add_hospital(self, name, phone_number, pin, city, state, available_facilities):
        # Add a provision to add doctors to the hospital, so that, they can be contacted in case of emergency.

        add = {
            'name': name,
            'phone_number': phone_number,
            'pin': pin,
            'city': city,
            'state': state,
            'rating': 1,
            # Array of available facilities.
            'available_facilities': available_facilities
        }

        try:
            self.hospitals.insert_one(add)
            return True
        except Exception as e:
            return False
    
    def find_hospital(self, method, query):

        search_results = []

        if(method == 'location'):
            match = {'location': query}
            found = self.hospitals.find(match)

            for value in found:
                search_results.append(value)

        elif(method == 'name'):
            match = {'name': query}
            found = self.hospitals.find(match)
            
            for value in found:
                search_results.append(value)

        return search_results


class Banks:

    def __init__(self):
        self.db = client.scifl
        self.banks = self.db.banks

    def add_bank(self, name, phone_number, pin, city, state):

        add = {
            'name': name,
            'phone_number': phone_number,
            'pin': pin,
            'city': city,
            'state': state,
            'rating': 1
        }

        try:
            self.banks.insert_one(add)
            return True
        except Exception as e:
            return False
    
    def find_bank(self, method, query):

        search_results = []

        if(method == 'location'):
            match = {'location': query}
            found = self.banks.find(match)

            for value in found:
                search_results.append(value)

        elif(method == 'name'):
            match = {'name': query}
            found = self.banks.find(match)
            
            for value in found:
                search_results.append(value)

        return search_results
