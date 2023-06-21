from pymongo import MongoClient
from flask import Flask, request, jsonify, Response
from datetime import timedelta
import json
import uuid

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose InfoSys database
db = client['DigitalAirlines']
users = db['Users']
flights = db['Flights']
reservations = db['Reservations']

# Initiate Flask App
app = Flask(__name__)

# Each session lasts 10 minues
app.permanent_session_lifetime = timedelta(minutes=10)

# Dictionary of Live Sessions (Users Logged-In)
live_sessions = {"admin": {}, "simple": {}}


# Create a live session for each Logged-In user
def create_session(email, role_admin):
    userID = str(uuid.uuid4())
    if role_admin:
        live_sessions['admin'][userID] = email
    else:
        live_sessions['simple'][userID] = email
    return True


# Simple User Sign-Up
@app.route('/sign_up', methods=['POST'])
def sign_up():
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON Content", status=500, mimetype='application/json')

    if data == None:
        return Response("Bad Request", status=500, mimetype='application/json')

    if not "username" in data or not "sirname" in data or not "email" in data or not "password" in data or not\
            "date_of_birth" in data or not "origin_country" in data or not "passport_number" in data:
        return Response("Information Incomplete", status=500, mimetype="application/json")

    if (users.find({"email": data['email']}).count() == 0) and (users.find({"username": data['username']}).count() == 0):
        simple_user = {"username": data['username'], "sirname": data['sirname'], "email": data['email'],
                       "entr_password": data['entr_password'], "date_of_birth": data['date_of_birth'],
                       "origin_country": data['origin_country'], "passport_number": data['passport_number'],
                       "category": 'simple'}
        users.insert_one(simple_user)
        return Response("User was added to the MongoDB", status=200, mimetype='application/json')
    else:
        return Response("A user with the given email or username already exists", status=200,
                        mimetype='application/json')


# User Log-In
@app.route('/log_in', methods=['POST'])
def log_in():
    data = None
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON Content", status=500, mimetype='application/json')

    if data == None:
        return Response("Bad Request", status=500, mimetype='application/json')

    if not "email" in data or not "entr_password" in data:
        return Response("Information Incomplete", status=500, mimetype="application/json")

    if users.find({"$and": [{"email": data['email']}, {"entr_password": data['entr_password']}]}).count() == 1:
        user = users.find_one({"$and": [{"email": data['email']}, {"entr_password": data['entr_password']}]})
        if user['category'] == "administrator":
            create_session(data['email'], True)
        elif user['category'] == "simple":
            create_session(data['email'], False)
        return Response("User Logged-In.", status=200, mimetype='application/json')
    else:
        return Response("Re-enter your credentials. Entered Email or Password does not exist or it is registered "
                        "multiple times (invalid)", status=400, mimetype='application/json')


