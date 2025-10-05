import threading
import traceback
import uuid

from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse

import json
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
import time
from multiprocessing.pool import AsyncResult

from scribblebug.scribble_utils import create_scribble

# helper functions
from scribblebug import scribble_utils, score_utils

# Yay, mutable global state
task_status = {}

def index(request):
    context={
        "my_scribbles": scribble_utils.get_user_scribbles(request.user),
        "recent_scribs": score_utils.get_recent_played(request.user),
    } if request.user.is_authenticated else {}

    return render(
        request,
        "index.html",
        context=context,
    )


def new_scribble(request):
    if request.method == "POST":
        data = json.loads(request.body)
        keywords = data.get('keywords', [])

        # Generate task ID
        task_id = str(uuid.uuid4())
        task_status[task_id] = {'status': 'processing', 'message': 'Starting...'}

        # Run in background thread
        thread = threading.Thread(
            target=process_scribble_background,
            args=(task_id, request.user, keywords)
        )
        thread.daemon = True
        thread.start()

        return JsonResponse({'task_id': task_id})
    else:
        return render(request, "new_scribble.html")

def process_scribble_background(task_id, user, keywords):
    """Runs in background thread"""
    try:
        # Update status
        task_status[task_id] = {'status': 'processing', 'message': 'Creating scribble...'}

        # Create scribble
        scribble = create_scribble(user, keywords)

        # Mark complete
        task_status[task_id] = {
            'status': 'complete',
            'scribble_id': scribble.id
        }
    except Exception as e:
        print(traceback.format_exc())
        task_status[task_id] = {'status': 'failed', 'error': str(e)}

def task_stream(request, task_id):
    """SSE endpoint"""
    def event_stream():
        while True:
            status = task_status.get(task_id, {'status': 'processing', 'message': 'Working...'})

            if status['status'] == 'complete':
                yield f"data: {json.dumps({'status': 'complete', 'redirect_url': f'/scribble/{status['scribble_id']}'})}\n\n"
                break
            elif status['status'] == 'failed':
                yield f"data: {json.dumps({'status': 'failed'})}\n\n"
                break
            else:
                yield f"data: {json.dumps({'status': 'processing', 'message': status.get('message', 'Working...')})}\n\n"

            time.sleep(2)

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


def logout_view(request):
    logout(request)

    return redirect(
        f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.SOCIAL_AUTH_AUTH0_KEY,
            },
            quote_via=quote_plus,
        ),
    )
