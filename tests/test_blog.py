import unittest
from app.models import User, Blog
from app import db
# testing test for blog class 
class BlogModelTest(unittest.TestCase):
    def setUp(self):
        self.user_shack = User(username='shack', password='1234', email='shack@gmail.com')
        self.new_blog = Blog(id=1, title='house', blogc='testing', user_id=self.user_shack.id)

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.title, 'house')
        self.assertEquals(self.new_blog.blogc, 'testing')
        self.assertEquals(self.new_blog.user_id, self.user_shack.id)

    def test_save_blog(self):
        self.new_blog.save()
        self.assertTrue(len(Blog.query.all()) > 0)

    def test_get_blog(self):
        self.new_blog.save()
        got_blog = Blog.get_blog(1)
        self.assertTrue(get_blog is not None)