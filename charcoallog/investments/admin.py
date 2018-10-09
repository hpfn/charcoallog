from django.contrib import admin

from charcoallog.investments.models import NewInvestment, NewInvestmentDetails


class NewInvestmentModelAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'date', 'money', 'kind', 'tx_op', 'brokerage')
    readonly_fields = ('user_name',)
    search_fields = ('date',)
    date_hierarchy = 'date'

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.filter(newinvestmentdetails=None)


admin.site.register(NewInvestment, NewInvestmentModelAdmin)


class NewInvestmentDetailsModelAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'date', 'money', 'kind', 'tx_op', 'brokerage',
                    'which_target', 'segment', 'tx_or_price', 'quant')
    readonly_fields = ('user_name',)
    search_fields = ('date',)
    date_hierarchy = 'date'


admin.site.register(NewInvestmentDetails, NewInvestmentDetailsModelAdmin)
