# APIs

## Developer API

**NOTE:** Only GET methods are allowed and all responses are JSON.

Version: 1

```http
GET /api/v1/<endpoint>/
Content-Type: application/json
Accept: application/json
X-DEV-API-KEY: <your-api-key>
```

| description                          | endpoint                   | method | arguments    |
| ------------------------------------ | -------------------------- | ------ | ------------ |
| Basic details for all your games     | /games/                    | GET    | -            |
| In-depth details of a single game    | /games/:game_id/           | GET    | game_id: int |
| Statistics of a single game          | /game-statistics/:game_id/ | GET    | game_id: int |
| Reviews you have submitted           | /my-reviews/               | GET    | -            |
| Reviews submitted for all your games | /game-reviews/             | GET    | -            |
| Reviews submitted for a single game  | /game-reviews/:game_id/    | GET    | game_id: int |

### Responses

Failed request example:

```http
  HTTP/1.1 403 Forbidden
  Date: Wed, 06 Feb 2019 13:36:46 GMT
  Server: gunicorn/19.9.0
  Content-Type: application/json
  X-Frame-Options: SAMEORIGIN
  Content-Length: 31

  {
    "message": "Invalid request."
  }
```

Successful request example:

```http
  HTTP/1.1 200 OK
  Date: Wed, 06 Feb 2019 13:36:46 GMT
  Server: gunicorn/19.9.0
  Content-Type: application/json
  X-Frame-Options: SAMEORIGIN
  Content-Length: 102

  {
    "content": [
      {
        "id": 1,
        "name": "Baz Lightyear!",
        "price": "0.01"
      }
    ],
    "count": 1,
    "message": "Success!"
  }
```
