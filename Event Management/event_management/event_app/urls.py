from django.urls import path
from .views import (ParticipantEventView, ParticipantEventDetailsView, ParticipantInterestView, PaymentInvoiceDownloadView, OrganizerEventView, OrganizerEventCreateView, OrganizerEventParticipantsView, PDFView)

urlpatterns = [
    path('', ParticipantEventView.as_view(), name='participant_event'),
    path('events/<int:pk>/', ParticipantEventDetailsView.as_view(), name='event_detail'),
    path('events/<int:event_id>/interest/', ParticipantInterestView.as_view(), name='participant_interest'),
    path('participation/<int:pk>/invoice/', PaymentInvoiceDownloadView.as_view(), name='payment_invoice_download'),
    path('organizer/events/', OrganizerEventView.as_view(), name='organizer_event'),
    path('organizer/events/create/', OrganizerEventCreateView.as_view(), name='organizer_event_create'),
    path('organizer/events/<int:pk>/participants/', OrganizerEventParticipantsView.as_view(), name='organizer_event_participants'),
    path('events/<int:event_id>/pdf/', PDFView.as_view(), name='event_pdf'),
]
