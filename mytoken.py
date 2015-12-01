import os
from itsdangerous import URLSafeTimedSerializer

secret_key = os.environ.get('SECRET_KEY')
security_password_salt = os.environ.get('SECURITY_PASSWORD_SALT')

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email,salt=security_password_salt)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(
                token,
                salt=security_password_salt,
                max_age=expiration
                )
    except:
        return False
    return email

#tt = generate_confirmation_token("yinyuanlin@gmail.com")
#print tt
#print confirm_token(tt)
