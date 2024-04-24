#Import Dependencies
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
import os

#define application and database variables
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app_version = "v1/"

# data and handling imports
from functions import fetch_data_from_api, FixWholeState
from urls import api_url_cov, api_url_med, api_url_zip

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
    print("\033[92m {}\033[00m" .format("Database created..."))


# PRE-FILL relevant data in db

# Zipcode Data
zip_db_data = ZipModel.query.all()
if len(zip_db_data) < 1:
    print("\033[93m {}\033[00m" .format("Parsing Zipcode data for DB, this won\'t take long..."))
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

# Covid Data
cov_db_data = CovidModel.query.all()
if len(cov_db_data) < 1:
    cov_data = fetch_data_from_api(api_url_cov)

    print("\033[93m {}\033[00m" .format("Parsing Covid data for DB, this may take a couple minutes..."))

    for i in cov_data:
        # Check to see if the state is in the functions file
        if FixWholeState(i['Bene_Geo_Desc']) != "NO STATE":
            # Checking to see if there is a state already in the db
            inst = CovidModel.query.filter_by(state = FixWholeState(i['Bene_Geo_Desc'])).first()
            if inst:
                try: 
                    inst.hospitalizations += int(i['Total_Hosp'])
                    db.session.commit()
                except:
                    pass
            else:
                new_cov_obj = CovidModel(state = FixWholeState(i['Bene_Geo_Desc']), hospitalizations = i['Total_Hosp'])
                db.session.add(new_cov_obj)
                db.session.commit()
    
    print("\033[92m {}\033[00m" .format("Finished inserting Covid data"))

# Medicare Data
med_db_data = MedicareModel.query.all()
if len(med_db_data) < 1:
    med_data = fetch_data_from_api(api_url_med)

    print("\033[93m {}\033[00m" .format("Parsing Medicare data for DB, this may take a couple minutes..."))
    for i in med_data:
        inst = MedicareModel.query.filter_by(state = i['BENE_STATE_ABRVTN']).first()
        if inst:
            try:
                inst.totalEnrollments += int(i['TOT_BENES'])
                db.session.commit()
            except:
                pass
        else:
            new_med = MedicareModel(state = i['BENE_STATE_ABRVTN'], totalEnrollments = i['TOT_BENES'])
            db.session.add(new_med)
            db.session.commit()

    print("\033[92m {}\033[00m" .format("Finished inserting Medicare data"))


#handle the incoming data request with a parser
#arguments for a put request

####################
# Changed these to not required to handle message responses within the requests
####################
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("user", help="User pincode", required=False)
user_put_args.add_argument("state", help="User state", required=False)
user_put_args.add_argument("zip", help="User zipcode", required=False)

#arguments for an update request
user_update_args = reqparse.RequestParser()
user_update_args.add_argument("user", help="User pincode", required=False)
user_update_args.add_argument("state", help="User state", required=False)
user_update_args.add_argument("zip", help="User zipcode", required=False)

# arguments for a get request
user_get_args = reqparse.RequestParser()
user_get_args.add_argument("user", help="User pincode", required=True)

# REST classes for requests
class Covid(Resource):
    # GET (READ in CRUD)
    def get(self):
        result = CovidModel.query.all()
        if not result:
            abort(500, message="Could not find any covid information")

        covArray = []
        for i in result:
            covArray.append({'state': i.state, 'hospitalizations': i.hospitalizations})
        return covArray, 200

class Medicare(Resource):
    # GET (READ in CRUD)
    def get(self):
        result = MedicareModel.query.all()
        if not result:
            abort(500, message="Could not find any medicare information")

        medArray = []
        for i in result:
            medArray.append({'state': i.state, 'total_enrollments': i.totalEnrollments})
        return medArray, 200
    
class AllUsers(Resource):
    # GET (READ in CRUD)
    def get(self):
        result = UserModel.query.all()
        if not result:
            abort(500, message="Could not find any users")

        userArray = []
        for i in result:
            userArray.append({'pincode': i.user, 'state': i.state, 'zipcode': i.zip})
        return userArray, 200

class User(Resource):
    #GET (READ in CRUD)
    def get(self):
        args = user_get_args.parse_args()
        result = UserModel.query.filter_by(user=args['user']).first()
        if not result:
            abort(404, message="Could not find a user matching that pincode")
        
        userState = result.state
        covidInfo = CovidModel.query.filter_by(state = userState).first()
        medicareInfo = MedicareModel.query.filter_by(state = userState).first()
        zipInfo = ZipModel.query.filter_by(state = userState).all()

        if medicareInfo:
            med_info_checked = medicareInfo.totalEnrollments
            med_info_checked_zip = medicareInfo.totalEnrollments / len(zipInfo)
        else:
            med_info_checked = "No medicare information"
            med_info_checked_zip = "No medicare information"

        new_user_resp_obj = {
            'Zipcode': result.zip,
            'State': result.state,
            'Covid_Hospitalizations_state': covidInfo.hospitalizations,
            'Medicare_Enrollments_state': med_info_checked,
            'Avg_Covid_Hosp_Zip': covidInfo.hospitalizations / len(zipInfo),
            'Avg_Medicare_Enr_Zip': med_info_checked_zip
        }
        return new_user_resp_obj, 200 # ADD INFORMATION PARTAINING TO THE USER

    #PUT (CREATE in CRUD)
    def put(self):
        args = user_put_args.parse_args()
        if args['user'] and args['state'] and args['zip']:
            result = UserModel.query.filter_by(user=args['user']).first()
            if result:
                abort(409, message="Creation failed... That user pincode is already taken...")
            if len(args['state']) != 2:
                return "You must use a 2-character state", 400
            if len(args['zip']) != 5:
                return "You must use a 5-digit zipcode", 400
            if len(args['user']) > 30:
                return "That pincode is too long... Please try a shorter one..."
            else:
                newUser = UserModel(user=args['user'], state=args['state'], zip=args['zip'])
                db.session.add(newUser)
                db.session.commit()
            return "User " + args['user'] + " has been created...", 201
        else:
            return "Information is missing, please check your request...", 400
   
    #PUT (UPDATE in CRUD)
    def patch(self):
        args = user_update_args.parse_args()
        result = UserModel.query.filter_by(user=args['user']).first()
        if not result:
            abort(404, message="User doesn't exist, cannot update...")

        if args['state']:
            if len(args['state']) != 2:
                return "You must use a 2-character state", 400
            else:
                result.state = args['state']
        if args['zip']:
            if len(args['zip']) != 5:
                return "You must use a 5-digit zipcode", 400
            else:
                result.zip = args['zip']
        if not args['zip'] and not args['state']:
            abort(400, message="You must include either a state or a zip to update...")

        db.session.commit()

        return "User with the pincode: " + args['user'] + " has been updated...", 200
    
    #DELETE (DELETE in CRUD)
    def delete(self):
        args = user_update_args.parse_args()
        result = UserModel.query.filter_by(user=args['user']).first()
        if not result:
            abort(404, message="User with pincode " + args['user'] + " doesn't exist, cannot delete...")
        else:
            db.session.delete(result)
            db.session.commit()
            return "User " + args['user'] + " was deleted.", 200
        

#Register the Resource called video to the API (remember to change versions when making changes for submission)
api.add_resource(User, "/" + app_version + "user")
api.add_resource(AllUsers, "/" + app_version + "user/all")
api.add_resource(Medicare, "/" + app_version + "medicare")
api.add_resource(Covid, "/" + app_version + "covid")

#Run the API body
if __name__ == "__main__":
    app.run(debug=True)