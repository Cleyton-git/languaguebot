from django.contrib.auth import get_user_model
from dotenv import load_dotenv
import os

load_dotenv()

USER_LOGIN = os.getenv("USER_LOGIN")
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username=USER_LOGIN,
        email=USER_EMAIL,
        password=USER_PASSWORD
    )