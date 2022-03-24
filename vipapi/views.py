from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from vipapi.models import VipWinner, RegisterVIP, PersonalInfo, PhotoPortfolio, DescribeYourself, ApplicantStatus, Messages, PhotoStory
from rest_framework import generics, permissions
from vipapi.serializers import VipWinnerSerializer, RegisterVIPSerializer, TokenSerializer, PersonalInfoSerializer, PhotoPortfolioSerializer, DescribeYourselfSerializer, ApplicantStatusSerializer, MessagesSerializer, PhotoStorySerializer
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
import datetime
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
#permissions class will use so that only authenticated uses can add,update or delete any candidates data.
# Create your views here.
def index(request):
    "the default page for the app"
    return HttpResponse("<br><h><b>Welcome to the VIPNAMES API SERVER</b></h>")

class PhotoStoryAPI(generics.ListAPIView):
    "to display list of VIPNAMES winners photos"
    queryset = PhotoStory.objects.all()
    serializer_class = PhotoStorySerializer

class VipWinnerAPI(generics.ListAPIView):
      "to display list of vip winners using ListAPIView"
      queryset = VipWinner.objects.all()
      serializer_class = VipWinnerSerializer

class RegisterNewAPI(generics.ListCreateAPIView):
      "to list or add new vip users in the list using ListCreateAPIView"
      queryset = RegisterVIP.objects.all()
      serializer_class = RegisterVIPSerializer
      def perform_create(self, serializer): #the method perform_create will save the password in correct hashing algorithm.
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UpdateRegistrationAPI(generics.RetrieveUpdateDestroyAPIView):
      "to get, update or delete users list using RetrieveUpdateDestroyAPIView"
      queryset = RegisterVIP.objects.all()
      serializer_class = RegisterVIPSerializer
      permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Add this view to authenticate user with JWT token. Earlier we were using rest-auth/login for authentication and logout.
# In the vipnames-reavctjs-app, we are using rest-auth/login to login users.
class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = VipWinner.objects.all()
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, email=username, password=password) #using email for authentication rather than username
        if user is not None:
            login(request, user) #saves user ID in the session using Django's session framework.
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PersonalInfoAPI(generics.CreateAPIView):
      "to add new user personal information in the database using CreateAPIView"
      queryset = PersonalInfo.objects.all()
      serializer_class = PersonalInfoSerializer
      permission_classes = (IsAuthenticated,)
      authentication_classes = (TokenAuthentication,) 

class GetPersonalInfoAPI(generics.ListAPIView):
    "to get personal information for the logon user or a specific user only"
    serializer_class = PersonalInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get_queryset(self):
        "this will return data for currently authenticated user only."
        user = self.request.user
        return PersonalInfo.objects.filter(email=user)

class EditPersonalInfoAPI(generics.RetrieveUpdateDestroyAPIView):
    "to update personal information for a specific user only"
    queryset = PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

class PhotoPortfolioAPI(generics.ListCreateAPIView):
    "to upload photos or view uploaded photos of an user's portfolio"
    parser_classes = (MultiPartParser,FormParser,) #required for file upload together with other form data.By default DRF only accepts json data.
    queryset = PhotoPortfolio.objects.all()
    serializer_class = PhotoPortfolioSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)  

class GetPhotoPortfolioAPI(generics.ListAPIView):
    "to get photoportfolio details for the authenticated user"  
    serializer_class = PhotoPortfolioSerializer
    permission_classes = (IsAuthenticated,)  
    authentication_classes = (TokenAuthentication,)
    def get_queryset(self):
        "this will return data for the specific user only"
        user = self.request.user
        return PhotoPortfolio.objects.filter(email=user)

class DescribeYourselfAPI(generics.CreateAPIView):
    "to save personality desc text from user"
    queryset = DescribeYourself.objects.all()
    serializer_class = DescribeYourselfSerializer
    permission_classes = (IsAuthenticated,)  
    authentication_classes = (TokenAuthentication,)

class GetDescribeYourselfAPT(generics.ListAPIView):
    "to get describeyourself text info for the requested user"
    serializer_class = DescribeYourselfSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get_queryset(self):
        "this will return data for the logged-in user only"
        user= self.request.user
        return DescribeYourself.objects.filter(email=user)   

