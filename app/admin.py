from django.contrib import admin
from .models import Classes, Post_Note, LikeNote, Review, LikeReview, FavoriteClass

admin.site.register(Classes)
admin.site.register(Post_Note)
admin.site.register(LikeNote)
admin.site.register(Review)
admin.site.register(LikeReview)
admin.site.register(FavoriteClass)
# Register your models here.
