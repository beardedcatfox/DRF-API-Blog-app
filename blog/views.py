from blog.forms import AuthorChangeForm, AuthorProfileForm, AuthorRegisterForm, PostForm
from blog.models import Author, Post

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView

from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import PostSerial


def register(request):
    if request.method == 'POST':
        form = AuthorRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = AuthorRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('post_list')


def logout_view(request):
    logout(request)
    return redirect('post_list')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    paginate_by = 10


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    queryset = Post.objects.filter(is_published=True).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        paginator = Paginator(self.queryset, self.paginate_by)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(Author, username=self.kwargs.get('username'))
        return Post.objects.filter(owner=user, is_published=True).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = get_object_or_404(Author, username=self.kwargs.get('username'))
        return context


def user_profile(request, username):
    user = get_object_or_404(Author, username=username)
    return render(request, 'blog/user_profile.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = AuthorChangeForm(request.POST, instance=request.user)
        profile_form = AuthorProfileForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            if not request.user.is_superuser and user.is_superuser:
                messages.error(request, 'Good try)')
                return redirect('edit_profile')
            user.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = AuthorChangeForm(instance=request.user)
        profile_form = AuthorProfileForm(instance=request.user)
    return render(request, 'blog/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'blog/password.html'
    success_url = reverse_lazy('edit_profile')


###  API  ###

class PostDRFAPIPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostDRFAPI(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerial
    permission_classes = (IsOwnerOrReadOnly, )
    pagination_class = PostDRFAPIPagination


class PostUpdateDRFAPI(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerial
    permission_classes = (IsOwnerOrReadOnly,)


class PostUpdateDelDRFAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerial
    permission_classes = (IsAdminOrReadOnly, IsOwnerOrReadOnly)


# ViewSet
class AuthorPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerial

    @action(methods=['get'], detail=False)
    def authors(selfs, request):
        authors = Author.objects.all()
        return Response({"Authors": [e.email for e in authors]})
