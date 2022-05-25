from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from user.models import MyUser
from django.contrib.auth import get_user_model


class Classes(models.Model):
    科目名 = models.TextField(blank=True, null=True)
    担当者氏名 = models.TextField(blank=True, null=True)
    全開講対象学科 = models.TextField(blank=True, null=True)
    年次 = models.TextField(blank=True, null=True)
    クラス = models.TextField(blank=True, null=True)
    講義学期 = models.TextField(blank=True, null=True)
    単位数 = models.IntegerField(blank=True, null=True)
    必選区分 = models.TextField(blank=True, null=True)
    学期_曜日_時限 = models.TextField(db_column='学期・曜日・時限', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    部門 = models.TextField(blank=True, null=True)
    備考 = models.TextField(blank=True, null=True)
    url = models.TextField(db_column='URL', blank=True, null=True)  # Field name made lowercase.
    講義id = models.IntegerField(db_column='講義ID', primary_key=True)  # Field name made lowercase.
    科目名_英字_field = models.TextField(db_column='科目名（英字）', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    対象研究科_専攻 = models.TextField(db_column='対象研究科・専攻', blank=True, null=True)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'classes'


class Post_Note(models.Model):
    text = models.CharField("本文", max_length=50, blank=True, null=True)
    image = models.ImageField("ノート", upload_to="Note/")
    created_at = models.DateTimeField("投稿日", default=timezone.now)
    target = models.ForeignKey(Classes, on_delete=models.SET_DEFAULT, default="deleted_class", db_constraint=False)
    User = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    target_time = models.IntegerField(default=0)
    count = models.IntegerField(default=0)


class LikeNote(models.Model):
    User = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    target_note = models.ForeignKey(Post_Note, on_delete=models.CASCADE, default=0)
    timestamp = models.DateTimeField(default=timezone.now)


class Review(models.Model):
    ClassID = models.ForeignKey(Classes, on_delete=models.SET_DEFAULT, default="deleted_class", db_constraint=False)
    UserId = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.CharField("本文", max_length=10000)
    test = models.CharField("テスト情報", max_length=500)
    attendance = models.CharField("出席情報", max_length=500)
    EasyRating = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    fullnessRating = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    created_at = models.DateTimeField("投稿日", default=timezone.now)
    count = models.IntegerField(default=0)


class LikeReview(models.Model):
    UserId = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    target_review = models.ForeignKey(Review, on_delete=models.CASCADE, default=0)
    timestamp = models.DateTimeField(default=timezone.now)


class FavoriteClass(models.Model):
    UserId = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    ClassID = models.ForeignKey(Classes, on_delete=models.SET_DEFAULT, default="deleted_class", db_constraint=False)


class ClassesAdditionFunction(models.Model):
    ClassID = models.OneToOneField(Classes, on_delete=models.SET_DEFAULT, default="deleted_class", db_constraint=False, primary_key=True)
    count = models.IntegerField(default=0)