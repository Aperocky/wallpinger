from django.test import TestCase
from .models import Website, Result
from .views import pingwebsite
import datetime

# Create your tests here.
class TestWall(TestCase):
    def setUp(self):
        mywebsite = Website.objects.create(website_name="Google", website_url="google.com")

    def testping(self):
        mywebsite = Website.objects.filter()[:1].get()
        sent, ret, avg, curr = pingwebsite(mywebsite)
        assert isinstance(sent, int)
        assert isinstance(ret, int)
        assert isinstance(avg, str)
        assert isinstance(curr, datetime.datetime)
        pingtime = curr
        # Testing result
        myresult = Result.objects.filter()[:1].get()
        self.assertEquals(pingtime, myresult.ping_time)
        self.assertEquals(avg, str(myresult.ping_result))
        