from django.db import models
from utils.random_letters import slugfy_new
from django.contrib.auth.models import User
from utils.resize_images import resize_image
from django_summernote.models import AbstractAttachment
from django.urls import reverse

class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)

        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name
        
        if file_changed:
            resize_image(image_django=self.file, new_width=900, quality=70)

        return super_save


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, blank=True, default=None, null=True, max_length=128)

    def save(self, *args, **kwargs):
        if not self.slug:
             self.slug = slugfy_new(self.name, 5)

        return super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, blank=True, default=None, null=True, max_length=128)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug =  slugfy_new(self.name, 5)

        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name


class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, default="", null=False, blank=True, max_length=128)
    is_published = models.BooleanField(default=False, help_text='A página somente será exibida caso essa opção esteja marcada')
    content = models.TextField()

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        else:
            return reverse('blog:page', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title, 5)

        return super().save(*args, **kwargs)
    

    def __str__(self) -> str:
        return self.title
    

class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).order_by('-pk')   


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    objects = PostManager()

    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, default="", null=False, blank=True, max_length=128)
    summary = models.CharField(max_length=128)
    is_published = models.BooleanField(default=False, help_text='O post somente será exibida caso essa opção esteja marcada')
    content = models.TextField(null=True, blank=True, default=None)

    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default=None)
    cover_in_post_content = models.BooleanField(default=True, help_text='A capa somente será exibida dentro do post caso essa opção esteja marcada')

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='post_created_by')

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='post_updated_by')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    tags = models.ManyToManyField(Tag, blank=True, default=None)

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        else:
            return reverse('blog:post', args=(self.slug,))
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title, 5)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)

        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name
        
        if cover_changed:
            resize_image(image_django=self.cover, new_width=900, quality=70)

        return super_save

    def __str__(self) -> str:
        return self.title
