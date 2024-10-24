# voting/views.py

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .utils import decode_qr_code_from_frame, is_valid_student_qr 
import json
from django.urls import reverse
from election.models import Candidate
from .models import Vote
import hashlib
import datetime

# Assume decode_qr_code_from_frame is already imported

def scan_qr(request):
    if request.method == 'POST':
        try:
            print("Request body size:", len(request.body))
            data = json.loads(request.body)
            frame_data = data.get('image')

            if not frame_data:
                print("Error: No frame data received.")
                return JsonResponse({
                    'status': 'error',
                    'message': 'No frame data provided.'
                })

            print("Received frame data size:", len(frame_data))
            print("Frame data (first 100 chars):", frame_data[:100])
            print("Frame data (last 100 chars):", frame_data[-100:])

            # Split the base64 data to remove the prefix if present
            if frame_data.startswith('data:image/png;base64,'):
                frame_data = frame_data.split(',', 1)[1]

            qr_code_data = decode_qr_code_from_frame(frame_data)

            if qr_code_data:
                if is_valid_student_qr(qr_code_data):
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Voter verified. Proceed to vote.',
                        'qr_data': qr_code_data
                    })
                else:
                    print("Error: Invalid QR code.")
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Invalid QR code. Please try again.'
                    })
            else:
                print("Error: No QR code found.")
                return JsonResponse({
                    'status': 'error',
                    'message': 'No QR code found in the image.'
                })

        except json.JSONDecodeError:
            print("Error: Invalid JSON format.")
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON format.'
            })

        except Exception as e:
            print("Error processing request:", e)
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

def voting_interface(request):
    # Fetch all candidates to display them on the page
    candidates = Candidate.objects.all()
    qr_code = request.GET.get('qr_code')  # Passed as GET parameter

    if request.method == 'POST':
        # Retrieve the selected candidates from the form (comma-separated string)
        candidates_id = request.POST.get('selected_candidates', '').split(',')
        student_id = request.POST['qr_code']  # Retrieve the hidden input value (qr_code from POST)

        # Generate a vote hash
        previous_hash = Vote.objects.last().hash if Vote.objects.exists() else "0"  # Use last vote hash or "0"
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("CanID",candidates_id)
        candidates_id.sort()
        print("CanID",candidates_id)
        # Combine student_id, timestamp, and previous_hash to create a unique hash
        vote_data = f'{student_id}{candidates_id}{timestamp}{previous_hash}'.encode('utf-8')
        vote_hash = hashlib.sha256(vote_data).hexdigest()
        print("\n\nFrom Views When Saving")
        print("\n\n",vote_data,"\n\n")
        # Create the vote instance
        vote = Vote(
            timestamp=timestamp,
            student_id=student_id,
            previous_hash=previous_hash,
            hash=vote_hash
        )
        vote.save()

        # Link the selected candidates to the vote
        for candidate_id in candidates_id:
            candidate = get_object_or_404(Candidate, candidate_key=candidate_id)
            vote.candidates.add(candidate)

        # Save the many-to-many relation
        vote.save()

        # Redirect to a success page after processing votes
        return redirect('vote_success')

    # Render the page with candidates and the provided qr_code
    return render(request, 'voting/voting_interface.html', {'candidates': candidates, 'qr_code': qr_code})

def vote_success(request):
    return render(request, 'voting/vote_success.html')
