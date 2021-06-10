from django.db import models
from bus_pair.models import BusPair
from bus_line.models import BusLine


class BusTimetable(models.Model):
    """バス時刻モデル"""

    class Meta:
        db_table = 'bus_timetable'
        ordering = ['created_at']
        verbose_name = verbose_name_plural = 'バス時刻'  # rm 's'

    bus_pair = models.ForeignKey(
        BusPair,
        db_constraint=False,
        verbose_name='バス停組み合わせ',
        on_delete=models.PROTECT,
        related_name="bus_pair")
    bus_line = models.ForeignKey(
        BusLine,
        db_constraint=False,
        verbose_name='バス路線',
        on_delete=models.PROTECT,
        related_name="bus_line")

    departure_at = models.DateTimeField(verbose_name='出発日時')
    arrive_at = models.DateTimeField(verbose_name='到着日時')
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)

    def __str__(self):
        return self
