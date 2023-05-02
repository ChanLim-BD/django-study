from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, FormView
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_GET
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import CustomUser
from .forms import CustomUserCreationForm, LoginForm

@require_GET
def check_email(request):
    email = request.GET.get('email')
    try:
        validate_email(email)
    except:
        return JsonResponse({'valid': False, 'available': False})

    user = CustomUser.objects.filter(email=email).first()
    if user:
        return JsonResponse({'valid': True, 'available': False})
    else:
        return JsonResponse({'valid': True, 'available': True})

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('signin')
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_approve = False  # 가입 대기 상태로 생성
        user.save()
        return super().form_valid(form)
    
class SignInView(FormView):
    template_name = 'signin.html'
    form_class = LoginForm
    success_url = reverse_lazy('accounts:standby_user_list')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class StandbyUserListView(ListView):
    model = CustomUser
    template_name = 'user_list.html'
    queryset = CustomUser.objects.filter(is_approved=False)
    context_object_name = 'users'

    
class StandbyUserDetailView(DetailView):
    model = CustomUser
    template_name = 'user_detail.html'
    context_object_name = 'user'

class StandbyUserPromoteView(View):
    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.is_staff = True
        user.save()
        return redirect('accounts:standby_user_detail', pk=pk)