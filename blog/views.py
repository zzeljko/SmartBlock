from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# def post_list(request):
#     return render(request, 'blog/post_list.html')
@login_required(login_url="/login/")
def home_page(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	return render(request, 'blog/home.html')

def account_settings(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	return render(request, 'blog/account.html')