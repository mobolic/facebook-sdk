from django.core.management.base import BaseCommand

import facebook

from blog.models import Post

token = '<Your token goes here>'


class Command(BaseCommand):
    """
    Simple command that will share posts on a Facebook page.
    It's just for illustration purpose.
    """

    @staticmethod
    def get_attachment(post):
        attachment = {
            'link': 'http://www.example.com/{}'.format(post.get_absolute_url()),
        }
        return attachment

    def handle(self, *args, **options):
        api = facebook.GraphAPI(token)

        for post in Post.objects.filter(published=False):
            api.put_wall_post(post.title, attachment=self.get_attachment(post))
            post.published = True
            post.save()
