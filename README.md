# Famtube
* API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## Key Features
* Fetch videos from youtube in each 30 second interval and store in Database.
* Get Api for paginated response of videos sorted in descending time of publish time.
* A search api to search api from stored db. It's able to search videos containing partial match for the search query in either video title or description.
Ex 1: A video with title How to make tea? Match for the search query tea how.
* API to add new api keys(New API Key will be automatically used once old expires).
* Dashboard to Get All videos in paginated list with search and filter features.

## Installation
```
    $ docker-compose --build
    $ docker-compose up
```

### API TESTING

* GET http://127.0.0.1:8000/famtube/videos/ ---> It returns list of all fetched videos sorted in order of published date.

* GET http://127.0.0.1:8000/famtube/videos/?search=cricket  ----> It returns the list of videos based on query parameter.

* POST http://127.0.0.1:8000/famtube/set_key/ ----> It saves the API Key in DB for later use. 

* http://127.0.0.1:8000/famtube/dashboard/ ----> Dashboard to see all videos along with filter and ordering feature.

