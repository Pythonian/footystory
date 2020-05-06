from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget(show_preview=False))
	publish = forms.DateField(widget=forms.SelectDateWidget)
	class Meta:
		model = Post
		fields = ['title', 'image', 'content', 'draft', 'publish']




# from django import forms
# from .models import Category, Tag
# from django.utils.html import mark_safe
# from mptt.forms import TreeNodeChoiceField
# from crispy_forms.helper import FormHelper
# from crispy_forms import layout, bootstrap


# class PostFilterForm(forms.Form):
# 	# category = forms.ModelChoiceField(
# 	# 	label="Category",
# 	# 	required=False,
# 	# 	queryset=Category.objects.all())
# 	tag = TreeNodeChoiceField(
# 		label='Tag',
# 		queryset=Tag.objects.all(),
# 		required=False,
# 		level_indicator=mark_safe(
# 			"&nbsp;&nbsp;&nbsp;&nbsp;"))

# 	# Then, create a URL rule, view, and template to show this form


# class MultipleChoiceTreeField(forms.ModelMultipleChoiceField):
# 	widget = forms.CheckboxSelectMultiple
# 	def label_from_instance(self, obj):
# 		return obj 


# class TagForm(forms.ModelForm):
# 	tags = MultipleChoiceTreeField(
# 		label='Tags',
# 		required=False,
# 		queryset=Tag.objects.all())

# 	class Meta:
# 		model = Tag
# 		fields = ['title']

# 	def __init__(self, *args, **kwargs):
# 		super(TagForm, self).__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_action = ""
# 		self.helper.form_method = "POST"
# 		self.helper.layout = layout.Layout(
# 		    layout.Field("title"),
# 		    layout.Field(
# 		         "tags",
# 		         template="blog/post_detail.html"
# 		    ),
# 		    bootstrap.FormActions(
# 		        layout.Submit("submit", "Save"),
# 		    )
# 		)
