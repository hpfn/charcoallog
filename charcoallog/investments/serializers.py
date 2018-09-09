from rest_framework import serializers

from charcoallog.investments.models import BasicData, Investment


class BasicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicData
        fields = ('pk', 'date', 'money', 'kind', 'which_target')


class InvestmentSerializer(serializers.ModelSerializer):
    basic_data = BasicDataSerializer()

    class Meta:
        model = Investment
        fields = ('tx_op', 'brokerage', 'basic_data')

    def update(self, instance, validated_data):
        basic_d = validated_data.pop('basic_data')
        bsc_dt = list(instance.basic_data._meta.default_manager.all())
        # bsc_dt = list(bsc_dt)
        instance.tx_op = validated_data.get('tx_op', instance.tx_op)
        instance.brokerage = validated_data.get('brokerage', instance.brokerage)
        # instance.save()

        # for data in basic_d:
        b_d = bsc_dt.pop(0)
        b_d.pk = basic_d.get('pk', instance.basic_data.pk)
        b_d.user_name = basic_d.get('user_name', instance.basic_data.user_name)
        b_d.date = basic_d.get('date', instance.basic_data.date)
        b_d.money = basic_d.get('money', instance.basic_data.money)
        b_d.kind = basic_d.get('kind', instance.basic_data.kind)
        b_d.which_target = basic_d.get('which_target', instance.basic_data.which_target)
        b_d.save()

        instance.basic_data = b_d
        instance.save()

        return instance