# Search Flights (for both Simple Users and Administrators)
@app.route('/search_flights', methods=['GET'])
def search_flights():
    userID = request.headers.get('authorization')
    data = None

    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON Content", status=500, mimetype='application/json')

    if data == None:
        return Response("Bad Request", status=500, mimetype='application/json')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')
    else:
        if userID in live_sessions['admin'] or userID in live_sessions['simple']:
            if "from_airport" in data and "to_airport" in data and "conducting_date" in data:
                if flights.find({"$and": [{"from_airport": data['from_airport']},
                                          {"to_airport": data['to_airport']},
                                          {"conducting_date": data['conducting_date']}]}).count() > 0:
                    my_flights = flights.find({"$and": [{"from_airport": data['from_airport']},
                                                 {"to_airport": data['to_airport']},
                                                 {"conducting_date": data['conducting_date']}]})
                    flight_list = []
                    for i in my_flights:
                        flight = {"_id": str(i['_id']), "conducting_date": i['conducting_date'],
                                  "from_airport": i['from_airport'], "to_airport": i['to_airport']}
                        flight_list.append(flight)
                    return Response("Flights:" + jsonify(flight_list), status=200, mimetype='application/json')
                else:
                    return Response("No flights with these conditions are registered",
                                    status=500, mimetype='application/json')
            elif "from_airport" in data and "to_airport":
                if flights.find({"$and": [{"from_airport": data['from_airport']},
                                          {"to_airport": data['to_airport']}]}).count() > 0:
                    my_flights = flights.find({"$and": [{"from_airport": data['from_airport']},
                                                 {"to_airport": data['to_airport']},]})
                    flight_list = []
                    for i in my_flights:
                        flight = {"_id": str(i['_id']), "conducting_date": i['conducting_date'],
                                  "from_airport": i['from_airport'], "to_airport": i['to_airport']}
                        flight_list.append(flight)
                    return Response("Flights:" + jsonify(flight_list), status=200, mimetype='application/json')
                else:
                    return Response("No flights with these conditions are registered",
                                    status=500, mimetype='application/json')
            elif "conducting_date" in data:
                if flights.find({"conducting_date": data['conducting_date']}).count() > 0:
                    my_flights = flights.find({"conducting_date": data['conducting_date']})
                    flight_list = []
                    for i in my_flights:
                        flight = {"_id": str(i['_id']), "conducting_date": i['conducting_date'],
                                  "from_airport": i['from_airport'], "to_airport": i['to_airport']}
                        flight_list.append(flight)
                    return Response("Flights:" + jsonify(flight_list), status=200, mimetype='application/json')
                else:
                    return Response("No flights with these conditions are registered",
                                    status=500, mimetype='application/json')
            else:
                if flights.find({}).count() > 0:
                    my_flights = flights.find({})
                    flight_list = []
                    for i in my_flights:
                        flight = {"_id": str(i['_id']), "conducting_date": i['conducting_date'],
                                  "from_airport": i['from_airport'], "to_airport": i['to_airport']}
                        flight_list.append(flight)
                    return Response("Flights:" + jsonify(flight_list), status=200, mimetype='application/json')
                else:
                    return Response("No flights registered", status=500, mimetype='application/json')
        else:
            return Response("Rogue User!", status=401, mimetype='application/json')


# Show Flight Details
@app.route('/show_flight/<id>', methods=['GET'])
def show_flight(id):
    userID = request.headers.get('authorization')

    if id == None:
        return Response("Bad Request", status=500, mimetype='application/json')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')
    else:
        if userID in live_sessions['admin'] or userID in live_sessions['simple']:
            if flights.find({"_id": str(id)}).count() == 1:
                i = flights.find_one({"_id": (id)})
                flight = {"_id": str(i['_id']), "conducting_date": i['conducting_date'],
                          "from_airport": i['from_airport'], "to_airport": i['to_airport'],
                          "ticket_num": {"business": i['ticket_num']['business'],
                                       "economy": i['ticket_num']['economy']},
                          "ticket_price": {"business": i['ticket_price']['business'],
                                         "economy": i['ticket_price']['economy']}}
                return Response("Flight:" + jsonify(flight) + "\n\nDeparture Airport: " +
                                str(flight['from_airport']) + "\nFinal Destination Airport: " +
                                str(flight['to_airport']) + "\nNumber of tickets available: \n\tBusiness Tickets: " +
                                str(flight['ticket_num']['business']) + "\n\tEconomy Tickets: " +
                                str(flight['ticket_num']['economy']) + "\nPrice of tickets: \n\tBusiness Tickets: " +
                                str(flight['ticket_price']['business']) + "\n\tEconomy Tickets: " +
                                str(flight['ticket_price']['economy']), status=200, mimetype='application/json')
            else:
                return Response("No valid flight with this id", status=500, mimetype='application/json')
        else:
            return Response("Rogue User!", status=401, mimetype='application/json')


# Reserve Ticket
@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    userID = request.headers.get('authorization')
    data = None

    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON Content", status=500, mimetype='application/json')

    if data == None:
        return Response("Bad Request", status=500, mimetype='application/json')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')

    if not "fid" in data or not "name" in data or not "sirname" in data or not "passport_number" in data or \
            not "date_of_birth" in data or not "email" in data or not "ticket_type" in data:
        return Response("Information Incomplete", status=500, mimetype="application/json")

    if userID in live_sessions['admin'] or userID in live_sessions['simple']:
        if flights.find({"_id": str(data['fid'])}).count() == 1:
            my_flight = flights.find_one({"_id": str(data['fid'])})
            if data['ticket_type'] == "business":
                flights.update_one({"_id": str(my_flight['_id'])},
                                   {'$set': {"ticket_num": {"business": int(my_flight['ticket_num']['business']) - 1}}})
            elif data['ticket_type'] == "economy":
                flights.update_one({"_id": str(my_flight['_id'])},
                                   {'$set': {"ticket_num": {"economy": int(my_flight['ticket_num']['economy']) - 1}}})
            else:
                Response("Invalid ticket type", status=500, mimetype='application/json')
            ticket_res = {"flight_id": str(data['fid']), "name": data['name'], "sirname": data['sirname'],
                          "passport_number": data['passport_number'], "date_of_birth": data['date_of_birth'],
                          "email": data['email'], "ticket_type": data['ticket_type']}
            reservations.insert_one(ticket_res)
            return Response("Ticket Reservation was made", status=200, mimetype='application/json')
        else:
            return Response("No valid flight with this id", status=500, mimetype='application/json')
    else:
        return Response("Rogue User!", status=401, mimetype='application/json')


