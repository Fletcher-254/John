from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Nyutu Systems API is running"})
