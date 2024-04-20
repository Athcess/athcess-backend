from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization
from ..models.physical_attribute import PhysicalAttribute
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from django.utils import timezone


class PhysicalAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalAttribute
        fields = ['username', 'created_at', 'height', 'weight', 'fat_mass', 'muscle_mass', 'sit_up', 'push_up', 'run']


class PhysicalAttributeViewSet(viewsets.ModelViewSet):
    queryset = PhysicalAttribute.objects.all()
    serializer_class = PhysicalAttributeSerializer
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        created_at = timezone.now()
        serializer = PhysicalAttributeSerializer(data={
            'username': request.user,
            'created_at': created_at,
            'height': request.data['height'],
            'weight': request.data['weight'],
            'fat_mass': request.data['fat_mass'],
            'muscle_mass': request.data['muscle_mass'],
        })

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PhysicalAttributeSerializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        for key, value in request.query_params.items():
            queryset = queryset.filter(**{key: value})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

