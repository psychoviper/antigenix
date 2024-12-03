from django.shortcuts import render
from django import forms
from .prediction import predict
from .transform import get_acc
from django.shortcuts import render,redirect
import pandas as pd
import numpy as np
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
# Create your views here.

class SequenceForm(forms.Form):
    CHOICES = [('bacterial','Bacteria'),('viral',"Virus")]
    sequence = forms.CharField(label="Enter Sequence Here", widget=forms.Textarea(attrs={'class': 'form-control', 'rows':3}))
    model = forms.ChoiceField(choices=CHOICES, required=True, label='Select a Model', widget=forms.Select(attrs={'class': 'form-select'}))

def index(request):
    if request.method == "POST":
        predictions=[]
        form = SequenceForm(request.POST)
        if form.is_valid():
            sequences=[]
            sequence = form.cleaned_data["sequence"]
            model = form.cleaned_data["model"]
            if(model=='bacterial'):
                val, acc_display = get_acc(sequence)
                val = val.reshape(1, -1)
                sequences.append(val)
                results = predict(sequences)[-1]
            else:
                val, acc_display = get_acc(sequence)
                val = val.reshape(1, -1)
                sequences.append(val)
                results = predict(sequences)[-1]
            for r in results:
                if(r>0.5):
                    predictions.append('Probable Antigen')
                else:
                    predictions.append("Probable Non-Antigen")
            # results.flatten()
            print(results)
            print(type(results))
            return render(request, "predictor/result.html", {"results":results, "predictions":predictions, "display":acc_display, 'sequence':sequence})
        else:
            pass
    else:
        example = "MAATQETAIDKYKKVKRIKWIVRLLGGSTGVVIAAAITLLLIVSMAIFGGQSSTGTPNGGISGTATVKNLPPEVMRWQAMVEQECAAQGVPELVPYVLAIIMVESNGISEKLPDIMQSSESQGWAMNTISNPKDSIYYGVMHLKGAFDDAKMLGINDLLAIVQTYNFGRNYVHWLAANNKTHSIQTADYYSLTVVAPAGGNRNGTTIGYSQPVAVAYNGGYRYINGGNFFYAEMVKQYLSFDGAGGTSGQIPGGSETFKVMMDEVLKYNGNPYVWGGKSSSQGFDCSGLTYWAYKTAGITIPISAATQYDFTVEVDPKDAQPGDLVFFRGTYGGPNHVSHVGIYIDANTMYDSNGSGVGYHQFTSSYWQQHYAGIRRVPR"
        form = SequenceForm()
    return render(request, 'predictor/index.html', {"form": form, "example": example})


def contact(request): #Diplays contact page . Sends email to HDPS using SMTP.
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        title = request.POST.get('title1')
        message = request.POST.get('message')
        
        send_mail(title , message+'\n'+'From : '+name+'\n'+'Email : '+email ,from_email=email, recipient_list=['focusus1@gmail.com']) #Sends mail to HDPS
    return render(request , 'predictor/contact.html')

def about(request): #Displays about us page.
    return render(request , 'predictor/about.html')

# Login and Logout

def signin(request): # For the user to sign in.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('signin')

        
    else:
        return render(request,'predictor/signin.html')


def signup(request): #For the user to resister or sign up.

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username taken')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email taken')
            return redirect('signup')
        else:
            user = User.objects.create_user(username=username, password=password,email=email,first_name = first_name,last_name=last_name)
            
            user.save()
            
            messages.success(request,f"User {username} created!")
            return redirect('signin')
        #return redirect('/')
    else:   
        return render(request,'predictor/signup.html')


def signout(request): # In order to logout from the website
    auth.logout(request)
    return redirect('/')
