# from django.contrib.auth import get_user_model
from . import models
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):

    class Meta:

        fields=('username','first_name','last_name','email','password1','password2')
        # model = get_user_model()
        model = models.User


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['username'].label = "User Name"
        self.fields['email'].label = "Email Address"
