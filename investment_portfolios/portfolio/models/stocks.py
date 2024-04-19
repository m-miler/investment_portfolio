import requests
import io

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.parsers import JSONParser
from ..models.portfolio import Portfolio


class PortfolioStocks(models.Model):
    portfolio_id = models.ForeignKey(
        Portfolio,
        related_name='stocks',
        on_delete=models.CASCADE,
        help_text="Portfolio FK",
        to_field="portfolio_id",
    )
    stock = models.CharField(max_length=10, help_text="Company Abbreviation")

    amount = models.IntegerField(
        help_text="Number of stocks in portfolio",
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    stock_price = models.DecimalField(
        help_text="Average stock price", max_digits=15, decimal_places=2
    )

    stock_buy_date = models.DateField(
        auto_now=True, help_text="Date of adding the stock"
    )

    def calculate_profit_loss(self) -> Decimal:
        return self.amount * (Decimal(self.last_price['close_price']) - self.stock_price)

    @property
    def last_price(self):
        return self.get_last_price(self.stock)

    def get_last_price(self, ticker: str):
        url = f"http://stock-api:8080/prices/last-price/?ticker={ticker}"
        content = requests.get(url).content
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        return data
