from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

user = User.objects.get(username='john')
token, created = Token.objects.get_or_create(user=user)
print(token.key)
