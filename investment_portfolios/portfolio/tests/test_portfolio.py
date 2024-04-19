import random

import pytest

from django.urls import reverse
from rest_framework import status
from ..models.stocks import PortfolioStocks
from decimal import Decimal


@pytest.mark.django_db
def test_if_portfolio_has_been_created(client):
    url = reverse('portfolio-create')
    response = client.post(url, data={'name': 'test', 'user_id': 1}, content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_if_stock_has_been_added_to_portfolio(fake_portfolio, fake_stock, get_last_price, client):
    url = reverse('stock-buy')
    response = client.put(url, data={'name': fake_portfolio.name,
                                     'user_id': fake_portfolio.user_id,
                                     'stock': fake_stock.stock,
                                     'amount': fake_stock.amount,
                                     'stock_price': fake_stock.stock_price}, content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_if_buy_stock_returns_validation_error(fake_portfolio, fake_stock, get_last_price, client):
    url = reverse('stock-buy')
    amount = random.randint(800, 1000)
    response = client.put(url, data={'name': fake_portfolio.name,
                                     'user_id': fake_portfolio.user_id,
                                     'stock': fake_stock.stock,
                                     'amount': amount,
                                     'stock_price': fake_stock.stock_price}, content_type="application/json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['non_field_errors'][0] == f"You don't have enough credits to buy {amount} of stocks."


@pytest.mark.django_db
def test_if_buy_stock_add_new_stock_to_existing_one(fake_stock, get_last_price, client):
    url = reverse('stock-buy')
    amount = random.randint(1, 10)
    response = client.put(url, data={'name': fake_stock.portfolio_id.name,
                                     'user_id': fake_stock.portfolio_id.user_id,
                                     'stock': fake_stock.stock,
                                     'amount': amount,
                                     'stock_price': fake_stock.stock_price}, content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED

    updated_stock = PortfolioStocks.objects.get(portfolio_id=fake_stock.portfolio_id, stock=fake_stock.stock)

    assert (updated_stock.stock_price == Decimal((fake_stock.stock_price + fake_stock.stock_price)/2)
            .quantize(Decimal('.01')))
    assert updated_stock.amount == (amount + fake_stock.amount)


@pytest.mark.django_db
def test_if_sell_stock_deducts_correct_amount_of_stocks_and_updates_balance(fake_stock, get_last_price, client):
    url = reverse('stock-sell')
    amount = random.randint(1, 2)
    stock_price = 20.90
    response = client.post(url, data={'name': fake_stock.portfolio_id.name,
                                      'user_id': fake_stock.portfolio_id.user_id,
                                      'stock': fake_stock.stock,
                                      'amount': amount,
                                      'stock_price': stock_price}, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK

    update_amount = PortfolioStocks.objects.get(portfolio_id=fake_stock.portfolio_id, stock=fake_stock.stock)

    assert update_amount.amount == (fake_stock.amount - amount)
    assert (update_amount.portfolio_id.opening_balance ==
            Decimal((fake_stock.portfolio_id.opening_balance + stock_price * amount)).quantize(Decimal('.01')))


@pytest.mark.django_db
def test_if_sell_stock_returns_validation_error(fake_stock, client):
    url = reverse('stock-sell')
    amount = random.randint(800, 1000)
    response = client.post(url, data={'name': fake_stock.portfolio_id.name,
                                      'user_id': fake_stock.portfolio_id.user_id,
                                      'stock': fake_stock.stock,
                                      'amount': amount,
                                      'stock_price': fake_stock.stock_price}, content_type="application/json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == f"There are not enough shares in the portfolio to sell."


@pytest.mark.django_db
def test_if_sell_stock_delete_stock_record_when_amount_is_zero(fake_stock, client):
    url = reverse('stock-sell')
    response = client.post(url, data={'name': fake_stock.portfolio_id.name,
                                      'user_id': fake_stock.portfolio_id.user_id,
                                      'stock': fake_stock.stock,
                                      'amount': fake_stock.amount,
                                      'stock_price': fake_stock.stock_price}, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK

    stock = PortfolioStocks.objects.filter(portfolio_id=fake_stock.portfolio_id, stock=fake_stock.stock).first()

    assert stock is None
