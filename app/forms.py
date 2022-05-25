from .models import Post_Note, LikeNote, Classes, Review, LikeReview
from django import forms





class PostNoteForm(forms.ModelForm):
    class Meta:
        model = Post_Note
        exclude = ('created_at', 'target', "User", "count")

    CHOICES_TIME = (
        (1, "第1回"), (2, "第2回"), (3, "第3回"), (4, "第4回"),
        (5, "第5回"), (6, "第6回"), (7, "第7回"), (8, "第8回"),
        (9, "第9回"), (10, "第10回"), (11, "第11回"), (12, "第12回"),
        (13, "第13回"), (14, "第14回"), (15, "第15回"), (0, "その他"),
    )
    text = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField()
    target_time = forms.ChoiceField(widget=forms.widgets.Select, choices=CHOICES_TIME, required=False, label="講義回")

class PostReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('created_at', 'ClassID', "UserId", "count")

    text = forms.CharField(label="本文", required=False)
    test = forms.CharField(label="テスト")
    attendance = forms.CharField(label="出席", required=False)
    EasyRating = forms.ChoiceField(label="楽単度", choices=((5,"5"), (4,"4"), (3,"3"), (2,"2"), (1,"1")))
    fullnessRating = forms.ChoiceField(label="充実度", choices=((5,"5"), (4,"4"), (3,"3"), (2,"2"), (1,"1")))


class SearchForm(forms.Form):
    def CHOICE_DEPARTMENT():
        departments_query_set = Classes.objects.values("全開講対象学科").distinct().order_by("全開講対象学科")
        department_list = list(departments_query_set)
        department_tuple_list = [(None, None)]
        for department in department_list:
            if department["全開講対象学科"] == None:
                pass
            else:
                department[department["全開講対象学科"]] = department["全開講対象学科"]
                del department["全開講対象学科"]
                department_tuple = tuple(department.values())

                if department_tuple[0] == "理工学部数学科理工学部情報工学科":
                    pass

                elif department_tuple[0] == "理工学部数学科農学部生物資源学科":
                    pass

                elif len(department_tuple[0]) <= 15:
                    department_tuple = tuple(department.values())
                    department_tuple = department_tuple + department_tuple
                    department_tuple_list.append(department_tuple)

        Choices = tuple(department_tuple_list)
        return Choices

    class Meta:
        model = Classes
        exclude = ("備考", "学期_曜日_時限", "単位数", "クラス", "url", "部門", "対象研究科_専攻")
    CHOICE_DEPARTMENT = CHOICE_DEPARTMENT()
    CHOICE_GRADE = (
            (None, "None"),
            ("１年次", "1年次"),
            ("２年次", "2年次"),
            ("３年次", "3年次"),
            ("４年次", "4年次"),
            ("５年次", "5年次"),
            ("６年次", "6年次"),
    )
    CHOICE_TERM = (
            (None, "None"),
            ("前期", "前期"),
            ("前期集中", "前期集中"),
            ("後期", "後期"),
            ("後期集中", "後期集中"),
            ("通年", "通年"),
            ("集中", "集中"),
    )
    CHOICE_CLASSE = (
        (None, "None"),
        ("選択科目", "選択科目"),
        ("選択必修科目", "選択必修科目"),
        ("必修科目", "必修科目"),
    )

    科目名 = forms.CharField(label="科目名", required=False)
    担当者氏名 = forms.CharField(required=False)
    全開講対象学科 = forms.ChoiceField(choices=CHOICE_DEPARTMENT, required=False)
    年次 = forms.ChoiceField(choices=CHOICE_GRADE, required=False)
    講義学期 = forms.ChoiceField(choices=CHOICE_TERM, required=False)
    必選区分 = forms.ChoiceField(choices=CHOICE_CLASSE, required=False)
    講義id = forms.IntegerField(required=False)
