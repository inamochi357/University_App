from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from .forms import AccountForm, CustomProfileChangeForm, LoginForm, CustomUsernameChangeForm, CustomEmailChangeForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.conf import settings
from .models import MyUser


class Login(LoginView): #ログインビュー
    template_name = "user/login.html"
    form_class = LoginForm  #ログインフォーム

    def form_invalid(self, form):   #エラー時の処理
        messages.error(self.request, "エラーあり!!!")
        return super().form_invalid(form)


class Logout(LogoutView):   #ログアウトビュー
    template_name = 'app/index.html'


class AccountRegistration(TemplateView):    #アカウント登録のピュー
    def __init__(self):
        self.params = {
            "AccountCreate": False,
            "account_form": AccountForm(),
        }

    def get(self, request):
        self.params["account_form"] = AccountForm()
        self.params["AccountCreate"] = False
        return render(request, "user/register.html", context=self.params)

    def post(self, request):
        self.params["account_form"] = AccountForm(data=request.POST)

        if self.params["account_form"].is_valid():  #フォームが有効な場合
            print("success!!")
            account = self.params["account_form"].save()
            account.set_password(account.password)
            user = self.params["account_form"].save()
            account.save()
            messages.success(self.request, "登録完了！")
            self.params["AccountCreate"] = True
            login(request, user)

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request, "user/register.html", context=self.params)


class ProfileChangeView(LoginRequiredMixin, FormView):  #プロフィールを変更するビュー
    template_name = 'user/Settings/Mypage.html'
    form_class = CustomProfileChangeForm    #フォームを指定
    context = {}

    def get_success_url(self):  #成功した場合の転送先URL
        return reverse_lazy("Profile", kwargs={"str": self.request.user.username})

    def form_valid(self, form): #フォームPostされたとき
        # formのupdateメソッドにログインユーザーを渡して更新
        if self.request.FILES.getlist('image', None):   #画像も更新された場合
            form.update(user=self.request.user)
            messages.success(self.request, "変更完了!!!")
            return super().form_valid(form)
        else:
            form.update_exclude_image(user=self.request.user)   #画像が更新されなかった場合画像以外のフォームを更新する。
            messages.success(self.request, "変更完了!!!")
            return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'nickname': self.request.user.nickname,
            'grade': self.request.user.grade,
            'department': self.request.user.department,
            'date_of_birth': self.request.user.date_of_birth,
            'image': self.request.user.image,
            'url': self.request.user.url,
            'introduction': self.request.user.introduction,
        })
        return kwargs


class UsernameChangeView(LoginRequiredMixin, FormView): #ユーザーネームを変更するビュー
    template_name = 'user/Settings/Mypage.html'
    form_class = CustomUsernameChangeForm
    success_url = reverse_lazy('Username')
    context = {}

    def form_valid(self, form): #フォームがPostされたとき
        # formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        messages.success(self.request, "変更完了!!!")
        return super().form_valid(form)

    def get_form_kwargs(self):
        username = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        username.update({'username': self.request.user.username})
        return username


class EmailChangeView(LoginRequiredMixin, FormView):    #Emailを変更するビュー
    template_name = 'user/Settings/Mypage.html'
    form_class = CustomEmailChangeForm
    success_url = reverse_lazy('Email')
    context = {}

    def form_valid(self, form): #フォームがPostされたとき
        # formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        messages.success(self.request, "変更完了!!!")
        return super().form_valid(form)

    def get_form_kwargs(self):
        email = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        email.update({'email': self.request.user.email})
        return email


@login_required(login_url="login")  #ログインが必要
def Settings(request):  #ログインユーザーの設定ページを開く
    context = {}
    username = request.user.username
    context["username"] = username
    return render(request, "user/Settings/settings.html", context)


def Profile(request, **kwargs): #プロフィールページを開く
    #学部学科のリスト
    Department_list = {
        None: "",
        "00": "法学部法学科",
        "01": "法学部応用実務法学科",
        "10": "外国語学部国際英語学科",
        "20": "情報工学部情報工学科",
        "30": "経営学部経営学科",
        "31": "経営学部国際経営学科",
        "40": "人間学部人間学科",
        "50": "経済学部経済学科",
        "51": "経済学部産業社会学科",
        "60": "都市情報学部都市情報学科",
    }

    object_list = MyUser.objects.filter(username=kwargs["str"]).values()
    DEPARTMENT = Department_list[object_list[0]["department"]]
    AWS_S3_CUSTOM_DOMAIN = settings.AWS_S3_CUSTOM_DOMAIN    #設定からS3のドメインを読み込む
    context = {
        "object_list": object_list[0],
        "DEPARTMENT": DEPARTMENT,
        "S3": AWS_S3_CUSTOM_DOMAIN,
    }

    if kwargs["str"] == request.user.username:  #もし自身のプロフィールを開いた場合Trueを渡しプロフィール編集ボタンを表示させる。
        context["user"] = True
    else:
        context["user"] = False

    return render(request, "user/ProfileView.html", context)
