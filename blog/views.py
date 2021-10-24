import django.contrib.auth.forms
import django.contrib.auth.models
import django.contrib.auth.views
import numpy.distutils.fcompiler.none
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout

from .forms import EmailPost, ComentarioModelForm, CadUsuarioForm
from .models import Post, Comentario

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


class ListarPostsView(ListView):
    queryset = Post.publicados.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = "blog/post/listarposts.html"


class DetalharPostView(DetailView):
    template_name = "blog/post/detalharpost.html"
    model = Post


    def _get_coments(self, id_post):
        try:
            return Comentario.objects.filter(post_id=id_post)
        except Comentario.DoesNotExist:
            raise Exception


    def get_context_data(self, **kwargs):
        context = super(DetalharPostView, self).get_context_data(**kwargs)
        context['coments'] = self._get_coments(self.object.id)
        return context


class FormContatoView(FormView):
    template_name = 'blog/post/sharepost.html'
    form_class = EmailPost
    success_url = reverse_lazy('blog:listar_posts')

    def get_post(self, id_post):
        try:
            return Post.publicados.get(pk=id_post)
        except Post.DoesNotExist:
            messages.error(self.request, 'O post nao existe!')
            reverse_lazy('blog:listar_posts')

    def get_context_data(self, **kwargs):
        context = super(FormContatoView, self).get_context_data(**kwargs)
        context['post'] = self.get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form, *args, **kwargs):
        meupost = self.get_context_data()['post']
        form.enviar_email(meupost)
        messages.success(self.request, f'Post {meupost.titulo}'  f'enviado com sucesso.')
        return super(FormContatoView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        meupost = self.get_context_data()['post']
        messages.error(self.request, f'Post {meupost.titulo}' f'nao enviado.')
        return super(FormContatoView, self).form_invalid(form, *args, **kwargs)


class ComentarioView(CreateView):
    template_name = 'blog/post/comentarios.html'
    form_class = ComentarioModelForm

    def _get_post(self, id_post):
        try:
            post = Post.publicados.get(pk=id_post)
            return post
        except Post.DoesNotExist:
            raise Exception

    def get_context_data(self, **kwargs):
        context = super(ComentarioView, self).get_context_data(**kwargs)
        context['post'] = self._get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form, *args, **kwargs):
        post = self._get_post(self.kwargs['pk'])
        form.salvar_comentario(post)
        return redirect('blog:detalhe', post.slug)


class CadUsuarioView(CreateView):
    template_name = 'blog/usuarios/cadusuario.html'
    form_class = CadUsuarioForm
    success_url = reverse_lazy('blog:loginuser')

    def form_valid(self, form, *args, **kwargs):
        form.cleaned_data
        form.save()
        messages.success(self.request, f'Usuario cadastrado com sucesso!!!')
        return super(CadUsuarioView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.success(self.request, f'Usuario nao cadastrado')
        return super(CadUsuarioView, self).form_invalid(form, *args, **kwargs)


class LoginUsuarioView(FormView):
    template_name = 'blog/usuarios/login.html'
    model = django.contrib.auth.models.User
    form_class = django.contrib.auth.forms.AuthenticationForm
    success_url = reverse_lazy('blog:listar_posts')

    def form_valid(self, form):
        nome = form.cleaned_data['username']
        senha = form.cleaned_data['password']
        usuario = django.contrib.auth.authenticate(self.request, username=nome, password=senha)
        if usuario is not None:
            django.contrib.auth.login(self.request, usuario)
            return redirect('blog:listar_posts')
        messages.error(self.request, f"Usuario nao existe")
        return redirect('blog:loginuser')

    def form_invalid(self, form):
        messages.success(self.request, f'Impossivel logar!!!')
        return redirect('blog:listar_posts')


class LogoutUsuarioView(LoginRequiredMixin, LogoutView):

    def get(self, request):
        logout(request)
        return redirect('blog:listar_posts')




