from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from ..serializers.stocks import StockSerializer
from portfolio.models.portfolio import Portfolio
from portfolio.models.stocks import PortfolioStocks
from decimal import Decimal


class Stocks(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = StockSerializer

    def get_object(self):
        portfolio_id = (f"{self.request.data['name']}_"
                        f"{self.request.data['user_id']}")
        stock = PortfolioStocks.objects.filter(portfolio_id=portfolio_id,
                                               stock=self.request.data.get("stock"))
        return stock

    def create(self, request, *args, **kwargs):
        portfolio_id = (f"{self.request.data['name']}_"
                        f"{self.request.data['user_id']}")
        self.request.data['portfolio_id'] = portfolio_id
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.update_portfolio_balance(self.request.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        portfolio_id = (f"{self.request.data['name']}_"
                        f"{self.request.data['user_id']}")
        self.request.data['portfolio_id'] = portfolio_id
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        self.request.data.update({'amount': f"-{self.request.data.get('amount')}"})
        self.update_portfolio_balance(self.request.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_portfolio_balance(self, validated_data):
        portfolio = Portfolio.objects.filter(portfolio_id=validated_data.get('portfolio_id'))
        new_balance = (portfolio.first().opening_balance - int(validated_data.get('amount')) *
                       Decimal(validated_data.get('stock_price')))
        portfolio.update(opening_balance=new_balance)
