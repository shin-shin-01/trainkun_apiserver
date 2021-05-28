import uuid
from django.db import models


class BusLine(models.Model):
    """バス路線モデル"""

    class Meta:
        db_table = 'bus_line'
        ordering = ['created_at']
        verbose_name = verbose_name_plural = 'バス路線'  # rm 's'

    name = models.CharField(verbose_name='名称', unique=True, max_length=50)
    code = models.CharField(verbose_name='コード', unique=True, max_length=20)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)

    def __str__(self):
        return self.name
