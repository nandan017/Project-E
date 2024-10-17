import hashlib
from voting.models import Vote

def calculate_hash(vote):
    """
    Helper function to calculate the hash of a vote.
    The hash is based on the vote data including the student_id, candidate_id, previous_hash, and timestamp.
    """
    print("CID:",vote.candidate.candidate_key)
    vote_data = f'{vote.student_id}{vote.candidate_id}{vote.timestamp}{vote.previous_hash}'.encode('utf-8')
    print("From utils",vote_data)
    return hashlib.sha256(vote_data).hexdigest()

def is_blockchain_valid():
    """
    Validates the entire blockchain by checking each vote.
    Returns True if the blockchain is valid, False otherwise.
    """
    votes = Vote.objects.all().order_by('timestamp')
    
    if not votes:
        print("No votes found in the blockchain.")
        return True  # Consider an empty blockchain as valid

    previous_hash = "0"  # Initialize previous_hash for the first vote

    for vote in votes:
        print(f"Validating vote: Student ID={vote.student_id}, Candidate={vote.candidate.name}, Previous Hash={vote.previous_hash}, Timestamp={vote.timestamp}")

        # Calculate the hash for the current vote
        recalculated_hash = calculate_hash(vote)
        print(f"Recalculated Hash: {recalculated_hash}, Stored Hash: {vote.hash}")

        # Check if the stored hash matches the recalculated hash
        if recalculated_hash != vote.hash:
            print(f'Hash mismatch for vote by {vote.student_id}.')
            return False
        
        # Check if the previous_hash matches the previous vote's hash
        if previous_hash != "0" and vote.previous_hash != previous_hash:
            print(f'Invalid blockchain: Previous hash mismatch for vote by {vote.student_id}. Expected: {previous_hash}, Found: {vote.previous_hash}')
            return False
        
        # Update previous_hash to current vote's hash for the next iteration
        previous_hash = vote.hash

    print("All votes are valid.")
    return True