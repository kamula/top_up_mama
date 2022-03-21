from statistics import mode
import uuid
from django.db import models


class BookComment(models.Model):
    book_id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    id = models.IntegerField()
    comment = models.CharField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
