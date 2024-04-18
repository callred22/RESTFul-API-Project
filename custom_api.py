#Import Dependencies
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

#define application and database variables
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app_version = "v1/"

#create the data definition
class ZipModel(db.model):
    id = db.Column(db.Integer, primary_key=True)
    zip = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)

class MedicareModel(db.model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    medicareAmount = db.Column(db.Integer, nullable=False)

class CovidModel(db.model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    hospitalizations = db.Column(db.Integer, nullable=False)

class UserModel(db.model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(100), nullable=False)



# class VideoModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     views = db.Column(db.Integer, nullable=False)
#     likes = db.Column(db.Integer, nullable=False)

#outputs to log/screen to verify data visually
def __repr__(self):
    return f"Info(avgMedicare = {avgMedicare}, avgCovidHosp = {avgCovidHosp}, state = {state})"
    # return f"Video(name = {name}, views = {views}, likes = {likes})"

#run this statement the first thme to create the database structure
#db.create_all()

#handle the incoming data request with a parser
#arguments for a put request
# video_put_args = reqparse.RequestParser()
# video_put_args.add_argument("name", type=str, help="Name of the video is required",required=True)
# video_put_args.add_argument("views", type=int, help="Views of the video",required=True)
# video_put_args.add_argument("likes", type=int, help="Likes on the video",required=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("user", help="User pincode", required=True)
user_put_args.add_argument("state", help="User state", required=True)
user_put_args.add_argument("zip", help="User zipcode", required=True)

#arguments for an update request
# video_update_args = reqparse.RequestParser()
# video_update_args.add_argument("name", type=str, help="Name of the video is required")
# video_update_args.add_argument("views", type=int, help="Views of the video")
# video_update_args.add_argument("likes", type=int, help="Likes on the video")

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("user", help="User pincode", required=True)
user_update_args.add_argument("state", help="User state", required=False)
user_update_args.add_argument("zip", help="User zipcode", required=False)

#Map the types to columns extracted from the database object
# resource_fields = {
#     'id': fields.Integer,
#     'name': fields.String,
#     'views': fields.Integer,
#     'likes': fields.Integer
# }

resource_fields = {
    'id': fields.Integer,
    'user': fields.String,
    'state': fields.String,
    'zip': fields.String
}


#Set up the Resource Functions for CRUD
# class Video(Resource):
#     #GET (READ in CRUD)
#     #@marshal_with serializes output from the DB as a dictionary (json object) so we can work with it in python
#     @marshal_with(resource_fields)
   
#     def get(self, video_id):
#         result = VideoModel.query.filter_by(id=video_id).first()
#         if not result:
#             abort(404, message="Could not find video with that id")
#         return result, 200

#     #POST (CREATE in CRUD)
#     @marshal_with(resource_fields)
#     def put(self, video_id):
#         args = video_put_args.parse_args()
#         result = VideoModel.query.filter_by(id=video_id).first()
#         if result:
#             abort(409, message="Video id taken...")
#         video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
#         db.session.add(video)
#         db.session.commit()
#         return video, 201
   
#     #PUT (UPDATE in CRUD)
#     @marshal_with(resource_fields)
#     def patch(self, video_id):
#         args = video_update_args.parse_args()
#         result = VideoModel.query.filter_by(id=video_id).first()
#         if not result:
#             abort(404, message="Video doesn't exist, cannot update")

#         if args['name']:
#             result.name = args['name']
#         if args['views']:
#             result.views = args['views']
#         if args['likes']:
#             result.likes = args['likes']

#         db.session.commit()

#         return result, 200

    #DELETE (DELETE in CRUD)
    #def delete(self, video_id):
        #abort_if_video_id_doesnt_exist(video_id)
        #del videos[video_id]
        #return '', 204

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