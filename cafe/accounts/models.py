from django.db import models
from django.utils import timezone
import bcrypt

class Account(models.Model):
    phone = models.CharField(max_length=45, unique=True)        # 사용자의 전화번호를 저장
    password = models.CharField(max_length=200)                 # 암호화된 사용자 비밀번호를 저장
    last_login = models.DateTimeField(default=timezone.now)     # 사용자가 마지막으로 로그인 한 날짜 및 시간을 저장
    is_active = models.BooleanField(default=True)               # 계정 활성화 여부 
    is_admin = models.BooleanField(default=False)               # 관리자 여부
    is_authenticated = True                                     # 인증 여부

    USERNAME_FIELD = 'phone'

    def set_password(self, password):
        # 입력 받은 비밀번호를 bcrypt 암호화 알고리즘을 사용하여 암호화하고, password 필드에 저장
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # 입력 받은 비밀번호가 bcrypt 암호화 알고리즘을 사용하여 암호화된 password 필드와 일치하는지 확인
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def has_perm(self, perm, obj=None):
        # Django의 권한 시스템을 사용하여 사용자 권한을 확인하는 데 사용
        return True

    def has_module_perms(self, app_label):
        # Django의 권한 시스템을 사용하여 사용자 권한을 확인하는 데 사용
        return True
    
    def get_username(self):
        # 사용자의 username을 반환
        return self.phone
    
    @property
    def is_staff(self):
        # 사용자가 관리자인지 여부를 반환
        return self.is_admin

