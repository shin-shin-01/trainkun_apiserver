import uuid
from django.db import models

class Busstop(models.Model):
    """バス停モデル"""

    class Meta:
        db_table = 'busstop'
        ordering = ['created_at']
        verbose_name = verbose_name_plural = 'バス停' # rm 's'

    name = models.CharField(verbose_name='名称', unique=True, max_length=50)
    code = models.CharField(verbose_name='コード', unique=True, max_length=20)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)

    def __str__(self):
        return self.name
