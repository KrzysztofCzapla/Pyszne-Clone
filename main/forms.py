from django import forms
from django.forms import Textarea
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RestaurantReviewForm(forms.ModelForm):

	class Meta:
		model = RestaurantReview
		fields ="__all__"
		exclude = ['user','restaurant','review_date','rating']
		auto_id = False
		widgets = {
			'review_text': Textarea(attrs={'cols': 50, 'rows': 7}),
		}
		labels = {
			"review_text": "",
		}

class OrderForm(forms.ModelForm):

	class Meta:
		model = Order
		fields=["delivery_address","notes"]
		
	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['notes'].required = False	