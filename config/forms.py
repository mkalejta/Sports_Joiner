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
            'placeholder': 'Podaj nazwę użytkownika',
            'help_text': '<span class="form-text text-muted"><small>Wymagany. 150 znaków lub mniej. Tylko litery, cyfry i @ / ./ + / - / _.</small></span>'
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Podaj imię'
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Podaj nazwisko'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Podaj adres e-mail'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Podaj hasło'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Potwierdź hasło'
        })
        self.fields['password1'].help_text = ('<ul class="form-text text-muted small"><li>Twoje hasło nie może być zbyt podobne do innych danych osobowych.</li>'
                                              '<li>Twoje hasło musi zawierać co najmniej 8 znaków.</li><li>Twoje hasło nie może być powszechnie używanym hasłem.</li>'
                                              '<li>Twoje hasło nie może być całkowicie numeryczne.</li></ul>')
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Wprowadź to samo hasło, co poprzednio, w celu weryfikacji.</small></span>'

        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['first_name'].label = 'Imię'
        self.fields['last_name'].label = 'Nazwisko'
        self.fields['email'].label = 'Adres e-mail'
        self.fields['password1'].label = 'Hasło'
        self.fields['password2'].label = 'Hasło (powtórz ponownie)'

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
    def __init__(self, *args, **kwargs):
        super(UpdateProfile, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Podaj nazwę użytkownika',
            'help_text': '<span class="form-text text-muted"><small>Wymagany. 150 znaków lub mniej. Tylko litery, cyfry i @ / ./ + / - / _.</small></span>'
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Podaj imię'
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Podaj nazwisko'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Podaj adres e-mail'
        })

        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['username'].help_text = 'Wymagany. 150 znaków lub mniej. Tylko litery, cyfry i @ / ./ + / - / _.'
        self.fields['first_name'].label = 'Imię'
        self.fields['last_name'].label = 'Nazwisko'
        self.fields['email'].label = 'Adres e-mail'

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


# Edit Profile Fields
class ProfilePicForm(f.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfilePicForm, self).__init__(*args, **kwargs)

        self.fields['profile_picture'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['birth_date'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['profile_picture'].widget.initial_text = 'Obecne zdjęcie'
        self.fields['profile_picture'].widget.input_text = "Zmień"

    profile_picture = f.ImageField(label="Zdjęcie profilowe")
    birth_date = f.DateField(label="Data urodzenia",
                             widget=f.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                             input_formats=["%Y-%m-%d"])

    class Meta:
        model = models.Profile
        fields = ('profile_picture', 'birth_date')


class CreateEventForm(f.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)

        self.fields['facility'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['estimated_time'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['max_participants'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['estimated_time'].label = 'Przewidywany czas trwania (w minutach)'
        self.fields['max_participants'].label = 'Maksymalna liczba uczestników'
        self.fields['description'].label = 'Opis(opcjonalnie)'

    date = f.DateField(label="Data", widget=f.DateInput(format="%Y-%m-%d",
                                                        attrs={"type": "text", "class": "form-control", 'placeholder': 'Wybierz datę',
                                                               'onfocus': "(this.type='date')"}), input_formats=["%Y-%m-%d"])
    time = f.TimeField(label="Czas rozpoczęcia", widget=f.TimeInput(format="%H:%M",
                                                        attrs={"type": "text", "class": "form-control", 'placeholder': 'Wybierz godzinę',
                                                               'onfocus': "(this.type='time')"}), input_formats=["%H:%M"])
    facility = f.ModelChoiceField(label="Adres spotkania", queryset=models.Facility.objects.all(), empty_label='Wybierz adres')

    class Meta:
        model = models.Event
        fields = ('facility', 'date', 'time', 'estimated_time', 'max_participants', 'description')