# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Bom(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20, blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    layer = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'BOM'
        unique_together = (('id', 'layer'),)


class Coa(models.Model):
    fid = models.CharField(primary_key=True, max_length=20)
    fname = models.CharField(max_length=20, blank=True, null=True)
    sid = models.CharField(max_length=20)
    sname = models.CharField(max_length=20, blank=True, null=True)
    num = models.IntegerField(blank=True, null=True)
    cleadtime = models.IntegerField(db_column='cleadTime', blank=True, null=True)  # Field name made lowercase.
    sleadtime = models.IntegerField(db_column='sleadTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COA'
        unique_together = (('fid', 'sid'),)


class Mas(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    method = models.CharField(max_length=20, blank=True, null=True)
    lossrate = models.FloatField(db_column='lossRate', blank=True, null=True)  # Field name made lowercase.
    leadtime = models.IntegerField(db_column='leadTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MAS'


class Stock(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20, blank=True, null=True)
    ostock = models.IntegerField(blank=True, null=True)
    mstock = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock'
