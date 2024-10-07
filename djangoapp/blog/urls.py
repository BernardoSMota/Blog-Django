from django.urls import path
from blog.views import PageDeatailView, PostDeatailView, AuthorsListView, CategoriesListView, TagsListView, SearchListView, IndexListView

app_name = 'blog'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('page/<slug:slug>/', PageDeatailView.as_view(), name='page'),
    path('post/<slug:slug>/', PostDeatailView.as_view(), name='post'),
    path('authors/<int:author_id>/', AuthorsListView.as_view(), name='authors'),
    path('categories/<slug:slug>/', CategoriesListView.as_view(), name='categories'),
    path('tags/<slug:slug>/', TagsListView.as_view(), name='tags'),
    path('search/', SearchListView.as_view(), name='search'),
]


