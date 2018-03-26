from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from .models import User, Quote
from django.core.urlresolvers import reverse

def index(request):
    return render(request, 'belt_app/index.html')

def success(request):
	return render(request, 'belt_app/quotes.html')

def register(request):
    response = User.objects.userValidation(request.POST)
    
    if len(response):
        for tag,error in response.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    if User.objects.userValidation(request.POST):
        errorFlag = True
        return redirect ('/returnQuotes')
    else:
        errorFlag = False
        request.session['user_id'] = User.objects.get(email = request.POST['email']).id
        return redirect('/')

def login(request):
    response = User.objects.verifyUserLogin(request.POST)
    if response['errorFlag'] == True:
        for tag,error in response.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        for tag, error in response.iteritems():
            messages.error(request, error, extra_tags=tag)
        request.session['user_id'] = User.objects.get(email = request.POST['email']).id
        return  redirect('/returnQuotes')

def returnUser(request):
	return User.objects.get(id = request.session['user_id'])

def returnQuotes(request):
	user = returnUser(request)

	context = {
		'user': user,
		'quotes': Quote.objects.exclude(favorites = user),
		'favorites': user.favorites.all()
	}

	return render(request, 'belt_app/quotes.html', context)

def createQuote(request):
        print "in createQuote"
	if request.method != 'POST':
		return redirect('/')

	validate = Quote.objects.quoteValidation(request.POST)
	if request.method != 'POST':
		return redirect('/returnQuotes')
	if validate['errorFlag'] == True:
		for error in validate['message']:
			messages.add_message(request, messages.INFO, error, extra_tags="add_item")
			return redirect('/returnQuotes')
	if validate['errorFlag'] == False:
		quote = Quote.objects.create(
			quote_text = request.POST.get('quote_text'),
			user_quote = returnUser(request),
			author = request.POST.get('author')
		)

	return redirect('/returnQuotes')
    
def addFavorite(request, id):
	user = returnUser(request)
	favorite = Quote.objects.get(id = id)

	user.favorites.add(favorite)

	return redirect('/returnQuotes')

def removeFavorite(request, id):
	user = returnUser(request)
	favorite = Quote.objects.get(id = id)

	user.favorites.remove(favorite)

	return redirect('/returnQuotes')

def showUser(request, id):
	user =  User.objects.get(id = id)
        print "user: ", user
	context = {
		'user': user,
		'favorites': user.favorites.all()		
	}
    
	return render(request, 'belt_app/user.html', context)

def logout(request):
    request.session.flush()
    return redirect ('/')

