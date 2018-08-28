from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from charcoallog.investments.forms import BasicDataForm, InvestmentForm
from charcoallog.investments.models import Investment, InvestmentDetails
from charcoallog.investments.serializers import InvestmentSerializer
from charcoallog.investments.service import ShowData


@login_required
def home(request):
    context = {
        'basic_data': BasicDataForm(),
        'form': InvestmentForm(),
        'show_data': ShowData(request)}
    return render(request, 'investments/home.html', context)


@login_required
def detail(request, kind):
    qs = InvestmentDetails.objects.select_related(
        'basic_data').user_logged(request.user).filter(
        basic_data__kind=kind)

    context = {
        'd': qs
    }
    return render(request, 'investments/detail.html', context)


class FormDeals(APIView):
    def get_object(self, pk):
        try:
            return Investment.objects.get(pk=pk)
        except Investment.DoesNotExist:
            raise Http404

    # def get(self, request, pk, format=None):
    #     investment = self.get_object(pk)
    #     serializer = InvestmentSerializer(investment)
    #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        investment = self.get_object(pk)
        serializer = InvestmentSerializer(investment, data=request.data)
        if serializer.is_valid():
            serializer.update(investment, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        investment = self.get_object(pk)
        investment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
