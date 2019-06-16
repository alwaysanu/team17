from django.shortcuts import render
from bored_api.models import BoredUser
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout, authenticate

# Create your views here.
def test(request):
    import requests
    resp = requests.get("https://www.boredapi.com/api/activity/")
    print(resp.text)

    return render(request, "bored_api/HomePage.html")

def bored_clicked(request):

    return render(request, "bored_api/SearchPage.html")

def saved_list(request):

    return render(request, "bored_api/SavedItems.html")


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        if email:
            if not BoredUser.objects.filter(email=email).exists():
                res = '0,'*9
                user = BoredUser.objects.create_user(email=email, category_weights=res[:-1],
                        saved_activities='', username=email.split('@')[0])
                user.save()
                messages.error(request, "Registered")
            user = authenticate(email=email)
            if user is not None:
                login(request, user)
                print(request, f"You are now logged in as {username}")
                print("You are now logged in")
                messages.error(request, "Logged in")
                return redirect("index")
        else:
            messages.error(request, "Invalid Email provided")
            return redirect('post_login')
    form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'bored_api/index.html', context)


def new_activity(request):
    import requests
    resp = requests.get("https://www.boredapi.com/api/activity/")
    context = {}
    return render(request, 'bored_api/activity.html', context)
