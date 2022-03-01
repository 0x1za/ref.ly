<h1 align="center">ref.ly 🔗</h1>
<p>
  <img alt="rf.ly: build" src="https://github.com/0x1za/ref.ly/actions/workflows/python-app.yml/badge.svg" />
  <img alt="Version" src="https://img.shields.io/badge/version-v1-blue.svg?cacheSeconds=2592000" />
  <a href="#" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <img alt="Imports: isort" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" />
</p>


> rf.ly is a referral & rewards management service for Amitree.

### Installation

Pull source code from this GitHub repository:

```sh
$ git clone git@github.com:0x1za/ref.ly.git
```

Create pipenv environment & install packages:

```sh
$ cd ref.ly/
$ pip install pipenv
$ pipenv install
```

Activate the virtual environment:

```sh
$ pipenv shell
```

### Database Initialization

This Flask application needs a SQLite database to store data. `Flask-Migrate` is used to manage database initialization and migrations

```
(rf.ly) $ flask db init
(rf.ly) $ flask db migrate -m "Initial migration."
(rf.ly) $ flask db upgrade
```


### Usage
Set the file that contains the Flask application and specify that the development environment should be used:

```sh
(venv) $ export FLASK_APP=app.py
(venv) $ export FLASK_ENV=development
```

```sh
FLASK_APP=refs.py FLASK_ENV=development flask run
```

### API Reference

**Create Referral**
```http
POST /v1/create/referral
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `invitee_email` | `string` | **Required**. User to be invited |
| `referer_email` | `string` | **Required**. Email of referer (person creating the referral.) |

**Create User**
```http
POST /v1/create/user
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `email` | `string` | **Required**. User email |
| `username` | `string` | **Required**. Unique username |
| `referral_code` | `string` | Referral code, *submit empty string if None* |

#### Responses

Many API endpoints return the JSON representation of the resources created or edited. However, if an invalid request is submitted, or some other error occurs, `rf.ly` returns a JSON response in the following format:

```javascript
{
  "message" : string,
  "success" : bool,
  "data"    : string
  "status"  : string
}
```

The `message` attribute contains a message commonly used to indicate errors or, in the case of deleting a resource, success that the resource was properly deleted.

The `success` attribute describes if the transaction was successful or not.

The `data` attribute contains any other metadata associated with the response. This will be an escaped string containing JSON data.

#### Status Codes

rf.ly returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |

### Author

👤 **Mwiza Simbeye**

* Github: [@0x1za](https://github.com/0x1za)

### 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/0x1za/ref.ly/issues).

### Show your support

Give a ⭐️ if this project helped you!
