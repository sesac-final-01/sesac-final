from django.urls import path
from . import views

app_name = 'lectures'
urlpatterns = [
    path('lists/', views.LectureListGetView.as_view(), name='lecture-list'),
    path('lists/search/', views.LectureSearchView.as_view(), name='search-lecture'),
    path('apply/', views.LectureApplyView.as_view(), name='lecture-apply'),
    path('cancel/', views.LectureCancelView.as_view(), name='lecture-cancel'),
    path('my-lectures/', views.MyLectureRetrieveView.as_view(), name='my-lectures'),
]
