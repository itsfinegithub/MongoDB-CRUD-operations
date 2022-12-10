from collections import UserString
from flask import Flask,Response,json,request
from bson.objectid import ObjectId
from pymongo import MongoClient
app = Flask(__name__)

###############################################
# mongoDB Connection
try:
    mongo = MongoClient(
        host ="localhost",
        port = 27017,
        serverSelectionTimeoutMS =1000

    )
    db = mongo.juntran_tech
    mongo.server_info() # this is going to trigger the Exception if cannot connect to db...

except:
    print("ERROR - cannot connect to db")

##################################################
# READ
@app.route("/read", methods = ["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"]= str(user["_id"])
        return Response(
            response = json.dumps(data),
            status = 200,
            mimetype = "application/json"
        )

    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"cannot read users"}))
        

##################################################
#INSERT
@app.route('/insert', methods=['GET', 'POST'])
def create_user():
    try:
        employees = [
        {"name":"lakshmi","age":25,"company":"juntran","address":"Karnataka"},
        { "name": "Papu", "age":25,"company":"juntran","address":"Odisha"},
        { "name": "sanket", "age":25,"company":"juntran","address":"maharastra"},
        { "name": "naresh", "age":25,"company":"juntran","address":"andrapradesh"},
        { "name": "navin", "age":25,"company":"juntran","address":"andrapradesh"},
        { "name": "rahul", "age":25,"company":"juntran","address":"madyapradesh"}
        ]
 
        dbResponse = db.users.insert_many(employees)
        return Response(
            response= json.dumps({"message":"users created"}),# it  takes an json object and returns string
            status = 200,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)


########################################################
# UPDATE
@app.route("/patch/<id>", methods = ["GET"])
def update_user(id):
    try:
        user = {"name":"lakshmi"}
        newvalue = {"$set":{"name":"Sarya"}}
        dbResponse = db.users.update_one(user,newvalue)
        
        if dbResponse.modified_count == 1:
            return Response(
                response = json.dumps(
                    {"message":"user updated"}),
                status = 200,
                mimetype="application/json" 
            )
        else:
            return Response(
                response = json.dumps(
                    {"message":"nothing to update"}),
                status = 200,
                mimetype="application/json" 
            ) 

        
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps(
                {"message":"sorry cannot update user"}),
                status = 500,
                mimetype = "application/json"
            )
        
##########################################################
# DELETION
@app.route("/delete/<id>", methods = ["GET"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(
                response = json.dumps(
                    {"message":"user deleted", "id":f"{id}"}),
                    status = 500,
                    mimetype = "application/json"
            )
        else:
            return Response(
                response = json.dumps(
                    {"message":"user not found"}),
                status = 200,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps(
                {"message":"sorry cannot delete user"}),
                status = 500,
                mimetype = "application/json"
            )



if __name__ == "__main__":
    app.run(debug = True)