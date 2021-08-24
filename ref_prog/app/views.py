from django.http import JsonResponse
import time
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import user_info
from django.contrib.auth import login, logout, authenticate
from .forms import user_info_form
# Create your views here.


def index(request):
    return render(request, 'index.html')


def signup(request, ref_code):
    if user_info.objects.filter(ref_code=ref_code).exists():
        user_down = user_info.objects.get(ref_code=ref_code)
        referred_users = []
        referred_users.append(user_info.objects.filter(
            referred_by_down=user_down.user))
        if len(referred_users[0]) >= 2 * user_down.sharing_increased:
            return render(request, 'signup.html', {'message': 'Referring user has used his sharing limit. Tell him to increase his sharing limit.'})
        else:
            user_down = user_down.user
            user_up = user_info.objects.get(user=user_down)
            user_up = str(user_up.referred_by_down)
            user_down = str(user_down)
            if request.method == 'POST':
                first_name = request.POST['first_name']
                username = request.POST['username']
                last_name = request.POST['last_name']
                email = request.POST['email']
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                if password1 != password2 or (len(password1) < 8 or len(password2) < 8):
                    return render(request, 'signup.html', {'message': 'Passwords do not match.'})
                elif User.objects.filter(username=username).exists() or len(username) > 20:
                    return render(request, 'signup.html', {'message': 'Username already being used.'})
                elif User.objects.filter(email=email).exists():
                    return render(request, 'signup.html', {'message': 'Email already being used.'})
                else:
                    user = User.objects.create(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password1
                    )
                    user.save()
                    user = User.objects.get(username=username)
                    user.user_info.set(user_up, user_down)
                    return redirect('dashboard')
            return render(request, 'signup.html', {'referring_user': user_down})
    else:
        return render(request, 'index.html', {'message': "Reffering person's account doesn't exist."})


def dashboard(request):
    context = {'code': request.user.user_info.ref_code}
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'dashboard.html', context)


def UserInfoEditView(request):
    form = user_info_form(instance=request.user.user_info)
    if request.method == 'POST':
        phone_no = request.POST['phone_number']
        form = user_info_form(
            request.POST, request.FILES, instance=request.user.user_info)
        if user_info.objects.filter(phone_number=phone_no).exists():
            return render(request, 'userInfoEditPage.html', {'form': form, 'message': 'Phone number taken.'})
        elif form.is_valid:
            form.save()
            return render(request, 'userInfoEditPage.html', {'form': form, 'message': 'Changes saved!'})
        else:
            return render(request, 'userInfoEditPage.html', {'form': form, 'message': 'Invalid input.!'})
    return render(request, 'userInfoEditPage.html', {'form': form})


def login_veiw(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'message': 'Invalid credentials.'})
    return render(request, 'login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'login.html', {'message': 'Logged out successfully.'})
    return render(request, 'login.html')


def network(request):
    if request.user.is_authenticated:
        user_up = request.user.user_info.referred_by_up
        user_down = request.user.user_info.referred_by_down
        referred_users = []
        referred_users.append(user_info.objects.filter(
            referred_by_down=request.user))
        sharing_increased = request.user.user_info.sharing_increased
        if len(referred_users[0]) == 2 * sharing_increased:
            return render(request, 'network.html', {'user_up': user_up, 'user_down': user_down, 'referred_users': referred_users[0], 'message': 'You have consumed your sharing limit. Please increase it to link more persons.'})
        else:
            sharing_remain = 2 * sharing_increased - len(referred_users[0])
            return render(request, 'network.html', {'user_up': user_up, 'user_down': user_down, 'referred_users': referred_users[0], 'message': f'You have {sharing_remain} slots free for sharing. Share more users.'})
    else:
        return redirect('login')


def helper_up(request):
    referr_up_user = request.user.user_info.referred_by_up
    context = {'user_for_help': referr_up_user}
    if request.method == 'POST':
        try:
            response = request.POST['has_helped_up']
            if response == 'on':
                request.user.user_info.has_helped_up_tick()
                return redirect('network')
        except:
            pass
    return render(request, 'help_up.html', context)


def helper_down(request):
    referr_down_user = request.user.user_info.referred_by_down
    context = {'user_for_help': referr_down_user}
    if request.method == 'POST':
        try:
            response = request.POST['has_helped_down']
            if response == 'on':
                request.user.user_info.has_helped_down_tick()
                return redirect('network')
        except:
            pass
    return render(request, 'help_down.html', context)


def sharing_increase(request):
    if request.method == 'POST':
        try:
            response = request.POST['sharing_increase']
            if response == 'on':
                request.user.user_info.sharing_increaser()
                redirect('network')
        except:
            pass
    return render(request, 'sharing_increase.html')
