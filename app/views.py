from urllib import request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, TemplateView, FormView, ListView
from .models import Classes, Post_Note, LikeNote, Review, LikeReview, FavoriteClass, ClassesAdditionFunction
from user.models import MyUser
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostNoteForm, SearchForm, PostReviewForm
from django.conf import settings
from django.db.models import Q


def index(request):
    context = {}
    ranking = ClassesAdditionFunction.objects.order_by('count')[:5]
    context["ranking"] = ranking
    ClassID_id = ranking.values("ClassID_id")
    RankingInfo = Classes.objects.filter(pk__in=ClassID_id)
    context["RankingInfo"] = RankingInfo
    if request.user.is_authenticated:
        ClassID = list(FavoriteClass.objects.values_list('ClassID', flat=True).filter(UserId=request.user))
        obj = Classes.objects.filter(pk__in=ClassID).values()
        context["obj"] = obj
        return render(request, "app/index.html", context)

    else:
        return render(request, "app/index.html", context)


class ClassDetailView(DetailView):
    model = Classes
    form_class = PostNoteForm

    def get_context_data(self, **kwargs):
        list = ["科目名", "担当者氏名", "全開講対象学科", "年次", "クラス", "講義学期", "単位数", "必選区分", "学期_曜日_時限", "部門", "備考", "url", "講義id",
                "科目名_英字_field", "対象研究科_専攻"]
        ClassDetailes = []
        columnes = []
        context = super().get_context_data(**kwargs)

        for x in list:
            ClassDetaile = getattr(context["object"], x)

            if ClassDetaile is not None:
                columnes.append(x)
                ClassDetailes.append(ClassDetaile)

        if self.request.user.is_authenticated:
            ClassID = Classes.objects.get(講義id=self.kwargs['pk'])
            is_like = FavoriteClass.objects.filter(UserId=self.request.user.id).filter(ClassID=ClassID).count()
            if is_like == 1:
                context["like"] = "Like "
            if is_like == 0:
                context["like"] = False

        context["columnes"] = columnes
        context["ClassDetailes"] = ClassDetailes

        return context

    def post(self, request, **kwargs):
        ClassID = Classes.objects.get(講義id=kwargs["pk"])
        is_like = FavoriteClass.objects.filter(UserId=request.user.id).filter(ClassID=ClassID).count()
        if is_like == 1:
            FavoriteClassFiltered = FavoriteClass.objects.filter(UserId=request.user.id).filter(ClassID=ClassID)
            FavoriteClassFiltered.delete()
            ClassesLike = ClassesAdditionFunction.objects.get(ClassID=ClassID)
            ClassesLike.count -= 1
            ClassesLike.save()
            return redirect("ClassDetail", pk=kwargs["pk"])

        if is_like == 0:
            FavoriteClass.objects.create(UserId=MyUser.objects.get(id=request.user.id), ClassID=ClassID)
            ClassesLike, result = ClassesAdditionFunction.objects.get_or_create(ClassID=ClassID)
            ClassesLike.count += 1
            ClassesLike.save()
            return redirect("ClassDetail", pk=kwargs["pk"])


