"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from profile import models
from django.contrib.auth.models import User

class ProfileTests(TestCase):

    def test_create_user(self):
        models.Profile.create_new_user('mrrm', 'mrrm@none.com', 'mrrm')
        print 'List of all users:'
        for user in User.objects.all():
            print '  Username: %s   Email: %s' % (user.username, user.email)

    def test_search_users(self):
        models.Profile.create_new_user('mrm1', 'mrm@none.com', 'mrm1')
        found = models.Profile.find('Mrm')
        for profile in found:
            user = profile.user
            print '  Username: %s   Email: %s' % (user.username, user.email)
        self.assertTrue(len(found) > 0)