# Show User Reservations
@app.route('/show_my_reservations', methods=['GET'])
def show_my_reservations():
    userID = request.headers.get('authorization')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')

    if userID in live_sessions['admin']: user_email = live_sessions['admin'][userID]
    elif userID in live_sessions['simple']: user_email = live_sessions['simple'][userID]
    else: Response("Rogue User!", status=401, mimetype='application/json')

    if reservations.find({"email": user_email}) > 0:
        my_reservations = reservations.find({"email": user_email})
        reservations_list = []
        for i in my_reservations:
            reservation = {"flight_id": str(i['_id']), "name": i['name'], "sirname": i['sirname'],
                      "passport_number": i['passport_number'], "date_of_birth": i['date_of_birth'],
                      "email": i['email'], "ticket_type": i['ticket_type']}
            reservations_list.append(reservation)
        return Response("Reservations:" + jsonify(reservations_list), status=200, mimetype='application/json')
    else:
        return Response("No reservations for this user", status=500, mimetype='application/json')


# Show Reservation Details
@app.route('/show_reservation/<id>', methods=['GET'])
def show_reservation(id):
    userID = request.headers.get('authorization')

    if id == None:
        return Response("Bad Request", status=500, mimetype='application/json')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')
    else:
        if userID in live_sessions['admin'] or userID in live_sessions['simple']:
            if reservations.find({"_id": str(id)}).count() == 1:
                i = reservations.find_one({"_id": str(id)})
                flightID = i['flight_id']
                if flights.find({"_id": str(flightID)}).count() == 1:
                    j = flights.find_one({"_id": str(flightID)})
                    reservation_details = {"from_airport": j['from_airport'], "to_airport": j['to_airport'],
                                           "conducting_date": j['conducting_date'], "name": i['name'],
                                           "sirname": i['sirname'], "passport_number": i['passport_number'],
                                           "date_of_birth": i['date_of_birth'], "email": i['email'],
                                           "ticket_type": i['ticket_type']}
                    return Response("Reservation Details:" + jsonify(reservation_details) + "\n\nDeparture Airport: " +
                                    str(reservation_details['from_airport']) + "\nFinal Destination Airport: " +
                                    str(reservation_details['to_airport']) + "\nConducting Date: " +
                                    str(reservation_details['conducting_date']) + "\nName: " +
                                    str(reservation_details['name']) + "\nSir Name: " +
                                    str(reservation_details['sirname']) + "\nPassport Number: " +
                                    str(reservation_details['passport_number']) + "\nDate of Birth: " +
                                    str(reservation_details['date_of_birth']) + "\nE-mail: " +
                                    str(reservation_details['email']) + "\nTicket Type: " +
                                    str(reservation_details['ticket_type']), status=200, mimetype='application/json')
                else:
                    return Response("No valid flight with this id", status=500, mimetype='application/json')
            else:
                return Response("No valid reservation with this id", status=500, mimetype='application/json')
        else:
            return Response("Rogue User!", status=401, mimetype='application/json')


