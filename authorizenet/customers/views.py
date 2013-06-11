from django.views.generic.edit import FormView

from authorizenet.forms import CustomerPaymentForm
from .models import CustomerProfile, CustomerPaymentProfile


class PaymentProfileCreationView(FormView):
    template_name = 'authorizenet/create_payment_profile.html'
    form_class = CustomerPaymentForm

    def form_valid(self, form):
        """If the form is valid, save the payment profile"""
        data = form.cleaned_data
        self.create_payment_profile(payment_data=data, billing_data=data)
        return super(PaymentProfileCreationView, self).form_valid(form)

    def create_payment_profile(self, **kwargs):
        """Create and return payment profile"""
        customer_profile = self.get_customer_profile()
        if customer_profile:
            return CustomerPaymentProfile.objects.create(
                customer_profile=customer_profile, **kwargs)
        else:
            customer_profile = CustomerProfile.objects.create(
                user=self.request.user, **kwargs)
            return customer_profile.payment_profiles.get()

    def get_customer_profile(self):
        """Return customer profile or ``None`` if none exists"""
        try:
            return CustomerProfile.objects.get(user=self.request.user)
        except CustomerProfile.DoesNotExist:
            return None
