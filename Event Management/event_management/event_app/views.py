from datetime import datetime, timezone
from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from accounts import forms
from accounts.models import Organizer
from .models import Event, Participation, Participant, Category
from .forms import InterestForm, EventForm
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.core.paginator import Paginator
from django.views.generic.edit import FormView, UpdateView

class ParticipantEventView(View):
    template_name = 'participant_event.html'

    # def get(self, request, *args, **kwargs):
    #     now = datetime.now()  
    #     events = Event.objects.filter(
    #         event_registration_end__gte=now, 
    #         event_registration_start__lte=now
    #     ).order_by('event_start_date')  
        
    #     context = {
    #         'events': events
    #     }

    #     paginator = Paginator(events, 8)
    #     page_number = request.GET.get('page')
    #     page_numbers = paginator.get_page(page_number)

    #     context = {
    #         'events': page_numbers
    #     }
    #     return render(request, self.template_name, context)
    
    # def get_queryset(self):
    #     slug = self.kwargs.get('slug',None)
    #     if slug:
    #         category = get_object_or_404(Category, slug=slug)
    #         return Event.objects.filter(category=category).order_by('-event_start_date')
    #     return Event.objects.all().order_by('-event_start_date')
    
    def get(self, request, *args, **kwargs):
        # context = super().get_context_data(**kwargs)

        now = datetime.now()  
        events = Event.objects.filter(
            event_registration_end__gte=now, 
            event_registration_start__lte=now
        ).order_by('event_start_date')  
        categories = Category.objects.all()

        paginator = Paginator(events, 9)
        page_number = request.GET.get('page')
        page_numbers = paginator.get_page(page_number)

        context = {
            'events': events,
            'events': page_numbers,
            'categories': categories

        }
        
        # return context
        return render(request, self.template_name, context)

# class ParticipantEventView(ListView):
#     model = Event
#     template_name = 'participant_event.html'
#     context_object_name = 'events'
#     # paginate_by = 9

#     def get_queryset(self):
#         now = datetime.now()
#         return Event.objects.filter(event_registration_end__gte=now, event_registration_start__lte=now).order_by('event_start_date')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         # now = datetime.now()

#         # events = Event.objects.filter(
#         #     event_registration_end__gte=now, 
#         #     event_registration_start__lte=now
#         # ).order_by('event_start_date')  
#         # categories = Category.objects.all()

#         # paginator = Paginator(events, 8)
#         # page_number = request.GET.get('page')
#         # page_numbers = paginator.get_page(page_number)

#         # context = {
#         #     'events': events,
#         #     'events': page_numbers,
#         #     'categories': categories

#         # }
#         return context
    
