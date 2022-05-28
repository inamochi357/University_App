from django import forms
from django.contrib.auth.models import User
from .models import MyUser
from django.forms import ChoiceField
from django.contrib.auth.forms import AuthenticationForm



class AccountForm(forms.ModelForm):
    #新規登録用
    password = forms.CharField(widget=forms.PasswordInput(), label="パスワード")

    class Meta:
        model = MyUser
        fields = ("username", "email", "password")
        labels = {"username": "ユーザーID", "email": "メールアドレス"}


class CustomProfileChangeForm(forms.ModelForm):
    #後で情報を変更するためのフォーム
    class Meta:
        model = MyUser
        fields = ("nickname", "date_of_birth", "image", "url", "introduction")
        labels = {
            "nickname": "ニックネーム",
            "date_of_birth": "誕生日",
            "image": "アイコン",
            "introduction": "自己紹介",
        }

    def __init__(self, nickname=None, grade=None, department=None, date_of_birth=None, image=None, url=None, introduction=None, *args, **kwargs):
        #学年を選択
        CHOICES_GRADE = (
            ("学部生", (
                ("1", "1年生"),
                ("2", "2年生"),
                ("3", "3年生"),
                ("4", "4年生"),
                ("5", "5年生"),
                ("6", "6年生")
            )),
            ("院生", (
                ("7", "1年生"),
                ("8", "2年生"),
            ))
        )

        #学部学科を選択
        CHOICES_DEPARTMENT = (
            ("法学部", (
                ("00", "法学科"),
                ("01", "応用実務法学科"),
            )),
            ("外国語学部", (
                ("10", "国際英語学科"),
            )),
            ("情報工学部", (
                ("20", "情報工学科"),
            )),
            ("経営学部", (
                ("30", "経営学科"),
                ("31", "国際経営学科"),
            )),
            ("人間学部", (
                ("40", "人間学科"),
            )),
            ("経済学部", (
                ("50", "経済学科"),
                ("51", "産業社会学科"),
            )),
            ("都市情報学部", (
                ("60", "都市情報学科"),
            )),
        )

        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['nickname'] = forms.CharField(initial=nickname, label="ニックネーム", required=False)
        self.fields['url'] = forms.CharField(initial=url, label="リンク", required=False)
        self.fields['date_of_birth'] = forms.CharField(initial=date_of_birth, label="誕生日", required=False)
        self.fields['grade'] = ChoiceField(choices=CHOICES_GRADE, initial=grade, label="学年", widget=forms.widgets.Select())
        self.fields['department'] = ChoiceField(choices=CHOICES_DEPARTMENT, initial=department, label="所属学科", widget=forms.widgets.Select())
        self.fields['image'] = forms.ImageField(required=False)
        self.fields['introduction'] = forms.CharField(widget=forms.Textarea, initial=introduction, label="自己紹介", required=False)

    #フォームに入力された情報でユーザー情報をアップデート
    def update(self, user):
        user.nickname = self.cleaned_data['nickname']
        user.grade = self.cleaned_data['grade']
        user.department = self.cleaned_data['department']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.image = self.cleaned_data['image']
        user.url = self.cleaned_data['url']
        user.introduction = self.cleaned_data['introduction']
        user.save()

    #画像がフォームに追加されなかった際のupdate関数
    def update_exclude_image(self, user):
        user.nickname = self.cleaned_data['nickname']
        user.grade = self.cleaned_data['grade']
        user.department = self.cleaned_data['department']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.url = self.cleaned_data['url']
        user.introduction = self.cleaned_data['introduction']
        user.save()


class CustomEmailChangeForm(forms.ModelForm):
    #Email変更のフォーム
    class Meta:
        model = MyUser
        fields = ["email"]
        labels = {"email": "メールアドレス"}

    def __init__(self, email=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['value'] = email  #登録済みの変更前のメールアドレスを予め入力しておく

    def update(self, user): #Emailをアップデート
        user.email = self.cleaned_data['email']
        user.save()


class CustomUsernameChangeForm(forms.ModelForm):
    #ユーザーネーム変更のフォーム
    class Meta:
        model = MyUser
        fields = ["username"]
        labels = {"username": "ユーザーネーム"}

    def __init__(self, username=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['value'] = username    #登録済みの変更前のusernameを予め入力しておく

    def update(self, user):
        user.username = self.cleaned_data['username']   #usernameをアップデート
        user.save()


class LoginForm(AuthenticationForm):    #ログインフォーム
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
