from users.models.custom_user import CustomUser, Athlete, Scout, Admin_organization, Organization
from ..models.post import Post
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response
from django.utils import timezone


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['following']


class FollowViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):

        try:
            organization = Organization.objects.get(club_name=request.data['club_name'])
        except Organization.DoesNotExist:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        user = CustomUser.objects.get(username=request.user)

        club_name = organization.club_name

        following_list = user.following.split(',') if user.following else []

        if club_name in following_list:
            following_list.remove(club_name)
            message = f"Removed {club_name} from following"
        else:
            following_list.append(club_name)
            message = f"Added {club_name} to following"

        updated_following = ','.join(following_list)

        user.following = updated_following
        user.save()

        organization = Organization.objects.get(club_name=club_name)

        follower_list = organization.followers.split(',') if organization.followers else []

        if user.username in follower_list:
            follower_list.remove(user.username)
        else:
            follower_list.append(user.username)

        updated_followers = ','.join(follower_list)
        organization.followers = updated_followers
        organization.save()

        return Response({'message': message, 'following': updated_following}, status=status.HTTP_200_OK)
