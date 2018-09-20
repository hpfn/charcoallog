# Save file for Details
# Investment only DELETE
from rest_framework import serializers

from charcoallog.investments.models import BasicData, InvestmentDetails


class BasicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicData
        fields = ('pk', 'date', 'money', 'kind')


class InvestmentDetailsSerializer(serializers.ModelSerializer):
    basic_data = BasicDataSerializer()

    class Meta:
        model = InvestmentDetails
        fields = ('which_target', 'segment', 'tx_or_price', 'quant', 'basic_data')

    def update(self, instance, validated_data):
        basic_d = validated_data.pop('basic_data')
        bsc_dt = instance.basic_data._meta.default_manager.all()
        bsc_dt = list(bsc_dt)

        b_d = bsc_dt.pop(0)
        b_d.pk = basic_d.get('pk', instance.basic_data.pk)
        b_d.user_name = basic_d.get('user_name', instance.basic_data.user_name)
        b_d.date = basic_d.get('date', instance.basic_data.date)
        b_d.money = basic_d.get('money', instance.basic_data.money)
        b_d.kind = basic_d.get('kind', instance.basic_data.kind)

        b_d.save()

        instance.basic_data = b_d
        instance.which_target = validated_data.get('which_target', instance.which_target)
        instance.segment = validated_data.get('segment', instance.segment)
        instance.tx_or_price = validated_data.get('tx_or_price', instance.tx_or_price)
        instance.quant = validated_data.get('quant', instance.quant)

        instance.save()

        return instance
