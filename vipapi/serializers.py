#serializers can transform django models into json data.
from rest_framework import serializers
from .models import VipWinner, RegisterVIP, PersonalInfo, PhotoPortfolio, DescribeYourself, ApplicantStatus, Messages, PhotoStory
from rest_auth.models import TokenModel

class PhotoStorySerializer(serializers.ModelSerializer):
      class Meta:
        model = PhotoStory
        fields = ('__all__')              

class VipWinnerSerializer(serializers.ModelSerializer):
      class Meta:
        model = VipWinner
        fields = ('__all__')

class RegisterVIPSerializer(serializers.ModelSerializer):
      class Meta:
        model = RegisterVIP
        fields = ('name', 'email', 'password', 'mobile_number')

class BasicUserInfoSerializer(serializers.ModelSerializer):
      class Meta:
        model = RegisterVIP
        fields = ('name', 'email', 'mobile_number')        

class TokenSerializer(serializers.Serializer): #for JWT
      token = serializers.CharField(max_length=255)    

class RestAuthTokenSerializer(serializers.ModelSerializer):
    user = BasicUserInfoSerializer()
    class Meta:
        model = TokenModel
        fields = ('key', 'user')     

class PersonalInfoSerializer(serializers.ModelSerializer):
      class Meta:
        model = PersonalInfo
        fields = ('__all__')   

class PhotoPortfolioSerializer(serializers.ModelSerializer):
        class Meta:
                model = PhotoPortfolio
                fields = ('__all__')  

class DescribeYourselfSerializer(serializers.ModelSerializer):
        class Meta:
                model = DescribeYourself
                fields = ('__all__') 

class ApplicantStatusSerializer(serializers.ModelSerializer):
        class Meta:
                model = ApplicantStatus
                fields = ('__all__')

class MessagesSerializer(serializers.ModelSerializer):
        class Meta:
                model = Messages
                fields = ('__all__')                                   

                               


