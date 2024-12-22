# community/context_processors.py
def latest_post(request):
    try:
        from .models import Post
        latest = Post.objects.order_by('-created_at').first()

        if latest:
            return {
                'latest_post': {
                    'title': latest.title,
                    'url': f'/community/{latest.id}/'  # URL 패턴 수정
                }
            }
        return {'latest_post': None}
    except:
        return {'latest_post': None}