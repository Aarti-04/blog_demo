from django.shortcuts import render
from rest_framework.views import APIView,Response,status
from .managers import CustomUserManager,PostManager
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser,CustomToken,Post
from .serializers import CustomTokenObtainPairSerializers,UserSerializer,PostSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.utils import timezone


def get_auth_token(authenticatedUser):
    # token_serializer = CustomTokenObtainPairSerializers()
    # token = token_serializer.get_token(authenticatedUser)
    # refresh = RefreshToken.for_user(authenticatedUser)
    # token["refresh"]=str(refresh)
    # token["userid"]=int( authenticatedUser.id)
    access_token=AccessToken.for_user(authenticatedUser)
    refresh_token=RefreshToken.for_user(authenticatedUser)
    token={"access_token":str(access_token),"refresh_token":str(refresh_token)}
    return token
class UserApiView(APIView):
    def get(self,request):
        users=CustomUser.objects.all()
        users=UserSerializer(users,many=True)
        return Response({"response":users.data})
    def post(self,request):
        user=request.data
        if "email" not in user or "password" not in user:
            raise ValueError("Username and Password is required")
                # return Response({"errors":""},status=status.HTTP_400_BAD_REQUEST) 
        password=user["password"]
        user= CustomUser(**user)
        user.set_password(password)
        user.save()
        return Response({"response":"User Registered successfully"},status=status.HTTP_201_CREATED)     
class UserLoginApiView(APIView):
    def post(self,request):
        user =request.data
        authenticatedUser=authenticate(request,**user)
        print("before login user")
        print(request.user)
        print(authenticatedUser)
        print("after login")
        print(request.user)
        if authenticatedUser is None:
            return Response({"Error":"Authentication failed"},status=status.HTTP_401_UNAUTHORIZED)  
        login(request,authenticatedUser)
        token=get_auth_token(authenticatedUser)
        custom_token, created = CustomToken.objects.get_or_create(user=authenticatedUser,defaults={"refresh_token":token["refresh_token"],"access_token":token["access_token"]})
        print("token created",created)
        if not created:
            custom_token.refresh_token = token["refresh_token"]
            custom_token.access_token = token["access_token"]
            custom_token.save(update_fields=['refresh_token',"access_token"])
            print("token updated")
        print(request.user)
        serializeduser=UserSerializer(authenticatedUser)
        res={
            "user":serializeduser.data,
            "status":
            {
                "message": "user authenticated",
                "code": status.HTTP_200_OK,
            },
            "token":
            {
                "access_token":token["access_token"],
                "refresh_token":token["refresh_token"]
            }
        }
        return Response(res)
class UserLogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        print(request.user)
        # print(request.user.auth_token)
        token=request.headers["Authorization"].split()[1]
        token_obj=CustomToken.objects.filter(access_token=token).first()
        response={
                "status":
                {
                    "message": "",
                    "code": ""
                }
            }
        print(token_obj)
        if token_obj:
            token_obj.delete()
            logout(request)
            response["status"]["message"]="logout successfully"
            response["status"]["code"]=status.HTTP_200_OK
            return Response(response)
        response["status"]["message"]="Something went wrong"
        response["status"]["code"]=status.HTTP_400_BAD_REQUEST
        return Response(response)

class PostApiView(APIView):
    
    def get(self,request):
        response={
            "post":"",
            "status":
            {
                "message": "user authenticated",
                "code": status.HTTP_200_OK,
            },}
        all_post=Post.objects.all()
        SerializedPost=PostSerializer(all_post,many=True)
        # if SerializedPost.is_valid():
        response["status"]["data"]=SerializedPost.data
        response["status"]["status"]=status.HTTP_200_OK
        response["status"]["message"]="All post"
        return Response(response)
    def post(self,request):
        permission_classes=[IsAuthenticated]
        print(request.user)
        post=request.data
        post["userid"]=request.user
        post_to_save=Post.objects.create(**post)
        print(post_to_save)
        # PostManager.create_post(post)
        response={
                "status":
                {
                    "message": "",
                    "code": ""
                }
            }
        response["status"]["message"]="post created succsessfully"
        response["status"]["code"]=status.HTTP_201_CREATED
        return Response(response)
    def put(self,request,*args,**kwargs):
        permission_classes=[IsAuthenticated]
        response={
                "status":
                {
                    "message": "",
                    "code": ""
                }
            }
        if "param" in kwargs:
            post_id=kwargs.get("param")
            new_data_to_update=request.data
            user=request.user
            post_user=Post.objects.filter(userid_id=user,id=post_id).first()
            if not post_user:
                response["status"]["message"]="your are not authorized or post does not exsist"
                response["status"]["code"]=status.HTTP_400_BAD_REQUEST
                return Response(response)
            print(post_user.title)
            post_to_update=Post.objects.filter(id=post_id).update(**new_data_to_update)
            print(post_to_update)
        return Response({"responce":"post to update"})
