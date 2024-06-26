from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Defining all the fields that we want to have in our video model
class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True) # unique identifier, different for each video
	name = db.Column(db.String(100), nullable=False) # can't be empty
	views = db.Column(db.Integer, nullable=False) # can't be empty
	likes = db.Column(db.Integer, nullable=False) # can't be empty

	# Gives a string representation 
	def __repr__(self):
		return f"Video(name = {name}, views = {views}, likes = {likes})"

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

# Allows the use to request any of these arguments in order to update a video
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

# 
resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

class Video(Resource):

	# Looks in the Model for a video with the video id
	# Returns if the video is found, and aborts with a error message if not found
	@marshal_with(resource_fields) # takes the return and serializes it using fields to be returned
	def get(self, video_id): 
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Could not find video with that id")
		return result

	# Makes a new object in the data base 
	# Aborts if the added video id already exists
	@marshal_with(resource_fields) # takes the return and serializes it using fields to be returned
	def put(self, video_id):
		args = video_put_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if result:
			abort(409, message="Video id taken...")

		video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
		db.session.add(video)
		db.session.commit() # Adds and commits objects to the database session 
		return video, 201

	# A way to update a specific video
	# Aborts if the video id does not exist
	@marshal_with(resource_fields) # takes the return and serializes it using fields to be returned
	def patch(self, video_id):
		args = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Video doesn't exist, cannot update")

		if args['name']:
			result.name = args['name']
		if args['views']:
			result.views = args['views']
		if args['likes']:
			result.likes = args['likes']

		db.session.commit() # commits the updated video
		return result

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
	app.run(debug=True)