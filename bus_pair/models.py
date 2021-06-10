from django.db import models
from busstop.models import Busstop

# https://stackoverflow.com/questions/60421962/django-change-foreign-keys-to-bigint


class BusPair(models.Model):
    """バス組み合わせモデル"""

    class Meta:
        db_table = 'bus_pair'
        ordering = ['created_at']
        verbose_name = verbose_name_plural = 'バス組み合わせ'  # rm 's'

    # set "db_constraint=False" cuz occurs error
    # "arrival_bus_stop_id" and "id" are of incompatible types: bigint and uuid.
    departure_bus_stop = models.ForeignKey(
        Busstop,
        db_constraint=False,
        verbose_name='出発バス停',
        on_delete=models.PROTECT,
        related_name="departure_bus_stop")
    arrival_bus_stop = models.ForeignKey(
        Busstop,
        db_constraint=False,
        verbose_name='到着バス停',
        on_delete=models.PROTECT,
        related_name="arrival_bus_stop")
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)

    def __str__(self):
        return self
