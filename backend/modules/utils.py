import pyrankvote
from pyrankvote import Candidate, Ballot
import itertools
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def get_tuesday_dates(n: int):
    now = datetime.now()
    next_month = (now.replace(day=1) + relativedelta(months=1))
    
    result = []
    
    date = next_month
    while date.weekday() != 1:
        date += timedelta(days=1)
    
    for i in range(n):
        if i < n:
            result.append((date + timedelta(weeks=i)).isoformat())
        else:
            result.append(now.isoformat())
    
    return result


def commit_voting(ballots_list: list, winners_count: int = 1):
    ballots_list = [[str(candidate) for candidate in ballot] for ballot in ballots_list]

    all_votes = itertools.chain.from_iterable(ballots_list)
    all_participating_ids = set(list(all_votes))

    candidates_submission_ids = [Candidate(participating_id) for participating_id in all_participating_ids]


    ballots = [Ballot(ranked_candidates=[Candidate(vote_id) for vote_id in ballot]) for ballot in ballots_list]


    election_result = pyrankvote.single_transferable_vote(
        candidates_submission_ids, ballots, number_of_seats=winners_count
    )

    election_results = []
    for candidate in election_result.rounds[-1].candidate_results:
        result = {
            'submission_id': int(candidate.candidate.name),
            "number_of_votes" : round(candidate.number_of_votes, 2),
            "status" : candidate.status
            }
        election_results.append(result)

    return election_results

