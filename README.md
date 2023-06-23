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
           1. Execute the command "docker cp flask/data/users.json mongodb:/users.json && docker cp flask/data/flights.json mongodb:/flights.json && docker cp
           flask/data/reservations.json mongodb:/reservations.json"
           2. Then, execute the command "docker exec -it mongodb mongoimport --db=DigitalAirlines --collection=Users --file=users.json && docker exec -it mongodb
           mongoimport --db=DigitalAirlines --collection=Flights --file=flights.json && docker exec -it mongodb mongoimport --db=DigitalAirlines --
           collection=Reservations --file=reservations.json"
       (If you have a Duplicate Key Error, it means some IDs from the JSON files have already been used. Change the IDs in the JSON files into valid, non-used
        ones, save changes and repeat step 4)
     2. If you want empty collections to add data to them yourself, then:
           1. Delete all content from the JSON files and save your changes.
           2. Execute the command "docker cp flask/data/users.json mongodb:/users.json && docker cp flask/data/flights.json mongodb:/flights.json && docker cp
           flask/data/reservations.json mongodb:/reservations.json"
           3. Then, execute the command "docker exec -it mongodb mongoimport --db=DigitalAirlines --collection=Users --file=users.json && docker exec -it mongodb
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

After adding ./data to the pyhton module serach path, we then connect to our local MongoDB (we get its hostname from localhost and we create a MongoClient). Then we choose the DigitalAirlines database and initiate Flask App.

*Internal Function create_session :
It is used in the log_in function. This function takes a given email and a boolean value role_admin as parameters. When it is called, it generates a uinque random id with uuid.uuid4, which is converted to a string. If role_admin is True (meaning a admin is logging in), then in the live_sessions dictionary, in the element with key "admin", an element is added with the unique id as its key and the email as its value. The correspoding squence (in the element with key "admin") happens if role_admin is False (meaning a simple user is logging in).

1. sign_up (for Simple Users and Administrators):

   ![sign_up1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/ae1c523f-9590-48db-84dc-20c857173109)


2. log_in (for Simple Users and Administrators):

   ![log_in1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/d304a03e-aebe-4ed9-a264-5e1a67f8cd03)

   To keep showing logged-in as this user, from now on we will put this User-Session ID in a user-ID header with this id as is value, before we send the request.
   ![headers](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/97e9fcf6-e4d3-4db4-a27a-4ce3e8a9efd0)

   
3. search_flights (for Simple Users and Administrators):

    ![search_flights1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/385c8269-42b5-4c1e-8f0c-1d0b071890f7)
   
    ![search_flights2](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/556637d6-4cd6-4f8f-932a-c72ad8b71880)


4. show_flight (for Simple Users and Administrators):

   ![show_flight1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/20c7a73a-ae13-45ec-8a5a-5a248f66cbe5)


5. make_reservation (for Simple Users and Administrators):

    ![make_res1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/2fe84972-27b5-468d-b3db-9759db1c6da9)

   ![make_res2](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/642cd660-284a-43e3-88a9-5ce9e11c4e6b)


6. show_my_reservations (for Simple Users and Administrators):

    ![show_my_res1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/132d9794-ded9-41d9-bd6f-84aa951ad549)


7. show_reservation (for Simple Users and Administrators):

    ![show_res1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/c2098f8a-1dd3-415e-acce-360bde5b06fd)


8. cancel_reservation (for Simple Users and Administrators):

    ![cancel_res1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/2644280f-37bf-4f1d-9729-486923e25802)

    ![cancel_res2](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/e94e1a27-f1b0-4dcd-8587-9112a5571aa2)

*If simple user tries to execute an Administrator only function:

![simple_users_admin_func](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/f14edb7c-09d0-4382-a6b4-0a40ffde9346)

*So we log-in as an Administrator:

![admin_login](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/0305f1ad-a2b1-434e-b5a7-1d7d952b7a17)


9. make_flight (for Administrators):

    ![make_flight1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/171b34e5-0777-443b-b1dd-e4a383244158)

    ![make_flight2](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/73159b57-5be7-4a37-b357-2b156a181455)


10. update_price (for Administrators):

    ![update_price1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/70b3a2e7-6191-437e-bd24-dae6b8e8ae3a)

    ![update_price2](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/46a4c32b-6d1e-47e6-8d33-5e554e3b659c)


11. delete_flight (for Administrators):

    ![delete_flight1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/cb35e4a9-53c7-4ea8-8600-d8bf52045f32)

    ![delete_flight2](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/51f70109-4432-41f2-8ca1-df94cd570137)


12. display_flight (for Administrators):

    ![diplay_flight1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/0deb45ec-872d-446f-bb06-c609918d4c4f)


13. log_out (for Simple Users and Administrators):

    ![log_out1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/185c151c-a0f5-4476-bc3d-3daf4ed39e4f)

    ![log_out2](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/cc1c1233-97cd-4bf4-a220-230938325f8a)

    ![log_out3](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/951063ad-5a2e-4b48-a3b9-d78c68aa960e)


14. delete_account (for Simple Users and Administrators):

    ![delete_account1](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/cac93be5-18ef-4b0e-b47e-bed5f8612f8f)

    ![delete_account2](https://github.com/SotirisDimitrakoulakos/YpoxreotikiErgasia23_E20040_Dimitrakoulakos_Sotirios/assets/116378407/07c40370-9cd5-49e5-9264-d8d26497a0ce)


