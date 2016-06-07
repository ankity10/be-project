from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Question
from django.contrib.auth.models import User
from .models import Contestant
from random import shuffle
from django.core.exceptions import ObjectDoesNotExist




def index(request):
	if request.user.is_authenticated:
		question_list = [q.question_text for q in Question.objects.all()]

	context = {
	"questions" : question_list
	}
	print(context)
	print("Printing done")

	return render(request,'q_db/index.html',context)


# Contest view ..first checks the current question state and then redirects to it
@login_required
def contest(request):
	usr = User.objects.get(username=request.user)
	try:
		contestant = Contestant.objects.get(user=usr)
	except ObjectDoesNotExist:
		contestant = Contestant(user=usr)
		contestant.save()
	# print(contestant.id)
	# print(contestant)
	# print(usr)
	if contestant.first_login is False:
		print("first login false")

		arr_length = int(Question.objects.all().count())+1
		que_list = [i for i in range(1,arr_length)]
		shuffle(que_list)
		ans_array = [i for i in range(1,arr_length)]
		str_ans_array = [str(s) for s in ans_array]
		final_ans_array = ' '.join(str_ans_array)
		Contestant.objects.filter(pk=contestant.id).update(ans_array=final_ans_array)


		que_list = [str(s) for s in que_list]
		array_str = ' '.join(que_list)
		Contestant.objects.filter(pk=contestant.id).update(que_array=array_str)
		Contestant.objects.filter(pk=contestant.id).update(first_login=True)
		id=1

	else:
		print("first login True")
		# q_list = contestant.que_array
		# q_list = [int(i) for i in q_list.split( )]
		id = contestant.current_que_id
		# id=q_list[q_pointer-6]

	q_list = contestant.que_array
	q_list = [int(i) for i in q_list.split( )]
	str_ans_array = contestant.ans_array.split(' ')
	try:
		trial_answer = str_ans_array[int(id)-1]
		if trial_answer.isdigit():
			print("not answered")
		else:
			print("answered")


		if(int(id)>0 and 6>int(id)):
			qid=q_list[int(id)-1]

			question = Question.objects.get(pk=qid+5)#remove pk after changing questions dataset
			context = {
			"question" : question,
			"id" : id,
			"answer":trial_answer,
			}	
			# redering the question ..success
			return render(request,'q_db/question.html',context)
			
	except IndexError:
		error = "Question not found!"
		context = {
		"error" : error,
		}	
		return render(request,'q_db/error.html',context)


@login_required
def q_submit(request):
	usr = User.objects.get(username=request.user)
	contestant = Contestant.objects.get(user=usr)

	if request.POST['type'] == 'next':
		if int(request.POST['cq']) <= contestant.current_que_id :
			cur_que = request.POST['cq']
			print(cur_que)
			Contestant.objects.filter(pk=contestant.id).update(current_que_id=int(cur_que)+1)
	else:
		cur_que = request.POST['cq']
		# print(cur_que)
		# usr = User.objects.get(username=request.user)
		# contestant = Contestant.objects.get(user=usr)
		# Contestant.objects.filter(pk=contestant.id).update(current_que_id=int(cur_que)-1)
	return HttpResponse("Succesfull ")

@login_required
def ans_submit(request):

	usr = User.objects.get(username=request.user)
	contestant = Contestant.objects.get(user=usr)
	q_list = contestant.que_array
	q_list = [int(i) for i in q_list.split( )]
	cur_que_index = int(request.POST['cq'])-1
	cur_que = q_list[cur_que_index]
	question = Question.objects.get(pk=cur_que+5) #remove pk after changing questions dataset
	answer = request.POST['ans']
	if answer == question.answer:
		print("write answer")
		# Contestant.objects.filter(pk=contestant.id).update(score=contestant.score+4) #updating score
	else:
		print("wrong answer")

	str_ans_array = contestant.ans_array
	ans_array = str_ans_array.split(' ')
	ans_array[cur_que_index]=answer
	updated_str_ans_array = ' '.join(ans_array)
	Contestant.objects.filter(pk=contestant.id).update(ans_array=updated_str_ans_array)


	return HttpResponse("Succesfull")


@login_required
def score(request):
	usr = User.objects.get(username=request.user)
	contestant = Contestant.objects.get(user=usr)
	# Contestant.objects.filter(pk=contestant.id).update(score=0) #updating score to 0
	
	q_list = contestant.que_array
	q_list = [int(i) for i in q_list.split( )]
	ans_array = contestant.ans_array
	ans_array = ans_array.split(' ')
	c_score = 0
	for i in range(contestant.current_que_id):
		contestant = Contestant.objects.get(user=usr)
		cur_que_index = i
		cur_que = q_list[cur_que_index]
		question = Question.objects.get(pk=cur_que+5) #remove pk after changing questions dataset
		answer = ans_array[i]
		if answer == question.answer:
			print("write answer")
			c_score = c_score + 4
	

	if contestant.score != c_score:
		Contestant.objects.filter(pk=contestant.id).update(score=c_score) #updating score

	context = {

	'score' : contestant.score,
	}

	return render(request,'q_db/score.html',context)