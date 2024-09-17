from datetime import datetime, timezone
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, View
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from .models import Event, Participation, Participant
from .forms import InterestForm, EventForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.core.paginator import Paginator

class ParticipantEventView(View):
    template_name = 'participant_event.html'

    def get(self, request, *args, **kwargs):
        now = datetime.now()  
        events = Event.objects.filter(
            event_registration_end__gte=now, 
            event_registration_start__lte=now
        ).order_by('event_start_date')  
        
        context = {
            'events': events
        }

        paginator = Paginator(events, 8)
        page_number = request.GET.get('page')
        page_numbers = paginator.get_page(page_number)

        context = {
            'events': page_numbers
        }
        return render(request, self.template_name, context)
    
    
class ParticipantEventDetailsView(DetailView):
    model = Event
    template_name = 'participant_event_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InterestForm()
        return context

class ParticipantInterestView(FormView):
    form_class = InterestForm
    template_name = 'participant_interest.html'

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        number_of_participants = form.cleaned_data['number_of_participants']
        
        Participation.objects.create(participant=self.request.user.participant, event=event, number_of_participants=number_of_participants, status='pending')
        return redirect('participant_event')

class PaymentInvoiceDownloadView(LoginRequiredMixin, DetailView):
    model = Participation
    template_name = 'payment_invoice_download.html'

    def get(self, request, *args, **kwargs):
        request_obj = self.get_object()
        if request_obj.status != 'confirmed':
            return HttpResponse("Payment not confirmed or invalid request.", status=400)
        
        event = request_obj.event
        context = {
            'event': event,
            'participant': request_obj.participant,
            'number_of_participants': request_obj.number_of_participants,
            'organizer': event.organizer,
            'ticket_price': event.event_ticket_price,
            'total_amount': request_obj.number_of_participants * event.event_ticket_price,
            'transition_id': request_obj.transition_id
        }

        html_string = render_to_string('events/invoice_template.html', context)
        pdf_file = BytesIO()
        pisa.CreatePDF(html_string.encode('UTF-8'), dest=pdf_file)
        
        response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{request_obj.transition_id}.pdf"'
        return response

class OrganizerEventView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'organizer_event.html'

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

class OrganizerEventCreateView(CreateView):
    form_class = EventForm
    template_name = 'organizer_event_creation.html'
    success_url = '/'

class OrganizerEventParticipantsView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'participants_list.html'

    def get(self, request, *args, **kwargs):
        event = self.get_object()
        now = datetime.now()
        if event.event_registration_end >= now:
            return HttpResponse("Registration still ongoing or event has not ended.", status=400)

        participants = Participation.objects.filter(event=event, status='confirmed')
        context = {
            'event': event,
            'participants': participants,
        }

        html_string = render_to_string('participants_list.html', context)
        pdf_file = BytesIO()
        pisa.CreatePDF(html_string.encode('UTF-8'), dest=pdf_file)
        
        response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="participants_list_{event.event_id}.pdf"'
        return response

class PDFView(View):
    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['event_id'])
        participation = Participation.objects.filter(event=event, status='confirmed')

        context = {
            'event': event,
            'participation': participation,
        }

        html_string = render_to_string('pdf_template.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        
        pisa_status = pisa.CreatePDF(html_string.encode('UTF-8'), dest=response)
        return response
