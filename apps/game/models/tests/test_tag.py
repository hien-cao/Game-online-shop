from django.test import TestCase

from ...models import Tag


class TagTestCase(TestCase):
    def test_tag_can_be_created(self):
        tag = Tag.objects.create(name='foo')
        self.assertIsInstance(tag, Tag)

    def test_tag__str__(self):
        tag = Tag.objects.create(name='foo')
        name = '{0}'.format(tag)
        self.assertEqual(name, 'foo')
