from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def summary(request):
    tamil_summary = request.GET.get('summary', '')
    return render(request, 'summary.html', {'summary': tamil_summary})


