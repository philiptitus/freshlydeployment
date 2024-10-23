from .serializers import OrderSerializer
from .models import Order
from .serializers import FAQMainPageSerializer
from .models import FAQMainPage
from .serializers import FAQSerializer
from .models import FAQ  # Assuming your FAQ model is named FAQ
from .models import *
from .serializers import FarmerSerializer
from .serializers import UserProfileSerializer
import json
from .models import CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer
from django.shortcuts import render, redirect
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed, JsonResponse
from .models import Product, Garden, Service, Blog, Banner
from .forms import ProductForm, ServiceRequestForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import BlogForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.views import APIView
from .models import Blog, Comment, Like, Share, Poll, Vote, IDVerification, Cart, Category, Notification, Order, OrderItem, Product
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from .serializers import BlogSerializer, ProductSerializer, GardenSerializer, CommentSerializer, LikeSerializer, ShareSerializer, PollSerializer, VoteSerializer, IDVerificationSerializer, CartSerializer, BannerSerializer, CategorySerializer, NotificationSerializer
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.contrib.auth import get_user_model, login, logout
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, OrderSerializer
from rest_framework.validators import UniqueValidator
# Import your custom validation here
from .validators import custom_validation, validate_email, validate_password
# csrf_protect_method = method_decorator(csrf_protect)
from django.utils import timezone
import json
from django.views.decorators.http import require_http_methods

# imports for checkout

from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderItem, Product
from .mpesa_utils import lipa_na_mpesa_online
from rest_framework import generics
from rest_framework.permissions import AllowAny
import random


# This is for typical django frontend html

from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def index(request):
    get_token(request)
    return render(request, 'index.html')


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


@api_view(['GET'])
# class Blogs(APIView):
# permission_classes = (AllowAny,)
# authentication_classes = ()
# @csrf_protect_method
@csrf_exempt
def blogs(request):
    if request.user.is_authenticated:
        # renderer_classes = [JSONRenderer]
        return render(request, 'blogs/BlogForm.jsx')


@login_required
def products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products')
    else:
        form = ProductForm()
    products = Product.objects.filter(user=request.user)
    return render(request, 'products.html', {'products': products, 'form': form})


@login_required
def services(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form = ServiceRequestForm()
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services, 'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html')


# The blog CRUD
@csrf_exempt
def blog_list(request):
    if request.method == 'GET':
        blogs = Blog.objects.all()
        return render(request, 'blog_list.html', {'blogs': blogs})
    else:
        return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'blog': blog})


@api_view(['GET', 'POST'])
@csrf_exempt
@permission_classes([AllowAny])
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blogs/BlogForm.jsx')
    else:
        form = BlogForm()
    return render(request, 'blogs/BlogForm.jsx', {'form': form})


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def blog_create(request):
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@csrf_exempt
def blog_update(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', slug=blog.slug)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blogs/BlogForm.jsx', {'form': form})


def blog_delete(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blog_confirm_delete.html', {'blog': blog})

# Implemented views for CRUD operations and like/share actions


class BlogListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def list(self, request, *args, **kwargs):
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request data: {request.data}")
        return super().list(request, *args, **kwargs)


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]  # This allows unauthenticated access

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        return queryset


