from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_GET
from django.core.validators import validate_email
from django.http import JsonResponse

from .models import CustomUser
from .forms import CustomUserCreationForm

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
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_approve = False  # 가입 대기 상태로 생성
        user.save()
        return super().form_valid(form)
    

class StandbyUserListView(ListView):
    model = CustomUser
    template_name = 'standby_user_list.html'
    queryset = CustomUser.objects.filter(is_approved=False)
    context_object_name = 'users'

    
class StandbyUserDetailView(DetailView):
    model = CustomUser
    template_name = 'standby_user_detail.html'
    context_object_name = 'user'
