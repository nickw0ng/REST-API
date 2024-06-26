# Video REST API with Flask
This is a simple RESTful API built using Flask and Flask-RESTful for managing video data in a SQLite database.

## Prerequisites
To run this application locally, make sure you have Python 3.x installed on your system. Additionally, install the required Python packages using pip:
- Flask 
- Flask-RESTful 
- Flask-SQLAlchemy 

## API Endpoints

### GET /video/<int:video_id>
Returns information about a specific video identified by video_id.

### PUT /video/<int:video_id>
Creates a new video entry in the database with the provided video_id, name, views, and likes.

### PATCH /video/<int:video_id>
Updates an existing video entry identified by video_id. It accepts name, views, or likes parameters to update.

## Request Parameters
- name (required for PUT, optional for PATCH): Name of the video.
- views (required for PUT, optional for PATCH): Number of views of the video.
- likes (required for PUT, optional for PATCH): Number of likes on the video.

## Response
All responses are returned in JSON format and include the fields:

- id: Unique identifier of the video.
- name: Name of the video.
- views: Number of views of the video.
- likes: Number of likes on the video.

## Error Handling 
- 404 Not Found: Returned when attempting to access a video that does not exist.
- 409 Conflict: Returned when trying to create a video with an existing video_id.

## Dependencies
- Flask: Web framework for Python.
- Flask-RESTful: Extension for quickly building REST APIs with Flask.
- Flask-SQLAlchemy: Provides SQLAlchemy integration for Flask to work with SQL databases.
