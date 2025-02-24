from django.urls import path
from . import views

urlpatterns = [
    path('boards/', views.create_board, name='create_board'),
    path('boards/<str:board_name>/', views.board_detail, name='board_detail'),
    path('boards/<str:board_name>/status/', views.status_manager, name='board_statuses'),
    path('cards/<str:board_name>/', views.card_manager, name='create_card'),
    path('cards/<str:board_name>/<str:card_name>/', views.card_manager, name='update_card'),
]

