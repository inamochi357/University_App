from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone


class AccountManager(BaseUserManager):  #BaseUserManagerを継承してカスタムユーザーを作成

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None): #管理者権限を持ったユーザーを作成
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):   #ユーザーの定義
    username = models.CharField(verbose_name='username', max_length=10, unique=True, validators=[MinLengthValidator(5,), RegexValidator(r'^[a-zA-Z0-9]*$',)])   #バリデーションを行う
    email = models.EmailField(verbose_name='Email', max_length=50, unique=True)
    nickname = models.CharField(verbose_name='ニックネーム', max_length=10, blank=False, null=False)
    grade = models.IntegerField(verbose_name="学年", blank=True, null=True)
    department = models.CharField(verbose_name="所属学部・学科", max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(verbose_name="誕生日", blank=True, null=True)
    image = models.ImageField(verbose_name='プロフィール画像', upload_to="icon/", blank=True, null=True, default="icon/default_icon")
    url = models.URLField(verbose_name='リンク', blank=True, null=True)
    introduction = models.TextField(verbose_name='自己紹介', max_length=300, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='登録日', default=timezone.now)
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "IS the user a member of staff?"
        return self.is_admin
