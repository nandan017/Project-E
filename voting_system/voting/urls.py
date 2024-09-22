from django.urls import path
from .views import scan_qr, manual_qr_submit, voting_interface, vote_success

urlpatterns = [
    path('scan_qr/', scan_qr, name='scan_qr'),
    path('manual_qr_submit/', manual_qr_submit, name='manual_qr_submit'),  # New URL for manual QR submission
    path('vote/', voting_interface, name='voting_interface'),
    path('vote-success/', vote_success, name='vote_success'),
]
