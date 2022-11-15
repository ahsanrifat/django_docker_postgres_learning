from rest_framework_simplejwt.views import TokenObtainPairView

from token_app.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
