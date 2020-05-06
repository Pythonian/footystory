from django import forms
from django.contrib.auth import get_user_model 
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from .models import Profile


User = get_user_model()


USERNAME_REGEX = '^[a-zA-Z0-9]*$'


DISALLOWED_USERNAMES = [
	'activate', 'account', 'admin', 'about', 'administrator', 'activity', 'account', 'auth', 'authentication',
	'blogs', 'blog', 'billing', 
	'create', 'cookie', 'contact', 'config', 'contribute', 'campaign',
	'disable', 'delete', 'download', 'downloads', 'delete',
	'edit', 'explore', 'email', 
	'footystory', 'follow', 'feed', 'forum', 'forums',
	'intranet',
	'jobs', 'join',
	'login', 'logout', 'library',
	'media', 'mail', 
	'news', 'newsletter',
	'help', 'home', 
	'privacy', 'profile',
	'registration', 'register', 'remove', 'root', 'reviews', 'review',
	'signin', 'signup', 'signout', 'settings', 'setting', 'static', 'support', 'status', 'search', 'subscribe', 'shop',
	'terms', 'term',
	'update', 'username', 'user', 'users', 
]


class SignUpForm(UserCreationForm):
	username = forms.CharField(
		max_length=150,
		validators=[RegexValidator(
			regex=USERNAME_REGEX,
			message="Your username contains invalid characters.",
			code='invalid_username' )],
		help_text='Username must be alphanumeric only.',
		required=True,
		)
	# password1 = forms.CharField(
	# 	label=_("Password"),
	# 	strip=False,
	# 	widget=forms.PasswordInput,
	# 	help_text='Password must contain at least 8 characters.',
	# )
	email = forms.EmailField(
		max_length=254,
		required=True,
		help_text='Enter a valid email address.'
	)
	favorite_club = forms.CharField(
		required=True,
	)

	class Meta:
		model = User 
		fields = ['username', 'email', 'password1', 'password2', 'favorite_club']

	def clean_username(self):
		username = self.cleaned_data.get('username').lower()
		if username in DISALLOWED_USERNAMES:
			raise forms.ValidationError("You are not allowed to make use of this username.")
		if len(username) < 4:
			raise forms.ValidationError("Your username must not be less than 4 (four) characters.")
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email__iexact=email).exists():
			raise forms.ValidationError("A user with that email already exists.")
		return email

	def clean_favorite_club(self):
		favorite_club = self.cleaned_data.get('favorite_club')
		if favorite_club == 'None':
			raise forms.ValidationError("This entry is invalid.")
		return favorite_club


class UserForm(forms.ModelForm):
	email = forms.EmailField(
		max_length=254,
		required=True,
		help_text='Enter a valid email address.'
	)
	class Meta:
		model = User 
		fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
	about = forms.CharField(widget=forms.Textarea, required=False)
	class Meta:
		model = Profile 
		fields = ['about', 'avatar', 'website', 'location', 'favorite_club']

	def clean_favorite_club(self):
		favorite_club = self.cleaned_data.get('favorite_club')
		if favorite_club == 'None':
			raise forms.ValidationError("This entry is invalid.")
		return favorite_club


class ResendActivationEmailForm(forms.Form):
	email = forms.EmailField(
		max_length=254,
		required=True,
		help_text='Enter your email address.'
	)

	# def save(self, **kwargs):
	# 	email = form.cleaned_data['email']
	# 	try:
	# 		user = User.objects.get(email=email, is_active=False)
	# 	except:
	# 		return None
	# 	self.send_mail(user=user, **kwargs)
	# 	return user


