from django.urls import re_path
from API.views.portfolios import Portfolios
from API.views.stocks import Stocks

urlpatterns = [
    re_path('portfolio/list/', Portfolios.as_view({'get': 'list'}), name='portfolios-list'),
    re_path('portfolio/create/', Portfolios.as_view({'post': 'create'}), name='portfolio-create'),
    re_path('portfolio/delete/', Portfolios.as_view({'get': 'destroy'}), name='portfolio-delete'),
    re_path('portfolio/buy/', Stocks.as_view({'put': 'create'}), name='stock-buy'),
    re_path('portfolio/sell/', Stocks.as_view({'post': 'update'}), name='stock-sell')
]

