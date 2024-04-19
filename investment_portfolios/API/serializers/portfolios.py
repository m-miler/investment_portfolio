from rest_framework.serializers import ModelSerializer
from portfolio.models.portfolio import Portfolio
from .stocks import StockSerializer


class PortfoliosSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(PortfoliosSerializer, self).__init__(*args, **kwargs)

    stocks = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ['portfolio_id', 'user_id', 'name', 'create_date', 'opening_balance', 'stocks']
