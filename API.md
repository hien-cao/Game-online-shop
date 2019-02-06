# APIs

## Developer API

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
