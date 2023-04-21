from django.shortcuts import render,get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
try:
	from django.utils import simplejson as json
except ImportError:
	import json
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.serializers import OrderSerializer

def index(request,SearchType=None):
	context = {}
	# Get double table from Restaurant model
	restaurantTypesFromModel = Restaurant.TypeofRestaurants
	# Get the real table
	restaurantTypes = []
	# Take only first parameter from table and put in in the real table
	for restaurantType in restaurantTypesFromModel:
		restaurantTypes.append(restaurantType[0])

	# Adding this to context
	context.update({"restaurantTypes":restaurantTypes})

	# Checking if there is searching for certain type of restaurant
	if SearchType:
		context.update({"SearchType":SearchType})
		Restaurants = Restaurant.objects.all().filter(TypeofRestaurant=SearchType)
	else:
		Restaurants = Restaurant.objects.all()

	if request.method == 'GET':
		if request.GET.get('sort') == 'Number of reviews':
			Restaurants = Restaurants.annotate(reviewsNumber=Count('reviews')).order_by('-reviewsNumber')
		elif request.GET.get('sort') == 'Rating':
			Restaurants = Restaurants.order_by('-rating')
		elif request.GET.get('sort') == 'Name':
			Restaurants = Restaurants.order_by('name')

	

	context.update({"Restaurants":Restaurants})
	if request.is_ajax():
			print(request.POST)

	return render(request, 'main/index.html', context)

@login_required
def restaurantDetails(request,RestaurantName):
	context = {}

	RestaurantDetail = Restaurant.objects.all().filter(name=RestaurantName)[0]

	

	FoodItemsOfRestaurant = FoodItem.objects.all().filter(restaurant=RestaurantDetail)

	if request.method == 'GET':
		if request.GET.get('sort') == 'Price Ascending':
			FoodItemsOfRestaurant = FoodItemsOfRestaurant.order_by('price')
		if request.GET.get('sort') == 'Price Descending':
			FoodItemsOfRestaurant = FoodItemsOfRestaurant.order_by('-price')
		elif request.GET.get('sort') == 'Name':
			FoodItemsOfRestaurant = FoodItemsOfRestaurant.order_by('name')

	

	CartOfUser = Cart.objects.get_or_create(user=request.user, restaurant=RestaurantDetail)[0]

	CartOfUser.FoodPackages.clear()

	FoodPackage.objects.all().filter(order_FoodPackage=None).delete()




	context.update({"Restaurant":RestaurantDetail})
	context.update({"FoodItems":FoodItemsOfRestaurant})
	context.update({"Cart":CartOfUser})



	return render(request, 'main/restaurantDetails.html', context)


@login_required
def orderdone(request):
	context = {}

	

	return render(request, 'main/orderdone.html', context)

@login_required
def profile(request, userID):
	context = {}
	
	Orders = Order.objects.all().filter(user=request.user).order_by('-created_at')
	
	context.update({"orders":Orders})

	Packages = FoodPackage.objects.all()


	context.update({"Packages":Packages})
	
	return render(request, 'main/profile.html', context)

@login_required
def order(request,RestaurantName):
	context = {}
	RestaurantDetail = Restaurant.objects.all().filter(name=RestaurantName)[0]
	CartOfUser = Cart.objects.get_or_create(user=request.user, restaurant=RestaurantDetail)[0]

	if request.method == "POST":
		orderFormObject = OrderForm(request.POST)
		print("BRUB")
		if orderFormObject.is_valid():
				

			orderObject = orderFormObject.save(commit=False)

			

			orderObject.delivery_adress = request.POST.get("adress")
			orderObject.notes = request.POST.get("notes")
			orderObject.total_price = CartOfUser.total_price
			orderObject.user = request.user
			orderObject.restaurant = RestaurantDetail
			orderObject.save()
			orderObject.FoodPackages.set(CartOfUser.FoodPackages.all())
			orderObject.save()
			return HttpResponseRedirect(reverse('main:orderdone'))

	else:
		orderFormObject = OrderForm()
		

	'''if request.method == 'POST':
		reviewForm = RestaurantReviewForm(request.POST, instance=ReviewOfUser)		
		if reviewForm.is_valid():
			review = reviewForm.save(commit=False)

			review.user = request.user
			review.restaurant = RestaurantDetail
			review.rating = request.POST.get('a')

			review.save()
			return HttpResponseRedirect(reverse('main:restaurantReviews',kwargs={'RestaurantName':RestaurantDetail.name}))'''

	context.update({"form":orderFormObject})

	Packages = FoodPackage.objects.all().filter(cart_FoodPackage=CartOfUser)
	context.update({"Packages":Packages})	

	context.update({"cart":CartOfUser})			

	return render(request, 'main/order.html', context)

