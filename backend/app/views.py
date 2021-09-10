from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login/")
def index(request):

    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))



import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("hello-world-e9c1c-firebase-adminsdk-ifpd6-3c008d733a.json")
firebase_admin.initialize_app(cred)

def Firebase_validation(id_token):
   """
   This function receives id token sent by Firebase and
   validate the id token then check if the user exist on
   Firebase or not if exist it returns True else False
   """
   try:
       decoded_token = auth.verify_id_token(id_token)
       uid = decoded_token['uid']
       provider = decoded_token['firebase']['sign_in_provider']
       image = None
       name = None
       if "name" in decoded_token:
           name = decoded_token['name']
       if "picture" in decoded_token:
           image = decoded_token['picture']
       try:
           user = auth.get_user(uid)
           email = user.email
           if user:
               return {
                   "status": True,
                   "uid": uid,
                   "email": email,
                   "name": name,
                   "provider": provider,
                   "image": image
               }
           else:
               return False
       except UserNotFoundError:
           print("user not exist")
   except ExpiredIdTokenError:
       print("invalid token")

class SocialSignupAPIView(GenericAPIView):
    """
    api for creating user from social logins
    """
    def post(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_header:
            id_token = auth_header.split(" ").pop()
            validate = Firebase_validation(id_token
            
            if validate:
                user = CustomUser.objects.filter(uid = validate["uid"]).first()
                
                if user:
                    data = {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "image": user.image,
                        "type": "existing_user",
                        "provider": validate['provider']
                   }
                   
                   return Response({“data”: data, “message”: “Login Successful” })
                   
                else:
                    user = CustomUser(
                        email = validate['email'],
                        name = validate['name'],
                        uid = validate['uid'],
                        image = validate['image']
                    )
                    
                    user.save()

                    data = {
                        "id": user.id,
                        "email": obj.email,
                        "name": obj.name,
                        "image": obj.image,
                        "type": "new_user",
                        "provider": validate['provider']
                    }
                    
                    return Response({“data”: data, “message”: “User Created Successfully” })
            else:
                return Response({“message”: “invalid token”})
        else:
            return Response({“message”: “token not provided”})