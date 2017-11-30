from django.views.generic import TemplateView, ListView, CreateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import KeyForm

# Create your views here.
# def post_list(request):
#     return render(request, 'blog/post_list.html')
@login_required(login_url="/login/")
def home_page(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	return render(request, 'blog/home.html')

# class KeyView(CreateView):
# 	model = Key
# 	form_class = KeyForm
# 	template_name = 'blog/profile_key.html'
# 	succes_url = 'blog/home.html'

@login_required(login_url="/login/")
def my_profile(request):
	# if not request.user.is_authenticated():
	# 	return HttpResponseRedirect('/')
	print ('aici')
	if request.method == 'POST':
		form = KeyForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
	else:
		form = KeyForm()
	return render(request, 'blog/profile.html', {"form": form})
