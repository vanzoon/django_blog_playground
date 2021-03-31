from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm
from .tasks import send_notification_email


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'
    template_name = 'contact.html'

    def form_valid(self, form):
        form.save()
        # send(form.instance.email)
        send_notification_email.delay(form.instance.email)
        return super().form_valid(form)
