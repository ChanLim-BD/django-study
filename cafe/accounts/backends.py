from django.contrib.auth.backends import BaseBackend # BaseBackend는 Django의 기본 인증 백엔드를 상속받는 클래스
from .models import Account

"""
이 코드는 Account 모델을 사용하여 사용자 인증을 처리합니다. 
Account 모델은 사용자 정보를 저장하는 Django 모델입니다.
phone 필드를 사용하여 사용자를 식별하고, check_password() 메서드를 사용하여 비밀번호를 검증합니다.

이 코드는 사용자 지정 인증 로직을 제공하기 위해 Django에서 제공하는 기본 인증 백엔드를 상속하고, Account 모델을 사용하는 방식으로 Django의 인증 시스템을 확장하고 있습니다.
"""

class AccountBackend(BaseBackend):
    # BaseBackend를 상속받은 AccountBackend 클래스에서는 authenticate()와 get_user() 메서드를 구현
    def authenticate(self, request, phone=None, password=None, **kwargs):
        # authenticate() 메서드는 사용자가 로그인할 때 호출
        try:
            user = Account.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        # authenticate() 메서드에서 반환된 유저 객체를 받아서, 해당 유저의 id 값을 이용해 유저 객체를 반환
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None

