from django import forms

from authentication.models import Profile, User


class ProfileUpdateForm(forms.ModelForm):
    email = forms.CharField(max_length=100)
    class Meta:
        model = Profile
        fields = '__all__'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('u_id', 'first_name', 'last_name', 'birthday')


class UserAddForm(forms.Form):
    username = forms.CharField(max_length=100, required = False)
    password = forms.CharField(max_length=100, required = False)
    
    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            user = User.objects.get(username=username)
        except user.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username "%s" is already in use.' % username)