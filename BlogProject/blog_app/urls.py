from django.urls import path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('post/list/page<int:page>/',views.PostListView.as_view(),name='list'),
    path('post/create/',views.PostCreateView.as_view(),name='create'),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name='detail'),
    path('post/<int:pk>/edit/',views.PostEditView.as_view(),name='edit'),
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(),name='delete'),
    path('post/user/<username>/page<int:page>/',views.UserPostsListView.as_view(),name='user_post'),
    path('post/<int:post_pk>/comments/create/',views.comment_create_view,name='comment_create'),
    path('post/<int:post_pk>/comments/<int:pk>/edit/',views.CommentEditView.as_view(),name='comment_edit'),
    path('post/<int:post_pk>/comments/<int:pk>/delete/',views.CommentDeleteView.as_view(),name='comment_delete'),
    path('post/<int:post_pk>/like/',views.post_like_view,name='post_like'),
]
