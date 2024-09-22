# voting/views.py

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from .utils import decode_qr_code_from_frame, is_valid_student_qr  # Import the utility function
import json
from django.urls import reverse

def scan_qr(request):
    if request.method == 'POST':
        # Log the incoming POST data to check if frames are correctly received
        print("Request body size:", len(request.body))  # To check the size of incoming data

        # Parse the JSON request to get the frame data
        try:
            data = json.loads(request.body)
            frame_data = data.get('frame')

            if frame_data:
                # Use the utility function to decode the QR code from the frame
                qr_code_data = decode_qr_code_from_frame(frame_data)
                print("QR Code Data:", qr_code_data)  # Log QR code data for debugging

                if qr_code_data:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Voter verified. Proceed to vote.',
                        'qr_data': qr_code_data
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Invalid QR code. Please try again.'
                    })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No frame data provided.'
                })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f"Error processing the frame: {str(e)}"
            })

    return render(request, 'voting/scan_qr.html')

# New view for manual QR code submission
def manual_qr_submit(request):
    if request.method == 'POST':
        manual_qr = request.POST.get('manual_qr')
        if manual_qr and is_valid_student_qr(manual_qr):
            # Redirect to the voting interface or any further validation
            voting_url = reverse('voting_interface') + f'?qr_code={manual_qr}'
            return HttpResponseRedirect(voting_url)
        else:
            return render(request, 'voting/scan_qr.html', {
                'error': 'Invalid QR code. Please try again.'
            })
    return render(request, 'voting/scan_qr.html')

# voting/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from election.models import Candidate
from .models import Vote
import hashlib
import datetime

def voting_interface(request):
    # Fetch all candidates to display them on the page
    candidates = Candidate.objects.all()
    qr_code = request.GET.get('qr_code')

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        student_id = request.POST.get('qr_code')
        print(qr_code)
        print(student_id)

        # Validate that the candidate exists
        candidate = get_object_or_404(Candidate, pk=candidate_id)

        # Create a vote instance
        previous_hash = Vote.objects.last().hash if Vote.objects.exists() else "0"  # Using the last vote's hash or "0"
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Combine student_id, candidate, and timestamp to create a unique hash
        vote_data = f'{student_id}{candidate_id}{timestamp}{previous_hash}'.encode()
        vote_hash = hashlib.sha256(vote_data).hexdigest()

        # Save the vote in the database
        vote = Vote(
            student_id=student_id,
            candidate=candidate,
            previous_hash=previous_hash,
            hash=vote_hash
        )
        vote.save()

        return redirect('vote_success')

    return render(request, 'voting/voting_interface.html', {'candidates': candidates, 'qr_code': qr_code})

def vote_success(request):
    return render(request, 'voting/vote_success.html')
