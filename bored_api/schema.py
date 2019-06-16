from graphene_django import DjangoObjectType
import graphene
from .models import BoredUser, Activity
from django.shortcuts import get_object_or_404

class UserType(DjangoObjectType):
    class Meta:
        model = BoredUser

class ActivityType(DjangoObjectType):
    class Meta:
        model = Activity


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, email=graphene.String())
    user_login = graphene.Field(UserType, username=graphene.String(), email=graphene.String())
    # saved_list = graphene.Field(UserType, username=graphene.String(), email=graphene.String())
    new_activity = graphene.Field(ActivityType, link=graphene.String(), email=graphene.String())
    like = graphene.Field(UserType, email=graphene.String(), category=graphene.String())

    def resolve_user(self, info, **kwargs):
        email = kwargs.get('email')
        return BoredUser.objects.get(email=email)

    def resolve_all_users(self, info, **kwargs):
        return BoredUser.objects.all()


    def resolve_user_login(self, info, **kwargs):
        print(info.context.user)
        email = kwargs.get('email')
        if BoredUser.objects.filter(email=email).exists():
            user = BoredUser.objects.get(email=email)
        else:
            res = '0,'*9
            user = BoredUser.objects.create_user(email=email, category_weights=res[:-1],
                    saved_activities='', username=email.split('@')[0])
            user.save()
        return user

    def resolve_new_activity(self, info, **kwargs):
        import json
        email = kwargs.get('email')

        if email and BoredUser.objects.filter(email=email).exists():
            import requests
            user = BoredUser.objects.get(email=email)
            from google import google
            resp = requests.get("https://www.boredapi.com/api/activity/")
            resp = json.loads(resp.text)
            num_page = 1
            search_results = google.search(resp['activity'], num_page)
            activity = Activity()
            activity.name = resp['activity']
            activity.category = resp['type']
            activity.participants = int(resp['participants'])
            activity.key = resp['key']

            activity.title = search_results[0].name
            activity.link = search_results[0].link
            activity.description = search_results[0].description
            activity.thumb = ''
            activity.save()

            user.last_activity = activity
            user.save()
            return activity

    def resolve_like(self, info, **kwargs):
        email = kwargs.get('email')
        category = kwargs.get('category')

        CATEGORIES = ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"]

        cat_idx = CATEGORIES.index(category)

        user = get_object_or_404(BoredUser, email=email)
        category_weights = user.category_weights.split(',')
        category_weights = category_weights
        print(type(category_weights[cat_idx]))
        category_weights[cat_idx] = str(int(category_weights[cat_idx])+ 1)
        user.category_weights = ",".join(category_weights)
        user.last_activity= None

        user.save()

        return user



schema = graphene.Schema(query=Query)
