from django.views import generic
from . import models
from . import forms
from accounts.models import User
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import (Http404,HttpResponseRedirect,JsonResponse)
from django import forms as django_forms
from django.contrib import messages


# Create your views here.
class PostListView(generic.ListView):
    model = models.Post
    paginate_by = 3
    paginate_orphans =1


class UserPostsListView(generic.ListView):
    template_name='blog_app/user_post_list.html'
    model = models.Post
    paginate_by = 3
    paginate_orphans = 1

    def get_queryset(self):
        try:
            self.post_user = get_object_or_404(User,username=self.kwargs['username'])
        except(User.DoesNotExist):
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['post_user']=self.post_user
        return context_data



class PostDetailView(generic.DetailView):
    model = models.Post

    def get_success_url(self):
        return reverse('blog_app:detail',kwargs={'pk':self.kwargs['pk']})

    def get_context_data(self,**kwargs):
        context_data = super().get_context_data(**kwargs)

        if models.Like.objects.filter(post__pk=self.object.pk).filter(user__pk=self.request.user.pk).exists():
            context_data['like_class']='fas'
        else:
            context_data['like_class']='far'

        return context_data


class PostCreateView(LoginRequiredMixin,generic.CreateView):
    form_class = forms.PostForm
    model = models.Post

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.current_user=User.objects.get(pk=self.request.user.pk)
        self.object.author = self.current_user
        self.object.save()
        messages.success(self.request,"Blog Created Successfully")
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin,generic.UpdateView):
    model = models.Post
    form_class= forms.PostForm

    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.current_user=User.objects.get(pk=self.request.user.pk)

        if self.current_user!=self.object.author:
            raise django_forms.ValidationError("You are not authorized to edit this post")

        self.object.save()
        messages.success(self.request,"Blog Edited Successfully")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = models.Post
    form_class = forms.PostForm
    success_url = reverse_lazy('blog_app:list',kwargs={'page':1})


    def delete(self, *args, **kwargs):

        self.current_user=User.objects.get(pk=self.request.user.pk)
        self.object = self.get_object()

        if self.current_user!=self.object.author:
            messages.error(self.request,"You are not authorized to delete this post")

        messages.success(self.request, "Blog Deleted successfully!")
        return super().delete(*args, **kwargs)


def comment_create_view(request,post_pk):

    if request.user.is_authenticated and request.method=='POST':

        author = User.objects.get(pk=request.user.pk)
        post = models.Post.objects.get(pk=post_pk)
        content = request.POST['content']

        comment = models.Comment.objects.create(author=author,post=post,content=content)
        comment.save()
        messages.success(request,'Comment posted Successfully')
    else:
        messages.error(request,'Please login inorder to post comments')

    return HttpResponseRedirect(reverse('blog_app:detail',kwargs={'pk':post_pk}))

class CommentEditView(LoginRequiredMixin,generic.UpdateView):
    model = models.Comment
    form_class = forms.CommentForm
    template_name = 'blog_app/_comment_edit_form.html'

    def form_valid(self,form):

        self.object = form.save(commit=False)
        self.current_user = User.objects.get(pk=self.request.user.pk)

        if self.object.author==self.current_user:
            self.object.save()
            messages.success(self.request,"Comment edited successfully.")
            return super().form_valid(form)

        messages.error(self.request,'You are not authorized to edit this comment.')
        return HttpResponseRedirect(reverse('blog_app:detail',kwargs={'pk':self.object.post.pk}))


class CommentDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = models.Comment
    form_class = forms.CommentForm

    def get_success_url(self):
        return reverse_lazy('blog_app:detail',kwargs={'pk':self.kwargs['post_pk']})

    def delete(self,*args,**kwargs):

        self.current_user = User.objects.get(pk=self.request.user.pk)
        self.object = self.get_object()

        if self.current_user==self.object.author:
            messages.success(self.request,"Comment deleted successfully!")
            return super().delete(*args,**kwargs)

        messages.error(self.request,"You are not authorized to delete this comment!")
        return HttpResponseRedirect(reverse('blog_app:detail',kwargs={'pk':self.object.post.pk}))


def post_like_view(request,post_pk):
    data={}

    if request.user.is_authenticated:
        data['is_valid_user']=True
        user = User.objects.get(pk=request.user.pk)
        post = models.Post.objects.get(pk=post_pk)

        query=models.Like.objects.filter(post=post).filter(user=user)

        if query.exists():
            query.delete()
            data.update({'add_class':'far','remove_class':'fas'})
        else:
            models.Like.objects.create(post=post,user=user)
            data.update({'add_class':'fas','remove_class':'far'})

        data['likes_count'] = " Likes: " + str(models.Like.objects.filter(post=post).count())
    else:
        data['is_valid_user']=False

    return JsonResponse(data)