"""
    def blog_create(request):
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('blogs/BlogForm.jsx')
        else:
            form = BlogForm()
        return render(request, 'blogs/BlogForm.jsx', {'form': form})
"""


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def Register(request):
    # Use the serializer to validate the input data
    serializer = UserRegisterSerializer(data=request.data)

    if serializer.is_valid():
        # Extract validated data
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "This username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "An account with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the user and profile (profile handled in serializer)
        user = serializer.save()

        # Generate refresh and access tokens for the new user
        refresh = RefreshToken.for_user(user)

        # Create a welcome notification
        notification_message = f'Hi there {user.email}, welcome aboard! You have successfully created your account.'
        Notification.objects.create(user=user, message=notification_message)

        # Return a successful response with the tokens
        return Response({
            "message": "Signup successful!",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    # Return validation errors if any
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeCreateAPIView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShareCreateAPIView(generics.CreateAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'password_reset.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return super().form_valid(form)
        else:
            messages.error(
                self.request, 'No user is associated with this email address.')
            return self.form_invalid(form)


# serialiser
class GardenListCreateAPIView(generics.ListCreateAPIView):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer


class GardenRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BlogViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        queryset = self.get_queryset()
        blog = get_object_or_404(queryset, slug=slug)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_blog(request):
    query = request.query_params.get('q', '')
    if query:
        blogs = Blog.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query))
    else:
        blogs = Blog.objects.all()

    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

# Polls


class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PollDetailView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


@permission_classes([AllowAny])
class PollListView(APIView):
    def get(self, request):
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)


