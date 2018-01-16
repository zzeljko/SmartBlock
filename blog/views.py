from django.shortcuts import render, redirect
from .forms import NewsPostForm
from .models import NewsPost, Key, PollQuestion, PollChoice, Vote, ImportantDate, OtherImportantContact 
from .models import IntrariIntretinere, CommonBill
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

		if 'water_index_cold' and 'water_index_hot' in request.POST:
			new_cold_index = float(request.POST['water_index_cold'])
			new_hot_index = float(request.POST['water_index_hot'])

			User.objects.filter(username=request.user.username).update(
				consum_apa_rece = new_cold_index - request.user.index_vechi_apa_rece)
			User.objects.filter(username=request.user.username).update(
				consum_apa_calda = new_hot_index - request.user.index_vechi_apa_calda)
			
			User.objects.filter(username=request.user.username).update(
				index_vechi_apa_rece = new_cold_index)
			User.objects.filter(username=request.user.username).update(
				index_vechi_apa_calda = new_hot_index)

			User.objects.filter(username=request.user.username).update(
				declared_water = True)

	users = User.objects.all().filter(is_staff=False)
	common_bills = CommonBill.objects.all().order_by('date').reverse()
	intrari_intretinere = IntrariIntretinere.objects.all()
	if len(intrari_intretinere) < len(common_bills) * len(users):

		total_cold_water_declared = 0.0
		total_hot_water_declared = 0.0
		nr_persons_water_not_declared = 0
		total_no_of_persons = 0
		for user in users:
			user.debt = user.total_to_pay - user.payed_amount
			total_no_of_persons += user.no_of_persons
			if user.declared_water == True:
				total_cold_water_declared += user.consum_apa_rece
				total_hot_water_declared += user.consum_apa_calda
			else:
				nr_persons_water_not_declared += user.no_of_persons

		cold_non_declared_consumption_per_person = 0
		hot_non_declared_consumption_per_person = 0
		if nr_persons_water_not_declared != 0:
			cold_non_declared_consumption_per_person = (common_bills[0].cons_apa_rece \
			- total_cold_water_declared) * 1.0 / nr_persons_water_not_declared 
			hot_non_declared_consumption_per_person = (common_bills[0].cons_apa_calda \
			- total_hot_water_declared) * 1.0 / nr_persons_water_not_declared

		cost_per_mc_apa_rece = common_bills[0].apa_rece * 1.0 / common_bills[0].cons_apa_rece
		cost_per_mc_apa_calda = common_bills[0].apa_calda * 1.0 / common_bills[0].cons_apa_calda
		cost_gaze_per_persoana = common_bills[0].gaze * 1.0 / total_no_of_persons
		cost_energie_per_persoana = common_bills[0].energie_electrica_parti_comune * 1.0 / total_no_of_persons
		cost_interfon_per_persoana = common_bills[0].intretinere_interfon * 1.0 / total_no_of_persons
		cost_deseuri_per_persoana = common_bills[0].deseuri_menajere * 1.0 / total_no_of_persons
		cost_salarii_per_persoana = common_bills[0].salarii_bloc * 1.0 / total_no_of_persons
		for user in users:

			if user.declared_water == False:
				user.consum_apa_rece = user.no_of_persons * cold_non_declared_consumption_per_person
				user.consum_apa_calda = user.no_of_persons * hot_non_declared_consumption_per_person
				user.index_vechi_apa_rece += user.consum_apa_rece
				user.index_vechi_apa_calda += user.consum_apa_calda 

			new_entry = IntrariIntretinere(user=user, date=common_bills[0].date, 
				consum_apa_rece=user.consum_apa_rece, 
				apa_rece=user.consum_apa_rece * cost_per_mc_apa_rece,
				consum_apa_calda=user.consum_apa_calda,
				apa_calda=user.consum_apa_calda * cost_per_mc_apa_calda,
				gaze=user.no_of_persons * cost_gaze_per_persoana,
				energie_parti_comune=user.no_of_persons * cost_energie_per_persoana,
				interfon=user.no_of_persons * cost_interfon_per_persoana,
				deseuri_menajere=user.no_of_persons * cost_deseuri_per_persoana,
				salarii=user.no_of_persons * cost_salarii_per_persoana,
				caldura=user.surface_factor * common_bills[0].incalzire_curenta,
				lift=user.surface_factor * common_bills[0].intretinere_lift,
				cheltuieli_neprevazute=user.surface_factor * common_bills[0].cheltuieli_neprevazute,
				restante=user.debt)

			new_entry.total_luna_curenta = new_entry.apa_rece + new_entry.apa_calda + new_entry.gaze \
			+ new_entry.energie_parti_comune + new_entry.interfon + new_entry.deseuri_menajere \
			+ new_entry.salarii + new_entry.caldura + new_entry.lift + new_entry.cheltuieli_neprevazute
			
			new_entry.total = new_entry.total_luna_curenta + new_entry.restante
			new_entry.save()

			user.month_to_pay = new_entry.total_luna_curenta
			user.total_to_pay = new_entry.total
			user.declared_water = False
			user.payed_amount = 0.0
			user.save()

	utilities_table_no_of_col = len(IntrariIntretinere._meta.get_fields()) - 2
	utilities_table_no_of_lines = len(users) + 2
	last_utility_table = []
	if len(common_bills) > 0:
		last_utility_table = IntrariIntretinere.objects.all().filter(date=common_bills[0].date).order_by('user')	
	
	total_pers_to_send = 0
	for user in users:
		total_pers_to_send += user.no_of_persons

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

	total_luna_curenta_to_send = common_bills[0].apa_rece + common_bills[0].apa_calda + common_bills[0].gaze \
	+ common_bills[0].energie_electrica_parti_comune + common_bills[0].intretinere_interfon \
	+ common_bills[0].deseuri_menajere + common_bills[0].salarii_bloc + common_bills[0].incalzire_curenta \
	+ common_bills[0].intretinere_lift + common_bills[0].cheltuieli_neprevazute

	total_debt_to_send = 0
	total_total_to_send = 0
	for user in users:
		total_debt_to_send += user.debt
		total_total_to_send += user.total_to_pay

	return render(request, 'blog/home.html', {'form' : form,
		'post_list' : post_list, 'poll_dict' : poll_dict, 'keys_list' : keys_list, 
		'freezed_questions' : freezed_questions, 'voted_choices' : voted_choices, 
		'number_of_users' : number_of_users, 'important_dates' : important_dates,
		'block_staff' : block_staff, 'other_important_contacts' : other_important_contacts,
		'utilities_table_no_of_col' : xrange(0,utilities_table_no_of_col), 
		'utilities_table_no_of_lines' : xrange(0,utilities_table_no_of_lines), 
		'last_utility_table' : last_utility_table,
		'total_pers_to_send' : total_pers_to_send,
		'current_common_bill' : common_bills[0],
		'total_luna_curenta_to_send' : total_luna_curenta_to_send,
		'total_debt_to_send' : total_debt_to_send,
		'total_total_to_send' : total_total_to_send})