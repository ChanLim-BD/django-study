from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_GET
from django.core.validators import validate_email
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login

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
        user.status = 'W' 
        user.save()
        return super().form_valid(form)
    

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.status == 'S':
                messages.error(request, "이미 탈퇴한 회원입니다.")
                return redirect('accountapp:login')
            else:
                login(request, user)
                return redirect('accountapp:user_list')
        else:
            messages.error(request, "잘못된 정보입니다.")
            return redirect('accountapp:login')
    

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
    context_object_name = 'users'

    def get_queryset(self):
        queryset = CustomUser.objects.filter(status__in=['A', 'S'])
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(email__icontains=search_query)
        return queryset



class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'user_detail.html'
    context_object_name = 'user'


@login_required
def update_permission(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.user.level == 'M':
        if request.method == 'POST':
            user.permission_approve = bool(request.POST.get('permission_approve'))
            user.permission_list = bool(request.POST.get('permission_list'))
            user.permission_edit = bool(request.POST.get('permission_edit'))
            user.permission_delete = bool(request.POST.get('permission_delete'))
            user.save()
            messages.success(request, f"{user.email} 회원의 권한이 변경되었습니다.")
            return redirect('accountapp:user_detail', pk=user.pk)
        else:
            context = {
                'user': user,
            }
            return render(request, 'update_permission.html', context)
    elif request.user.level == 'A' and user.level == 'U':
        if request.method == 'POST':
            user.permission_approve = bool(request.POST.get('permission_approve'))
            user.permission_list = bool(request.POST.get('permission_list'))
            user.permission_edit = bool(request.POST.get('permission_edit'))
            user.permission_delete = bool(request.POST.get('permission_delete'))
            user.save()
            messages.success(request, f"{user.email} 회원의 권한이 변경되었습니다.")
            return redirect('accountapp:user_detail', pk=user.pk)
        else:
            context = {
                'user': user,
            }
            return render(request, 'update_permission.html', context)
    else:
        return HttpResponseForbidden()


@login_required
def update_level(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.user.level == 'M':
        if request.method == 'POST':
            if user.level == 'U':
                user.level = 'A'
                user.permission_approve = True
                user.permission_list = True
                user.permission_edit = True
                user.permission_delete = True
            else:
                user.level ='U'
                user.permission_approve = False
                user.permission_list = True
                user.permission_edit = True
                user.permission_delete = False
            user.save()
            messages.success(request, f"{user.email} 회원의 등급이 변경되었습니다.")
            return redirect('accountapp:user_list')
    elif request.user.level == 'A' and user.level == 'U':
        if request.method == 'POST':
            if user.level == 'U':
                user.level = 'A'
                user.permission_approve = True
                user.permission_list = True
                user.permission_edit = True
                user.permission_delete = True
            else:
                user.level ='U'
                user.permission_approve = False
                user.permission_list = True
                user.permission_edit = True
                user.permission_delete = False
            user.save()
            messages.success(request, f"{user.email} 회원의 등급이 변경되었습니다.")
            return redirect('accountapp:user_list')
    else:
        return HttpResponseForbidden()

@login_required
@user_passes_test(lambda u: u.permission_edit == True)
def update_user_info(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.name = request.POST.get('name')
        user.phone_number = request.POST.get('phone_number')
        user.save()
        messages.success(request, f"{user.email} 회원 정보가 수정되었습니다.")
        return redirect('accountapp:user_detail', pk=user.pk)
    else:
        context = {
            'user': user,
        }
        return render(request, 'update_user_info.html', context)



@login_required
@user_passes_test(lambda u: u.permission_approve == True)
def reject_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        reject_reason = request.POST.get('reject_reason')
        user.status = 'R'
        user.date_rejected = timezone.now()
        user.reject_reason = reject_reason
        user.save()
        messages.success(request, f"{user.email} 회원이 거절되었습니다.")
    return redirect('accountapp:standby_user_detail', pk=user.pk)


@login_required
@user_passes_test(lambda u: u.permission_approve == True)
def approve_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, status='W')
    user.status = 'A'
    user.permission_list = True
    user.permission_edit = True
    user.save()
    messages.success(request, f"{user.email} 회원이 승인되었습니다.")
    return redirect('accountapp:standby_user_detail', pk=user.pk)


@login_required
@user_passes_test(lambda u: u.permission_delete == True)
def secession_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        secession_reason = request.POST.get('secession_reason')
        user.status = 'S'
        user.date_secession = timezone.now()
        user.secession_reason = secession_reason
        user.save()
        messages.success(request, f"{user.email} 회원이 탈퇴되었습니다.")
    return redirect('accountapp:user_detail', pk=user.pk)