from django.conf.urls.static import static
from django.urls import path,include
from django.conf import settings
from .views import (quiz_view,createquiz_view,question_view)

app_name="quizzes"
urlpatterns = [
path('',quiz_view,name="quizy"),
path('create',createquiz_view,name="create_quizy"),
path('question/<slug:my_id>/<int:num>',question_view,name="question"),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
