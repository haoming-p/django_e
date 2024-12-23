from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)


# waht tag applied to what object
class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # 需要Type(table liek product, video, article), 需要ID(find item in the table)
    # ContentType: allow generic relationships
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()