from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from .forms import AccountForm, CustomProfileChangeForm, LoginForm, CustomUsernameChangeForm, CustomEmailChangeForm
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.conf import settings
from .models import MyUser


class Login(LoginView):
    template_name = "user/login.html"
    form_class = LoginForm

    def form_invalid(self, form):
        messages.error(self.request, "エラーあり!!!")
        return super().form_invalid(form)


class Logout(LogoutView):
    template_name = 'app/index.html'


class AccountRegistration(TemplateView):
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

        if self.params["account_form"].is_valid():
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


class ProfileChangeView(LoginRequiredMixin, FormView):
    template_name = 'user/Settings/Mypage.html'
    form_class = CustomProfileChangeForm
    context = {}
    context["req"] = "{% url 'ProfileChange' %}"
    context['Custom_Profile_ChangeForm'] = CustomProfileChangeForm

    def get_success_url(self):
        return reverse_lazy("Profile", kwargs={"str": self.request.user.username})

    def form_valid(self, form):
        # formのupdateメソッドにログインユーザーを渡して更新
        if self.request.FILES.getlist('image', None):
            form.update(user=self.request.user)
            messages.success(self.request, "変更完了!!!")
            return super().form_valid(form)
        else:
            form.update_exclude_image(user=self.request.user)
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


class UsernameChangeView(LoginRequiredMixin, FormView):
    template_name = 'user/Settings/Mypage.html'
    form_class = CustomUsernameChangeForm
    success_url = reverse_lazy('Username')
    context = {}
    context["req"] = "{% url 'Username' %}"

    def form_valid(self, form):
        # formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        messages.success(self.request, "変更完了!!!")
        return super().form_valid(form)

    def get_form_kwargs(self):
        username = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        username.update({'username': self.request.user.username})
        return username


class EmailChangeView(LoginRequiredMixin, FormView):
    template_name = 'user/Settings/Mypage.html'
    form_class = CustomEmailChangeForm
    success_url = reverse_lazy('Email')
    context = {}
    context["req"] = "{% url 'Email' %}"

    def form_valid(self, form):
        # formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        messages.success(self.request, "変更完了!!!")
        return super().form_valid(form)

    def get_form_kwargs(self):
        email = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        email.update({'email': self.request.user.email})
        return email


@login_required(login_url="login")
def Settings(request):
    context = {}
    username = request.user.username
    context["username"] = username
    return render(request, "user/Settings/settings.html", context)


def Profile(request, **kwargs):
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
    AWS_S3_CUSTOM_DOMAIN = settings.AWS_S3_CUSTOM_DOMAIN
    context = {
        "object_list": object_list[0],
        "DEPARTMENT": DEPARTMENT,
        "S3": AWS_S3_CUSTOM_DOMAIN,
    }

    if kwargs["str"] == request.user.username:
        context["user"] = True
    else:
        context["user"] = False

    return render(request, "user/ProfileView.html", context)
