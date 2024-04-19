import pytest
import random
import psycopg2

from django.db import connections
from django.core.management import call_command
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .factories import PortfolioFactory, PortfolioStockFactory
from unittest import mock
from ..models.stocks import PortfolioStocks


def run_sql(sql):
    conn = psycopg2.connect(database='postgres', user='postgres', password='postgres', host='localhost')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()


@pytest.fixture(scope='session', autouse=True)
def django_db_setup(django_db_blocker):
    from django.conf import settings

    settings.DATABASES['default']['NAME'] = 'portfolios'
    settings.DATABASES['default']['USER'] = 'postgres'
    settings.DATABASES['default']['PASSWORD'] = 'postgres'
    settings.DATABASES['default']['HOST'] = 'localhost'

    run_sql('DROP DATABASE IF EXISTS portfolios')
    run_sql('CREATE DATABASE portfolios')
    with django_db_blocker.unblock():
        call_command('migrate', '--noinput')
    yield

    for connection in connections.all():
        connection.close()

    run_sql('DROP DATABASE portfolios')


@pytest.fixture
def fake_portfolio():
    yield PortfolioFactory()


@pytest.fixture
def fake_stock():
    yield PortfolioStockFactory()


@pytest.fixture
def get_last_price():
    with mock.patch.object(PortfolioStocks, "get_last_price",
                           return_value={'close_price': 20.00}):
        yield PortfolioStocks

