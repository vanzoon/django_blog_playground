from django.shortcuts import redirect, render

def redirect_to_blog(request):
    return redirect('posts_list_url', permanent=True)

def auth(request):
    return render(request, 'oauth.html')
