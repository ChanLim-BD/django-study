from urllib import response
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render

from django.conf import settings

from django.views.generic import TemplateView, UpdateView, CreateView

from accounts.forms import ProfileForm
from accounts.models import Profile

User = get_user_model()

# @login_required
# def  profile(request):
#     return render(request, 'accounts/profile.html')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

profile = ProfileView.as_view()

@login_required
def profile_edit(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, 'accounts/profile_form.html', {
        'form': form,
    })

class SignupView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url=settings.LOGIN_REDIRECT_URL
    template_name = 'accounts/signup_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        auth_login(self.request, user)
        return response

signup = SignupView.as_view()

def logout(request):
    pass

# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = Profile
#     form_class = ProfileForm

# profile_edit = ProfileUpdateView.as_view()