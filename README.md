# YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios
# Digital Airlines Information System


# How to Execute:

- You can execute this project both in Windows and Linux. This guide will show the Windows Version.
- The Postman REST API Client Software was used to make the requests to the server, in the following example.

1. Git Bash to your desired directory and clone this repository there with the "git clone https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios" command.
2. Open a cmd or powershell window and "cd" with the write path, inside the "DigitalAirlinesFiles" directory.
3. Execute the command "docker-compose up -d" (May take a few seconds).
4. Make your Database:
    1. If you want to use the data that are provided in the JSON files (users, reservations, flights), then:
           - Execute the command "docker cp flask/data/users.json mongodb:/users.json && docker cp flask/data/flights.json mongodb:/flights.json && docker cp
           flask/data/reservations.json mongodb:/reservations.json"
           - Then, execute the command "docker exec -it mongodb mongoimport --db=DigitalAirlines --collection=Users --file=users.json && docker exec -it mongodb
           mongoimport --db=DigitalAirlines --collection=Flights --file=flights.json && docker exec -it mongodb mongoimport --db=DigitalAirlines --
           collection=Reservations --file=reservations.json"
       (If you have a Duplicate Key Error, it means some IDs from the JSON files have already been used. Change the IDs in the JSON files into valid, non-used
        ones, save changes and repeat step 4)
     2. If you want empty collections to add data to them yourself, then:
           - Delete all content from the JSON files and save your changes.
           - Execute the command "docker cp flask/data/users.json mongodb:/users.json && docker cp flask/data/flights.json mongodb:/flights.json && docker cp
           flask/data/reservations.json mongodb:/reservations.json"
           - Then, execute the command "docker exec -it mongodb mongoimport --db=DigitalAirlines --collection=Users --file=users.json && docker exec -it mongodb
           mongoimport --db=DigitalAirlines --collection=Flights --file=flights.json && docker exec -it mongodb mongoimport --db=DigitalAirlines --
           collection=Reservations --file=reservations.json"
6. (Optional / If you have no Admins) The Web Service doesn't provide a way to sing up Administrators. If you want to add Administrator Users, use the Mongo Shell:
   1. Execute the command "docker exec -it mongodb mongosh --port 27017" (Mongo Shell command prompt will open)
   2. Execute the command "use DigitalAirlines"
   3. Add your Administrator accounts to the Users collection. Example:
     - Execute: "db.Users.insertOne({"username":"Sotiris","sirname":"Dimitrakoulakos",
       "email":"sdimitrakoulakos@gmail.com","entr_password":"complicated_password123",
       "date_of_birth":[{"day":{"$numberInt":"19"},"month":"July","year":{"$numberInt":"2002"}}],
       "origin_country":"Greece","passport_number":{"$numberInt":"333333333"},"category":"administrator"})"
     - Execute: "db.Users.insertOne({"username":"Chrysostomos","sirname":"Symvoulidis",
       "email":"chrsym@gmail.com","entr_password":"complicated_password456",
       "date_of_birth":[{"day":{"$numberInt":"01"},"month":"January","year":{"$numberInt":"1999"}}],
       "origin_country":"Greece","passport_number":{"$numberInt":"444444444"},"category":"administrator"})"
     - Execute: "db.Users.insertOne({"username":"Jean-Didier","sirname":"Totow",
       "email":"jdtotow@gmail.com","entr_password":"complicated_password789",
       "date_of_birth":[{"day":{"$numberInt":"01"},"month":"January","year":{"$numberInt":"1999"}}],
       "origin_country":"Greece","passport_number":{"$numberInt":"555555555"},"category":"administrator"})"
     - [ Us 3 as Admins ;) ]
7. Make Requests and see Responses! The Postman Software was used in the following example.


# Analysis and Examples:

After adding ./data to the pyhton module serach path, we then connect to our local MongoDB (we get its hostname from localhost and we create a MongoClient).

*Internal Function create_session :
It is used in the log_in function. This function takes a given email and a boolean value role_admin as parameters. When it is called, it generates a uinque random id with uuid.uuid4, which is converted to a string. If role_admin is True (meaning a admin is logging in), then in the live_sessions dictionary, in the element with key "admin", an element is added with the unique id as its key and the email as its value. The correspoding squence (in the element with key "admin") happens if role_admin is False (meaning a simple user is logging in).
