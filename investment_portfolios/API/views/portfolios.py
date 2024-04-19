from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from portfolio.models.portfolio import Portfolio
from API.serializers.portfolios import PortfoliosSerializer


class Portfolios(ModelViewSet):
    serializer_class = PortfoliosSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        queryset = Portfolio.objects.filter(user_id=user_id).all()
        return queryset

    def get_object(self):
        portfolio_id = (f"{self.request.query_params.get('name')}_"
                        f"{self.request.query_params.get('user_id')}")
        obj = Portfolio.objects.filter(portfolio_id=portfolio_id).first()

        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        self.request.data['portfolio_id'] = (f"{self.request.data['name']}_"
                                             f"{self.request.data['user_id']}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
