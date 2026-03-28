# Project 12: Movie Catalog

This repository contains a Django MVC application for managing a movie catalog.

## Implemented Features

- movie list page
- create movie form
- edit movie form
- delete confirmation page
- search by title or director
- Django admin configuration for movies
- basic automated tests for CRUD flow and search

## Data Model

`Movie`
- `title`
- `director`
- `rating`

## Project Structure

- Model: `backend/movies/models.py`
- Controller/View logic: `backend/movies/views.py`
- Templates: `backend/movies/templates/movies/`
- Routing: `backend/movies/urls.py`, `backend/config/urls.py`

## How To Run

1. Activate the virtual environment:

```bash
cd backend
source ../.venv/bin/activate
```

2. Apply migrations:

```bash
python manage.py migrate
```

3. Start the development server:

```bash
python manage.py runserver
```

4. Open the app:

```text
http://127.0.0.1:8000/
```

## Run Tests

```bash
cd backend
../.venv/bin/python manage.py test
```

## Notes

- rating validation allows values from `1.0` to `10.0`
- interface language is set to Ukrainian
- timezone is set to `Europe/Warsaw`
