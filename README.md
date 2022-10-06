## Books

Manager role jwt token - eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpDMTJFa1p2Nnl0azcySy1iLUgxTyJ9.eyJpc3MiOiJodHRwczovL2Rldi1ydTduaW04cS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMzZWQxZDNhMTI3NTJmZjQ4ZmNmOGNhIiwiYXVkIjoiaHR0cDovLzEyNy4wLjAuMTo1MDAwLyIsImlhdCI6MTY2NTA3MDI1OCwiZXhwIjoxNjY1MDc3NDU4LCJhenAiOiI1dEtkWWhObWRLUGRSMDNBWXNYV3dFdUpJUW83VEZ4byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmdlbnJlcyIsImdldDpib29rcyIsImdldDpib29rcy1kZXRhaWxzIiwiZ2V0OmdlbnJlcyIsInBvc3Q6Ym9va3MiLCJwb3N0OmdlbnJlcyJdfQ.Lc5t11SHlVJqfVFT_yqW6TDJT3qZSe54UY_1uUUpLErc3Lcd29OtzmizA7Fll4PtXsTgATiNsiyY_kQE5JPQk3aOoagqLULCGiQLmU7NmzR7C1t67a5xRJ59ulS_VozHlq8-ci7-_xSpGGsHsfmOVWT4k_6MPtH_CxtVfZspVJkD3NBIgvAer0BnxxDLC8maSxoV8jurBdkjtKW9r44MCNcj161QiXWOIqDfJakoNWlROK-Y0d5h4IG3sPvTC7bPzCzjV7q02-37bHy_jrGo0Yyi8l2RwkVbZnCvicXT5i_DwEbz6bpss6vTLAI275dYsi3zcQqVlrZRFsR2-n4_yA

## Introduction

This repository contains endpoints with authorization and RBAC implemented for a books data store.
The DB contails two tables, one for Books (id, name, description, genre) and the second is the list of genres. They follow a many to one relation in the Data Model
### NOTE - THE DATA FOR THE TWO TABLES HAVE BEEN PROVIDE IN .csv book_table and genre_table, Please make copy in db first, you can use DB GUIs

## Installing Dependencies

Python 3.7
Follow instructions to install the latest version of python for your platform in the python docs.

### Virtual Enviornment

Recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs.

### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

pip install -r requirements.txt
This will install all of the required packages.

## Server setup

ENV variables

```
export DATABASE_URL=<database-connection-url>
export FLASK_APP=app.py
flask run --reload
```

## API Reference

Authentication: This application requires authentication to perform various actions. All the endpoints require different permissions.

The application has two role -

- Manager -the manager has all the permissions
  - get:genres - Permission to get all the genres available
  - get:books - Permission to get all the available books
  - get:books-details - To fetch any one book's details with a given id
  - delete:genres - To Delete the book with the provided id
  - post:genres - Add a new genre in the table
  - post:books - Add a new book in the table
- User -The use only has the permissions to fetch data
  - get:genres - Permission to get all the genres available
  - get:books - Permission to get all the available books
  - get:books-details - To fetch any one book's details with a given id

## Error handling

Errors are Returned in a well formatter JSON

```
{
    "error": 404,
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
    "success": false
}
```

Handled errors -

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 405: Method Not Allowed
- 422: Unprocessable Entity
- 500: Internal Server Error

## Endpoints

`GET '/'`

- This endpoint is the callback endpoint for the auth0 login success
- Request Arguments: None
- Returns -

```
"Hi, Welcome!
```

`GET '/api/v1.0/login'`

- Request Arguments: None
- Returns: Redirect you to the auth0 sign in page

`GET '/api/v1.0/genres'`

- This endpoint needs a user with get:genres permission to fetch all the genres
- Request Arguments: None
- Returns -

```json
{
    "success": "True",
    "Genre": [formatted_genres],
    "total_Genres": 10
}
```

`DELETE '/api/v1.0/genres/<int:id>'`

- This endpoint needs a user with delete:genres permission to delete a genre with id = id
- Request Arguments: None (only in the URL the id is passed)
- Returns -

```json
{
    "success": "True",
    "deleted": "<id>"
}
```

`GET '/api/v1.0/books'`

- API endpoint to fetch all books from db,only user with get:books permission can access it 
- Request Arguments: None 
- Returns -

```json
{
    "success": "True",
    "bookings": [formatted_genres],
    "total_bookings": 10
}
```


`GET '/api/v1.0/books/<int:id>'`

- API endpoint to fetch a book's detail from db with id = id Only user with get:books-details permission can access it 
- Request Arguments: None (Only in the url)
- Returns - 

```json
{
  "success": "True",
  "id": <id>,
  "book_name": "book.book_name",
  "Genre_id": "book.Genre_id",
  "book_description": "book.book_description"
}
```

### Postman collection can be found in the project folder as udacity-fsnd-udaspicelatte.postman_collection.json


