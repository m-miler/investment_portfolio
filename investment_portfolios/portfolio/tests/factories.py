import factory

from ..models.portfolio import Portfolio
from ..models.stocks import PortfolioStocks


class PortfolioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Portfolio
        django_get_or_create = ("portfolio_id",)

    user_id = 1
    name = factory.Sequence(lambda n: f"PortfolioTest{n}")
    portfolio_id = factory.LazyAttribute(lambda obj: f"{obj.name}_{obj.user_id}")


class PortfolioStockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PortfolioStocks
        django_get_or_create = ("stock",)

    portfolio_id = factory.SubFactory(PortfolioFactory)
    stock = factory.Faker("pystr", min_chars=3, max_chars=3)
    amount = factory.Faker("pyint", min_value=5, max_value=10)
    stock_price = factory.Faker(
        "pyfloat", min_value=133.00, max_value=134.00, right_digits=2
    )
