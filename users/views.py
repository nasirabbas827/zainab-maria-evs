from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Election, Candidate
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm


@login_required
def home(request):
    # Retrieve the list of elections and candidates
    elections = Election.objects.all()
    candidates = Candidate.objects.all()

    context = {
        'elections': elections,
        'candidates': candidates,
    }

    return render(request, 'users/home.html', context)

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Election, Candidate

def view_candidates(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    candidates = Candidate.objects.filter(election=election)

    context = {
        'election': election,
        'candidates': candidates,
    }
    return render(request, 'users/view_candidates.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import messages for displaying messages to the user
from .models import Candidate, Vote , BlockchainCode

from .blockchain import Blockchain

import hashlib  # Make sure hashlib is imported at the beginning of the file

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def vote(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    user = request.user
    election = candidate.election

    # Check if the election status is not "ongoing"
    if election.status != 'ongoing':
        messages.error(request, "The election is not ongoing. You cannot cast your vote at this time.")
        return redirect('view_candidates', election_id=election.id)

    # Check if the user has already voted in the same election
    if Vote.objects.filter(user=user, candidate__election=election).exists():
        messages.error(request, "You've already voted in this election.")
    else:
        # Create a new vote record
        Vote.objects.create(user=user, candidate=candidate)
        # Update the candidate's vote count
        candidate.votes += 1
        candidate.save()

        # Generate a blockchain code
        vote_data = f"Vote for {candidate.name} by {user.username}"
        blockchain_code = hashlib.sha256(vote_data.encode()).hexdigest()

        # Save the blockchain code in the database
        BlockchainCode.objects.create(user=user, vote=Vote.objects.get(user=user, candidate=candidate), code=blockchain_code)

        messages.success(request, f"You've successfully voted for {candidate.name}. Blockchain Code: {blockchain_code}")

    return redirect('view_candidates', election_id=election.id)

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)





class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

from django.shortcuts import render
from .models import Election, Candidate

def election_winner(request):
    election_winners = []

    # Query elections with status "complete"
    elections = Election.objects.filter(status='completed')

    for election in elections:
        # Query candidates for the current election and order them by votes in descending order
        candidates = Candidate.objects.filter(election=election).order_by('-votes')

        if candidates:
            # The candidate with the most votes is the winner
            winner = candidates[0]
            # Add the image URL to the winner's data
            winner_data = {
                'election_name': election.name,
                'winner_name': winner.name,
                'winner_votes': winner.votes,
                'winner_image_url': winner.image.url,
            }
            election_winners.append(winner_data)

    return render(request, 'users/election_winner.html', {'election_winners': election_winners})
