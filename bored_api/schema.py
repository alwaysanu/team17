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
    saved_list = graphene.List(ActivityType, email=graphene.String())
    new_activities = graphene.List(ActivityType, link=graphene.String(), email=graphene.String())
    like = graphene.Field(UserType, email=graphene.String(), category=graphene.String())
    save_request = graphene.Field(UserType, email=graphene.String(), category=graphene.String(), name=graphene.String(),
        participants=graphene.Int(), key=graphene.String(), title=graphene.String(), desc=graphene.String(),
        link=graphene.String(), thumb=graphene.String())

    # test_save = graphene.Field(UserType, email=graphene.String(), key=graphene.String())

    def resolve_saved_list(self,info, **kwargs):
        email = kwargs.get('email')
        user = BoredUser.objects.get(email=email)
        activityList  = user.saved_activities
        print(type(activityList))
        return activityList.all()
        # import requests
        # for item in activityList:

    def resolve_save_request(self, info, **kwargs):
        email = kwargs.get('email')

        activity = Activity()
        activity.name = kwargs.get('name')
        activity.category = kwargs.get('category')
        activity.participants = kwargs.get('participants')
        activity.key = kwargs.get('key')

        activity.title = kwargs.get('title')
        activity.link = kwargs.get('link')
        activity.description = kwargs.get('desc')
        activity.thumb = kwargs.get('thumb')
        activity.save()

        user = BoredUser.objects.get(email=email)
        user.saved_activities.add(activity)
        user.save()
        return user


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
            user = BoredUser.objects.create_user(email=email, category_weights=res[:-1], username=email.split('@')[0])
            user.save()
        return user

    def resolve_new_activities(self, info, **kwargs):
        import json
        email = kwargs.get('email')

        if email and BoredUser.objects.filter(email=email).exists():
            import requests
            import random
            from webpreview import web_preview
            prob = random.random()
            user = BoredUser.objects.get(email=email)
            weights = user.category_weights.split(',')
            weights = [int(x) for x in weights]
            fav_category = weights.index(max(weights))
            # print(fav_category)
            CATEGORIES = ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"]
            from google import google

            if prob>0.6:
                resp = requests.get("https://www.boredapi.com/api/activity/")
            else:
                resp = requests.get("https://www.boredapi.com/api/activity?type="+CATEGORIES[fav_category])
            resp = json.loads(resp.text)

            from googleapiclient.discovery import build
            API_KEY = "AIzaSyDIFF1lEqsuX-9vd-W8cUu1unZH5oeQe4s"
            CSE_ID = "010456897677353178205:0mffw7ezvwy"

            def google_search(search_term, api_key, cse_id, **kwargs):
                service = build("customsearch", "v1", developerKey=api_key)
                res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
                return res

            # result = google_search(resp['activity'], API_KEY, CSE_ID)
            num_page = 1
            result = google.search(resp['activity'], num_page)
            activities = []

            for search_results in result[:6]:
                activity = Activity()
                activity.name = resp['activity']
                activity.category = resp['type']
                activity.participants = int(resp['participants'])
                activity.key = resp['key']

                activity.title = search_results.name
                activity.link = search_results.link
                activity.description = search_results.description
                img_url = web_preview(activity.link)[2]
                # img_url = ""
                activity.thumb = img_url if img_url else ''
                activity.save()
                activities.append(activity)

            user.last_activity = activity
            user.save()
            return activities

    def resolve_like(self, info, **kwargs):
        email = kwargs.get('email')
        category = kwargs.get('category')

        CATEGORIES = ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"]
        user = get_object_or_404(BoredUser, email=email)

        if category !='dislike':
            cat_idx = CATEGORIES.index(category)
            category_weights = user.category_weights.split(',')
            category_weights = category_weights
            print(type(category_weights[cat_idx]))
            category_weights[cat_idx] = str(int(category_weights[cat_idx])+ 1)
            user.category_weights = ",".join(category_weights)
        user.last_activity= None

        user.save()

        return user



schema = graphene.Schema(query=Query)
