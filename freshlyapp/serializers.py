from django.db import IntegrityError
from .models import Profile  # Ensure Profile model is imported
from .models import Order, OrderItem
from .models import FAQMainPage
from .models import Profile
import os
from PIL import Image
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Blog, Product, Garden, Comment, Like, Share, Poll, Vote, IDVerification, Review, Farmer, Cart, CartItem, Banner, Category, Notification, FAQMainPage, FAQ
from django.contrib.auth import get_user_model, authenticate
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User
from better_profanity import profanity

from rest_framework import serializers


UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['location', 'phone']


class UserRegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'first_name', 'last_name', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        # Ensure a profile is created if it doesn't already exist
        profile, created = Profile.objects.get_or_create(
            user=user, defaults=profile_data)

        if not created:
            # If the profile already exists, update it if needed
            profile.phone = profile_data['phone']
            profile.location = profile_data['location']
            profile.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise ValidationError('Invalid credentials')
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})

        # Update user fields only if provided
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.save()

        # Update profile fields only if provided
        profile = instance.profile
        profile.location = profile_data.get('location', profile.location)
        profile.phone = profile_data.get('phone', profile.phone)
        profile.save()

        return instance


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        # Price validation
        if data.get('price', 0) < 0:
            raise serializers.ValidationError(
                {'price': 'Price cannot be negative.'})

        if not (0.01 <= data.get('price', 0) <= 99999.99):
            raise serializers.ValidationError(
                {'price': 'Price must be between 0.01 and 99999.99.'})

        if len(str(data.get('price', 0)).split('.')[-1]) > 2:
            raise serializers.ValidationError(
                {'price': 'Price cannot have more than two decimal places.'})

        # Quantity validation
        if data.get('qtty', 0) < 0:
            raise serializers.ValidationError(
                {'qtty': 'Quantity cannot be negative.'})

        if data.get('qtty', 0) > 10000:
            raise serializers.ValidationError(
                {'qtty': 'Quantity cannot exceed 10,000.'})

        # Name validation
        if len(data.get('name', '').strip()) == 0:
            raise serializers.ValidationError(
                {'name': 'Name cannot be empty.'})

        if len(data.get('name', '')) > 255:
            raise serializers.ValidationError(
                {'name': 'Name cannot exceed 255 characters.'})

        # Description validation
        if len(data.get('desc', '')) < 10:
            raise serializers.ValidationError(
                {'desc': 'Description is too short. It should be at least 10 characters long.'})

        if profanity.contains_profanity(data.get('desc', '')):
            raise serializers.ValidationError(
                {'desc': 'Description contains prohibited or inappropriate content.'})

        # Image validation
        image = data.get('image')
        if image:
            ext = os.path.splitext(image.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if ext not in valid_extensions:
                raise serializers.ValidationError(
                    {'image': 'Unsupported file extension. Allowed extensions are: .jpg, .jpeg, .png'})

            if image.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(
                    {'image': 'Image file size cannot exceed 5MB.'})

            image = Image.open(image)
            width, height = image.size
            if width < 800 or height < 600:
                raise serializers.ValidationError(
                    {'image': 'Image resolution too low. Minimum resolution is 800x600.'})
            if width > 4000 or height > 3000:
                raise serializers.ValidationError(
                    {'image': 'Image resolution too high. Maximum resolution is 4000x3000.'})

        return data


class ReviewSerializer(serializers.ModelSerializer):
    # Nested serializer to display product details
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )  # To allow assignment of product by ID

    class Meta:
        model = Review
        fields = ['id', 'product', 'product_id',
                  'rating', 'comment', 'created_at']


class FarmerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone = serializers.CharField(source='user.profile.phone', read_only=True)
    location = serializers.CharField(
        source='user.profile.location', read_only=True)

    class Meta:
        model = Farmer
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'phone', 'location', 'user']


class GardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields = ['id', 'name', 'location', 'size', 'description']


class BlogSerializer(serializers.ModelSerializer):
    # comments = serializers.StringRelatedField(many=True)
    # likes = serializers.StringRelatedField(many=True)
    # shares = serializers.StringRelatedField(many=True)

    class Meta:
        model = Blog
        fields = ['id', 'user', 'title', 'content',
                  'image', 'comments', 'likes', 'shares']
        # These fields are typically read-only
        read_only_fields = ['id', 'comments', 'likes', 'shares']

