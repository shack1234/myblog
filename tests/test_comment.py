import unittest
from app.models import User,Comment,Blog
from app import db

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.user_shack = User(username='shack', password='1234', email='shack@gmail.com')
        self.new_blog = Blog(id=1, title='house', blogc='testing', user_id=self.user_shack.id)
        self.new_comment = Comment(id=1, comment ='cool', user_id=self.user_shack.id, blog_id = self.new_blog.id )

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()
        Comment.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment, 'cool')
        self.assertEquals(self.new_comment.user_id, self.user_shack.id)
        self.assertEquals(self.new_comment.blog_id, self.new_blog.id)

    def test_save_comment(self):
        self.new_comment.save()
        self.assertTrue(len(Comment.query.all()) > 0)

    def test_get_comment(self):
        self.new_comment.save()
        got_comment = Comment.get_comment(1)
        self.assertTrue(get_comment is not None)