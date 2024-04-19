from django.db import models


class Portfolio(models.Model):
    portfolio_id = models.CharField(
        max_length=150,
        help_text="Portfolio primary key user_portfolio_name",
        unique=True,
    )
    user_id = models.BigIntegerField()
    name = models.CharField(max_length=20, help_text="User portfolio name")
    create_date = models.DateField(
        auto_now_add=True, help_text="Date of portfolio creation"
    )
    opening_balance = models.DecimalField(
        default=10000.00,
        max_digits=15,
        decimal_places=2,
        help_text="Start balance 10k PLN",
    )
