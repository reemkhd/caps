# Casting Agency 

This project is the last step in Udacity Full Stack Developer Nanodegree and the first step in the fully developed web application. 
It's a web app for a casting agency where users can add movies, actors, and relate each actor to the movies he acted in, and vice versa. <br>
The backend follows PEP8 style guidelines, and there is no frontend to the app, you can use it by Postman or cURL. <br>
This project uses Python, flask, and Postgresql for its backend and hosted on Haruko.


## Installing Dependencies

### Python 3.7
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python0)

### Virtual Enviornment
as a tool to create isolated Python environments.<br>

I recommend working within a virtual environment whenever using Python for projects. This keeps dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for the platform can be found in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python0)

### PIP Dependencies
Install dependencies by run
```
pip3 install -r requirements.txt
```
This will install all of the required packages we selected within the requirements.txt file.

#### Key Dependencies
- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Development Setup
1- Download the project starter code locally
```
git clone https://github.com/reemkhd/capstone.git
cd capstone
```
2- Create an empty repository in your Github account online. To change the remote repository path in your local repository, use the commands below:
```
git remote -v 
git remote remove origin 
git remote add origin <https://github.com/<USERNAME>/<REPO_NAME>.git>
git branch -M master
```
Once you have finished editing your code, you can push the local repository to your Github account using the following commands.
```
git add . --all   
git commit -m "your comment"
git push -u origin master
```
3- Initialize and activate a virtualenv using:
```
python -m virtualenv env
source env/bin/activate
```
Note - In Windows, the env does not have a bin directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

4- Install the dependencies:
```
pip install -r requirements.txt
```
5- Running the server:<br>
To run the server, on mac & Linux execute:
```
export FLASK_APP=app.py
export FLASK_ENV=development
python3 app.py
```
On Windows:
```
set FLASK_APP=app.py
set FLASK_ENV=development
python3 app.py
```
Sourcing ```setup.sh``` sets some environment variables used by the app.<br>
Setting the ```FLASK_APP``` variable to ```app.py``` directs flask to use this file to find the application.<br>
Setting the ```FLASK_ENV``` variable to ```development``` will detect file changes and restart the server automatically.<br>

## API Reference
### Getting Started
- Base URL: You can run this API locally at the default [http://0.0.0.0:8080](http://0.0.0.0:8080/)
- Authentication: This app has 3 users. Each has his own token which are provided in setup.sh file. Details about each user privlages are provided below.

### Endpoints
- GET '/movies'
- GET '/actors'
- POST '/movies'
- POST '/actors'
- PATCH '/movies'
- PATCH '/actors'
- DELETE '/movies'
- DELETE '/actors'

#### GET '/movies'
- Fetch all movies info from db <br>
- Request Argument : None <br>
- Returns : JSON response containing all movies with their info, and request status <br>
- Run: 
```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:8080/movies
```
- The expected result:
```
{
    "movies": [
        {
            "actors": [
                "Tom"
            ],
            "id": 5,
            "name": "Blue eyes",
            "relase_date": "Tue, 09 Mar 2021 21:45:07 GMT"
        }
    ],
    "success": true
}
```

#### GET '/actors'
- Fetch all actors info from db <br>
- Request Argument : None <br>
- Returns : JSON response containing all actors with their info, and request status <br>
- Run: 
```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" http://localhost:8080/actors
```
- The expected result:
```
{
    "actors": [
        {
            "movies": [
                "My Ajusshi",
                "Blue eyes"
            ],
            "id": 1,
            "name": "Tom",
            "age": 21,
            "gendar": "male"
        }
    ],
    "success": true
}
```

#### POST '/movies'
- Insert movie info into db
- Request Argument : name, relase date, and actor ID
- Returns: JSON response containing the movie info that inserted, and request status
- Run:
```
curl -X POST -H  "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}" -d '{"name":"Go", "relase_date":"2021-03-09 21:45:07", "actor_id":5}' http://127.0.0.1:8080/movies
```
- The expected result:
```
{
    "movie": {
        "actors": [
            "Ahmad"
        ],
        "id": 5,
        "name": "Blue eyes",
        "relase_date": "Tue, 09 Mar 2021 21:45:07 GMT"
    },
    "success": true
}
```

#### POST '/actors'
- Insert actors info into db
- Request Argument : name, age, gendar, and movie ID
- Returns: JSON response containing the actor info that inserted, and request status
- Run:
```
curl -X POST -H  "Content-Type: application/json" -H "Authorization: Bearer {INSERT_TOKEN_HERE}"  -d '{"name":"Ahmad", "age":43, "gendar":"male", "movies"=2}' http://127.0.0.1:8080/actors
```
- The expected result:
```
{
    "actor": {
        "age": 12,
        "gendar": "male",
        "id": 3,
        "movies": [
            "Blue eyes"
        ],
        "name": "Ali"
    },
    "success": true
}
```

#### PATCH '/movies/int:id'
- Update movies info into db
- Request Argument : Movie ID, name, and relase date
- Returns: JSON response containing the movie info that updated, and request status
- example:
```
{
    "movie": {
        "id": 3,
        "name": "blue eyes",
        "relase_date": "Tue, 09 Mar 2004 21:45:07 GMT"
    },
    "success": true
}
```

#### PATCH '/actors/int:id'
- Update actors info into db
- Request Argument : Actor ID, name, and gendar
- Returns: JSON response containing the movie info that updated, and request status
- example:
```
{
    "actor": {
        "age": 40,
        "gendar": "female",
        "id": 3,
        "movies": [
            "Blue eyes"
        ],
        "name": "lolo"
    },
    "success": true
}
```

#### DELETE '/movies/int:id'
- delete movie from db
- Request Argument : Movie ID
- Returns: JSON response containing request status
- Run:

```
 {
   "success": true
 }
```

#### DELETE '/actors/int:id'
- delete actor from db
- Request Argument : Actor ID
- Returns: JSON response containing request status
- example:
```
 {
   "success": true
 }
```


## Users
This app has 3 users. Each has his own token which are provided in setup.sh file. 

#### Casting Assistant <br>
- Can view actors and movies <br>

#### Casting Director <br>
- All permissions a Casting Assistant has and… <br>
- Add or delete an actor from the database <br>
- Modify actors or movies <br>

#### Executive Producer <br>
- All permissions a Casting Director has and… <br>
- Add or delete a movie from the database <br>


## Testing
To run the tests, run
```
python test_app.py
```


## Deployment
This app is deployed on heruko under this [link](https://cap-reem.herokuapp.com/).
