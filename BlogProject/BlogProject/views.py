from django.shortcuts import redirect
from django.urls import reverse

def HomeView(request):
    return redirect(reverse('blog_app:list',kwargs={'page':1}))
