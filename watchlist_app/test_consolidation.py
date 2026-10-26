"""Regression coverage for integrating the two internship projects."""
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIClient
from watchlist_app.models import Movie, StreamPlatform, WatchList, Review


class ConsolidationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.admin = User.objects.create_user('staff', password='practice-pass-123', is_staff=True)
        self.alice = User.objects.create_user('alice', password='practice-pass-123')
        self.bob = User.objects.create_user('bob', password='practice-pass-123')
        self.platform = StreamPlatform.objects.create(name='Netflix', about='Streaming', website='https://example.com')
        self.show = WatchList.objects.create(title='Example', storyline='A learning example', platform=self.platform)
        self.movie = Movie.objects.create(name='Example', description='A foundational movie example')

    def test_imported_read_styles_share_the_original_watchlist(self):
        for path in ('/movie/list/', '/examples/mixins/watchlist/', '/examples/generic/watchlist/',
                     '/examples/generic/netflix/', '/examples/router/watchlist/'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json()[0]['id'], self.show.pk)

    def test_detail_styles_find_same_record_and_missing_ids_return_404(self):
        for prefix in ('/movie/', '/examples/mixins/watchlist/', '/examples/generic/watchlist/',
                       '/examples/generic/crud/', '/examples/router/watchlist/'):
            with self.subTest(prefix=prefix):
                self.assertEqual(self.client.get(f'{prefix}{self.show.pk}/').status_code, 200)
                self.assertEqual(self.client.get(f'{prefix}99999/').status_code, 404)

    def test_mixin_list_and_detail_reject_inapplicable_methods(self):
        self.client.force_authenticate(self.admin)
        self.assertEqual(self.client.put('/examples/mixins/watchlist/', {}, format='json').status_code, 405)
        self.assertEqual(self.client.delete('/examples/mixins/watchlist/').status_code, 405)
        self.assertEqual(self.client.post(f'/examples/mixins/watchlist/{self.show.pk}/', {}, format='json').status_code, 405)

    def test_foundational_json_and_serializer_routes(self):
        plain = self.client.get('/examples/django/movies/').json()
        self.assertEqual(plain['movies'][0]['id'], self.movie.pk)
        for prefix in ('/examples/django/movies/', '/examples/functions/movies/', '/examples/manual/movies/'):
            self.assertEqual(self.client.get(f'{prefix}{self.movie.pk}/').status_code, 200)
            self.assertEqual(self.client.get(f'{prefix}99999/').status_code, 404)

    def test_function_view_create_patch_delete_and_validation(self):
        self.client.force_authenticate(self.admin)
        path = '/examples/functions/movies/'
        data = {'name': 'New movie', 'description': 'A sufficiently long description'}
        created = self.client.post(path, data, format='json')
        self.assertEqual(created.status_code, 201)
        detail = f"{path}{created.json()['id']}/"
        self.assertEqual(self.client.patch(detail, {'active': False}, format='json').status_code, 200)
        self.assertEqual(self.client.patch(detail, {'name': 'New movie'}, format='json').status_code, 200)
        self.assertEqual(self.client.patch(detail, {'description': 'short'}, format='json').status_code, 400)
        self.assertEqual(self.client.post(path, data, format='json').status_code, 400)
        self.assertEqual(self.client.patch(detail, {'description': 'New movie'}, format='json').status_code, 400)
        self.assertEqual(self.client.delete(detail).status_code, 204)

    def test_manual_serializer_persists_partial_updates(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post('/examples/manual/movies/', {'name': 'Manual', 'description': 'Manual exercise'}, format='json')
        self.assertEqual(response.status_code, 201)
        pk = response.json()['id']
        self.assertEqual(self.client.patch(f'/examples/manual/movies/{pk}/', {'active': False}, format='json').status_code, 200)
        self.assertFalse(Movie.objects.get(pk=pk).active)

    def test_catalog_write_permissions_apply_across_styles(self):
        for user in (None, self.alice):
            self.client.force_authenticate(user)
            for path in ('/movie/list/', '/movie/stream/', '/examples/functions/movies/',
                         '/examples/manual/movies/', '/examples/mixins/watchlist/',
                         '/examples/router/watchlist/', '/examples/router/stream_platform/'):
                with self.subTest(user=user, path=path):
                    self.assertIn(self.client.post(path, {}, format='json').status_code, (401, 403))

    def test_catalog_creation_supports_writable_relationship(self):
        self.client.force_authenticate(self.admin)
        data = {'title': 'Created', 'storyline': 'Relational practice', 'platform_id': self.platform.pk}
        for path in ('/movie/list/', '/examples/mixins/watchlist/', '/examples/router/watchlist/'):
            with self.subTest(path=path):
                response = self.client.post(path, data, format='json')
                self.assertEqual(response.status_code, 201)
                self.assertEqual(WatchList.objects.get(pk=response.json()['id']).platform, self.platform)

    def test_hyperlinked_and_nested_platform_representations(self):
        detail = self.client.get(f'/movie/stream/{self.platform.pk}/')
        self.assertEqual(detail.status_code, 200)
        self.assertTrue(detail.json()['movies'][0].endswith(f'/movie/{self.show.pk}/'))
        nested = self.client.get(f'/examples/router/stream_platform/{self.platform.pk}/')
        self.assertEqual(nested.status_code, 200)
        self.assertEqual(nested.json()['movies'][0]['id'], self.show.pk)

    def test_netflix_queryset_excludes_other_platforms(self):
        other = StreamPlatform.objects.create(name='Other', about='Other service', website='https://example.org')
        WatchList.objects.create(title='Other', storyline='Other entry', platform=other)
        self.assertEqual(len(self.client.get('/examples/generic/netflix/').json()), 1)

    def test_review_author_binding_owner_permissions_and_validation(self):
        path = '/movie/review/'
        data = {'rating': 5, 'description': 'Interesting example', 'watchlist': self.show.pk, 'review_user': self.bob.pk}
        self.assertEqual(self.client.post(path, data, format='json').status_code, 401)
        self.client.force_authenticate(self.alice)
        created = self.client.post(path, data, format='json')
        self.assertEqual(created.status_code, 201)
        review = Review.objects.get(pk=created.json()['id'])
        self.assertEqual(review.review_user, self.alice)
        detail = f'{path}{review.pk}/'
        self.client.force_authenticate(self.bob)
        self.assertEqual(self.client.patch(detail, {'rating': 3}, format='json').status_code, 403)
        self.assertEqual(self.client.delete(detail).status_code, 403)
        self.client.force_authenticate(self.alice)
        self.assertEqual(self.client.patch(detail, {'rating': 6}, format='json').status_code, 400)
        self.assertEqual(self.client.patch(detail, {'rating': 4}, format='json').status_code, 200)
        self.assertEqual(self.client.delete(detail).status_code, 204)

    def test_review_filters_search_ordering_and_cursor_pagination(self):
        for i in range(5):
            Review.objects.create(review_user=self.alice, watchlist=self.show, rating=i + 1, description='Interesting example')
        Review.objects.create(review_user=self.bob, watchlist=self.show, rating=5, description='Other')
        response = self.client.get('/movie/review/?username=alice&search=Interesting&ordering=-rating').json()
        self.assertEqual([r['rating'] for r in response['results']], [5, 4, 3])
        self.assertIsNotNone(response['next'])
        page_two = self.client.get(response['next']).json()
        self.assertEqual([r['rating'] for r in page_two['results']], [2, 1])
        by_url = self.client.get('/movie/review/alice/?rating=5').json()
        self.assertEqual(len(by_url['results']), 1)

    def test_educational_review_rate_limit(self):
        self.client.force_authenticate(self.alice)
        for _ in range(3):
            self.assertEqual(self.client.get('/movie/review/').status_code, 200)
        self.assertEqual(self.client.get('/movie/review/').status_code, 429)

    def test_register_login_token_authentication_and_logout(self):
        created = self.client.post('/register/', {'username': 'new-user', 'password': 'practice-pass-123',
                                                 'confirm_password': 'practice-pass-123'}, format='json')
        self.assertEqual(created.status_code, 201)
        user = User.objects.get(username='new-user')
        self.assertTrue(user.check_password('practice-pass-123'))
        self.assertEqual(self.client.post('/login/', {'username': 'new-user', 'password': 'wrong'}, format='json').status_code, 400)
        logged_in = self.client.post('/login/', {'username': 'new-user', 'password': 'practice-pass-123'}, format='json')
        self.assertEqual(logged_in.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + logged_in.json()['token'])
        self.assertEqual(self.client.post('/logout/').status_code, 200)
        self.assertEqual(self.client.post('/logout/').status_code, 401)