def category(request, category_id):
    now = datetime.now()
    category = Category.objects.filter(pk=category_id).first()
    
    if category is None:
        return redirect('home')
    
    events = Event.objects.filter(
        category=category,
        event_registration_end__gte=now,
        event_registration_start__lte=now
    ).order_by('event_start_date')

    paginator = Paginator(events, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    return render(request, 'participant_event.html', {
        'events': page_obj,
        'events': events,
        'categories': categories
    })

    
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
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        number_of_participants = form.cleaned_data['number_of_participants']
        
        Participation.objects.create(participant=self.request.user.participant, event=event, number_of_participants=number_of_participants, status='pending')
        
        # return redirect('participant_event')
        return redirect(self.success_url)

    # def get_success_url(self):
    #     return redirect('participant_event')


class ParticipantHistoryView(ListView):
    model = Participation
    template_name = 'Participant_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'history'
        user = self.request.user

        # Get the user's participation history
        # Order by the event_created_at field in the Participation model
        participations = Participation.objects.filter(participant__user=user).order_by('-event_created_at')

        # Add participation details to the context
        context['participations'] = participations
        context['event_status'] = {p.event: p.status for p in participations}

        return context

# class ParticipantEventInterestView(LoginRequiredMixin,ListView):
#     model = Participant
#     template_name = 'participant_event_interest.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['active_page'] = 'my_books'
#         return context
    
#     def get_queryset(self):

#         queryset = Participant.objects.filter(user=self.request.user, status__isnull=True)
#         return queryset

# class ParticipantEventInterestView(LoginRequiredMixin,ListView):
#     model = Event
#     template_name = 'participant_event_interest.html'  
#     context_object_name = 'events' 
#     # paginate_by = 8

#     # def get(self, request, *args, **kwargs):

#     #     events = Event.objects.all
    
#     #     paginator = Paginator(events, 8)
#     #     page_number = request.GET.get('page')
#     #     page_numbers = paginator.get_page(page_number)

#     #     context = {
#     #         'events': page_numbers
#     #     }
#     #     return render(request, self.template_name, context)

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_authenticated:
#             participations = Participation.objects.filter(
#                 participant__user=user,
#                 status='confirmed'
#             )
#             return Event.objects.filter(participation__in=participations)
#         else:
#             return Event.objects.none()
#         #     return Event.objects.filter(participation__in=participations, 
#         #                                 event_registration_end__gte=now(), 
#         #                                 event_registration_start__lte=now()
#         #                                ).order_by('event_start_date')
#         # else:
#         #     return Event.objects.none()
#         # return Event.objects.filter(

#         #     paginator = Paginator(events, 8)
#         # page_number = request.GET.get('page')
#         # page_numbers = paginator.get_page(page_number)

#         # context = {
#         #     'events': page_numbers
#         # }

class ParticipantEventInterestView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'participant_event_interest.html'
    context_object_name = 'events'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            participations = Participation.objects.filter(
                participant__user=user,
                status='confirmed'
            )
            return Event.objects.filter(participation__in=participations)
        return Event.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['active_page'] = 'my_interest'
        
        # Map each event to its participation
        events = context['events']
        participation_map = {
            participation.event_id: participation
            for participation in Participation.objects.filter(participant__user=user)
        }
        
        for event in events:
            event.participation = participation_map.get(event.pk)
        
        return context


# class ParticipantPaymentConfirmView(View):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         participation = get_object_or_404(Participation, pk=pk)
        

#         participation.status = 'confirmed'
#         participation.save()
        
#         return redirect('participant_event_interest')
# 

# class ParticipantPaymentConfirmView(View):
#      def post(self, request, *args, **kwargs):
#         participation_id = self.kwargs.get('pk')

#         try:
#             participation = Participation.objects.get(pk=participation_id, status='pending')
#             participation.status = 'confirmed'
#             participation.is_payment_confirmed = True  # Set the payment as confirmed
#             participation.save()

#             return redirect('download_invoice', pk=participation.pk)
#         except Participation.DoesNotExist:
#             return HttpResponseBadRequest("Participation not found or already confirmed")

# class ParticipantPaymentConfirmView(View):
#     template_name = 'payment_confirmed.html'  # HTML template for confirmation

#     def get(self, request, *args, **kwargs):
#         participation_id = kwargs.get('pk')
#         participation = get_object_or_404(Participation, pk=participation_id, status='pending')
        
#         # Calculate total price
#         number_of_participants = participation.number_of_participants
#         ticket_price = participation.event.event_ticket_price
#         total_cost = number_of_participants * ticket_price

#         # Prepare the context with necessary details
#         context = {
#             'event': participation.event,
#             'organizer': participation.event.organizer,
#             'ticket_price': ticket_price,
#             'number_of_participants': number_of_participants,
#             'total_cost': total_cost,
#             'participation': participation,
#         }

#         return render(request, self.template_name, context)
    

#     # def post(self, request, *args, **kwargs):
#     #     participation_id = kwargs.get('pk')

#     #     # Confirm the payment
#     #     try:
#     #         participation = Participation.objects.get(pk=participation_id, status='pending')
#     #         participation.status = 'confirmed'
#     #         participation.is_payment_confirmed = True
#     #         participation.save()

#     #         return redirect('download_invoice', pk=participation.pk)
#     #     except Participation.DoesNotExist:
#     #         return HttpResponseBadRequest("Participation not found or already confirmed")
#     def post(self, request, *args, **kwargs):
#         participation_id = kwargs.get('pk')

#         if participation_id:
#             try:
#                 participation = Participation.objects.get(pk=participation_id)

#                 # Check if the payment is already confirmed
#                 if participation.is_payment_confirmed:
#                     return HttpResponseBadRequest("Payment already confirmed")

#                 # Confirm payment
#                 participation.is_payment_confirmed = True
#                 participation.save()

#                 return redirect('download_invoice', pk=participation.pk)

#             except Participation.DoesNotExist:
#                 return HttpResponseBadRequest("Participation not found")
#         else:
#             return HttpResponseBadRequest("Invalid participation ID")

class ParticipantPaymentConfirmView(View):
    template_name = 'payment_confirmed.html'

    def get(self, request, *args, **kwargs):
        participation_id = kwargs.get('pk')
        participation = get_object_or_404(Participation, pk=participation_id, status='pending')
        
        # Calculate total price
        number_of_participants = participation.number_of_participants
        ticket_price = participation.event.event_ticket_price
        total_cost = number_of_participants * ticket_price

        # Prepare the context with necessary details
        context = {
            'event': participation.event,
            'organizer': participation.event.organizer,
            'ticket_price': ticket_price,
            'number_of_participants': number_of_participants,
            'total_cost': total_cost,
            'participation': participation,
        }

        return render(request, self.template_name, context)
 


class PaymentConfirmView(View):
       
    def post(self, request, *args, **kwargs):
        participation_id = kwargs.get('pk')

        if participation_id:
            try:
                participation = Participation.objects.get(pk=participation_id)

                # Check if the payment is already confirmed
                if participation.is_payment_confirmed:
                    return HttpResponseBadRequest("Payment already confirmed")

                # Confirm payment
                participation.is_payment_confirmed = True
                participation.save()

                return redirect('participant_event_interest')  # Adjust this URL as needed

            except Participation.DoesNotExist:
                return HttpResponseBadRequest("Participation not found")
        else:
            return HttpResponseBadRequest("Invalid participation ID")



class PaymentInvoiceDownloadView(DetailView):
    model = Participation
    template_name = 'payment_invoice_download.html'

    def get(self, request, *args, **kwargs):

        participation = self.get_object()
        if not participation.is_payment_confirmed:
            return HttpResponse("Payment not confirmed.", status=400)
        
        

        # # Prepare context for the invoice
        # context = {
        #     'event': participation.event,
        #     'participant': participation.participant,
        #     'number_of_participants': participation.number_of_participants,
        #     'organizer': participation.event.organizer,
        #     'ticket_price': participation.event.event_ticket_price,
        #     'total_member': participation.number_of_participants,
        #     'total_cost': participation.event.event_ticket_price,
        #     'transition_id': participation.transition_id
        # }
        # number_of_participants = participation.number_of_participants
        # ticket_price = participation.event.event_ticket_price
        # subtotal = number_of_participants * ticket_price
        # vat = subtotal * 0.15  # 15% VAT
        # platform_charge = subtotal * 0.05  # 5% platform charge
        # total_amount = subtotal + vat + platform_charge

        # # Prepare context for the invoice
        # context = {
        #     'event': participation.event,
        #     'participant': participation.participant,
        #     'number_of_participants': number_of_participants,
        #     'ticket_price': ticket_price,
        #     'subtotal': subtotal,
        #     'vat': vat,
        #     'platform_charge': platform_charge,
        #     'total_amount': total_amount,
        #     'transition_id': participation.transition_id,
        #     'organizer': participation.event.organizer
        # }

        if not participation.is_payment_confirmed:
            return HttpResponse("Payment not confirmed.", status=400)

        # Check for valid number_of_participants and ticket_price
        number_of_participants = participation.number_of_participants  # Default to 1 if None
        ticket_price = participation.event.event_ticket_price  # Default to 0 if None

        # Perform calculations
        subtotal = (float(number_of_participants) * float(ticket_price))
        vat = subtotal * 0.15  # 15% VAT
        platform_charge = subtotal * 0.05  # 5% platform charge
        total_amount = subtotal + vat + platform_charge

        # Prepare context for the invoice
        context = {
            'event': participation.event,
            'participant': participation.participant,
            'number_of_participants': number_of_participants,
            'ticket_price': ticket_price,
            'subtotal': subtotal,
            'vat': vat,
            'platform_charge': platform_charge,
            'total_amount': total_amount,
            'transition_id': participation.transition_id,
            'organizer': participation.event.organizer
        }

        # Render invoice as a PDF
        html_string = render_to_string('payment_invoice_download.html', context)
        pdf_file = BytesIO()
        pisa.CreatePDF(html_string.encode('UTF-8'), dest=pdf_file)

        response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{participation.transition_id}.pdf"'
        return response

class PaymentStatusView(View):
    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        try:
            participation = Participation.objects.get(event_id=event_id, participant=request.user.participant)
            return JsonResponse({'is_payment_confirmed': participation.is_payment_confirmed})
        except Participation.DoesNotExist:
            return JsonResponse({'is_payment_confirmed': False})
        
class OrganizerEventView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'organizer_event.html'

    def get(self, request, *args, **kwargs):
        now = datetime.now()  
        events = Event.objects.filter(
            event_registration_end__gte=now, 
            event_registration_start__lte=now,
            organizer=self.request.user.organizer
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
    
    def get_queryset(self):
        organizer= Organizer.objects.get(user=self.request.user)
        return Event.objects.filter(organizer=organizer)

class OrganizerEventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'organizer_event_creation.html'
    # success_url = 'organizer_event'

    def form_valid(self, form):
        form.instance.organizer = self.request.user.organizer
        return super().form_valid(form)
    
    def get_success_url(self):

        return reverse_lazy('or-home')
    
class OrganizerEventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'organizer_event_creation.html'


    def get_object(self, queryset = None):
        # return Event.objects.get(user = self.request.user)
        # return Event.objects.all()
        event_id = self.kwargs.get('event_id')
        return get_object_or_404(Event, id=event_id)
    
    def form_valid(self, form):
        event = form.save(commit = False)
        event.save()
        return super().form_valid(form)
    
        
    def get_success_url(self):

        return reverse_lazy('or-home')
    
    
    










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
    



