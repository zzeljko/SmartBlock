from django.shortcuts import render, redirect
from .forms import NewsPostForm
from .models import NewsPost, Key, PollQuestion, PollChoice, Vote, ImportantDate, OtherImportantContact
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.models import Q
from .models import User
from django.http import HttpResponse
from sets import Set

@login_required(login_url="/login/")
def home_page(request):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	form_class = NewsPostForm
    # if request is not post, initialize an empty form
	form = form_class(request.POST or None)
	
	""" Form logic for registering a new post """
	if request.method == "POST":

		if 'keyset' in request.POST:
			for keyset in request.POST.getlist('keyset'):
				query = keyset.split('-')
				if query[1] == "not_at_me":
					Key.objects.filter(name=query[0]).update(is_used = False)
				elif query[1] == "at_me_not_using_it":
					Key.objects.filter(name=query[0]).update(is_used = False)
					Key.objects.filter(name=query[0]).update(owner = request.user)
				else:
					Key.objects.filter(name=query[0]).update(is_used = True)
					Key.objects.filter(name=query[0]).update(owner = request.user)

		form = NewsPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

        if 'choice' in request.POST:
			choice_id = request.POST['choice']
			choices = PollChoice.objects.filter(pk=choice_id)
			choice = choices[0]
			if not Vote.objects.all().filter(poll_choice=choice, user=request.user):
				choices.update(number_of_votes=F('number_of_votes')+1)
				Vote.objects.create(poll_choice=choice, user=request.user)

	form = NewsPostForm()
	keys_list = Key.objects.all()
	post_list = NewsPost.objects.all().order_by('published_date').reverse()
	
	poll_dict = {}
	poll_list = PollQuestion.objects.all().filter(due_date__gt=timezone.now()).order_by('due_date')
	for x in poll_list:
		poll_dict[x] = PollChoice.objects.all().filter(poll_question=x)

	current_user_votes = Vote.objects.all().filter(user=request.user)
	freezed_questions = []
	voted_choices = []
	for vote in current_user_votes:
		voted_choices.append(vote.poll_choice)
		freezed_questions.append(vote.poll_choice.poll_question)

	users = User.objects.all()
	number_of_users = len(users)
	block_staff = users.filter(Q(is_administrator=True) | Q(is_president=True))

	important_dates = ImportantDate.objects.all()
	other_important_contacts = OtherImportantContact.objects.all()

	return render(request, 'blog/home.html', {'form' : form,
		'post_list' : post_list, 'poll_dict' : poll_dict, 'keys_list' : keys_list, 
		'freezed_questions' : freezed_questions, 'voted_choices' : voted_choices, 
		'number_of_users' : number_of_users, 'important_dates' : important_dates,
		'block_staff' : block_staff, 'other_important_contacts' : other_important_contacts})