# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Area(models.Model):
    areaid = models.IntegerField(primary_key=True)
    areaname = models.CharField(max_length=50)
    parentid = models.IntegerField()
    arealevel = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area'

class UserInfo(models.Model):
    """用户"""
    uname = models.CharField(max_length=100,verbose_name='用户名')
    pwd = models.CharField(max_length=100,verbose_name='密码')

    def __str__(self) -> str:
        return self.uname

class Address(models.Model):
    aname = models.CharField(max_length=30)
    aphone = models.CharField(max_length=11)
    addr = models.CharField(max_length=100)
    isdefault = models.BooleanField(default=False)
    userinfo = models.ForeignKey(UserInfo,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.aname
