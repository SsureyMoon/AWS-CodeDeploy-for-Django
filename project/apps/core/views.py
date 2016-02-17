from django.http import JsonResponse


def api_404(request):
    return JsonResponse({'detail': 'url not found'}, status=404)
