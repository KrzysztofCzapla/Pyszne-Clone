from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

'''def register(response):
	if response.method == "POST":
		form = UserCreationForm(response.POST)
		if form.is_valid():
			form.save()
			return redirect("/")
	else:
		form = UserCreationForm()
	return render(response, "register/register.html",{"form":form})
'''
def register(response):
    form = UserCreationForm()
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(response, "register/register.html",{"form":form})

'''def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main:homepage")
    form = NewUserForm()
    return render (request=request, template_name="register/register.html", context={"register_form":form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})'''