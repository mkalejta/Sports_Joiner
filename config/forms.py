import django.forms as f
from app import models
from django.contrib.auth.forms import User, UserCreationForm, UserChangeForm

def CapitalizeValidation(c):
    if c[0].islower():
        raise f.ValidationError(f"{c} musi się zaczynać wielką literą!")


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username',
            'help_text': '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
        self.fields['password1'].help_text = ('<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li>'
                                              '<li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li>'
                                              '<li>Your password can\'t be entirely numeric.</li></ul>')
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    username = f.CharField(max_length=30)
    first_name = f.CharField(max_length=150, validators=[CapitalizeValidation])
    last_name = f.CharField(max_length=150, validators=[CapitalizeValidation])
    email = f.EmailField(max_length=150)
    password1 = f.CharField(widget=f.PasswordInput)
    password2 = f.CharField(widget=f.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


# Edit User Fields
class UpdateProfile(f.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


# Edit Profile Fields
class ProfilePicForm(f.ModelForm):
    profile_picture = f.ImageField(label="Profile Picture")
    birth_date = f.DateField(label="Birth Date",
                             widget=f.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                             input_formats=["%Y-%m-%d"])

    class Meta:
        model = models.Profile
        fields = ('profile_picture', 'birth_date')


class CreateEventForm(f.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)

        self.fields['facility'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['estimated_time'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['max_participants'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['estimated_time'].label = 'Estimated time (in minutes)'

    date = f.DateField(label="Date", widget=f.DateInput(format="%Y-%m-%d",
                                                        attrs={"type": "text", "class": "form-control", 'placeholder': 'Choose date',
                                                               'onfocus': "(this.type='date')"}), input_formats=["%Y-%m-%d"])
    time = f.TimeField(label="Time", widget=f.TimeInput(format="%H:%M",
                                                        attrs={"type": "text", "class": "form-control", 'placeholder': 'Choose time',
                                                               'onfocus': "(this.type='time')"}), input_formats=["%H:%M"])
    facility = f.ModelChoiceField(queryset=models.Facility.objects.all(), empty_label='Select facility')

    class Meta:
        model = models.Event
        fields = ('facility', 'date', 'time', 'estimated_time', 'max_participants', 'description')