# Created serializers for Blog, Comment, Like, and Share.


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'blog', 'user', 'content', 'created_at', 'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'blog', 'user']


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ['id', 'blog', 'user', 'shared_at']

# Polls serializer


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['poll', 'user', 'choice']

    def create(self, validated_data):
        # Check if user already voted
        vote, created = Vote.objects.get_or_create(
            poll=validated_data['poll'],
            user=validated_data['user'],
            defaults={'choice': validated_data['choice']}
        )

        if not created:
            # If vote already exists, update the choice
            vote.choice = validated_data['choice']
            vote.save()

        return vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'poll', 'user', 'choice', 'created_at']


class PollSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 'votes', 'created_at']


# IDverification


class IDVerificationSerializer(serializers.ModelSerializer):
    id_document_number = serializers.CharField(required=True)
    document_image = serializers.ImageField(required=True)
    photo_image = serializers.ImageField(required=True)

    class Meta:
        model = IDVerification
        fields = ['id_document_type', 'id_document_number',
                  'document_image', 'photo_image', 'is_verified']

    def validate(self, data):
        """
        Validate and verify the ID number and photo.
        """
        instance = self.instance if self.instance else IDVerification(**data)

        # Validate ID number format
        if not instance.verify_id_number():
            raise serializers.ValidationError(
                {"id_document_number": "Invalid ID number format for the selected document type."})

        # Validate and verify photo
        if not instance.verify_photo():
            raise serializers.ValidationError(
                {"photo_image": "Photo verification failed. The photo does not match the ID document."})

        return data

    def update(self, instance, validated_data):
        """
        Update the instance after verification and mark it as verified if successful.
        """
        instance.id_document_type = validated_data.get(
            'id_document_type', instance.id_document_type)
        instance.id_document_number = validated_data.get(
            'id_document_number', instance.id_document_number)
        instance.document_image = validated_data.get(
            'document_image', instance.document_image)
        instance.photo_image = validated_data.get(
            'photo_image', instance.photo_image)

        # Perform verification
        if instance.verify_user():
            instance.is_verified = True
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(
                "Verification failed. ID number or photo is not correct.")


# Banner Serializer for Marketplace Page


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'url',
                  'active', 'created_at', 'category', "countdown"]


# Category Serializer:

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', "image", "bgColor"]


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def validate(self, data):
        # Quantity validation
        if data.get('quantity', 0) <= 0:
            raise serializers.ValidationError(
                {'quantity': 'Quantity must be at least 1.'})

        # Max quantity validation
        if data.get('quantity', 0) > CartItem.MAX_QUANTITY:
            raise serializers.ValidationError(
                {'quantity': f'Quantity cannot exceed {CartItem.MAX_QUANTITY} per product.'})

        # Stock availability validation
        if data['quantity'] > data['product'].qtty:
            raise serializers.ValidationError(
                {'quantity': f'Not enough stock. Available stock is {data["product"].qtty}.'})

        # Ensure product exists
        if not data.get('product'):
            raise serializers.ValidationError(
                {'product': 'Product must exist for the cart item.'})

        return data


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

    def validate(self, data):
        # Ensure user or session is present
        if not data.get('user') and not data.get('session_id'):
            raise serializers.ValidationError(
                {'user': 'A user or session must be associated with the cart.'})

        # Discount code validation (if used)
        if data.get('discount_code') and len(data['discount_code']) > 50:
            raise serializers.ValidationError(
                {'discount_code': 'Discount code cannot exceed 50 characters.'})

        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification

        fields = ['id', 'message', 'read', 'timestamp', 'user']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_name', 'product_price', 'product_quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_id', 'customer_name', 'customer_email', 'customer_phone',
                  'delivery_fee', 'total_price', 'payment_method', 'items', 'created_at', 'updated_at']
        read_only_fields = ['order_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'description']


# serializers.py


class FAQMainPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQMainPage
        fields = ['id', 'question', 'answer']
