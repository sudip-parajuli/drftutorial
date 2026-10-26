# Consolidation record

Consolidated on 26 October 2026. Retained repository: `sudip-parajuli/drftutorial`.
Source to retire after verification: `sudip-parajuli/RESTFrameworkTutorial`.

## What was retained

| Original material | Consolidated location |
| --- | --- |
| drftutorial watchlist/platform/review models and nine migrations | `watchlist_app/models.py`, `watchlist_app/migrations/` |
| drftutorial authentication, permissions, filters, search, ordering, throttles | `user/`, `watchlist_app/api/v1/` |
| RESTFrameworkTutorial standalone Movie model | `watchlist_app/models.py` and a new additive migration |
| Explicit Serializer create/update lesson | `watchlist_app/api/v1/serializers/foundations.py` |
| ModelSerializer custom validation and status field | `FoundationMovieSerializer` in the same file |
| Plain Django and DRF function-view exercises | `watchlist_app/api/v1/views/examples.py` |
| GenericAPIView/mixins, concrete views, Netflix queryset override | Same examples module, under `/examples/` |
| ModelViewSets, router, nested platform representation | Same module and `example_urls.py` |
| APIView CRUD, StringRelatedField and hyperlink relationships | Main `/movie/` API and shared serializers |
| Alternative page-number/limit-offset pagination snippets | Runnable classes in `pagination.py` |

Equivalent catalog CRUD methods, serializer declarations, starter files and
second-project settings were consolidated rather than copied wholesale. Existing
`/movie/` and user routes remain; imported lessons are under `/examples/`. The
obsolete source router is intentionally represented under that prefix.

## Corrections needed for the combined project

- Added the missing django-filter dependency; use Django 5.2 and DRF 3.16.
- Enabled the existing token authentication and permission classes.
- Bind reviews to the authenticated author and enforce review-owner writes.
- Give hyperlinked serializers request context through generic views.
- Add writable `platform_id` alongside the read-only platform name.
- Return 404 for missing records rather than unhandled model exceptions.
- Restore function examples shadowed by same-named classes in the old file.
- Correct the description-validator field name, update self-duplicate detection,
  partial-update missing-field handling and concatenated prohibited-word entries.
- Replace commented repetitions with named, importable examples and tests.
- Remove a hardcoded development secret from current settings. Historical commits
  are preserved, so this does not erase old settings from Git history.

No production/customer database is present or migrated. Existing drftutorial
schema migrations are preserved; the foundational Movie uses its own table.

## History preservation

The consolidation commit has two parents: the previous drftutorial tip and the
original RESTFrameworkTutorial tip. Thus the source's original author/committer
metadata and every original file remain reachable after its repository is removed.

Original tips:

- drftutorial: `bdc7b19d25f2860780066491c886ecfe74a98e39`
- RESTFrameworkTutorial: `dd515ae8864e7180817fbf9456e0b865e4b2dce3`

To inspect the original project after cloning this repository:

```sh
git log dd515ae8864e7180817fbf9456e0b865e4b2dce3
git show dd515ae8864e7180817fbf9456e0b865e4b2dce3:movie_app/api/v1/views/movies.py
```

The source had one branch (`main`), no issues/pull requests and no releases at
the time of review. Separate local Git bundles provide an additional backup.
