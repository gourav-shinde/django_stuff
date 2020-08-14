
from django.urls import path,include

from .views import (quiz_view,createquiz_view,question_view,quiz_detail_view,question_delete,quiz_delete,quiz_edit,
                    quiz_stud,quiz_dock,quiz_trans,quiz_back,quiz_end,score_view
                    #json
                    ,quiz_student_list,quiz_jview)

app_name="quizzes"
urlpatterns = [
path('',quiz_view,name="quizy"),
path("jquiz",quiz_jview),
path('delete/<slug:my_id>',quiz_delete,name="quizy_delete"),
path('edit/<slug:my_id>',quiz_edit,name="quizy_edit"),
path('create',createquiz_view,name="create_quizy"),

path('question/<slug:my_id>/<int:num>/<int:flag>',question_view,name="question"),
path('question/<slug:my_id>/<int:num>/delete',question_delete,name="question_delete"),


path('view/<slug:my_id>',quiz_detail_view,name="quiz_view"),

path('scores/<slug:my_id>',score_view,name="score"),

# path('view',quiz_stud,name="quiz_stud"),  delete this
path('view',quiz_student_list,name="quiz_stud"),

path('trans/<slug:my_id>',quiz_trans,name="quiz_trans"),
path('back/<slug:my_id>',quiz_back,name="quiz_back"),
path('dock/<slug:my_id>',quiz_dock,name="quiz_dock"),
path('end/<slug:my_id>/<int:score>',quiz_end,name="quiz_end"),

    
]