class PostNoteView(LoginRequiredMixin, FormView):
    template_name = "app/PostImage.html"
    form_class = PostNoteForm

    def form_valid(self, form):
        post_pk = self.kwargs["pk"]
        post = get_object_or_404(Classes, pk=post_pk)
        Note = form.save(commit=False)
        Note.target = post
        Note.User = MyUser.objects.get(pk=self.request.user.id)
        Note.save()
        return redirect("NoteView", pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["postimage"] = get_object_or_404(Classes, pk=self.kwargs["pk"])
        context["note_list"] = Post_Note.objects.filter(target=self.kwargs["pk"])

        return context


class PostReviewView(LoginRequiredMixin, FormView):
    form_class = PostReviewForm
    template_name = "app/PostReview.html"

    def form_valid(self, form):
        post_pk = self.kwargs["pk"]
        post = get_object_or_404(Classes, pk=post_pk)
        Review = form.save(commit=False)
        Review.ClassID = post
        Review.UserId = self.request.user
        Review.save()
        return redirect("ReviewView", pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def ReviewListView(request, **kwargs):
    context = {}
    if request.method == 'POST':
        ClassID = request.POST.get("ClassID", None)
        target_review = Review.objects.get(id=kwargs["pk"])
        is_like = LikeReview.objects.filter(UserId=request.user.id).filter(target_review=target_review).count()
        # unlike
        if is_like == 1:
            LikeReviewFiltered = LikeReview.objects.filter(UserId=request.user.id).filter(target_review=target_review)
            LikeReviewFiltered.delete()
            target_review.count -= 1
            target_review.save()
            return redirect("ReviewView", pk=ClassID)

        # like
        if is_like == 0:
            target_review.count += 1
            target_review.save()
            LikeReview.objects.create(UserId=MyUser.objects.get(id=request.user.id), target_review=target_review)
            return redirect("ReviewView", pk=ClassID)

    if Review.objects.filter(ClassID=kwargs["pk"]):
        context["Review_lists"] = Review.objects.filter(ClassID=kwargs["pk"]).values().order_by("-count")
        for x, obj in enumerate(context["Review_lists"]):
            UserId = obj["UserId_id"]
            target_review = obj["id"]
            context["Review_lists"][x]["nickname"] = list(MyUser.objects.values_list("nickname", flat=True).filter(pk=UserId))
            context["Review_lists"][x]["username"] = list(MyUser.objects.values_list("username", flat=True).filter(pk=UserId))
            if request.user.is_authenticated:
                if LikeReview.objects.filter(UserId=request.user.id, target_review=target_review):
                    context["Review_lists"][x]["Like"] = True
                else:
                    context["Review_lists"][x]["Like"] = False
        return render(request, "app/ReviewView.html", context)

    else:
        return render(request, "app/ReviewView.html", context)


class NoteView(ListView):
    model = Post_Note
    template_name = "app/NoteView.html"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        AWS_S3_CUSTOM_DOMAIN = settings.AWS_S3_CUSTOM_DOMAIN
        context["S3"] = AWS_S3_CUSTOM_DOMAIN

        if self.request.GET.getlist('checks[]'):
            checks_value = []
            value = self.request.GET.getlist('checks[]')

            for x in value:
                x = int(x)
                checks_value.append(x)
            context["object_lists"] = list(Post_Note.objects.filter(target=self.kwargs['pk']).filter(target_time__in=checks_value).values().order_by("-count"))
            context["target_time"] = checks_value

            for x, obj in enumerate(context["object_lists"]):
                UserId = obj["User_id"]
                context["object_lists"][x]["nickname"] = list(MyUser.objects.values_list("nickname", flat=True).filter(pk=UserId))
                context["object_lists"][x]["username"] = list(MyUser.objects.values_list("username", flat=True).filter(pk=UserId))
                if self.request.user.is_authenticated:
                    if LikeNote.objects.filter(User=self.request.user.id, target_note=obj["id"]):
                        context["object_lists"][x]["Like"] = True
                    else:
                        context["object_lists"][x]["Like"] = False
            return context

        else:
            context["object_lists"] = list(Post_Note.objects.filter(target=self.kwargs['pk']).values().order_by("-count"))
            for x, obj in enumerate(context["object_lists"]):
                UserId = obj["User_id"]
                context["object_lists"][x]["nickname"] = list(MyUser.objects.values_list("nickname", flat=True).filter(pk=UserId))
                context["object_lists"][x]["username"] = list(MyUser.objects.values_list("username", flat=True).filter(pk=UserId))
                if self.request.user.is_authenticated:
                    if LikeNote.objects.filter(User=self.request.user.id, target_note=obj["id"]):
                        context["object_lists"][x]["Like"] = True
                    else:
                        context["object_lists"][x]["Like"] = False
            return context

    def post(self, request, **kwargs):
        target_note = request.POST.get("target_note", None)
        Note = Post_Note.objects.get(id=target_note)
        is_like = LikeNote.objects.filter(User=request.user.id).filter(target_note=target_note).count()
        # unlike
        if is_like == 1:
            LikeNoteFiltered = LikeNote.objects.filter(User=request.user.id).filter(target_note=Note)
            LikeNoteFiltered.delete()
            Note.count -= 1
            Note.save()
            return redirect("NoteView", pk=kwargs["pk"])

        # like
        if is_like == 0:
            Note.count += 1
            Note.save()
            LikeNote.objects.create(User=MyUser.objects.get(id=request.user.id), target_note=Note)
            return redirect("NoteView", pk=kwargs["pk"])


class SearchFormView(ListView):
    model = Classes
    template_name = "app/SearchForm.html"
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm
        return context

    def get_queryset(self):
        if "search" in self.request.GET:
            #self.request.GET.get('フォームのフィールド名？', None)
            q_objects = Q()

            if self.request.GET.get('科目名', None) != "" and self.request.GET.get('科目名', None) != None:
                ClassName = self.request.GET.get('科目名', None)
                q_objects &= Q(科目名__icontains=ClassName)
            if self.request.GET.get('担当者氏名', None) != "" and self.request.GET.get('担当者氏名', None) != None:
                Teacher = self.request.GET.get('担当者氏名', None)
                q_objects &= Q(担当者氏名__icontains=Teacher)
            if self.request.GET.get('全開講対象学科', None) != "" and self.request.GET.get('全開講対象学科', None) != None:
                Target = self.request.GET.get('全開講対象学科', None)
                q_objects &= Q(全開講対象学科__icontains=Target)
            if self.request.GET.get('年次', None) != "" and self.request.GET.get('年次', None) != None:
                Grade = self.request.GET.get('年次', None)
                q_objects &= Q(年次__icontains=Grade)
            if self.request.GET.get('講義学期', None) != "" and self.request.GET.get('講義学期', None) != None:
                semester = self.request.GET.get('講義学期', None)
                q_objects &= Q(講義学期__icontains=semester)
            if self.request.GET.get('必選区分', None) != "" and self.request.GET.get('必選区分', None) != None:
                Classification = self.request.GET.get('必選区分', None)
                q_objects &= Q(必選区分__icontains=Classification)
            if self.request.GET.get('講義id', None) != "" and self.request.GET.get('講義id', None) != None:
                ID = self.request.GET.get('講義id', None)
                q_objects &= Q(講義id__icontains=ID)


            if q_objects == Q():
                object_list = Classes.objects.none().order_by("講義id")
                return object_list
            else:
                object_list = Classes.objects.filter(q_objects).order_by("講義id")
                return object_list

        else:
            return Classes.objects.none().order_by("講義id")
