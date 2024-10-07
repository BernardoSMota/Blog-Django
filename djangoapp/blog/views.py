from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.db.models import Q
from blog.models import Post, Page, Tag
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView

PER_PAGE = 9

class IndexListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)

        context.update({'windowTitle': 'Home - '})

        return context


class AuthorsListView(IndexListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_vars = {}

    def get(self, request, *args, **kwargs):
        author_id = self.kwargs.get('author_id')
        user = User.objects.filter(id=author_id).first()
        
        if user is None:

            raise Http404

        self._temp_vars.update({
            'author_id': author_id, 
            'user': user,
            })
        
        return super().get(request, *args, **kwargs)    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        
        user = self._temp_vars['user']
        user_full_name = f'{user.first_name} {user.last_name}' if user.first_name else user.username

        page_title = f'Posts de {user_full_name} -'

        
        context.update({'windowTitle': page_title})

        return context
    
    def get_queryset(self):
        querryset = super().get_queryset()
        author_id = self._temp_vars['author_id']
        querryset = querryset.filter(created_by__id=author_id)

        return querryset


class CategoriesListView(IndexListView):
    allow_empty = False
    
    
    def get_queryset(self) -> QuerySet[Any]:
        slug = self.kwargs.get('slug')
        return super().get_queryset().filter(category__slug=slug)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'Categorias - {self.object_list[0].category} - '
        
        context.update({'windowTitle': page_title})
        return context
        

class TagsListView(IndexListView):
    allow_empty = False
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        slug = self.kwargs.get('slug')
        name = Tag.objects.filter(slug=slug).first().name
        page_title = f'Tags - {name} - '
        

        context.update({'windowTitle': page_title})
        return context
    
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        
        return super().get_queryset().filter(tags__slug=slug)


class SearchListView(IndexListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._search_value = ''
    
        
    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search').strip()
        return super().setup(request, *args, **kwargs)
    
    
    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index') 
        return super().get(request, *args, **kwargs)
        
    
    def get_queryset(self):
        return super().get_queryset().filter(Q(title__icontains=self._search_value) | Q(summary__icontains=self._search_value))[:PER_PAGE]
    
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'{self._search_value[0:30]} - '
        context.update({'windowTitle': page_title, 'search_value': self._search_value})
        return context


class PageDeatailView(DetailView):
    template_name = 'blog/pages/page.html'
    model = Page
    slug_field = 'slug'
    context_object_name = 'page'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'{page.title} - '
        context.update({'windowTitle': page_title})
        
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)


class PostDeatailView(DetailView):
    template_name = 'blog/pages/post.html'
    model = Post
    context_object_name = 'post'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)
    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        
        post = self.get_object()
        page_title = f'{post.title} - '
        
        ctx.update({'windowTitle': page_title})
        
        return ctx