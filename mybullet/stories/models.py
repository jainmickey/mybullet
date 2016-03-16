# Third Party Stuff
from django.conf import settings
from django.db import models
from uuid_upload_path import upload_to
from versatileimagefield.fields import PPOIField, VersatileImageField

from mybullet.base.models import TimeStampedUUIDModel


class StoryImage(TimeStampedUUIDModel):
    image = VersatileImageField(
        upload_to=upload_to,
        ppoi_field='image_poi'
    )
    image_poi = PPOIField(verbose_name="Image's Point of Interest")  # point of interest
    is_deleted = models.BooleanField(
        verbose_name='Deleted',
        default=False,
        help_text='Select this instead of deleting an image.',
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.id)


class Story(TimeStampedUUIDModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stories')
    image = models.ForeignKey(StoryImage, related_name='story')
    caption = models.CharField(max_length=255, db_index=True, help_text='Caption of the story.')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Story/Experience',
                                   help_text='Your story or experience related to image')
    is_deleted = models.BooleanField(verbose_name='Deleted', default=False,
                                     help_text='Select this instead of deleting an event.')

    class Meta:
        verbose_name = 'story'
        verbose_name_plural = 'stories'
        ordering = ('-created', )

    def __str__(self):
        return '{} -> {}'.format(self.created_by, self.caption)

    def get_number_of_likes(self):
        return self.likes.count()

    def get_number_of_fakes(self):
        return self.fakes.count()


class LikeStory(TimeStampedUUIDModel):
    story = models.ForeignKey(Story, related_name='likes')
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='liked_stories')

    class Meta:
        unique_together = ('story', 'liked_by')

    def __str__(self):
        return '{} -> {}'.format(self.liked_by, self.story)


class FakeStory(TimeStampedUUIDModel):
    story = models.ForeignKey(Story, related_name='fakes')
    faked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='faked_stories')

    class Meta:
        unique_together = ('story', 'faked_by')

    def __str__(self):
        return '{} -> {}'.format(self.faked_by, self.story)
