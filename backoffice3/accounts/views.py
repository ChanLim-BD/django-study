from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_GET
from django.core.validators import validate_email
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

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
    success_url = reverse_lazy('accountapp:login')
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.status = 'W'  # 가입 대기 상태로 생성
        user.save()
        return super().form_valid(form)
    

class StandbyUserListView(ListView):
    model = CustomUser
    template_name = 'standby_user_list.html'
    queryset = CustomUser.objects.filter(status__in=['W', 'R'])
    context_object_name = 'users'

    
class StandbyUserDetailView(DetailView):
    model = CustomUser
    template_name = 'standby_user_detail.html'
    context_object_name = 'user'
    

class UserListView(ListView):
    model = CustomUser
    template_name = 'user_list.html'
    queryset = CustomUser.objects.filter(status='A')
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'user_detail.html'
    context_object_name = 'user'


@login_required
@user_passes_test(lambda u: u.level == 'M')
def update_level(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    print(user.level)
    if request.method == 'POST':
        if user.level == 'U':
            user.level = 'A'
            user.permission_approve = True
            user.permission_list = True
            user.permission_edit = True
            user.permission_delete = True
        else:
            user.level ='U'
        user.save()
        messages.success(request, f"{user.email} 회원의 등급이 변경되었습니다.")
    return redirect('accountapp:standby_user_list')

@login_required
@user_passes_test(lambda u: u.level == 'M')
def update_permission(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.permission_approve = bool(request.POST.get('permission_approve'))
        user.permission_list = bool(request.POST.get('permission_list'))
        user.permission_edit = bool(request.POST.get('permission_edit'))
        user.permission_delete = bool(request.POST.get('permission_delete'))
        user.save()
        messages.success(request, f"{user.email} 회원의 권한이 변경되었습니다.")
        return redirect('accountapp:standby_user_detail', pk=user.pk)
    else:
        context = {
            'user': user,
        }
        return render(request, 'update_permission.html', context)


@login_required
@user_passes_test(lambda u: u.level == 'M')
def reject_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        reject_reason = request.POST.get('reject_reason')
        user.is_rejected = True
        user.date_rejected = timezone.now()
        user.reject_reason = reject_reason
        user.save()
        messages.success(request, f"{user.email} 회원이 거절되었습니다.")
    return redirect('accountapp:standby_user_detail', pk=user.pk)

@login_required
@user_passes_test(lambda u: u.level == 'M')
def approve_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, status='W')
    user.status = 'A'
    user.permission_list = True
    user.permission_edit = True
    user.save()
    messages.success(request, f"{user.email} 회원이 승인되었습니다.")
    return redirect('accountapp:standby_user_detail', pk=user.pk)
