from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import EmailField


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        # создаем юзера
        user = self.model(email=email, **extra_fields)
        # создаем пароль и хэшируем
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
            # создаем супер юзера
        user = self.model(email=email, **extra_fields)
        # создаем пароль и хэшируем
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    email = EmailField(unique=True)
    username = models.CharField(max_length=155, unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=30, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def create_activation_code(self):
        """
        шифрование:
        1. hashlib.md5(self.email + str(self.id)).encode() -> hexdigest()
        test@test.com.com155 -> GIHIUGENI4UT98WY873*(^YIHdeguweh*&Yuhoi9u08
        2. get_random_string(50, allowed_char=['какие символы разрешены в нашей рандомной строке, из чего будут состоять'])
        3. UUID
        4. datetime.datetime.now() or time.time() + timestamp() 01.01.1978
        """
        import hashlib
        string = self.email + str(self.id)
        encode_string = string.encode()
        md5_object = hashlib.md5(encode_string)
        activation_code = md5_object.hexdigest()
        self.activation_code = activation_code

    def __str__(self):
        return f'{self.username} {self.email}'