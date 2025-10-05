from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse

# From Auth0 Django Tutorial
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
import time
from multiprocessing.pool import AsyncResult
from scribblebug.tasks import create_scribble_task


# helper functions
from scribblebug import scribble_utils, score_utils


def index(request):
    # return HttpResponse("Hello, world.")

    current_spider = request.user

    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
            "nums": list(range(20)),
            "my_scribbles": scribble_utils.get_user_scribbles(current_spider),
            "recent_scribs": score_utils.get_recent_played(current_spider),
        },
    )

def new_scribble(request):
    if request.method == "POST":
        data = json.loads(request.body)
        keywords = data.get('keywords', [])

        if not keywords:
            return JsonResponse({'error': 'No keywords provided'}, status=400)

        # Start background task
        task = create_scribble_task.delay(request.user.id, keywords)
        return JsonResponse({'task_id': task.id})
    else:
        return render(request, "new_scribble.html")

def task_stream(request, task_id):
    def event_stream():
        task = AsyncResult(task_id)
        while not task.ready():
            yield f"data: {json.dumps({'status': 'processing', 'message': 'Working...'})}\n\n"
            time.sleep(2)

        if task.successful():
            yield f"data: {json.dumps({'status': 'complete', 'redirect_url': f'/scribble/{task.result}/'})}\n\n"
        else:
            yield f"data: {json.dumps({'status': 'failed'})}\n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

#
# # OAuth Set up
# oauth = OAuth()
# oauth.register(
#     "auth0",
#     client_id=settings.AUTH0_CLIENT_ID,
#     client_secret=settings.AUTH0_CLIENT_SECRET,
#     client_kwargs={
#         "scope": "openid profile email",
#     },
#     server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
# )
# def login(request):
#     return oauth.auth0.authorize_redirect(
#         request, request.build_absolute_uri(reverse("callback"))
#     )
# def callback(request):
#     token = oauth.auth0.authorize_access_token(request)
#     request.session["user"] = token
#     return redirect(request.build_absolute_uri(reverse("index")))
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