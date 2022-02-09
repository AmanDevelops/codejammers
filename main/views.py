from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import competitions, resultmodel, submissions, contact


# Create your views here.

def home(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        ready = contact(name=name, email=email, message=message)
        ready.save()
        return redirect('/')

    else:
        return render(request, 'main/index.html')


def base(request):
    return render(request, 'main/base.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    
                    messages.info(request, 'Username Already Exists')
                    return redirect('register')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.info(request, 'Email Already Exists')
                        return redirect('register')
                    else:
                        user = User.objects.create_user(
                            username=username,
                            password=password1,
                            email=email,
                            first_name=first_name,
                            last_name=last_name
                        )
                        user.save()
                        messages.info(request, 'User Created')
                        return redirect('register')
                        
            else:
                messages.info(request, 'Password Not Matching')
                return redirect('register')
        else:
            return render(request, 'main/register.html',)


def login(request):
    if request.user.is_authenticated:
        print('already logged in')
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('login')
        else:
            return render(request, 'main/login.html')


def logout(request):
    user = request.user
    if user.is_authenticated:
        auth.logout(request)
        return redirect('/')
    else:
        return redirect('/')


def dashboard(request):
    if request.user.is_authenticated:
        comps = competitions.objects.all()
        return render(request, 'main/dashboard.html', {'comps': comps})
    else:
        return redirect('login')


def view(request):
    if request.GET.get('id') is not None:
        idg = request.GET['id']
        subs = submissions.objects.filter(pgid=idg)
        comp = competitions.objects.get(id=idg)

        username = request.user.username
        
        subs2 = submissions.objects.filter(submitted_by=username)
        a = ''
        for subal in subs2:
            a = subal.submitted_by
        
        if a == '':
            submitted = False
        else:
            submitted = True
        return render(request, 'main/view.html', {
            'comps': comp,
            'id': idg,
            'sub': subs,
            'submitted': submitted,
            'pos': 0
        })
    else:
        return redirect('/login')


def submit(request):
    pgidget = request.GET.get('id')
    if pgidget is not None:
        username = request.user.username
        subs2 = submissions.objects.filter(submitted_by=username)
        a = ''
        for subal in subs2:
            a = subal.submitted_by
            
        if a == '':
            if request.method == 'POST':
                link = request.POST['code']
                pgidget = request.GET.get('id')
                temp_link = link.lower()
                if temp_link.find('colab.research.google.com') == -1:
                    messages.info(request, 'Please Paste The Google Collab Link')
                    return redirect('/submit?id='+pgidget)
                else:
                    username = request.user.username

                    ready = submissions(pgid=pgidget, submitted_by=username, code=link)
                    ready.save()
                    return redirect('/view?id='+pgidget)
            else:
                pgidget1 = request.GET['id']
                return render(request, 'main/submit.html', {'idgt': pgidget1, })
        else:
            return redirect('/view?id='+pgidget)
    else:
        return redirect('/dashboard')


def code(request):
    idd = request.GET['id']
    data = submissions.objects.filter(id=idd)
    
    return render(request, 'main/submissions.html', {'data': data})


def result(request):
    cid = request.GET.get('id')
    if cid is not None:
        res = resultmodel.objects.filter(comp_id=cid)
        subs = submissions.objects.filter(pgid=cid)
        print(res, subs)

        return render(request, 'main/result.html', {'resmod': res, 'submod': subs})
    else:
        return redirect('/dashboard')


def contact(request):
    return render(request, 'main/contact.html')
