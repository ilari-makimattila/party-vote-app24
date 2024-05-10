Party Voting App for the Year 2024
==================================

This is becoming a yearly tradition. This is the same app as [the 2023 version](https://github.com/ilari-makimattila/party-vote-app)
which is the iterated version of [the first hack I did at 2022](https://github.com/ilari-makimattila/eurovision-party).

This version is written as I would write a production grade app. It's made using TDD first and foremost.
In fact I didn't even spin it up until I was at the point of making the UI. The complete flow was there before the app was usable.
It is also fully typed. 

The app is a simple Python [FastAPI](https://fastapi.tiangolo.com/) app with some [HTMX](https://htmx.org/).
It works completely without JavaScript but adds some handy features when JavaScript is available.

Developing
----------

You will need:
    * Python 3.12
    * NodeJS and npm
    * [Poetry](https://python-poetry.org/)

Start with running
```
make bootstrap
```

It will install the dependencies you will need.

### Running tests

```
make test       # a single run
make watchtest  # run tests automatically when something chages
```

### Running checks

```
make check
```

This will run `ruff` and `mypy` to check for formatting and typing respectively.

If you need to reformat the code, `make format` will help.

### Running the app

```
make dev
```

If you want to use the file system database, set `DATABASE_DIR` environment variable to a writable folder.
