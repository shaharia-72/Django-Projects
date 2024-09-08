from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import BooksDetailViews, ConfirmOderViews, ReturnBookView, MyBooksView, HistoryViews, CouponView, CouponConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books_detail/<int:pk>/', BooksDetailViews.as_view(), name='books_detail'),
    path('book/<int:pk>/confirm_order/', ConfirmOderViews.as_view(), name='confirm_order'),
    path('book/my_books/', MyBooksView.as_view(), name='my_books'),
    path('return_book/<int:pk>/', ReturnBookView.as_view(), name='return_book'),
    path('history', HistoryViews.as_view(), name='history'),
    path('coupons', CouponView.as_view(), name='coupons'),
    path('coupons_confirm/<int:coupon_id>/', CouponConfirmView.as_view(), name='coupons_confirm'),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)