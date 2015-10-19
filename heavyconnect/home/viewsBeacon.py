from django.template.context_processors import request
from rest_framework import viewsets
from tutorial.beaconsapi.models import Beacon
from tutorial.beaconsapi.serializers import BeaconSerializer
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, get_list_or_404

dir(settings)
settings.__dict__



class BeaconViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    lookup_field = 'beacon_id'
    queryset = Beacon.objects.all()
    serializer_class = BeaconSerializer

def InventoryReportView(request):
    query_results = Beacon.objects.all()
    return render(request, 'beaconsapi/inventory-report.html', {'query_results': query_results})
