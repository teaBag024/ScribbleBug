from scribblebug.models import Score, Scribble

def get_recent_played(spider):
    scores = Score.objects.filter(spider=spider)
    if not scores: return []

    scores = scores.order_by('-last_played')[:20]
    return list(scores.values("scribble"))

def new_score(spider, scribble_name, score):
    scrib = Scribble.objects.filter(name=scribble_name, spider=spider)
    if scrib:
        scrib = scrib.first()
        s = Score.objects.filter(scribble=scrib)
        if s: #already exists
            s = s.first()
            if s.score < score: # new high score
                s.score = score
            # OTHER: update last played by saving
            s.save()

        else: # yet to make
            s = Score( score=score, scribble=scrib, spider=spider)
            s.save()

    else: return