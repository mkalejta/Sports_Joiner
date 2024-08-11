from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib.messages.views import messages
from app import models, forms
from django.contrib.auth.views import LoginView
from app.forms import CustomAuthenticationForm

def SignUpView(request):
    form = forms.SignUpForm()
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, ("You have successfully registered!"))
            return redirect('home')

    return render(request, "registration/registration.html", {'form': form})

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

@login_required
def user_dashboard(request, pk):
    user = models.User.objects.get(id=pk)
    context = {
        'user': user,
    }
    return render(request, 'dashboard.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = forms.UpdateProfile(request.POST, request.FILES, instance=request.user)
        profile_form = forms.ProfilePicForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, "Your profile was successfully updated")
            return redirect('user_dashboard', pk=request.user.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = forms.UpdateProfile(instance=request.user)
        profile_form = forms.ProfilePicForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def events_list(request):
    if request.method == 'POST':
        if request.POST.get('sport_category') == 'All':
            qs = models.Event.objects.all()
            wybrana_wartosc = 'All'
        else:
            wybrana_wartosc = request.POST.get('sport_category')
            sport_category_query = request.POST.get('sport_category')
            qs = models.Event.objects.filter(facility__sport__name=sport_category_query)
    else:
        wybrana_wartosc = None
        qs = models.Event.objects.all()
    context = {
        'queryset': qs,
        'wybrana_wartosc': wybrana_wartosc
    }
    return render(request, "events_list.html", context)


@login_required
def create_event(request):
    form = forms.CreateEventForm
    if request.method == 'POST':
        form = forms.CreateEventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.organizer = request.user
            new_event.save()
            new_event.participants.add(new_event.organizer.profile)
            new_event.save()
            return redirect('events_list')
    return render(request, "create_event.html", {'form': form})


@login_required
def event_details(request, pk):
    event = models.Event.objects.get(id=pk)
    context = {
        'event': event,
    }
    return render(request, 'event_details.html', context)

@login_required
def join_event(request, event_id):
    event = models.Event.objects.get(id=event_id)
    profile = request.user.profile

    if profile not in event.participants.all():
        event.participants.add(profile)
        event.save()

    return redirect('events_list')

@login_required
def leave_event(request, event_id):
    event = models.Event.objects.get(id=event_id)
    profile = request.user.profile

    if profile in event.participants.all():
        event.participants.remove(profile)
        event.save()

    return redirect(request.META.get("HTTP_REFERER"))

@login_required
def my_events(request, pk):
    events = models.Event.objects.filter(participants__id__icontains=pk)
    if request.method == 'POST':
        sport_query = request.POST.get('sport_category')
        status_query = request.POST.get('user_event_status')
        if sport_query == 'All' and status_query == 'all':
            wybrana_wartosc1 = 'All'
            wybrana_wartosc2 = 'all'
        elif sport_query == 'All' and status_query != 'all':
            wybrana_wartosc1 = 'All'
            wybrana_wartosc2 = status_query
            if status_query == 'organizer':
                events = events.filter(organizer__id=pk)
            elif status_query == 'participant':
                events = events.exclude(organizer__id=pk)
        elif sport_query != 'All' and status_query == 'all':
            events = events.filter(facility__sport__name=sport_query)
            wybrana_wartosc1 = sport_query
            wybrana_wartosc2 = 'all'
        else:
            events = events.filter(facility__sport__name=sport_query)
            wybrana_wartosc1 = sport_query
            wybrana_wartosc2 = status_query
            if status_query == 'organizer':
                events = events.filter(organizer__id=pk)
            elif status_query == 'participant':
                events = events.exclude(organizer__id=pk)
    else:
        wybrana_wartosc1 = None
        wybrana_wartosc2 = None
    context = {
        'events': events,
        'wybrana_wartosc1': wybrana_wartosc1,
        'wybrana_wartosc2': wybrana_wartosc2
    }
    return render(request, 'my_events.html', context)

@login_required
def edit_event(request, event_id):
    event = models.Event.objects.get(id=event_id)
    if request.user == event.organizer:
        edit_form = forms.CreateEventForm(request.POST or None, instance=event)
        if request.method == 'POST':
            if edit_form.is_valid():
                new_event = edit_form.save(commit=False)
                new_event.organizer = request.user
                new_event.save()
                return redirect('my_events', pk=request.user.id)
        context = {
            'event': event,
            'form': edit_form
        }
        return render(request, 'edit_event.html', context)
    else:
        return redirect('home')

@login_required
def delete_event(request, event_id):
    event = models.Event.objects.get(id=event_id)
    if request.user == event.organizer:
        event.delete()
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        return redirect('home')
