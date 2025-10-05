from scribblebug.models import Score, Scribble

def get_recent_played(spider):
    scores = Score.objects.filter(spider=spider)
    if not scores: return []

    scores = scores.order_by('-last_played')[:20]
    ret = []
    for s in scores:
        ret.append(s.scribble)
    return list(ret)

def get_scores_of_scrib(scrib):
    return list(Score.objects.filter(scribble=scrib).order_by('score')[:10])

def update_play(scrib_id, spider):

    s = Score.objects.filter(scribble_id=scrib_id, spider=spider)
    if s:
        s=s.first()
        s.save()
    else:
        scribble = Scribble.objects.filter(id=scrib_id).first()
        s = Score( score=0, scribble=scribble, spider=spider)
        s.save()

def new_score(spider, scribble_id, score):
    scrib = Scribble.objects.filter(id=scribble_id, spider=spider)
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