from django.contrib.auth.forms import UserCreationForm

from .models import User

class CustomerRegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('phone', 'first_name', 'last_name', 'email', 'address1', 'address2', 'city', 'country', 'zip_code', 'user_type',)


class AgentRegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('address1', )