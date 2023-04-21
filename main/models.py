from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# Add this later if you implement GeoDjango
'''
class Address(models.Model):
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
	address_line_1 = models.CharField(max_length=50)
	address_line_2 = models.CharField(max_length=50, blank=True)
	city = models.CharField(max_length=50)
	zip_code = models.CharField(max_length=10)
	location = LocationField(srid=4326)
	point = models.PointField(srid=4326)
	latitude = models.FloatField(blank=True, null=True)
	longitude = models.FloatField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
'''


class Restaurant(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=250)

	address = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=50)

	rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

	image = models.FileField(blank=True,null=True)

	TypeofRestaurants = [
		('Polish','Polish'),
		('Asian','Asian'),
		('Kebab','Kebab'),
		('Pizza','Pizza'),
		('Sushi','Sushi'),
		('Italian','Italian'),
		('Burger','Burger'),
		('American','American'),
		('Other','Other'),
	]
	TypeofRestaurant = models.CharField(
		max_length=20,
		choices=TypeofRestaurants,
		default='Other',
	)

	@property
	def total_reviews(self):
		return self.reviews.all().count()

	# Get the list of stars to use in frontend
	@property
	def positiveStars(self):
		posStars = []
		for i in range(round(self.rating)):
			posStars.append(i)
		return posStars

	@property
	def negativeStars(self):
		negStars = []
		for i in range(5-round(self.rating)):
			negStars.append(i)
		return negStars
			
class FoodItem(models.Model):
	
	
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

	name = models.CharField(max_length=100)
	description = models.CharField(max_length=250)

	price = models.DecimalField(max_digits=10, decimal_places=2)
	
	image = models.FileField(blank=True,null=True)


class RestaurantReview(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reviews")
	rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

	review_text = models.CharField(max_length=500)
	review_date = models.DateTimeField("DateofReview",auto_now=True)

	@property
	def positiveStars(self):
		posStars = []
		for i in range(round(self.rating)):
			posStars.append(i)
		return posStars

	@property
	def negativeStars(self):
		negStars = []
		for i in range(5-round(self.rating)):
			negStars.append(i)
		return negStars

class FoodPackage(models.Model):
	FoodIteminPackage = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

	quantity = models.DecimalField(max_digits=10, decimal_places=0)

class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

	delivery_address = models.CharField(max_length=50)
	FoodPackages = models.ManyToManyField(FoodPackage, related_name='cart_FoodPackage')

	total_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

	delivery_address = models.CharField(max_length=50)
	FoodPackages = models.ManyToManyField(FoodPackage, related_name='order_FoodPackage')

	notes = models.CharField(max_length=100,default=None)

	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)

	Statuses = [
		('Food is being prepared','Food is being prepared'),
		('In delivery','In delivery'),
		('Delivered','Delivered'),
	]
	orderStatus = models.CharField(
		max_length=30,
		choices=Statuses,
		default='Food is being prepared',
	)
	