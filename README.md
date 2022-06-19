# Famtube
* Application to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.
### Tech Used
* Django and DRF for creating api's and views.
* Celery, Celery Beat and Redis for asynchronous background task.
* Docker to containerize the application.
* Basic html, css to build dashboard.

## Key Features
* Fetch videos from youtube in each 30 second interval and store in Database.
* Get Api for paginated response of videos sorted in descending time of publish time.
* A search api to search api from stored db. It's able to search videos containing partial match for the search query in either video title or description.
Ex 1: A video with title How to make tea? Match for the search query tea how.
* API to add new api keys(New API Key will be automatically used once old expires).
* Dashboard to Get All videos in paginated list with search and filter features.

## Installation
* Copy secret keys from .env_template and create .env file in the same directory, Paste secret keys to it.
```
    $ docker-compose build
    $ docker-compose up
```

### API TESTING

* GET http://127.0.0.1:8000/famtube/videos/
- It returns list of all fetched videos sorted in order of published date (i.e. latest published video appears first in the list and old is last in the list.). The response is paginated and will be giving only 5 videos list in a single page response.


* GET http://127.0.0.1:8000/famtube/videos/?search=cricket
- It returns the list of videos based on query parameter. Matches searched keyword with Title and Description of the videos and returns the list of videos if even single word matches. Page is 

* POST http://127.0.0.1:8000/famtube/set_key/ 
```
body = {
    'api_key' : 'some_valid_api_key'
}
```
- It saves the API Key in DB for use in case if API KEY expired because of high request. It fetches the API_KEY from the db for use. It takes api_key and saves it in DB.

* http://127.0.0.1:8000/famtube/dashboard/ 
- Dashboard to list all the videos in a paginated dashboard. User can filter by title, description or duration. Duration filter returns all the videos which are smaller than entered length of the videos. On video click it redirects to youtube link of the particular video.


