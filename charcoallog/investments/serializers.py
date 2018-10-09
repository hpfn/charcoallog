# Save file for Details
# Investment only DELETE
from rest_framework import serializers

from charcoallog.investments.models import NewInvestment, NewInvestmentDetails


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewInvestment
        fields = ('tx_op', 'brokerage', 'kind', 'money', 'date', 'pk')

    def update(self, instance, validated_data):
        instance.pk = validated_data.get('pk', instance.pk)
        instance.date = validated_data.get('date', instance.date)
        instance.money = validated_data.get('money', instance.money)
        instance.kind = validated_data.get('kind', instance.kind)
        instance.tx_op = validated_data.get('tx_op', instance.tx_op)
        instance.brokerage = validated_data.get('brokerage', instance.brokerage)
        instance.user_name = validated_data.get('user_name', instance.user_name)

        instance.save()

        return instance


class InvestmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewInvestmentDetails
        fields = ('pk', 'date', 'money', 'kind',
                  'which_target', 'segment', 'tx_or_price',
                  'quant')

    def update(self, instance, validated_data):
        instance.pk = validated_data.get('pk', instance.pk)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.date = validated_data.get('date', instance.date)
        instance.money = validated_data.get('money', instance.money)
        instance.kind = validated_data.get('kind', instance.kind)

        instance.which_target = validated_data.get('which_target', instance.which_target)
        instance.segment = validated_data.get('segment', instance.segment)
        instance.tx_or_price = validated_data.get('tx_or_price', instance.tx_or_price)
        instance.quant = validated_data.get('quant', instance.quant)

        instance.save()

        return instance
