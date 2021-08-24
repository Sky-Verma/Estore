from django.forms import ModelForm
from .models import user_info


class user_info_form(ModelForm):

    class Meta:
        model = user_info
        fields = ['profile_image', 'phone_number', 'about']