class ApplicantStatusAPI(generics.ListAPIView):
    "to provide information regarding status of his/her application to participate in VIPNAMES contest"
    serializer_class = ApplicantStatusSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get_queryset(self):
        "to check different database tables to confirm applicant profile completeness status"
        profilepercent = ApplicantStatus.objects.get(email=self.request.user).profilepercent
        if profilepercent=='100%':
           return ApplicantStatus.objects.filter(email=self.request.user)
        else: 
           queryset1 = PersonalInfo.objects.filter(email=self.request.user)
           queryset2 = PhotoPortfolio.objects.filter(email=self.request.user)
           queryset3 = DescribeYourself.objects.filter(email=self.request.user)
           if queryset1.exists():
              ApplicantStatus.objects.filter(email=self.request.user).update(profilepercent='25%')
           if queryset2.exists():
              ApplicantStatus.objects.filter(email=self.request.user).update(profilepercent='50%')
           if queryset3.exists():
              ApplicantStatus.objects.filter(email=self.request.user).update(profilepercent='25%')    
           if queryset1.exists() and queryset2.exists():
              ApplicantStatus.objects.filter(email=self.request.user).update(profilepercent='75%')    
           if queryset1.exists() and queryset2.exists() and queryset3.exists():
              ApplicantStatus.objects.filter(email=self.request.user).update(profilepercent='100%')
           return ApplicantStatus.objects.filter(email=self.request.user)  

class MessagesAPI(generics.ListAPIView):
    "to get messages sent by the Admin for the requested user"
    serializer_class = MessagesSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get_queryset(self):
        "this will return data for the logged-in user only"
        user= self.request.user
        return Messages.objects.filter(email=user) 

#currently not used
class DeleteUserAPI(APIView):
    "to delete an user account" 
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def delete(self, request, format=None):
        "this will delete user based on its username" 
        RegisterVIP.objects.get(email=request.user).delete()
        return Response({'message':'user account deleted'})

class CheckUserPasswordAPI(APIView):
    "to check user password before deleting the account"
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def post(self, request, format=None): 
        User =  RegisterVIP.objects.get(email=request.user)
        password = self.request.POST['password']
        if check_password(password, User.password):
           RegisterVIP.objects.get(email=request.user).delete()
           result1 = PersonalInfo.objects.filter(email=request.user)
           if result1.exists():
              PersonalInfo.objects.get(email=request.user).delete()
           result2 = PhotoPortfolio.objects.filter(email=request.user)
           if result2.exists():   
              PhotoPortfolio.objects.get(email=request.user).delete()
           result3 = DescribeYourself.objects.filter(email=request.user)
           if result3.exists():    
              DescribeYourself.objects.get(email=request.user).delete()
           result4 = ApplicantStatus.objects.filter(email=request.user)
           if result4.exists():   
              ApplicantStatus.objects.get(email=request.user).delete()
           result5 = Messages.objects.filter(email=request.user)
           if result5.exists():    
              Messages.objects.get(email=request.user).delete() 
           content = {'message': 'password okay, account is deleted now'}
           return Response(content)
        else:
           content = {'message': 'invalid password'}
           return Response(content)    



def checkapplicants(request):
    "to provide interface to check who applied for the contest,check their profile and send update to them."
    if request.user.is_superuser:
       year = datetime.datetime.now().year 
       applicantlist = ApplicantStatus.objects.filter(registeredon__year=year)
       currentyear = datetime.date.today().year
       lasttenthyear = currentyear-10
       currentyear = currentyear+1
       yearlist = []
       for x in range(lasttenthyear, currentyear):
           yearlist = yearlist+[x]
       yearlist.reverse()
       return render(request, 'admin/checkapplicants.html', {'applicantlist':applicantlist, 'yearlist':yearlist})
    else:
        return HttpResponse("<h>You are not authorised.</h>") 

def checkapplicantsbyyear(request):
    "to provide applicants details according to the selected year"
    if request.user.is_superuser:
       year = request.GET['year']
       applicantlist = ApplicantStatus.objects.filter(registeredon__year=year)
       return render(request, 'admin/checkapplicantsbyyear.html', {'applicantlist':applicantlist})  
    else:
       return HttpResponse("<h>You are not authorised.</h>")  

