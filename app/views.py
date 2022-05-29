from urllib import request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, TemplateView, FormView, ListView
from .models import Classes, Post_Note, LikeNote, Review, LikeReview, FavoriteClass, ClassesAdditionFunction
from user.models import MyUser
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostNoteForm, SearchForm, PostReviewForm
from django.conf import settings
from django.db.models import Q


def index(request): #メインページ
    context = {}
    ranking = ClassesAdditionFunction.objects.order_by('-count')[:5] #5位までのランキングをClassesAdditionFunctionから取得
    context["ranking"] = ranking
    ClassesID = ranking.values("ClassID_id")   #上で取得したランキングからクラスのIDを取得
    RankingInfo = []
    for ClassID in ClassesID:
        RankingInfo.append(Classes.objects.filter(pk=ClassID['ClassID_id']).values()) #ランキングに乗った授業の情報を取得
    context["RankingInfo"] = RankingInfo
    if request.user.is_authenticated:   #ログイン済みの時の処理
        ClassID = list(FavoriteClass.objects.values_list('ClassID', flat=True).filter(UserId=request.user)) #自分の登録しているクラスIDをリストで取得
        obj = Classes.objects.filter(pk__in=ClassID).values()   #授業の情報を変数objに入れて取得
        context["obj"] = obj
        return render(request, "app/index.html", context)

    else:
        return render(request, "app/index.html", context)


class ClassDetailView(DetailView):  #クラスの詳細な情報を表示するビュー
    model = Classes
    form_class = PostNoteForm

    def get_context_data(self, **kwargs):
        list = ["科目名", "担当者氏名", "全開講対象学科", "年次", "クラス", "講義学期", "単位数", "必選区分", "学期_曜日_時限", "部門", "備考", "url", "講義id",
                "科目名_英字_field", "対象研究科_専攻"]
        ClassDetailes = []
        columnes = []
        context = super().get_context_data(**kwargs)

        for x in list:
            ClassDetail = getattr(context["object"], x) #取得したcontextからxについての情報を取得

            if ClassDetail is not None: #xについての情報が存在した場合カラムと情報を追加。
                columnes.append(x)
                ClassDetailes.append(ClassDetail)

        if self.request.user.is_authenticated:  #ログイン中の場合の処理
            ClassID = Classes.objects.get(講義id=self.kwargs['pk'])   #ClassIDを取得
            is_like = FavoriteClass.objects.filter(UserId=self.request.user.id).filter(ClassID=ClassID).count() #いいねしているかしていないかの情報を取得
            if is_like == 1:    #いいねしていた場合Trueを入れ、テンプレート側で登録を外すボタンを表示
                context["like"] = True
            if is_like == 0:    #いいねしていた場合Falseを入れ、テンプレート側で登録ボタンを表示
                context["like"] = False

        context["columnes"] = columnes
        context["ClassDetailes"] = ClassDetailes

        return context

    def post(self, request, **kwargs):  #Postメソッド、つまりいいねが押されたときの処理
        ClassID = Classes.objects.get(講義id=kwargs["pk"])
        is_like = FavoriteClass.objects.filter(UserId=request.user.id).filter(ClassID=ClassID).count()
        if is_like == 1:    #いいねがiだったら、つまりいいねが押されていた時の処理
            FavoriteClassFiltered = FavoriteClass.objects.filter(UserId=request.user.id).filter(ClassID=ClassID)
            FavoriteClassFiltered.delete()  #ユーザーのいいねを削除
            ClassesLike = ClassesAdditionFunction.objects.get(ClassID=ClassID)
            ClassesLike.count -= 1  #ランキングで使う全体のいいね数を1減らす
            ClassesLike.save()
            return redirect("ClassDetail", pk=kwargs["pk"])

        if is_like == 0:
            FavoriteClass.objects.create(UserId=MyUser.objects.get(id=request.user.id), ClassID=ClassID)    #ユーザーのいいねを作成
            ClassesLike, result = ClassesAdditionFunction.objects.get_or_create(ClassID=ClassID)    #データが作成されていなかった場合Create、存在していた場合はgetする。
            ClassesLike.count += 1  #ランキングで使う全体のいいね数を1増やす
            ClassesLike.save()
            return redirect("ClassDetail", pk=kwargs["pk"])


