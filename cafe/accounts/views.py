import re, bcrypt, jwt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login, logout
from cafe.settings import SECRET_KEY
from .models import Account

# 계정 생성을 위한 API 등록 보기
class SignUpView(APIView):
    def post(self, request):
        data = request.data

        try:
            # 전화 번호 확인 (정규 표현식으로 01로 시작해서 8~11자리의 숫자만 받도록)
            phone_regex = re.compile(r'^01[0-9]{8,11}$')
            if data['phone'] == '' or (phone_regex.match(str(data['phone'])) is None):
                return Response({'meta': {'code': 400, 'message': 'INVALID_PHONE_NUMBER'}}, status=status.HTTP_400_BAD_REQUEST)
            
            # 암호가 제공되었는지 확인
            if data['password'] == '':
                return Response({'meta': {'code': 400, 'message': 'PASSWORD_IS_REQUIRED'}}, status=status.HTTP_400_BAD_REQUEST)

            # 중복된 전화 번호 확인
            if Account.objects.filter(phone=data['phone']).exists() and (data['phone'] != ''):
                return Response({'meta': {'code': 400, 'message': 'PHONE_DUPLICATED'}}, status=status.HTTP_400_BAD_REQUEST)

            # 암호 길이 확인
            if (len(data['password']) < 8):
                return Response({'meta': {'code': 400, 'message': 'PASSWORD_VALIDATION'}}, status=status.HTTP_400_BAD_REQUEST)

            # 암호 해시
            password = data['password']
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # 계정 생성
            Account.objects.create(
                phone=data['phone'],
                password=hashed_pw.decode('utf-8'),
                is_active=True, # 스태프 권한 여부
                is_admin=True, # 활성화 여부
            )
            return Response({'meta': {'code': 201, 'message': 'SUCCESS'}}, status=status.HTTP_201_CREATED)
        except KeyError as ex:
            return Response({'MESSAGE': 'KEY_ERROR_' + str.upper(ex.args[0])}, status=status.HTTP_400_BAD_REQUEST)

# 로그인을 위한 로그인 APIView
class SignInView(APIView):
    def post(self, request):
        data = request.data

        try:
            # 요청 데이터에서 전화 및 암호 가져오기
            password = data['password']
            account = data['phone']

            # 전화 번호와 암호가 제공되었는지 확인
            if account == '' or password == '':
                return Response({'meta': {'code': 400, 'message': 'Enter Your User Phone or Password'}}, status=status.HTTP_400_BAD_REQUEST)

            # 계정이 있는지 확인하고 암호 확인
            if Account.objects.filter(phone=account).exists():
                account_data = Account.objects.get(phone=account)

                if bcrypt.checkpw(password.encode('utf-8'), account_data.password.encode('utf-8')) == False:
                    return Response({'meta': {'code': 401, 'message': 'INVALID_USER'}}, status=status.HTTP_401_UNAUTHORIZED)

                # 사용자 인증 및 액세스 토큰 생성
                user = authenticate(request, phone=account, password=password)
                if user is not None:
                    login(request, user)
                    access_token = jwt.encode({'phone': account}, SECRET_KEY, algorithm='HS256')
                    return Response({'meta': {'code': 200, 'message': 'SUCCESS', 'Authorization': access_token}}, status=status.HTTP_200_OK)
                else:
                    return Response({'meta': {'code': 401, 'message': 'INVALID_USER'}}, status=status.HTTP_401_UNAUTHORIZED)

            else:
                return Response({'meta': {'code': 401, 'message': 'INVALID_USER'}}, status=status.HTTP_401_UNAUTHORIZED)

        except KeyError as ex:
            return Response({'meta': {'code': 400, 'message': 'KEY_ERROR_' + str.upper(ex.args[0])}}, status=status.HTTP_400_BAD_REQUEST) 
    
class SignOutView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능하도록 권한 설정

    def get(self, request):
        # 로그아웃 처리
        logout(request)
        return Response({'MESSAGE': 'SUCCESS'}, status=status.HTTP_200_OK)

