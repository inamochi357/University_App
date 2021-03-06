# Generated by Django 3.2.5 on 2021-11-23 14:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('科目名', models.TextField(blank=True, null=True)),
                ('担当者氏名', models.TextField(blank=True, null=True)),
                ('全開講対象学科', models.TextField(blank=True, null=True)),
                ('年次', models.TextField(blank=True, null=True)),
                ('クラス', models.TextField(blank=True, null=True)),
                ('講義学期', models.TextField(blank=True, null=True)),
                ('単位数', models.IntegerField(blank=True, null=True)),
                ('必選区分', models.TextField(blank=True, null=True)),
                ('学期_曜日_時限', models.TextField(blank=True, db_column='学期・曜日・時限', null=True)),
                ('部門', models.TextField(blank=True, null=True)),
                ('備考', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, db_column='URL', null=True)),
                ('講義id', models.IntegerField(db_column='講義ID', primary_key=True, serialize=False)),
                ('科目名_英字_field', models.TextField(blank=True, db_column='科目名（英字）', null=True)),
                ('対象研究科_専攻', models.TextField(blank=True, db_column='対象研究科・専攻', null=True)),
            ],
            options={
                'db_table': 'classes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=10000, verbose_name='本文')),
                ('test', models.CharField(max_length=500, verbose_name='テスト情報')),
                ('attendance', models.CharField(max_length=500, verbose_name='出席情報')),
                ('EasyRating', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('fullnessRating', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日')),
                ('count', models.IntegerField(default=0)),
                ('ClassID', models.ForeignKey(db_constraint=False, default='deleted_class', on_delete=django.db.models.deletion.SET_DEFAULT, to='app.classes')),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post_Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=50, null=True, verbose_name='本文')),
                ('image', models.ImageField(upload_to='Note/', verbose_name='ノート')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日')),
                ('target_time', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(db_constraint=False, default='deleted_class', on_delete=django.db.models.deletion.SET_DEFAULT, to='app.classes')),
            ],
        ),
        migrations.CreateModel(
            name='LikeReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('target_review', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.review')),
            ],
        ),
        migrations.CreateModel(
            name='LikeNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('target_note', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.post_note')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ClassID', models.ForeignKey(db_constraint=False, default='deleted_class', on_delete=django.db.models.deletion.SET_DEFAULT, to='app.classes')),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
