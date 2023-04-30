import json, re, bcrypt, jwt

from django.views import View
from django.http import JsonResponse

from cafe.settings import SECRET_KEY
from .models import Account

class SignUpView(View): #회원가입
    def post(self, request):
        data = json.loads(request.body)

        try:
            phone_regex = re.compile(r'^01([016789]?)-?[1-9]\d{4}-?\d{4}$')
            if data['phone'] == '' and (phone_regex.match(str(data['phone'])) != None) == False:
                return JsonResponse({'MESSAGE': 'Phone number is required'}, status=400)
            if data['password'] == '':
                return JsonResponse({'MESSAGE': 'password is required'}, status=400)

            if Account.objects.filter(phone = data['phone']).exists() and (data['phone'] != ''):
                return JsonResponse({'MESSAGE':'PHONE_DUPLICATED'}, status = 400)

            if (len(data['password']) < 8):
                return JsonResponse({'MESSAGE':'PASSWORD_VALIDATION'}, status = 400)

            password = data['password']
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            Account.objects.create(
                phone 	 = data['phone'], 
                password = hashed_pw.decode('utf-8')
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)
        except KeyError as ex:
            return JsonResponse({'MESSAGE':'KEY_ERROR_' + str.upper(ex.args[0])}, status = 400)
        

class SignInView(View): #로그인
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            password = data['password']
            account  = data['phone']
            
            if account == '' or password == '':
                return JsonResponse({'MESSAGE':'Enter Your User Password'}, status = 400)
                       
            if Account.objects.filter(phone = account).exists():
                account_data = Account.objects.get(phone = account)

                if bcrypt.checkpw(password.encode('utf-8'), account_data.password.encode('utf-8')) == False:
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status = 401)
                
                access_token = jwt.encode({'phone': account}, SECRET_KEY, algorithm='HS256')

            else:
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status = 401)

            return JsonResponse({'MESSAGE':'SUCCESS', 'Authorization':access_token}, status = 200)
        except KeyError as ex:
            return JsonResponse({'MESSAGE':'KEY_ERROR_' + str.upper(ex.args[0])}, status = 400)
        
class SignOutView(View): #로그아웃
    def get(self, request):
        request.session.flush()
        return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)