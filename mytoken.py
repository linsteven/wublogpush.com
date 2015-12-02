import os
from itsdangerous import URLSafeSerializer

secret_key = os.environ.get('SECRET_KEY')
security_password_salt = os.environ.get('SECURITY_PASSWORD_SALT')

def generate_confirmation_token(email):
    serializer = URLSafeSerializer(secret_key,salt=security_password_salt)
    return serializer.dumps(email)

def confirm_token(token):
    serializer = URLSafeSerializer(secret_key,salt=security_password_salt)
    try:
        email = serializer.loads(token)
    except:
        return False
    return email

#tt = generate_confirmation_token("yinyuanlin@gmail.com")
#print tt
#print confirm_token(tt)