# Cancel Reservation
@app.route('/cancel_reservation/<id>', methods=['DELETE'])
def cancel_reservation(id):
    userID = request.headers.get('authorization')

    if id == None:
        return Response("Bad Request", status=500, mimetype='application/json')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')
    else:
        if userID in live_sessions['admin'] or userID in live_sessions['simple']:
            if reservations.find({"_id": str(id)}).count() == 1:
                i = reservations.find_one({"_id": str(id)})
                flightID = i['flight_id']
                if flights.find({"_id": str(flightID)}).count() == 1:
                    my_flight = flights.find_one({"_id": str(flightID)})
                    if i['ticket_type'] == "business":
                        flights.update_one({"_id": str(flightID)}, {
                            '$set': {"ticket_num": {"business": int(my_flight['ticket_num']['business']) + 1}}})
                    elif i['ticket_type'] == "economy":
                        flights.update_one({"_id": str(flightID)}, {
                            '$set': {"ticket_num": {"economy": int(my_flight['ticket_num']['economy']) + 1}}})
                    else:
                        Response("Invalid ticket type", status=500, mimetype='application/json')
                    for j, res in enumerate(reservations):
                        if res['_id'] == id:
                            del res[j]
                    return Response("Reservation Cancelled", status=200,
                                    mimetype='application/json')
                else:
                    return Response("No valid flight with this id", status=500, mimetype='application/json')
            else:
                return Response("No valid reservation with this id", status=500, mimetype='application/json')
        else:
            return Response("Rogue User!", status=401, mimetype='application/json')


# Administrator Function: Make Flight
@app.route('/make_flight', methods=['POST'])
def make_flight():
    userID = request.headers.get('authorization')
    data = None

    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON Content", status=500, mimetype='application/json')

    if data == None:
        return Response("Bad Request", status=500, mimetype='application/json')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')

    if not "from_airport" in data or not "to_airport" in data or not "conducting_date" in data or \
            not "ticket_num" in data or not "ticket_price" in data or not "business" in data['ticket_num'] or \
            not "economy" in data['ticket_num'] or not "business" in data['ticket_price'] or \
            not "economy" in data['ticket_price']:
        return Response("Information Incomplete", status=500, mimetype="application/json")

    if userID in live_sessions['admin']:
        new_flight = {"from_airport": data['from_airport'], "to_airport": data['to_airport'],
                      "conducting_date": data['conducting_date'], "ticket_num": data['ticket_num'],
                      "ticket_price": data['ticket_price']}
        flights.insert_one(new_flight)
        return Response("Flight was made", status=200, mimetype='application/json')
    elif userID in live_sessions['simple']:
        return Response("Simple Users don't have the authority to use this function.",
                        status=401, mimetype='application/json')
    else:
        return Response("Rogue User!", status=401, mimetype='application/json')


# Administrator Function: Update Flight Ticket Price
@app.route('/update_price', methods=['PATCH'])
def update_price():
    userID = request.headers.get('authorization')
    data = None

    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("Bad JSON Content", status=500, mimetype='application/json')

    if data == None:
        return Response("Bad Request", status=500, mimetype='application/json')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')

    if userID in live_sessions['admin']:
        if "business_price" in data and "economy_price" in data:
            flights.update_many({}, {"and": [{"$set": {"ticket_price": {"business": data['business_price']}}},
                                             {"$set": {"ticket_price": {"economy": data['economy_price']}}}]})
        elif "business_price" in data:
            flights.update_many({}, {"$set": {"ticket_price": {"business": data['business_price']}}})
        elif "economy_price" in data:
            flights.update_many({}, {"$set": {"ticket_price": {"economy": data['economy_price']}}})
        else:
            return Response("Information Incomplete", status=500, mimetype="application/json")
    elif userID in live_sessions['simple']:
        return Response("Simple Users don't have the authority to use this function.",
                        status=401, mimetype='application/json')
    else:
        return Response("Rogue User!", status=401, mimetype='application/json')


# Administrator Function: Delete Flight
@app.route('/delete_flight/<id>', methods=['DELETE'])
def delete_flight(id):
    userID = request.headers.get('authorization')

    if id == None:
        return Response("Bad Request", status=500, mimetype='application/json')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')
    else:
        if userID in live_sessions['admin']:
            if flights.find({"_id": str(id)}).count() == 1:
                if reservations.find({"flight_id": str(id)}).count() > 0:
                    Response("Reservation for this flight exists.", status=500, mimetype='application/json')
                else:
                    for j, fl in enumerate(flights):
                        if fl['_id'] == id:
                            del fl[j]
                    return Response("Flight Deleted", status=200, mimetype='application/json')
            else:
                return Response("No valid flight with this id", status=500, mimetype='application/json')
        elif userID in live_sessions['simple']:
            return Response("Simple Users don't have the authority to use this function.",
                            status=401, mimetype='application/json')
        else:
            return Response("Rogue User!", status=401, mimetype='application/json')


