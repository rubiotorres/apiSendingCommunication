<h1 align="center">
   Django Api schedule - Basic API for scheduling messages
</h1>

<p align="center">
  <a href="#page_with_curl-sobre">About</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#scroll-decisões-de-projeto">Project Decisions</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#books-requisitos">Requirements</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#gear-instalação-de-requisitos">Instalação</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
</p>

## :page_with_curl: About
This repository contains an automation environment, written in python, being responsible for receiving message schedules and saving them in a database.

***Python***: The choice was made because it is a simple language and present on any platform. The JSON file contained in the project was chosen to make the project more independent, being able to modify the note at any time.

***Django***: The Django framework was chosen for its robustness, security and scalability when building an api..

***Folder Structure***: The choice for this folder structure was mainly due to the scalability of the system! Trying to modularize the system so that in the future it can integrate more services.

## :scroll: Project Decisions

This project is built on Docker containers using an image that already has python, to facilitate the use of some dependencies.

***The project***: The use of a RESTFULL api working with HTTP requests was chosen to have greater cross-platform accessibility, in order to be able to receive requests from anywhere that can send http requests.


## :books: Requirements
- Have [**Git**](https://git-scm.com/) to clone the project.
- Have [**Docker**](https://www.docker.com/) installed.

## Environment creation

The target host needs a database named schedule;

For this you can create in any interface or via the command line:

```
create database schedule CHARACTER SET utf8mb4;
```
It is important to remember the need for a user with access to create tables in this database. If not, it is necessary to create this user:

```
CREATE USER 'user'@'localhost' IDENTIFIED BY 'senha';
GRANT ALL ON schedule.* TO 'user'@'localhost';
```

## :gear: Installation requirements
``` bash
   # Clone the project:
   $ git clone https://github.com/rubiotorres/apiSendingCommunication.git
   
   #Create initial SuperUser to manager others users
   python manage.py createsuperuser

   # Replace on `api/settings.py` with a valid host and database, if you want run on docker with localhost use `host.docker.internal` as host
   "database": {
         'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
   }

   # Run the Docker found at the root of the repository:
   $ docker-compose up --build
  },

```
At the end you will have a service running in backgroud.

## How to authenticate
To authenticate you must first do the step of creating the first user by migrate.
This way you should navigate to and the folder 'apiSendingCommunication/src' and execute the command:

```
#Create initial SuperUser to manager others users
python manage.py createsuperuser
```
This first user is the first system administrator, with him it is possible to enter the url below to add other users who will have different access, depending on the administrator's choice.

```
http://127.0.0.1:8000/admin/
```
In this interface it is possible to browse with the administrator user, create groups, users and rules for the use of the api.

## How to use

It is important to remember that all routes are browser-friendly and can be used directly from the browser if you type using url.

The api has five endpoints:

### GET: /scheduling/status/id/<id> 
This endpoint is authentication-free and returns message status to whoever has the ID number.

The decision to leave it authentication free was to make it easier for those who already have the ID.

To use it we must use a GET request for the url example:

```
curl --location --request GET 'http://localhost:8000/scheduling/status/<id>'
```

### GET: /scheduling/search/
This endpoint is authenticated via token and returns the status of all registered messages.

The decision to create it is for an administrator to have greater visualization of the data. It has been kept with authentication so that outsiders cannot access all messages.

To use it we must use a GET request for the url:

```
curl --location --request GET 'http://localhost:8000/scheduling/search/<id>' \
--header 'Authorization: Token <token>'
```
### POST: /scheduling/create/

This endpoint is authentication free and schedules the message.

The decision to leave authentication free was to facilitate message creation.

The endpoint expects a JSON in its body like:

```
{
   "sender": "<sender>",
   "date_send": "yyyy-mm-ddThh:mm:ssZ",
   "receiver": "<receiver>",
   "message": "<message>"
}
```

To use it, we must use a POST request for the url example:

```
curl --location --request POST 'http://localhost:8000/scheduling/create/' \
--header 'Content-Type: application/json' \
--data-raw '{
   "sender": "<sender>",
   "date_send": "yyyy-mm-ddThh:mm:ssZ",
   "receiver": "<receiver>",
   "message": "<message>"
}'
```

### POST: /scheduling/api-token-auth/

This endpoint is authentication free and returns the authentication token.

The decision to leave authentication is due to the fact that it returns the token to authenticate.

The endpoint expects a JSON in its body like:

```
{
    "username":"<user>",
    "password": "<pwd>"
}
```

To use it, we must use a POST request for the url example:

```
curl --location --request POST 'http://localhost:8000/scheduling/api-token-auth/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"<user>",
    "password": "<pwd>"
}'
```

Remembering that to use this one, the user must be registered as shown in previous topics.

## DELETE: /scheduling/delete/

This endpoint is authenticated via token and deletes scheduled messages.

The decision to keep it protected by authentication is so that it cannot be deleted by anyone.

To use it, we must use a DELETE request for the url:

```
curl --location --request DELETE 'http://localhost:8000/scheduling/delete/<id>' \
--header 'Authorization: Token <token>'
```

## Tests

This API has some unit tests implemented in order to assess possible problems.

To run this test you must navigate to the folder 'apiSendingCommunication/src' where you can run the command below:

```
python manage.py test
```
<h1></h1>

<p align="center">Rubio Viana</p>
