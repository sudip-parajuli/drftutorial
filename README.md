# Django REST Framework Internship Practice

My Django REST Framework exercises from my internship, consolidated from
`drftutorial` and `RESTFrameworkTutorial` into one runnable learning project.
This is a practice repository, not a production movie service.

The project follows a movie/watchlist domain to compare API implementation
styles and learn serializers, relationships, authentication and access control.
The examples intentionally expose several ways to work with the same records;
they do not maintain duplicate watchlist or streaming-platform models.

## Topics covered

- Plain Django JSON responses, DRF function views and `APIView`.
- Explicit `Serializer.create/update`, `ModelSerializer`, field/object validation.
- Foreign keys, nested serializers and hyperlinked relationships.
- `GenericAPIView` with mixins, concrete generic views and queryset overrides.
- `ModelViewSet` and `DefaultRouter`.
- Registration, token login/logout and session authentication.
- Staff-only catalog writes and review-owner permissions.
- Filtering, search, ordering, cursor pagination and throttling.
- Standalone page-number/limit-offset pagination examples.

## Run locally

Requires Python 3.11 or 3.12. Uses SQLite; no PostgreSQL server is required.

```sh
git clone https://github.com/sudip-parajuli/drftutorial.git
cd drftutorial
python -m venv .venv
```

Activate with `.venv\Scripts\Activate.ps1` in PowerShell or
`source .venv/bin/activate` on macOS/Linux, then:

```sh
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `/admin/` to add data, `/api-auth/login/` for the browsable API session
login, `/movie/list/` for the main watchlist API, or `/examples/router/` for
the router-generated API root. All URLs below are relative to localhost:8000.

## Main API

| Route | Purpose |
| --- | --- |
| `POST /register/` | Create a user and return a token |
| `POST /login/` | Return a token for valid username/password |
| `POST /logout/` | Revoke the caller's token |
| `/movie/list/`, `/movie/<id>/` | List/create and retrieve/update/delete watchlist records |
| `/movie/stream/`, `/movie/stream/<id>/` | Streaming-platform CRUD with movie hyperlinks |
| `/movie/review/`, `/movie/review/<id>/` | Reviews; cursor-paginated list |
| `/movie/review/<username>/` | Filter reviews by username |

Catalog reads are public; catalog writes require staff. Review creation requires
login; only its author can change or delete a review. The server assigns the
review author. Authenticate API requests with `Authorization: Token <token>`.
For session-authenticated writes, send Django's CSRF token.

Example watchlist body:

```json
{"title": "Example film", "storyline": "An internship practice entry.", "active": true, "platform_id": 1}
```

`platform` is the read-only name; `platform_id` is the writable relationship.
Create the platform first. Review bodies use `rating` (1–5), `description`,
`watchlist` (the watchlist ID) and optionally `active`.

Filtering examples:

```text
/movie/review/?username=alice&rating=5
/movie/review/?search=interesting&ordering=-rating
```

Review-list requests from authenticated users are limited to three per day by
the educational `ReviewRateThrottle`. These low values demonstrate throttling;
they are not a production traffic policy. Anonymous reads are not throttled by
this user-rate class. Page-number/limit-offset classes are provided for study;
the active review list uses cursor pagination with three records per page.

## Compare implementation styles

| Prefix | What it demonstrates |
| --- | --- |
| `/examples/django/movies/` | Plain Django JSON list and `<id>/` detail |
| `/examples/functions/movies/` | Validated DRF function-view CRUD and `<id>/` detail |
| `/examples/manual/movies/` | Manual serializer create/update and `<id>/` detail |
| `/examples/mixins/watchlist/` | GenericAPIView + CRUD mixins and `<id>/` detail |
| `/examples/generic/watchlist/` | Concrete list and `<id>/` retrieve views |
| `/examples/generic/update/<id>/` | UpdateAPIView |
| `/examples/generic/crud/<id>/` | RetrieveUpdateDestroyAPIView |
| `/examples/generic/netflix/` | Queryset restricted to platform name `Netflix` |
| `/examples/router/watchlist/` | Router + watchlist ModelViewSet |
| `/examples/router/stream_platform/` | Router + nested platform serializer |

The foundational `Movie` model has `name`, `description`, `active`; it is the
earlier standalone CRUD exercise. `WatchList` is the later relational model
with `title`, `storyline`, `platform`, and reviews. The manual serializer is
deliberately basic; the function-view serializer adds the original custom
validation exercises. They are alternative lessons, not identical contracts.

## Verify

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

The regression suite checks the imported routes against shared data, relationship
representations, partial-update validation, token login/logout, permissions,
filtering, pagination and throttling. GitHub Actions runs it on Python 3.11/3.12.

## Consolidation and limitations

See [the consolidation record](docs/CONSOLIDATION.md) for the source mapping and
history recovery instructions. Both original Git histories are parents of the
consolidation commit. Old snippets remain available in history; copied project
settings and duplicate model/view implementations are not left in the main tree.

Local debug mode is enabled by default. A random development secret is generated
unless `DJANGO_SECRET_KEY` is set. Set a stable private key if you need sessions
to survive server restarts. Do not expose this learning server to the internet.
Production hosting, password reset, account verification, business moderation,
and production-rate-limit infrastructure are outside the scope of these exercises.

This repository records learning during my internship. It is not a claim that
standard DRF patterns or framework examples are original research.
