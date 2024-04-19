from rest_framework.serializers import ModelSerializer, ValidationError, DecimalField
from portfolio.models.stocks import PortfolioStocks
from django.db.models.expressions import F


class StockSerializer(ModelSerializer):
    profit_loss = DecimalField(max_digits=15, decimal_places=2, source="calculate_profit_loss", default=0)

    class Meta:
        model = PortfolioStocks
        fields = ['portfolio_id', 'stock', 'amount', 'stock_price', 'stock_buy_date', 'profit_loss', 'last_price']

    def create(self, validated_data):
        stock, created = PortfolioStocks.objects.get_or_create(
            portfolio_id=validated_data.get("portfolio_id"),
            stock=validated_data.get("stock"),
            defaults={'portfolio_id': validated_data.get("portfolio_id"),
                      'stock': validated_data.get("stock"),
                      'amount': validated_data.get("amount"),
                      'stock_price': validated_data.get("stock_price")}
        )
        if not created:
            PortfolioStocks.objects.filter(portfolio_id=stock.portfolio_id, stock=stock.stock).update(
                        amount=F('amount') + validated_data.get("amount"),
                        stock_price=(F('stock_price') + validated_data.get("stock_price"))/2)

        return stock

    def update(self, instance,  validated_data):
        if instance.first().amount - validated_data.get("amount") == 0:
            instance.delete()
            return validated_data
        elif instance.first().amount < validated_data.get("amount"):
            raise ValidationError(f"There are not enough shares in the portfolio to sell.")

        instance.update(amount=F('amount') - validated_data.get("amount"))
        return validated_data
    
    def validate(self, data):
        if self.context['request'].method == "PUT":
            if data.get('portfolio_id').opening_balance < data.get("amount") * data.get("stock_price"):
                raise ValidationError(f"You don't have enough credits to buy {data.get('amount')} of stocks.")
            return data
        return data
