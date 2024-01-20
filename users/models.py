from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from locations.models import Area
from project.celery import notfiy

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,username, password):
        user = self.create_user(
            username=username,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ]

class User(AbstractBaseUser):
    email= models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=11, unique=True)
    gender =models.CharField(max_length=20, choices=GENDER_CHOICES)
    city = models.ForeignKey(Area, on_delete=models.PROTECT, null=True, blank=True)
    credits = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    img = models.CharField(max_length=100, blank=True, null=True)
    
    notification_token = models.CharField(max_length=255, null=True, blank=True)
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'username' 

    REQUIRED_FIELDS = []

    objects = MyUserManager()
    
    def __str__(self):
        return  self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True
    

    def remove_notification_token(self):
        self.notification_token = None
        self.save(update_fields=['notification_token'])
        
    def update_notification_token(self, new_token):
        self.notification_token = new_token
        self.save(update_fields=['notification_token'])
        
    def deduct_credits(self, amount):
        if self.credits >= amount:
            self.credits -= amount
            self.save(update_fields=['credits'])
            return True  # Deduction successful
        else:
            raise ValueError('No enough credits.')
        
    def refund_credits(self, amount):
        self.credits += amount
        self.save(update_fields=['credits'])
        return True
    
    def send_notification(self, notification_body, details=None):
        fcm_url = "https://fcm.googleapis.com/fcm/send"
        fcm_server_key = "AAAAxm5MHOE:APA91bFTvcbli2I_poG2wffmnyrLSiYpFYUTpceFEq8MfCQndP3xWMmcrmNrQZuZCytXqaG9YIfsKj4SzB3D8-j9gWNFVWbB2LHJ0cIvm5qXgi1QHFhTRFNADYdQ9YaP-TDVqbjdLcPZ"
        headers = {
            "Authorization": "key=" + fcm_server_key,
            "Content-Type": "application/json"
        }

        payload = {
            "to": self.notification_token,
            "notification": {
                "body": notification_body,
                "title": "Momayz",
                "android_channel_id": "2"
            },
            "data": details,
            "priority": "high",
        }

        notfiy.delay(fcm_url, payload, headers)