@login_required
def restaurantReviews(request,RestaurantName):
	context = {}

	RestaurantDetail = Restaurant.objects.all().filter(name=RestaurantName)[0]

	RestaurantDetail.rating = 0

	RestaurantReviews = RestaurantReview.objects.all().filter(restaurant=RestaurantDetail).order_by('-review_date')

	try:
		ReviewOfUser = RestaurantReview.objects.all().filter(restaurant=RestaurantDetail, user=request.user)[0]
	except Exception as e:
		ReviewOfUser = None
	

	##### 

	allRatings = 0
	howMany = 0

	for review in RestaurantReviews:
		allRatings += review.rating
		howMany += 1

	if howMany > 0:
		allRatings = round(allRatings/howMany, 2)

	RestaurantDetail.rating = allRatings
	RestaurantDetail.save()

	#####

	hasUserPostedReview = False

	for review in RestaurantReviews:
		if review.user == request.user:
			hasUserPostedReview = True
	
	if request.method == 'GET':
		if request.GET.get('sort') == 'Highest':
			RestaurantReviews = RestaurantReviews.order_by('-rating')
		elif request.GET.get('sort') == 'Lowest':
			RestaurantReviews = RestaurantReviews.order_by('rating')
	

	context.update({"Restaurant":RestaurantDetail})
	context.update({"RestaurantReviews":RestaurantReviews})
	context.update({"hasUserPostedReview":hasUserPostedReview})

	if request.method == 'POST':
		reviewForm = RestaurantReviewForm(request.POST, instance=ReviewOfUser)		
		if reviewForm.is_valid():
			review = reviewForm.save(commit=False)

			review.user = request.user
			review.restaurant = RestaurantDetail
			review.rating = request.POST.get('a')

			review.save()
			return HttpResponseRedirect(reverse('main:restaurantReviews',kwargs={'RestaurantName':RestaurantDetail.name}))
	else:
		reviewForm = RestaurantReviewForm(instance=ReviewOfUser)


	context.update({"form":reviewForm})	

	return render(request, 'main/restaurantReviews.html', context)

@login_required
@require_POST
def addToCart(request):
	#print(request.POST.dir)

	if request.method == 'POST':
		

		restaurantName = request.POST.get('restaurantName', None)
		restaurant = get_object_or_404(Restaurant, name=restaurantName)

		FoodItemName = request.POST.get('FoodItemName', None)
		FoodItemObject = get_object_or_404(FoodItem, name=FoodItemName, restaurant=restaurant)

		NumberOfItems = request.POST.get('NumberOfItems', None)
		CartOfUser = Cart.objects.get_or_create(user=request.user, restaurant=restaurant)[0]

		CartOfUser.total_price = request.POST.get('cartprice', None)
		CartOfUser.save()

		FoodPackageObject = FoodPackage(quantity=0)
		FoodPackageObject.FoodIteminPackage = FoodItemObject
		FoodPackageObject.quantity = NumberOfItems
		FoodPackageObject.save()
		

		
		CartOfUser.FoodPackages.add(FoodPackageObject)


	ctx = {'hehe': 1}

	return HttpResponse(json.dumps(ctx), content_type='application/json')

@login_required
@require_POST
def deleteFromCart(request):

	if request.method == 'POST':

		restaurantName = request.POST.get('restaurantName', None)
		restaurant = get_object_or_404(Restaurant, name=restaurantName)

		CartOfUser = Cart.objects.get_or_create(user=request.user, restaurant=restaurant)[0]

		


		FoodItemName = request.POST.get('FoodItemName', None)
		FoodItemObject = FoodItem.objects.all().filter(name=FoodItemName, restaurant=restaurant)[0]

		NumberOfItems = request.POST.get('NumberOfItems', None)
		
		FoodPackageObject = FoodPackage.objects.all().filter(FoodIteminPackage=FoodItemObject, quantity=NumberOfItems)[0]

		CartOfUser.FoodPackages.remove(FoodPackageObject)

		CartOfUser.total_price = request.POST.get('cartprice', None)
		CartOfUser.save()


	ctx = {'hehe': 1}
	
	return HttpResponse(json.dumps(ctx), content_type='application/json')

##### API

@api_view(['GET'])
def order_collection(request):
	if request.method == 'GET':
		orders = Order.objects.all()
		serializer = OrderSerializer(orders, many=True)
		return Response(serializer.data)


@api_view(['GET'])
def order_element(request, orderID):
	try:
		order = Order.objects.get(pk=orderID)
	except Order.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = OrderSerializer(order)
		return Response(serializer.data)

@api_view(['POST'])
def AddOrderAPI(request):
	if request.method == 'POST':
		orders = Order.objects.all()
		serializer = OrderSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
		return Response()
#########	


