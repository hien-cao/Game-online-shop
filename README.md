# wsd2018-project

CS-C3170 Course Project:
Online JavaScript game store; a Django application.

## Collaborators

* Juho Jokela - 718554
* Touko Hallasmaa - 718208
* Hien Cao - 716718

## TOC

- [wsd2018-project](#wsd2018-project)
  - [Collaborators](#collaborators)
  - [TOC](#toc)
  - [Project description](#project-description)
    - [Core features](#core-features)
      - [Authentication](#authentication)
      - [Purchasing Games](#purchasing-games)
      - [Playing Games](#playing-games)
      - [Searching Games](#searching-games)
      - [Adding Game](#adding-game)
      - [Statistics](#statistics)
      - [Updating a game](#updating-a-game)
      - [Saving/Loading](#savingloading)
      - [Third-Party Login / Logout](#third-party-login--logout)
    - [Extra](#extra)
      - [Tests](#tests)
      - [Reviews](#reviews)
      - [REST API](#rest-api)
      - [Highscores](#highscores)
  - [API](#api)
    - [Models](#models)
      - [Profile](#profile)
      - [Game](#game)
      - [Purchase](#purchase)
      - [Save](#save)
      - [Highscore](#highscore)
      - [Review](#review)
      - [Tag](#tag)
    - [Paths and views](#paths-and-views)
      - [Core](#core)
      - [Profile views and paths](#profile-views-and-paths)
      - [Game views and paths](#game-views-and-paths)
      - [Review view and paths](#review-view-and-paths)
      - [REST API](#rest-api-1)
  - [Management, collaboration and contributing to project](#management-collaboration-and-contributing-to-project)
    - [Order of work](#order-of-work)
    - [Timetable](#timetable)

## Project description

This repository contains the source-code for an online JavaScript game store. The project is developed during the span of Web Software Development (CS-C3170) -course and the project instruction can be found from https://plus.cs.hut.fi/wsd/2018.

A rough mockup of the visuals of the web application can be seen [here](https://app.moqups.com/juho.i.jokela@gmail.com/XX8tNXjSen/view).

The project is written in Python (3+) and it utilizes the Django framework. The authentication is provided by third-party Single-Sign-On (GitHub). In addition to this, we use Bootstrap for faster templating with columns. We use JavaScript (ES6) with Redom as UI library and Parcel for final compilation to ES5.

To ease the development and maintenance we have decided to split this project into five apps. These are:

* Core:
  * Common templates and resources
* Profile
  * Anything related to users
* Game
  * Anything related to games, purchases etc.
* Review
  * The social media aspect of the web application
* REST API
  * Cross-Domain /GET requests for developers to query data

### Core features

#### Authentication

We plan on using the model `AbstractUser` (Django default User) and the build-in Django authentication. We extend the Model with simple OneToOne-relation. We will enable developers to also play games.

#### Purchasing Games

The purchases are handled with [payments API](http://payments.webcourse.niksula.hut.fi). This is not a real banking API but it mimics some common features that such an API could have. We are not interested in the balance of the accounts, but that the transactions are safe and money gets transferred as intended (repeatability is prevented with nonce, a running number).

#### Playing Games

Conditions to get to play:

* User must be authenticated
* Provided link to play must be valid as we do not host the games
* The game is listed as free or be present in Player's purchase history (games)

The games are shown on our website using `<iframe>`s.
We plan on allowing users to store their play details such as score.

All additional information can be found below e.g. [Saving/Loading](#Saving/Loading).

#### Searching Games

Games can be sought by name, category and developer name. This is implemented with a single search input, with Twitter like hashtags and handles. The search box provides you with suggestions based on your current input.

#### Adding Game

Conditions for adding games:

* User must be authenticated (as developer)
* The name of the game must be unique
* The URL must be valid (simple validation with Django)

We use a simple form for this.

#### Statistics

For developers:

* number of times played
* number of purchases:
  * purchases this week/month/year
* cumulative revenue

For players:

* total playtime
  * playtime per game
* purchase history

#### Updating a game

Same conditions as in [adding games](#Adding\ Game) apply.
Additionally, game cannot be deleted if anyone has purchased it. Changing the cost of the game does not affect the old purchases in any way so that they are still valid (price is what it was at the hour of purchase).

#### Saving/Loading

The raw game states (`gameState` JSON attribute) are stored into the PostgreSQL database. This field will be characters (encoded with Base64). This is a separate table.

When a load is made, we fetch the raw JSON (stringified) from the database and parse it in the browser.

When a save is made, we `POST` the JSON and store it to the aforesaid table.

#### Third-Party Login / Logout

Users do not have to "register" when an user tries to login and if a user with those login credentials do not exist, a user is created. We plan on using GitHub for login/logout.

### Extra

List of the extra features we plan on implementing (if we have extra time).

#### Tests

We will do Unit tests for any non-Safe methods, any method that modifies data on the server. If there is time to spare we might implement more tests, than just the crucial ones.

#### Reviews

Who can review:

* Anyone who is authenticated, even the developers

An user can submit a review with the grade. Your and the reviews of others can be seen when viewing the details of a a game.

#### REST API

We plan on having a small API for the developers. We will have an application that stores the APIKeys into a table. These APIKeys are used instead of the regular authentication for Cross-Domain requests for the REST API (`/api/v1/{some_additional_path}`).

Developers can generate and remove APIKeys from their profile page.

**NOTE:** Only GET methods are allowed and all responses are JSON.

#### Highscores

Users can see highscores for games.

## API

In this chapter all the Models of the web app are listed, as they are in the database below.

![Database](./docs/Database_ER.jpg)

### Models

List of our models and their descriptions

#### Profile

Extends the default Django user model.

```python
  user = OneToOneField(User, primary_key=True, ...)
```

In addition to the extended fields a profile object contains:

```python
  is_developer = BooleanField(default=False)
  games = ManyToManyField('Game', ..., through='Purchase')
```

#### Game

Contains the basic details of the game.

```python
  name = CharField(min_length=128, unique=True, ...)
  description = TextField(...)
  url = URLField(unique=True, ...)
  price = DecimalField(default=0, max_digits=5, decimal_places=2)
  created_at = DateField(...)
  created_by = ForeignKey('Developer', ...)
  tags = ManyToMany('Tag', ...)
```

#### Purchase

Contains purchase information.

```python
  purchased_at = DateField(...)
  game = ForeignKey('Game', ...)
  created_by = ForeignKey('User', ...)
```

#### Save

Contains the information about the save file

```python
  game = ForeignKey('Game', ...)
  user = ForeignKey('User', ...)
  content = TextField(...)
```

#### Highscore

Contains the high score information

```python
  score = IntegerField(...)
  created_by = ForeignKey('Developer', ...)
  game = ForeignKey('Game', ...)
```

#### Review

Contains the review information

```python
  game = ForeignKey('Game', ...)
  created_by = ForeignKey('Developer', ...)
  grade = IntegerField(validators=[
    MinValueValidator(0),
    MaxValueValidator(5)
  ])
  content = TextField(...)
```

#### Tag

Contains the tag name of game catagories

```python
  name = CharField(max_length=32, unique=True)
```

List of model attributes

### Paths and views

#### Core

* {{ base_url }}/ – Home
* {{ base_url }}/terms-and-conditions – Terms and Conditions

#### Profile views and paths

* {{ base_url }}/oauth/ – Social authentication
* {{ base_url }}/login/ – Use internal login views
* {{ base_url }}/logout/ – Use internal logout views
* {{ base_url }}/profile/ – Separate profile view
* {{ base_url }}/profile/password/ – Password view
* {{ base_url }}/forgot-password/ – Optional
* {{ base_url }}/reset-password/ – Optional

#### Game views and paths

* {{ base_url }}/games/ – Browse all games / create a new game (POST - Developer)
* {{ base_url }}/games/libary – Browse games user has purchased
* {{ base_url }}/games/my - Browse games user has uploaded
* {{ base_url }}/games/:id – View / Update / Delete a game

#### Review view and paths

* {{ base_url }}/{{ target }}/review

#### REST API

* {{ base_url }}/api/{{ version_number }}

The API will change during the project so we do not list any of the API features as of now.

## Management, collaboration and contributing to project

See [guidelines](./docs/Contribution.md) for contributing.

### Order of work

At this point we have done the initial planning and design work and will start focusing to the project itself straight after christmas vacations. In addition to semi-regular face-to-face meetings arranged as needed, we will use tools provided by GitLab repository manager alongside with [Trello](https://trello.com).

### Timetable

We set out the deadlines for each task to be somewhat reasonable, so that the core application (fullfilling all required features) is developed first, and only after that the additional features will be implemented. We are planning to use Trello cards to track each issue more subtly.

| features                                | deadline  | assignee | core | Status |
| --------------------------------------- | --------- | -------- | ---- | ------ |
| [Authentication](#Authentication)       | 16.1.2019 | Juho     | x    | ok     |
| [Third-Party Login](#Third-Party-Login) | 16.1.2019 | Juho     | x    | ok     |
| [Adding Game](#Adding-Game)             | 22.1.2019 | Juho     | x    | -      |
| [Purchasing Games](#Purchasing-Games)   | 24.1.2019 | Touko    | x    | -      |
| [Playing Games](#Playing-Games)         | 31.1.2019 | Juho     | x    | -      |
| [Searching Games](#Searching-Games)     | 31.1.2019 | Hien     | x    | -      |
| [Updating Game](#Updading-a-game)       | 31.1.2019 | Juho     | x    | -      |
| Core templates                          | 31.1.2019 | Hien     | x    | -      |
| [Saving/Loading](#Saving/Loading)       | 7.2.2019  | Touko    | x    | -      |
| [Statistics](#Statistics)               | 10.2.2019 | Juho     | x    | -      |
| [Reviews](#Reviews)                     | 16.2.2019 | Juho     | -    | -      |
| [REST API](#REST-API)                   | 16.2.2019 | Hien     | -    | -      |
| [Highscores](#Highscores)               | 16.2.2019 | Juho     | -    | -      |
| Custom JavaScript game                  | 24.2.2019 | Touko    | -    | -      |
| Polishing                               | 24.2.2019 | -        | -    | -      |
