from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import FormView, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.viewsets import GenericViewSet

from photos.forms import CommentForm, SearchForm, PhotoForm
from photos.models import Comment, Photo

from rest_framework import mixins

from api.serializers import PhotoSerializer


# Create your views here.
class PhotoViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class HomeView(ListView):
    template_name = "home.html"
    model = Photo
    context_object_name = 'photos'
    ordering = ('-date_publish',)
    extra_context = {"comments": Comment.objects.all()}

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):

        queryset = super().get_queryset().all()  # .exclude(is_deleted=True)
        if self.search_value:
            query = Q(author__full_name__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        context['comment_form'] = CommentForm()
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context


class CommentAddView(LoginRequiredMixin, FormView):
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=kwargs.get('pk'))
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            if text:
                curr_user = request.user
                comment = Comment()
                comment.photo = photo
                comment.text = text
                comment.author = curr_user
                comment.save()
                messages.success(request, 'Комментарий к фото добавлено!')
            else:
                messages.warning(request, 'Комментарий к фото не добавлено!')
        return redirect('home')

фото
class PhotoDetailView(DetailView):
    template_name = 'photo_detail.html'
    model = Photo
    extra_context = {'comments': Comment.objects.all()}


class PhotoUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = 'photo_update.html'
    form_class = PhotoForm
    model = Photo
    success_message = 'Фото обновлено!'

    def get_success_url(self):
        return reverse('photo_detail', kwargs={'pk': self.object.pk})


class PhotoDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'photo_confirm_delete.html'
    model = Photo
    success_url = reverse_lazy('home')
    success_message = 'Фото удалено!'


class PhotoCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'photo_create.html'
    model = Photo
    form_class = PhotoForm
    success_message = 'Фото создано!'

    def get_success_url(self):
        return reverse('photo_detail', kwargs={'pk': self.object.pk})


def create_blank(request: WSGIRequest):
    if request.method == "GET":
        photo = Photo()
        photo.author = request.user
        print(photo.image)
        photo.save()
        return redirect(reverse('photo_update', kwargs={'pk': photo.pk}))
    return redirect('home')

def photo_check(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if photo.description == '' and photo.is_new and ('blank.jpg' in str(photo.image)):
        photo.delete()
        return redirect('home')
    elif photo.is_new and not('blank.jpg' in photo.image):
            photo.is_new = False
            photo.save()
    return redirect(reverse('photo_detail', kwargs={'pk': photo.pk}))