class PostNoteView(LoginRequiredMixin, FormView):   #ノートを投稿するビュー
    template_name = "app/PostImage.html"
    form_class = PostNoteForm

    def form_valid(self, form): #フォームがポストされたとき
        post_pk = self.kwargs["pk"]
        post = get_object_or_404(Classes, pk=post_pk)   #Classesをpkで検索、なければ404エラーを返す。
        Note = form.save(commit=False)
        Note.target = post  #Noteと該当の講義を結びつける
        Note.User = MyUser.objects.get(pk=self.request.user.id) #Noteを誰が投稿したか結びつける
        Note.save()
        return redirect("NoteView", pk=post_pk)


class PostReviewView(LoginRequiredMixin, FormView): #レビューを投稿する時のビュー
    form_class = PostReviewForm
    template_name = "app/PostReview.html"

    def form_valid(self, form): #フォームがPostされた時の処理
        post_pk = self.kwargs["pk"]
        Review = form.save(commit=False)
        Review.ClassID = get_object_or_404(Classes, pk=post_pk) #ClassIDGet、なければ404エラーを返す
        Review.UserId = self.request.user   #ユーザー情報を取得
        Review.save()
        return redirect("ReviewView", pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def ReviewListView(request, **kwargs):  #
    context = {}
    if request.method == 'POST':    #Post、つまりいいねされた時の処理
        ClassID = request.POST.get("ClassID", None)
        target_review = Review.objects.get(id=kwargs["pk"])
        is_like = LikeReview.objects.filter(UserId=request.user.id).filter(target_review=target_review).count() #現在ログイン中のユーザーがいいねしてるかの値を取得

        if is_like == 1:    #いいねしていた場合
            LikeReviewFiltered = LikeReview.objects.filter(UserId=request.user.id).filter(target_review=target_review)
            LikeReviewFiltered.delete() #ユーザーのいいねを削除
            target_review.count -= 1    #いいね数を1つ減らす
            target_review.save()
            return redirect("ReviewView", pk=ClassID)

        # like
        if is_like == 0:    #いいねしていなかった場合
            target_review.count += 1    #いいねを1足す
            target_review.save()
            LikeReview.objects.create(UserId=MyUser.objects.get(id=request.user.id), target_review=target_review)   #ユーザーのいいねを作成
            return redirect("ReviewView", pk=ClassID)

    if Review.objects.filter(ClassID=kwargs["pk"]): #レビューが存在していた場合の処理
        context["Review_lists"] = Review.objects.filter(ClassID=kwargs["pk"]).values().order_by("-count")   #レビューを取得していいね順に並べる
        for x, obj in enumerate(context["Review_lists"]):
            UserId = obj["UserId_id"]   #レビューを投稿した人の名前を取得
            target_review = obj["id"]   #レビューのIDを取得
            context["Review_lists"][x]["nickname"] = list(MyUser.objects.values_list("nickname", flat=True).filter(pk=UserId))  #レビュー投稿者のニックネームを取得
            context["Review_lists"][x]["username"] = list(MyUser.objects.values_list("username", flat=True).filter(pk=UserId))  #レビュー投稿者のユーザーネームを取得
            if request.user.is_authenticated:   #ログイン中だった場合
                if LikeReview.objects.filter(UserId=request.user.id, target_review=target_review):  #いいねしていた場合Trueを
                    context["Review_lists"][x]["Like"] = True
                else:                                                                               #いいねしていなかった場合Falseを
                    context["Review_lists"][x]["Like"] = False
        return render(request, "app/ReviewView.html", context)

    else:
        return render(request, "app/ReviewView.html", context)


class NoteView(ListView):   #ノートを見るビュー
    model = Post_Note
    template_name = "app/NoteView.html"
    paginate_by = 100   #1ページに表示する量

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        AWS_S3_CUSTOM_DOMAIN = settings.AWS_S3_CUSTOM_DOMAIN    #HTMLに表示するためにS3のURLを取得
        context["S3"] = AWS_S3_CUSTOM_DOMAIN

        if self.request.GET.getlist('checks[]'):    #チェックボックスにチェックが入っていた時に実行
            checks_value = []
            value = self.request.GET.getlist('checks[]')    #チェックボックスの値を取得

            for x in value:
                x = int(x)
                checks_value.append(x)
            #チェックボックスに入れられた値で絞り込み、いいね順に並び替える。
            context["object_lists"] = list(Post_Note.objects.filter(target=self.kwargs['pk']).filter(target_time__in=checks_value).values().order_by("-count"))
            context["target_time"] = checks_value

            for x, obj in enumerate(context["object_lists"]):
                UserId = obj["User_id"]     #ノートを投稿した人の名前を取得
                context["object_lists"][x]["nickname"] = list(MyUser.objects.values_list("nickname", flat=True).filter(pk=UserId))  #ノートを投稿した人のニックネームを取得
                context["object_lists"][x]["username"] = list(MyUser.objects.values_list("username", flat=True).filter(pk=UserId))  #ノートを投稿した人のユーザーネームを取得
                if self.request.user.is_authenticated:  #ログイン中の場合の処理
                    if LikeNote.objects.filter(User=self.request.user.id, target_note=obj["id"]):   #いいねをしていたらTrue
                        context["object_lists"][x]["Like"] = True
                    else:                                                                           #いいねしてなかったらFalse
                        context["object_lists"][x]["Like"] = False
            return context

        else:   #チェックがなかった時の処理、チェックボックスの値を処理する以外は上のif文と概ね同様の処理。
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

    def post(self, request, **kwargs):  #Post、つまりいいねされた時の処理
        target_note = request.POST.get("target_note", None)
        Note = Post_Note.objects.get(id=target_note)
        is_like = LikeNote.objects.filter(User=request.user.id).filter(target_note=target_note).count() #いいねの値を取得
        # unlike
        if is_like == 1:    #いいねされていたら
            LikeNoteFiltered = LikeNote.objects.filter(User=request.user.id).filter(target_note=Note)
            LikeNoteFiltered.delete()   #ユーザーのいいねを削除
            Note.count -= 1             #いいねカウントを1減らす
            Note.save()
            return redirect("NoteView", pk=kwargs["pk"])

        # like
        if is_like == 0:
            Note.count += 1 #いいねカウントを1増やす
            Note.save()
            LikeNote.objects.create(User=MyUser.objects.get(id=request.user.id), target_note=Note)  #ユーザーのいいねをクリエイト
            return redirect("NoteView", pk=kwargs["pk"])


class SearchFormView(ListView): #検索ビュー
    model = Classes
    template_name = "app/SearchForm.html"
    paginate_by = 100   #一度に表示する数を表示

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm #フォームを受け渡す
        return context

    def get_queryset(self):
        if "search" in self.request.GET:
            #self.request.GET.get('フォームのフィールド名？', None)
            q_objects = Q() #Qオブジェクトを用いて&検索

            if self.request.GET.get('科目名', None) != "" and self.request.GET.get('科目名', None) != None:   #もし空白かつNoneでは無い時Qオブジェクトに追加、以下同様
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


            if q_objects == Q():    #もしq_objectsが初期のままで何も追加されていないのなら何も検索結果に表示しない
                object_list = Classes.objects.none().order_by("講義id")
                return object_list
            else:   #Qオブジェクトを用いて検索し講義id順に並べる。
                object_list = Classes.objects.filter(q_objects).order_by("講義id")
                return object_list

        else:   #何も検索結果に表示しない
            return Classes.objects.none().order_by("講義id")
