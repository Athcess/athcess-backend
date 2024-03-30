from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from ..models.physical_attribute import PhysicalAttribute
from ..models.user import User


# class SearchViewSet(viewsets.Viewset) :
#     def search(self, request):
#         if request.method == 'POST' :
#             searched = request.POST['searched']
#             if searched is not None :
#                 searchedModel = [User, PhysicalAttribute]
#                 for eachModel in searchedModel :
#                     if eachModel == User :
#                         queries = User.objects.filter(name__contains=searched)
#                     elif eachModel == PhysicalAttribute :
#                         queries = PhysicalAttribute.objects.filter(Q(height__contains=searched) | Q(weight__contains=searched))
#                 return Response([queries])
#             else :
#                 return Response('Search is empty')
#         else :
#             return Response('error in request method') 
class SearchViewSet(viewsets.ViewSet):
    def searched(self, request) :
        if request.method == 'POST' :
            return request.data

# class SearchViewSet(viewsets.ViewSet):
#     def searched(self, request):  # Add the 'request' argument here
#         if request.method == 'POST':
#             # Your code for handling the POST request and performing search
#             return request.data
    