# Administrator Function: Display Flight Details
@app.route('/display_flight/<id>', methods=['GET'])
def display_flight(id):
    userID = request.headers.get('authorization')

    if id == None:
        return Response("Bad Request", status=500, mimetype='application/json')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')
    else:
        if userID in live_sessions['admin']:
            if flights.find({"_id": str(id)}).count() == 1:
                i = flights.find_one({"_id": (id)})
                reserved_tickets_bis = reservations.find({"$and": [{"flight_id": str(id)},
                                                                   {"ticket_type": "business"}]}).count()
                reserved_tickets_eco = reservations.find({"$and": [{"flight_id": str(id)},
                                                                   {"ticket_type": "economy"}]}).count()
                total_tickets_bis = int(i['ticket_num']['business']) + reserved_tickets_bis
                total_tickets_eco = int(i['ticket_num']['economy']) + reserved_tickets_eco
                total_tickets_all = total_tickets_bis + total_tickets_eco
                my_reservations = reservations.find({"flight_id": str(id)})
                res_list = []
                for r in my_reservations:
                    res = {"name": r['name'], "sirname": r['sirname'], "ticket_type": r['ticket_type']}
                    res_list.append(res)
                return Response("Departure Airport: " + str(i['from_airport']) + "\nFinal Destination Airport: " +
                                str(i['to_airport']) + "\nTotal Number of All Tickets:" + str(total_tickets_all) +
                                "\n\tTotal Number of Business Tickets: " + str(total_tickets_bis) +
                                "\n\tTotal Number of Economy Tickets: " + str(total_tickets_eco) +
                                "\nTicket Price: \n\tBusiness Tickets Price: " + str(i['ticket_price']['business']) +
                                "\n\tEconomy Tickets Price: " + str(i['ticket_price']['economy']) +
                                "\nAvailable Number of Tickets: " + str(int(i['ticket_num']['business']) +
                                int(i['ticket_num']['economy'])) + "\n\tAvailable Number of Business Tickets: " +
                                str(i['ticket_num']['business']) + "\n\tAvailable Number of Economy Tickets: " +
                                str(i['ticket_num']['economy']) + "\n\nList of Reservation Details:\n" + jsonify(res_list),
                                status=200, mimetype='application/json')
            else:
                return Response("No valid flight with this id", status=500, mimetype='application/json')
        elif userID in live_sessions['simple']:
            return Response("Simple Users don't have the authority to use this function.",
                            status=401, mimetype='application/json')
        else:
            return Response("Rogue User!", status=401, mimetype='application/json')


# User Log-out
@app.route('/log_out', methods=['DELETE'])
def log_out():
    userID = request.headers.get('authorization')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')
    else:
        if userID in live_sessions['admin']:
            del live_sessions['admin'][userID]
            return Response("Administrator Logged-Out", status=200, mimetype='application/json')
        elif userID in live_sessions['simple']:
            del live_sessions['simple'][userID]
            return Response("Simple User Logged-Out", status=200, mimetype='application/json')
        else:
            return Response("Rogue User!", status=401, mimetype='application/json')


# User Delete Account
@app.route('/delete_account', methods=['DELETE'])
def delete_account():
    userID = request.headers.get('authorization')

    if userID == None:
        return Response("Bad Header Request", status=500, mimetype='application/json')
    else:
        if userID in live_sessions['admin']:
            user_email = live_sessions['admin'][userID]
            del live_sessions['admin'][userID]
            users.delete_one({'email': user_email})
            return Response("Administrator Account Logged-Out and Deleted", status=200, mimetype='application/json')
        elif userID in live_sessions['simple']:
            user_email = live_sessions['simple'][userID]
            del live_sessions['simple'][userID]
            users.delete_one({'email': user_email})
            return Response("Simple User Account Logged-Out and Deleted", status=200, mimetype='application/json')
        else:
            return Response("Rogue User!", status=401, mimetype='application/json')


# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


# Testing was done with the help of test_api.py (changed accordingly for the purposes of the Project) from GitHub.
# The project is uploaded on GitHub, in a private repository.
