from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

# Create your models here.
class MyLogin(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        if len(username) > 18:
            raise ValidationError("Username cannot exceed 18 characters.")
        return username