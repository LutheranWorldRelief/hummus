from django.db import models


class AuthItem(models.Model):
    type = models.SmallIntegerField()
    name = models.CharField(primary_key=True, max_length=64)
    description = models.TextField(blank=True, null=True)
    rule_name = models.ForeignKey('AuthRule', models.DO_NOTHING, db_column='rule_name', blank=True, null=True)
    data = models.BinaryField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['type', 'name']
        db_table = 'auth_item'


class AuthAssignment(models.Model):
    user = models.ForeignKey('AuthUserYii', models.DO_NOTHING)
    item_name = models.ForeignKey('AuthItem', models.DO_NOTHING, db_column='item_name')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'auth_assignment'
        ordering = ['user', 'item_name']
        unique_together = (('item_name', 'user'),)


class AuthItemChild(models.Model):
    parent = models.ForeignKey(AuthItem, models.DO_NOTHING, db_column='parent', related_name="parent")
    child = models.ForeignKey(AuthItem, models.DO_NOTHING, db_column='child', related_name="child")

    class Meta:
        db_table = 'auth_item_child'
        unique_together = (('parent', 'child'),)


class AuthRule(models.Model):
    name = models.CharField(primary_key=True, max_length=64)
    data = models.BinaryField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'auth_rule'


class AuthUserYii(models.Model):
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    access_token = models.TextField(blank=True, null=True)
    countries = models.TextField(blank=True, null=True)  # This field type is a guess.
    projects = models.TextField(blank=True, null=True)  # This field type is a guess.

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'auth_user_yii'

