from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from .models import Tweet

# Create your tests here.
User = get_user_model()


class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        self.userb = User.objects.create_user(username='cfe-2', password='somepassword2')
        Tweet.objects.create(content="my first tweet", user=self.user)
        Tweet.objects.create(content="my second tweet", user=self.user)
        Tweet.objects.create(content="my third tweet", user=self.userb)
        self.currentCount = Tweet.objects.all().count()

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content="my fourth tweet", user=self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user)

    def get_client(self):
        # Make all requests in the context of a logged in session.
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client

    def test_api_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {'id': 1, 'action': 'like'})
        like_count = response.json().get('likes')
        user = self.user
        my_like_instances_count = user.tweetlike_set.count()
        my_related_likes = user.tweet_user.count()
        self.assertEqual(like_count, 1)
        self.assertEqual(my_like_instances_count, 1)
        self.assertEqual(my_like_instances_count, my_related_likes)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {'id': 2, 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        response = client.post('/api/tweets/action/', {'id': 2, 'action': 'unlike'})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 0)

    def test_action_retweet(self):
        client = self.get_client()
        current_count = self.currentCount
        response = client.post('/api/tweets/action/', {'id': 3, 'action': 'retweet'})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get('id')
        self.assertNotEqual(3, new_tweet_id)
        self.assertEqual(current_count + 1, new_tweet_id)

    def test_tweet_create_api_view(self):
        request_data = {'content': 'This is my test tweet.'}
        current_count = self.currentCount
        client = self.get_client()
        response = client.post('/api/tweets/create/', request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get('id')
        self.assertNotEqual(3, new_tweet_id)
        self.assertEqual(current_count + 1, new_tweet_id)

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get('/api/tweets/1/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get('id')
        self.assertEqual(_id, 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete('/api/tweets/1/delete/')
        self.assertEqual(response.status_code, 200)
        response = client.delete('/api/tweets/1/delete/')
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete('/api/tweets/3/delete/')
        self.assertEqual(response_incorrect_owner.status_code, 401)

    def test_tweet_related_names(self):
        user = self.user
        self.assertEqual(self.user.tweets.count(), 2)