@permission_classes([AllowAny])
class PollVoteView(APIView):
    def put(self, request, pk):
        poll = Poll.objects.get(pk=pk)
        choice = request.data.get('choice')
        # Example of getting the logged-in user
        user = User.objects.get(id=request.user.id)

        # Create or update the vote for the poll
        vote, created = Vote.objects.update_or_create(
            poll=poll, user=user,
            defaults={'choice': choice}
        )

        return Response({'status': 'vote updated'}, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
@api_view(['POST'])
def SubmitVote(request):
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        vote = serializer.save()
        poll = vote.poll
        return Response({
            'message': 'Vote submitted successfully',
            'poll': poll.vote_counts()  # Return updated vote counts
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@require_http_methods(["PUT"])
def vote_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    try:
        data = json.loads(request.body)
        choice = data.get('choice')

        if choice not in ['YES', 'NO', 'MAYBE', 'OTHER']:
            return JsonResponse({'error': 'Invalid choice'}, status=400)

        Vote.objects.create(poll=poll, user=request.user, choice=choice)
        return JsonResponse({'message': 'Vote recorded successfully'})

    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)

# Verification photo and Id views
# install bot03
# to configure aws cli for face recogniotn.


class VerifyIDView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            verification = request.user.id_verification
            if verification.verify_user():
                notification_message = f'Hi {request.user.email}, you have successfully verified your ID'
                Notification.objects.create(
                    user=request.user, message=notification_message)

                return Response({"message": "User successfully verified."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Verification failed. ID or photo did not match."}, status=status.HTTP_400_BAD_REQUEST)
        except IDVerification.DoesNotExist:
            return Response({"error": "ID verification record not found."}, status=status.HTTP_404_NOT_FOUND)


class IDVerificationUpdateView(generics.UpdateAPIView):
    queryset = IDVerification.objects.all()
    serializer_class = IDVerificationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.id_verification

    def put(self, request, *args, **kwargs):
        verification_instance = self.get_object()
        serializer = self.get_serializer(
            verification_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User successfully verified."}, status=status.HTTP_200_OK)


class IDVerificationDetailView(generics.RetrieveAPIView):
    queryset = IDVerification.objects.all()
    serializer_class = IDVerificationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.id_verification


# PRODUCT ENDPOINTS


class CreateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class UpdateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteProduct(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([AllowAny])
class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        # Filter products based on the search query parameter
        search_query = request.query_params.get('name')
        if search_query is not None:
            filtered_products = Product.objects.filter(
                name__icontains=search_query)
        else:
            filtered_products = Product.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        result_page = paginator.paginate_queryset(filtered_products, request)

        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

# code for checkout
# views.py


@login_required(login_url='loginpage')
def checkout(request):
    # Fetch all cart items of the authenticated user
    raw_cart = Cart.objects.filter(user=request.user)

    # Validate the cart (e.g., check product quantity)
    for item in raw_cart:
        if item.product_qty > item.product.quantity:
            Cart.objects.filter(id=item.id).delete()
            messages.warning(
                request, f"Some products were removed due to insufficient stock.")

    # Calculate total price
    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.product.selling_price * item.product_qty

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'store/checkout.html', context)


@login_required(login_url='loginpage')
def place_order(request):
    if request.method == 'POST':
        # Create a new order for the user
        new_order = Order(
            user=request.user,
            fname=request.POST.get('fname'),
            lname=request.POST.get('lname'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            country=request.POST.get('country'),
            pincode=request.POST.get('pincode'),
            payment_mode=request.POST.get('payment_mode'),
        )

        # Generate a tracking number for the order
        track_no = 'freshly' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = 'freshly' + str(random.randint(1111111, 9999999))

        new_order.tracking_no = track_no
        new_order.total_price = calculate_cart_total(request)
        new_order.save()

        # Add all items from the user's cart to the order
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )

            # Update product stock quantity
            product = Product.objects.get(id=item.product.id)
            product.quantity -= item.product_qty
            product.save()

        # Clear the user's cart after order placement
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, "Your order has been placed successfully!")

        return redirect('home')
    else:
        return redirect('checkout')


def calculate_cart_total(request):
    """Helper function to calculate total cart price"""
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += item.product.selling_price * item.product_qty
    return total_price


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(request, username=email, password=password)

    if user is not None:
        # If authentication is successful, generate a token
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
        }, status=status.HTTP_200_OK)
    else:
        # If authentication fails
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# View all orders for a user
@api_view(['GET'])
def my_orders(request):
    try:
        user_orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(user_orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error fetching orders: {str(e)}")
        return Response({"error": "Failed to fetch orders"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Cancel an order (allowed only if the status is 'out for shipping')
@api_view(['POST'])
def cancel_order(request, tracking_no):
    try:
        order = Order.objects.get(tracking_no=tracking_no, user=request.user)
        if order.status == 'out_for_shipping':
            order.status = 'cancelled'
            order.save()
            notification_message = f'Hi {request.user.email}, your order of ID : {order.id} has been cancelled'
            Notification.objects.create(
                user=request.user, message=notification_message)

            return Response({"message": "Order has been cancelled"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Cannot cancel order unless it is 'out for shipping'"}, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error cancelling order: {str(e)}")
        return Response({"error": "Failed to cancel order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View specific order details by tracking number
@api_view(['GET'])
def view_order(request, tracking_no):
    try:
        order = Order.objects.filter(
            tracking_no=tracking_no, user=request.user).first()
        if order:
            order_items = OrderItem.objects.filter(order=order)
            order_serializer = OrderSerializer(order)
            items_serializer = OrderItemSerializer(order_items, many=True)
            return Response({
                "order": order_serializer.data,
                "items": items_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Error viewing order: {str(e)}")
        return Response({"error": "Failed to fetch order details"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# # Banner for Marketplace Page
@permission_classes([AllowAny])
class BannerListView(generics.ListAPIView):
    queryset = Banner.objects.filter(active=True).order_by('-created_at')
    serializer_class = BannerSerializer


# Category Views

@permission_classes([AllowAny])
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@permission_classes([AllowAny])
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Cart Endpoints
@api_view(['GET'])
def get_cart_instance(request):
    # Check if user is authenticated
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Use session for non-authenticated users
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    # Serialize the cart data
    cart_data = CartSerializer(cart).data

    # Return the cart along with its items in the response
    return Response(cart_data, status=status.HTTP_200_OK)


def get_cart_instance2(request):
    # Assuming the user is logged in, get or create the user's cart.
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@api_view(['POST'])
def add_to_cart(request):
    cart = get_cart_instance2(request)
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    if not product_id:
        return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Invalid product ID"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the product already exists in the cart
    if CartItem.objects.filter(cart=cart, product_id=product_id).exists():
        return Response({"error": "This item already exists in the cart. Use the update quantity option instead."}, status=status.HTTP_400_BAD_REQUEST)

    cart_item_data = {
        'cart': cart.id,
        'product': product.id,
        'quantity': quantity
    }

    serializer = CartItemSerializer(
        data=cart_item_data, context={'cart_id': cart.id})
    if serializer.is_valid():
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_quantity(request):
    # Ensure this returns the cart object, not serialized data
    cart = get_cart_instance2(request)
    product_id = request.data.get("product_id")
    new_quantity = request.data.get("quantity")

    if not product_id:
        return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    if new_quantity is None or int(new_quantity) <= 0:
        return Response({"error": "A valid quantity is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the product exists in the cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    except CartItem.DoesNotExist:
        return Response({"error": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND)

    cart_item_data = {
        'cart': cart.id,
        'product': product_id,
        'quantity': new_quantity
    }

    serializer = CartItemSerializer(cart_item, data=cart_item_data)
    if serializer.is_valid():
        serializer.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def remove_from_cart(request):
    # Ensure this returns the cart object, not serialized data
    cart = get_cart_instance2(request)
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity")

    if not product_id:
        return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    except CartItem.DoesNotExist:
        return Response({"error": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND)

    if quantity is None:
        quantity = cart_item.quantity

    if quantity < 1:
        return Response({"error": "Quantity must be at least 1"}, status=status.HTTP_400_BAD_REQUEST)

    if quantity >= cart_item.quantity:
        # Remove item from cart if quantity to remove is greater than or equal to the existing quantity
        cart_item.delete()
        return Response({"success": "Item removed from cart"}, status=status.HTTP_200_OK)
    else:
        # Adjust the quantity of the cart item
        cart_item.quantity -= int(quantity)
        cart_item.save()
        return Response({"success": "Item quantity updated in cart"}, status=status.HTTP_200_OK)


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get all unread notifications ordered by timestamp
        notifications = Notification.objects.filter(
            user=request.user.id, read=False).order_by('-timestamp')

        # Paginate the results
        paginator = PageNumberPagination()
        paginator.page_size = 3
        result_page = paginator.paginate_queryset(notifications, request)

        # Serialize the notifications
        serializer = NotificationSerializer(result_page, many=True)

        # Return the paginated response first
        response = paginator.get_paginated_response(serializer.data)

        # Mark all unread notifications as read after the response is prepared
        notifications.update(read=True)

        return response


# List and Create Orders (No authentication required for creating orders)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # Allow anyone to create an order

# Retrieve, Update, and Delete Order (Still requires authentication)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'order_id'
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # You can keep the default permission classes here (IsAuthenticated by default)


class FAQListView(APIView):
    # This line allows unrestricted access to this view
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)


# views.py


class FAQMainPageListView(generics.ListAPIView):
    queryset = FAQMainPage.objects.all()
    serializer_class = FAQMainPageSerializer
    permission_classes = [AllowAny]
# Payment views


@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        user = request.user

        # Initiate the M-Pesa payment
        response = lipa_na_mpesa_online(user, phone_number, amount)

        return JsonResponse({
            "status": response.status,
            "message": "Payment initiated" if response.status == 'completed' else "Payment failed",
            "error": response.error_message if response.status == 'failed' else None
        })


@csrf_exempt
def mpesa_callback(request):
    mpesa_response = json.loads(request.body.decode('utf-8'))
    # Handle the response here (e.g., save the transaction to your database)

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})


# Fetch user profile

@permission_classes([IsAuthenticated])
class GetUserProfile(APIView):

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, many=False)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class UpdateUserProfile(APIView):

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(
            user, data=request.data, partial=True)  # Allow partial updates

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FarmerListView(APIView):
    def get(self, request, *args, **kwargs):
        # Filter farmers based on verification status
        verified_farmers = Farmer.objects.filter(
            user__id_verification__is_verified=True)

        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        result_page = paginator.paginate_queryset(verified_farmers, request)

        serializer = FarmerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
