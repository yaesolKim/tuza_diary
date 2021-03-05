from django.db.models import Model, CharField, DateField, FloatField, ForeignKey, CASCADE
from django.contrib.postgres.fields import JSONField


# Create your models here.
class User(Model):
    name = CharField(max_length=100)
    email = CharField(max_length=100)
    password = CharField(max_length=50)

    def __str__(self):
        return self.name


class Account(Model):
    account = CharField(max_length=50)
    user = ForeignKey(User, on_delete=CASCADE, null=True)


class Market(Model):
    name = CharField(max_length=10)
    code = CharField(max_length=10)

    def __str__(self):
        return self.name


class Candle(Model):
    code = CharField(max_length=50)
    code_name = CharField(max_length=50)
    market = ForeignKey(Market, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.code_name


def default_dict():
    return {'data': []}


# 게시글(Post)엔 제목(title), 내용(summary)이 존재합니다
class Post(Model):
    title = CharField(max_length=50)
    summary = CharField(max_length=1000, null=True)
    buy_json = JSONField(default=default_dict, null=True)
    sell_json = JSONField(default=default_dict, null=True)
    to_buy_json = JSONField(default=default_dict, null=True)
    to_sell_json = JSONField(default=default_dict, null=True)

    user = ForeignKey(User, on_delete=CASCADE, null=True)
    candle = ForeignKey(Candle, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.title


class Devidend(Model):
    date = DateField()
    profit = FloatField()

    user = ForeignKey(User, on_delete=CASCADE, null=True)
    account = ForeignKey(Account, on_delete=CASCADE, null=True)
    candle = ForeignKey(Candle, on_delete=CASCADE, null=True)


class Budget(Model):
    date = DateField()
    amount = FloatField()
    memo = CharField(max_length=1000, null=True)

    user = ForeignKey(User, on_delete=CASCADE, null=True)
    account = ForeignKey(Account, on_delete=CASCADE, null=True)