def applicantdetails(request, id):
    "to provide interface to check applicant profile and to do necessary actions."
    if request.user.is_superuser:
       email = ApplicantStatus.objects.get(id=id).email
       checkstatus = ApplicantStatus.objects.get(id=id).checkedbyadmin
       checkedodate = ApplicantStatus.objects.get(id=id).checkedondate
       result1 = PersonalInfo.objects.filter(email=email)
       if result1.exists():
          fullname = PersonalInfo.objects.get(email=email).fullname
       else:
          fullname = RegisterVIP.objects.get(email=email).name    
       result2 = PersonalInfo.objects.filter(email=email)
       if result2.exists():   
          personalinfo = PersonalInfo.objects.filter(email=email)
       else:
          personalinfo = '0'   
       result3 = PhotoPortfolio.objects.filter(email=email)
       if result3.exists():    
          portfolio = PhotoPortfolio.objects.filter(email=email)
       else:
          portfolio = '0'    
       result4 = DescribeYourself.objects.filter(email=email)
       if result4.exists():  
          selftext = DescribeYourself.objects.filter(email=email)
       else:
          selftext = '0'      
       return render(request, "admin/applicantdetails.html", { 'personalinfo':personalinfo, 'portfolio':portfolio, 'selftext':selftext, 'checkstatus':checkstatus, 'checkedondate':checkedodate, 'fullname':fullname, 'id':id, 'email':email })   
    else:
       return HttpResponse("<h>You are not authorised.</h>")

def markaschecked(request):
    "to mark the check status of an applicant's profile as checked by Admin"
    if request.user.is_superuser:
        id = request.GET['id']
        ApplicantStatus.objects.filter(id=id).update(checkedbyadmin='Yes', checkedondate=datetime.date.today())
        day = datetime.date.today().day
        month = datetime.date.today().month
        year = datetime.date.today().year  
        microtime = datetime.datetime.now().microsecond
        applicantid = int(str(microtime)+str(day)+str(month)+str(year))  
        ApplicantStatus.objects.filter(id=id).update(applicantid=applicantid)
        return HttpResponse(" ")
    else:
        return HttpResponse("<h>You are not authorised.</h>") 

def sendmessage(request):
    "to save message in the messages model so that user can get message data"   
    if request.user.is_superuser:
        id = request.POST['id']
        message = request.POST['message']
        email = ApplicantStatus.objects.get(id=id).email
        name = ApplicantStatus.objects.get(id=id).name
        p1 = Messages(email=email, name=name, message=message)
        p1.save()
        return HttpResponse("Message sent successfully.")
    else:
        return HttpResponse("<h>You are not authorised.</h>")   

def sendemail(request):
    "to send email to the registered user for his/her application status to participate in the VIPNAMES contest."  
    if request.user.is_superuser:
        subject = request.POST['subject']
        message = request.POST['message']
        toaddress = request.POST['to']
        msg = EmailMessage(subject, message, to=[toaddress], from_email='vipnamesmohali@gmail.com')
        msg.content_subtype = 'html'
        msg.send() 
        print('email sent!!')
        return HttpResponse("Email sent successfully")
    else:
        return HttpResponse("<h>You are not authorised.</h>")   

def deleteapplicantaccount(request):
    "to delete account of the user registered to apply for the VIPNAMES contest"
    if request.user.is_superuser:
        id = request.GET['id']
        email = ApplicantStatus.objects.get(id=id).email
        RegisterVIP.objects.get(email=email).delete()
        result1 = PersonalInfo.objects.filter(email=email)
        if result1.exists():
            PersonalInfo.objects.get(email=email).delete()
        result2 = PhotoPortfolio.objects.filter(email=email)
        if result2.exists():
            PhotoPortfolio.objects.get(email=email).delete()
        result3 = DescribeYourself.objects.filter(email=email)
        if result3.exists():     
            DescribeYourself.objects.get(email=email).delete()
        result4 = Messages.objects.filter(email=email)
        if result4.exists():
            Messages.objects.filter(email=email).delete()
        ApplicantStatus.objects.get(id=id).delete()    
        return HttpResponseRedirect('/checkapplicants')
    else:
        return HttpResponse("<h>You are not authorised.</h>")   

def passwordreset(request):
    "used in the password reset"
    return HttpResponse('')     
                      



        





    

    


      

                    
