from pymongo import MongoClient
from flask import Flask, request, jsonify, Response
from datetime import timedelta, datetime
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
        return Response("Information Incompleted", status=500, mimetype="application/json")

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


# Search Flights
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
                    return Response("No flights registered",
                                    status=500, mimetype='application/json')
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
            if flights.find({"_id": 'id'}).count() > 0:
                my_flights = flights.find({"_id": 'id'})
                flight_list = []
                for i in my_flights:
                    flight = {"_id": str(i['_id']), "conducting_date": i['conducting_date'],
                              "from_airport": i['from_airport'], "to_airport": i['to_airport'],
                              "ticket_num": {"buisness": i['ticket_num']['buisness'],
                                           "economy": i['ticket_num']['economy']},
                              "ticket_price": {"buisness": i['ticket_price']['buisness'],
                                             "economy": i['ticket_price']['economy']}}
                    flight_list.append(flight)
                return Response("Flights:" + jsonify(flight_list), status=200, mimetype='application/json')
            else:
                return Response("No flight with this id", status=500, mimetype='application/json')
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


# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


# Testing was done with the help of test_api.py (changed accordingly for the purposes of the Project) from GitHub.
# The project is uploaded on GitHub, in a private repository.
