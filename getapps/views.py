from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import FAQ, ExchangeRule, KYCAMLCheck, CurrencyNews, OneMoment, Contact, Contest, Application, Discount, \
    Footer, Review


class AllDataView(APIView):
    def get(self, request, *args, **kwargs):
        lang = self.kwargs.get("lang", None)

        def filter_by_language(queryset):
            if lang and hasattr(queryset.model, 'language'):
                return queryset.filter(language=lang)
            return queryset

        faqs = filter_by_language(FAQ.objects.all())
        exchange_rules = filter_by_language(ExchangeRule.objects.all())
        kyc_aml_checks = filter_by_language(KYCAMLCheck.objects.all())
        currency_news = filter_by_language(CurrencyNews.objects.all())
        one_moments = filter_by_language(OneMoment.objects.all())
        contacts = filter_by_language(Contact.objects.all())  # Assuming no language field
        contests =filter_by_language(Contest.objects.all())# Assuming no language field
        applications = filter_by_language(Application.objects.all())
        discounts = filter_by_language(Discount.objects.all())
        footers = filter_by_language(Footer.objects.all())
        reviews = filter_by_language(Review.objects.all())

        data = {
            'faqs': FAQSerializer(faqs, many=True).data,
            'exchange_rules': ExchangeRuleSerializer(exchange_rules, many=True).data,
            'kyc_aml_checks': KYCAMLCheckSerializer(kyc_aml_checks, many=True).data,
            'currency_news': CurrencyNewsSerializer(currency_news, many=True).data,
            'one_moments': OneMomentSerializer(one_moments, many=True).data,
            'contacts': ContactSerializer(contacts, many=True).data,
            'contests': ContestSerializer(contests, many=True).data,
            'applications': ApplicationSerializer(applications, many=True).data,
            'discounts': DiscountSerializer(discounts, many=True).data,
            'footers': FooterSerializer(footers, many=True).data,
            'reviews': ReviewSerializer(reviews, many=True).data,
        }

        return Response(data)
