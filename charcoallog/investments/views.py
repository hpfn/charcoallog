from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import Http404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from charcoallog.investments.detail_post_service import DetailPost
from charcoallog.investments.forms import (
    BasicDataForm, InvestmentDetailsForm, InvestmentForm
)
from charcoallog.investments.models import Investment, InvestmentDetails
# from charcoallog.investments.serializers import InvestmentSerializer
from charcoallog.investments.serializers import InvestmentDetailsSerializer
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
    post = DetailPost(request)  # noqa F841

    qs = InvestmentDetails.objects.select_related(
        'basic_data').user_logged(request.user).filter(
        basic_data__kind=kind)

    context = {
        'd': qs,
        'basic_data': BasicDataForm,
        'form': InvestmentDetailsForm()
    }
    return render(request, 'investments/detail.html', context)


class FormDeals(LoginRequiredMixin, APIView):
    raise_exception = True

    def get_object(self, pk):
        try:
            return Investment.objects.get(pk=pk)
        except Investment.DoesNotExist:
            raise Http404

    # def get(self, request, pk, format=None):
    #     investment = self.get_object(pk)
    #     serializer = InvestmentSerializer(investment)
    #     return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     investment = self.get_object(pk)
    #     serializer = InvestmentSerializer(investment, data=request.data)
    #     if serializer.is_valid():
    #         serializer.update(investment, serializer.validated_data)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        investment = self.get_object(pk)
        investment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# API for details here
class DetailAPI(LoginRequiredMixin, APIView):
    raise_exception = True

    def get_object(self, pk):
        try:
            return InvestmentDetails.objects.get(pk=pk)
        except InvestmentDetails.DoesNotExist:
            raise Http404

        # def get(self, request, pk, format=None):
        #     investment = self.get_object(pk)
        #     serializer = InvestmentSerializer(investment)
        #     return Response(serializer.data)

    def put(self, request, pk, format=None):
        investment_d = self.get_object(pk)
        serializer = InvestmentDetailsSerializer(investment_d, data=request.data)
        if serializer.is_valid():
            serializer.update(investment_d, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        investment_d = self.get_object(pk)
        investment_d.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
