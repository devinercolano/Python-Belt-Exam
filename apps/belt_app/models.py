# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
import re

emailRegEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
passwordCharUppercaseRegEx = re.compile(r'[A-Z]+')
passwordNumRegEx = re.compile(r'[0-9]+')

class UserManager(models.Manager):
    def userValidation(self, postData):
        response = {}
        messages = {}

        errorFlag = False
        if len(postData['name']) < 2:
            messages["name"]=("name cannot be empty!")
            errorFlag = True
        elif postData['name'].isalpha() == False :
            messages["name"]= ("name must contain only alphabetic characters!")
            errorFlag = True

        if len(postData['alias']) < 2:
            messages["alias"] = ("alias cannot be empty!", 'error')
            errorFlag = True
        elif postData['alias'].isalpha() == False :
            messages["alias"]= ("alias must contain only alphabetic characters!")
            errorFlag = True
        
        if len(postData['birthDate']) == 0:
           messages["birthDate"]= (" Enter a date!")

        if len(postData['email']) < 1:
            messages["email"]=("email cannot be empty!")
            errorFlag = True
        elif not emailRegEx.match(postData['email']):
            messages["email"]=("Invalid Email Address!")
            errorFlag = True

        if len(postData['password']) < 1 :
            messages["password"]=("Password cannot be empty!")
            errorFlag = True
        elif len(postData['password']) <= 8:
            messages["password"]=("Password must be longer than 8 characters")
            errorFlag = True

        if postData['password'] != postData['confirmPassword'] :
            messages["password"]=("Password confirmation and password entries must match!")
            errorFlag = True

        if not passwordCharUppercaseRegEx.search(postData['password']) :
            errorFlag = True
            messages["password"]=("Password must contain at least 1 uppercase letter")

        if not passwordNumRegEx.search(postData['password']) :
            errorFlag = True
            messages["password"]=("Password must contain at least 1 number")   

        if User.objects.filter(email = postData['email']):
                messages["email"]=("Error! Duplicate email")
                errorFlag = True
        if errorFlag == False :
            hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name = postData['name'], alias = postData['alias'], birthDate = postData['birthDate'],  email = postData['email'], password = hashed)
            response['user']= user
        
        response['message']= messages
        response['errorFlag'] = errorFlag
        
        return response

    def verifyUserLogin(self, postData):
        messages = {}
        response = {}
        errorFlag = False
        email_address = User.objects.filter(email=postData['email'])
        if len(email_address) < 1 :
            messages['login'] = ("Unsuccessful login. Incorrect email")
            errorFlag = True
        else : 
            hashed = User.objects.get(email=postData['email']).password
            if not bcrypt.checkpw(postData['password'].encode(), hashed.encode()):
                messages['login'] = ("Unsuccessful login. Incorrect password")
                errorFlag = True            
        
        if errorFlag == False :
            messages['success'] = ("Welcome " + User.objects.get(email = postData['email']).name + "!")
        
        response['message']= messages
        response['errorFlag'] = errorFlag

        return response

class QuoteManager(models.Manager):
    def quoteValidation(self, postData):
        errorFlag = False
        messages = {}
        response = {}
        if len(postData['quote_text']) < 10:
            errorFlag = True
            messages['message'] = "Quote must be more than 10 characters"

        response['message']= messages
        response['errorFlag'] = errorFlag

        return response

class User(models.Model):
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    birthDate = models.DateField(default = False)
    favorites = models.ManyToManyField("Quote", related_name="favorites", default=None)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
	quote_text = models.CharField(max_length = 255)
	author = models.CharField(max_length = 255)
	user_quote = models.ForeignKey(User, related_name = 'authors_quotes')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = QuoteManager()
