# Famtube
* Application to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.
### Tech Used
* Django and DRF for creating api's and views.
* Celery, Celery Beat and Redis for asynchronous background task.
* Docker to containerize the application.
* Basic html, css to build dashboard.

## Key Features
* Fetch videos from youtube in each 60 second interval and store in Database.
* Get Api for paginated response of videos sorted in descending order of publish time.
* A search api to search from stored db. It's able to search videos containing partial match for the search query in either video title or description.
Ex 1: A video with title How to make tea? Match for the search query tea how.
* API to add new api keys(New API Keys will be automatically used once old expires).
* Dashboard to Get All videos in paginated list with sorting and filtering options. Search can be done by title, description or duration of video.

## Installation
 Copy secret keys from .env_template and create .env file in the same directory, Paste secret keys to it.
```
    $ cp .env_template .env
```
* Add a new api key to get videos using set_key post API. It takes api_key as body parameter for post API.
```
curl --location --request POST 'http://127.0.0.1:8000/famtube/set_key/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "api_key": "AIzaSyB4i0AHFn6P3yKG8q2MjxRV71Qqlil9eQw"
}'

```
*
```
    $ docker-compose build
    $ docker-compose up
```
- If celery beat don't start because of periodic task. Use the same command $ docker-compose up again. It works.
## API TESTING

#### GET http://127.0.0.1:8000/famtube/videos/
* It returns list of all fetched videos sorted in order of published date (i.e. latest published video appears first in the list and old is last in the list.). The response is paginated and will be giving only 5 videos list in a single page response.


#### GET http://127.0.0.1:8000/famtube/videos/?search=cricket
* It returns paginated list of videos based on query parameter. Matches searched keyword with Title and Description of the videos and returns the list of videos if even single word matches. 

#### POST http://127.0.0.1:8000/famtube/set_key/ 

* API Curl ->
```
curl --location --request POST 'http://127.0.0.1:8000/famtube/set_key/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "api_key": "AIzaSyB4i0AHFn6P3yKG8q2MjxRV71Qqlil9eQw"
}'
```
* It saves the API Key in DB for use in case if API KEY expired because of too many request. These api keys are fetched later when a api_key is expired. It takes api_key and saves it in DB.

#### http://127.0.0.1:8000/famtube/dashboard/ 
* Dashboard to list all the videos in a paginated dashboard. User can filter by title, description or duration. Duration filter returns all the videos which are smaller than entered length of the videos. On video click it redirects to youtube link of the particular video. 

![alt text](Famtube.png)

