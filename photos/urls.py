from django.urls import path
from photos.views import CommentAddView, PhotoDetailView, photo_check, PhotoUpdateView, PhotoDeleteView, create_blank

urlpatterns = [
    path('comment_add/<int:pk>', CommentAddView.as_view(), name='comment_add'),
    path('photo/<int:pk>/view/', PhotoDetailView.as_view(), name='photo_detail'),
    path('photo/add/', create_blank, name='photo_add'),
    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='photo_update'),
    path('photo/<int:pk>/check/', photo_check, name='photo_check'),
    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo_delete'),
    path('photo/<int:pk>/confirm_delete/', PhotoDeleteView.as_view(), name='confirm_delete'),
]