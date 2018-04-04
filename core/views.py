from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required



# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def home(request):
	return render(request, 'core/home.html', {
        'chat_by' : request.user
        })

@login_required
def room(request, room_name):
    a = room_name.split('-')
    a.sort()
    room_name1 = a[0]+'-'+a[1]
    print(room_name1)
    #print(type(a[0]), type(str(request.user)))
    if str(request.user) == a[0] or str(request.user) == a[1]:
        #print('yes')
        return render(request, 'core/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name1))
            })
    else:
        return redirect('home')

        
    

"""
return render(request, 'core/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
        })
"""