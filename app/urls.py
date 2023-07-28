from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import LoginForm, ChangePasswordForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth import views as auth_views


urlpatterns = [
         
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('contact/', views.MailContact, name="contact"),
     
    path('', views.ProductView.as_view(), name="home"),

    path('product-detail/<int:id>/',
         views.ProductDetailView.as_view(), name='product_detail'),

    path('mobile/', views.mobile, name='mobile'),

    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),

    path('laptop/', views.laptop, name='laptop'),

    path('laptop/<slug:data>/', views.laptop, name='laptopdata'),

    path('topwear/', views.topwear, name='topwear'),
    
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    
    path('shoes/', views.shoes, name='shoes'),
    
    path('watch/', views.watch, name='watch'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('address/', views.address, name='address'),

    path('edit_address/<int:id>/',
         views.EditAddressView.as_view(), name='edit_address'),

    path('delete_address/<int:id>/',
         views.DeleteAddressView.as_view(), name='delete_address'),

    path('add_to_cart/', views.add_to_cart, name='add-to-cart'),

    path('show_cart/', views.show_cart, name='show_cart'),

    path('plus_cart/', views.plus_cart, name='plus_cart'),

    path('minus_cart/', views.minus_cart, name='minus_cart'),

    path('remove_cart/', views.remove_cart, name='remove_cart'),

    path('checkout/', views.checkout, name='checkout'),

    path('orderdone/', views.orderdone, name='orderdone'),

    path('orders/', views.orders, name='orders'),

    path('buy/', views.buy_now, name='buy-now'),

    path('registration/', views.CustomerRegistrationView.as_view(),
         name='customerregistration'),

    #     path('login/', views.LoginView.as_view(), name='login'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name="app/login.html",
         authentication_form=LoginForm), name='login'),

    path('logout/', views.user_logout, name='logout'),

    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name="app/changepassword.html",
         form_class=ChangePasswordForm, success_url="/changepassworddone/"), name="changepassword"),

    path('changepassworddone/', auth_views.PasswordChangeDoneView.as_view(
        template_name="app/changepassworddone.html"), name="changepassworddone"),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name="app/password_reset.html", form_class=MyPasswordResetForm), name="password_reset"),

    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name="app/password_reset_done.html"), name="password_reset_done"),

    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html", form_class=MySetPasswordForm), name="password_reset_confirm"),

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="app/password_reset_complete.html"), name="password_reset_complete"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
