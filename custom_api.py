#Import Dependencies
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import os

# API URLS
api_url_med = "https://data.cms.gov/data-api/v1/dataset/d7fabe1e-d19b-4333-9eff-e80e0643f2fd/data"
api_url_zip = "https://raw.githubusercontent.com/millbj92/US-Zip-Codes-JSON/master/USCities.json"
api_url_cov = "https://data.cms.gov/data-api/v1/dataset/2684c3e2-3598-4997-a598-0991bad6fbf2/data"

# Fetch/Driver File
from driver import fetch_data_from_api

# Random Functions
from functions import FixWholeState

#define application and database variables
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app_version = "v1/"

#create the data definition
class ZipModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zip = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)

class MedicareModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    totalEnrollments = db.Column(db.Integer, nullable=False)

class CovidModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    hospitalizations = db.Column(db.Integer, nullable=False)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(100), nullable=False)

#outputs to log/screen to verify data visually
def __repr__(self):
    return f"Info(avgMedicare = {avgMedicare}, avgCovidHosp = {avgCovidHosp}, state = {state})"

# CHECKS to see if there is a db, if there is not it creates one
if os.path.isfile('./database.db'):
    print("\033[92m {}\033[00m" .format("Database connected..."))
    pass
elif not os.path.isfile('./database.db'):
    print("\033[93m {}\033[00m" .format("Database not found... creating..."))
    db.create_all()


# PRE-FILL relevant data in db

zip_db_data = ZipModel.query.all()
if len(zip_db_data) < 1:
    zip_data = fetch_data_from_api(api_url_zip)

    # Zipcode array to be saved to db
    new_zips = []
    for i in zip_data:
        if i['zip_code'] < 1000:
            raw_zip = "00" + str(i['zip_code'])
        elif i['zip_code'] < 10000:
            raw_zip = "0" + str(i['zip_code'])
        else:
            raw_zip = str(i['zip_code'])

        new_zip_obj = ZipModel(zip= raw_zip, state = i['state'])
        new_zips.append(new_zip_obj)
    
    db.session.add_all(new_zips)
    db.session.commit()
    print("\033[92m {}\033[00m" .format("Finished inserting zipcode data"))

cov_db_data = CovidModel.query.all()
if len(cov_db_data) < 1:
    cov_data = fetch_data_from_api(api_url_cov)

    # Zipcode array to be saved to db
    new_covs = []
    for i in cov_data:
        # Check to see if the state is in the functions file
        if FixWholeState(i['Bene_Geo_Desc']) != "NO STATE":
            new_cov_obj = CovidModel(state = FixWholeState(i['Bene_Geo_Desc']), hospitalizations = i['Total_Hosp'])
            new_covs.append(new_cov_obj)
    
    db.session.add_all(new_covs)
    db.session.commit()
    print("\033[92m {}\033[00m" .format("Finished inserting Covid data"))

med_db_data = MedicareModel.query.all()
if len(med_db_data) < 1:
    med_data = fetch_data_from_api(api_url_med)

    # Zipcode array to be saved to db
    new_meds = []
    for i in med_data:
        new_med = MedicareModel(state = i['BENE_STATE_ABRVTN'], totalEnrollments = i['TOT_BENES'])
        new_meds.append(new_med)
    
    db.session.add_all(new_meds)
    db.session.commit()
    print("\033[92m {}\033[00m" .format("Finished inserting Medicare data"))


#handle the incoming data request with a parser
#arguments for a put request

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("user", help="User pincode", required=True)
user_put_args.add_argument("state", help="User state", required=True)
user_put_args.add_argument("zip", help="User zipcode", required=True)

#arguments for an update request

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("user", help="User pincode", required=True)
user_update_args.add_argument("state", help="User state", required=False)
user_update_args.add_argument("zip", help="User zipcode", required=False)

resource_fields = {
    'id': fields.Integer,
    'user': fields.String,
    'state': fields.String,
    'zip': fields.String
}

class User(Resource):
    #GET (READ in CRUD)
    #@marshal_with serializes output from the DB as a dictionary (json object) so we can work with it in python
    @marshal_with(resource_fields)
   
    def get(self, user):
        result = UserModel.query.filter_by(user=user).first()
        if not result:
            abort(404, message="Could not find a user matching that pincode")
        return result, 200 # ADD INFORMATION PARTAINING TO THE USER

    #POST (CREATE in CRUD)
    @marshal_with(resource_fields)
    def put(self, user):
        args = user_put_args.parse_args()
        result = UserModel.query.filter_by(user=user).first()
        if result:
            abort(409, message="That user pincode is already taken...")

        newUser = UserModel(user=user, state=args['state'], zip=args['zip'])
        db.session.add(newUser)
        db.session.commit()
        return newUser, 201
   
    #PUT (UPDATE in CRUD)
    @marshal_with(resource_fields)
    def patch(self, user):
        args = user_update_args.parse_args()
        result = UserModel.query.filter_by(user=user).first()
        if not result:
            abort(404, message="User doesn't exist, cannot update...")

        if args['state']:
            result.state = args['state']
        if args['zip']:
            result.zip = args['zip']
        if not args['zip'] and not args['state']:
            abort(500, message="Server error: You must include either a state or a zip to update...")

        db.session.commit()

        return result, 200
    
    #DELETE (DELETE in CRUD)
    def delete(self, user):
        result = UserModel.query.filter_by(user=user).first()
        if not result:
            abort(404, message="User doesn't exist, cannot delete...")
        else:
            db.session.delete(result)
            db.session.commit()
            return "User " + result.user + " was deleted.", 200
        

#Register the Resource called video to the API (remember to change versions when making changes for submission)
api.add_resource(User, "/" + app_version + "user/<int:user>")

#Run the API body
if __name__ == "__main__":
    app.run(debug=True)