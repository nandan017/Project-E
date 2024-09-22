from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Candidate
from voting.models import Vote

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to a dashboard view
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'election/login.html')

def dashboard(request):
    total_votes = Vote.objects.count()
    total_candidates = Candidate.objects.count()
    
    # Get vote count per candidate
    candidate_votes = {candidate: Vote.objects.filter(candidate=candidate).count() for candidate in Candidate.objects.all()}

    context = {
        'total_votes': total_votes,
        'total_candidates': total_candidates,
        'candidate_votes': candidate_votes,
    }
    
    return render(request, 'election/dashboard.html', context)

def add_candidate(request):
    if request.method == 'POST':
        name = request.POST['name']
        forum = request.POST['forum']
        image = request.FILES['image']

        # Create a new candidate
        candidate = Candidate(name=name, forum=forum, image=image)
        candidate.save()

        return redirect('dashboard')  # Redirect to dashboard after adding

    return render(request, 'election/add_candidate.html')