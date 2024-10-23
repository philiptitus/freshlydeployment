from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from django.urls import re_path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import BlogListCreateView, BlogListView, CustomPasswordResetView, Register, search_blog, initiate_payment, mpesa_callback
from .views import PollDetailView, PollListCreateView, VerifyIDView, SubmitVote, IDVerificationUpdateView, IDVerificationDetailView, BannerListView, CategoryListCreateView, CategoryDetailView, vote_poll
from .views import *
from .forms import MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from . import views
from django.conf import settings
from django.conf.urls.static import static


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path
from .views import OrderListCreateView, OrderDetailView

# faq
from .views import FAQListView
from .views import FAQMainPageListView


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


from .views import (
    BlogRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView,
    LikeCreateAPIView, ShareCreateAPIView
)

urlpatterns = [
    path('register/', Register, name='register'),
    path('login/', login, name='login'),

    path('admin/', admin.site.urls),
    path('freshlyapp/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('freshlyapp/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    # Catch-all route to serve React app for all frontend routes
    path('', TemplateView.as_view(template_name='index.html')),

    path('about-us/', TemplateView.as_view(template_name='index.html')),
    path("marketplace/", TemplateView.as_view(template_name="index.html")),
    path("signup/", TemplateView.as_view(template_name="index.html")),

    # path('blogs/', views.blogs, name='blogs'),
    path('freshlyapp/blogs/', BlogListView.as_view(), name='blog-list'),
    path('freshlyapp/create/', BlogListCreateView.as_view(),
         name='blog-list-create'),
    # path('create-blogs/', views.blog_create, name='blogs_create'),
    # path('freshlyapp/blogs/', views.blog_create, name='blog_create'),
    path('freshlyapp/search/', views.search_blog, name='search_blog'),


    path('login/', auth_views.LoginView.as_view, name='login'),
    # path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'), name='password_change_done'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    #     path('products/', views.products, name='products'),
    path('services/', views.services, name='services'),
    path('profile/', views.GetUserProfile.as_view(), name='profile'),
    path('profile/update/', UpdateUserProfile.as_view(),
         name='user-profile-update'),

    # path('blogs/', BlogListCreateAPIView.as_view(), name='blog_list_create'),
    path('blogs/<int:pk>/', BlogRetrieveUpdateDestroyAPIView.as_view(),
         name='blog_detail'),
    path('comments/', CommentListCreateAPIView.as_view(),
         name='comment_list_create'),
    path('comments/<int:pk>/',
         CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment_detail'),
    path('likes/', LikeCreateAPIView.as_view(), name='like_create'),
    path('shares/', ShareCreateAPIView.as_view(), name='share_create'),
    # path('search_blog/<int:pk>/', views.search_blog, name='search_blog'),
    path('search_blog/', views.search_blog, name='search_blog'),

    path('freshlyapp/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('freshlyapp/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),

    # Poll URLs
    path('freshlyapp/polls/', PollListCreateView.as_view(), name='poll-list-create'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    #     path('polls/<int:pk>/vote/', SubmitVote.as_view(), name='vote-create'),
    path('submit-vote/', SubmitVote, name='submit_vote'),

    # Testing new format
    path('api/polls/', PollListView.as_view(), name='poll-list'),
    #     path('api/polls/<int:pk>/vote/', PollVoteView.as_view(), name='poll-vote'),

    path('api/polls/<int:poll_id>/vote/', views.vote_poll, name='vote_poll'),

    # Verifications
    path('freshlyapp/verification/verify/',
         VerifyIDView.as_view(), name='verify-id'),
    path('freshlyapp/verification/', IDVerificationUpdateView.as_view(),
         name='id-verification-update'),
    path('freshlyapp/verification/detail/',
         IDVerificationDetailView.as_view(), name='id-verification-detail'),


    # product urls
    path('products/', ProductListView.as_view(), name='list-products'),
    path('products/create/', CreateProduct.as_view(), name='create-product'),
    path('products/<int:pk>/', RetrieveProduct.as_view(), name='retrieve-product'),
    path('products/<int:pk>/update/',
         UpdateProduct.as_view(), name='update-product'),
    path('products/<int:pk>/delete/',
         DeleteProduct.as_view(), name='delete-product'),


    # Banner URL

    path('freshlyapp/banners/', BannerListView.as_view(), name='banner-list'),

    path('orders/', OrderListCreateView.as_view(), name='OrderListCreateView'),
    path('orders/<uuid:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # faq
    path('api/faqs/', FAQListView.as_view(), name='faq-list'),
    path('api/faqsmainpage/', FAQMainPageListView.as_view(),
         name='faq-mainpage-list'),

    # Category URL

    path('freshlyapp/categories/', CategoryListCreateView.as_view(),
         name='category-list-create'),
    path('freshlyapp/categories/<int:pk>/', CategoryDetailView.as_view(),
         name='category-detail'),



    # CART URLS
    path('cart/', views.get_cart_instance, name='get_cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_quantity, name='update_quantity'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),




    # notification url
    path('notifications/', NotificationListView.as_view(),
         name='notification-list'),

    # true order
    path('orders/', OrderListCreateView.as_view(), name='OrderListCreateView'),
    path('orders/<uuid:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # faq
    path('api/faqs/', FAQListView.as_view(), name='faq-list'),
    path('api/faqsmainpage/', FAQMainPageListView.as_view(),
         name='faq-mainpage-list'),







    # notification url
    path('notifications/', NotificationListView.as_view(),
         name='notification-list'),

    # Payment urls
    path('api/initiate-payment/', initiate_payment, name='initiate-payment'),
    path('api/mpesa-callback/', mpesa_callback, name='mpesa-callback'),


    # Verified Farmers
    path('verified-farmers/', FarmerListView.as_view(), name='verified-farmers'),

]
