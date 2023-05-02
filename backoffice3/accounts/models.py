from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11)

    # 회원 상태 값 추가
    STATUS_CHOICES = (
        ('W', '대기'),
        ('A', '승인'),
        ('R', '거절'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='W')

    # 회원 등급 추가
    LEVEL_CHOICES = (
        ('M', '마스터'),
        ('A', '관리자'),
        ('U', '일반'),
    )
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, default='U')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    permission_approve = models.BooleanField(default=False)
    permission_list = models.BooleanField(default=False)
    permission_edit = models.BooleanField(default=False)
    permission_delete = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    date_rejected = models.DateTimeField(blank=True, null=True)
    reject_reason = models.TextField(blank=True, null=True)

    date_secession = models.DateTimeField(blank=True, null=True)
    secession_reason = models.TextField(blank=True, null=True) 

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['name', 'phone_number']

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # 권한 설정 메서드 추가
    def can_approve_users(self):
        return self.level == 'M'

    def can_change_user_level(self, user):
        return self.level == 'M' and user.level != 'M'

    def can_manage_user_permissions(self, user):
        return self.level == 'M' and user.level != 'M'

    def can_manage_user(self, user):
        """
        해당 user를 관리할 수 있는지 검사하는 메서드
        """
        return self.level == 'M' or self.level == 'A' or self == user

    def can_view_user(self, user):
        """
        해당 user를 조회할 수 있는지 검사하는 메서드
        """
        return self.level != 'U' or self == user

    def can_edit_user(self, user):
        """
        해당 user를 수정할 수 있는지 검사하는 메서드
        """
        return self.level == 'M' or self == user

    def can_delete_user(self, user):
        """
        해당 user를 삭제할 수 있는지 검사하는 메서드
        """        
        return self.level == 'M' or self == user

