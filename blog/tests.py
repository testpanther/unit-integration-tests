from django.test import TestCase, RequestFactory, Client
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib.staticfiles.testing \
  import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

from django.contrib.auth import get_user_model
from blog.models import Publication, Post

class BlogTestCase(TestCase):
  def setUp(self):
    User = get_user_model()
    self.author = User.objects.create(username="Narf")
    self.author.set_password('narf')
    self.author.save()
    
  def test_post(self):
    blog = Publication.objects.create(
              name='Hello', slug='hw')
    post = Post.objects.create(
              title = 'Test post', slug = 'test',
              body = 'body', blog = blog, 
              author = self.author
    )
    self.assertEqual(blog.post_set.all().count(), 1)
    

  def test_obtain_token(self):
    self.factory = RequestFactory()
    request = self.factory.post(
      '/api-token-auth/',
      {'username': 'Narf', 'password': 'narf'}
    )
    request.user = self.author
    response = obtain_jwt_token(request)
    self.assertEqual(response.status_code, 200)
    
  def test_obtain_token_2 (self):
    self.client = Client()
    response = self.client.post(
      '/api-token-auth/',
      {'username': 'Narf', 'password': 'narf'}
    )
    self.assertEqual(response.status_code, 200)
    self.assertIn('token', response.content.decode('utf-8'))
    

class MySeleniumTests(StaticLiveServerTestCase):
  @classmethod
  def setUpClass(cls):
    super(MySeleniumTests, cls).setUpClass()
    cls.selenium = WebDriver()
    
  @classmethod
  def tearDownClass(cls):
    cls.selenium.quit()
    super(MySeleniumTests, cls).tearDownClass()
    
  def test_login(self):
    self.selenium.get(
      '{}/graphql'.format(self.live_server_url))
    element = self.selenium.find_element_by_xpath(
      '/html/body/div/div[2]/div[1]/div/div[3]/a[1]')
    self.assertEqual(element.text, 'Prettify')
    