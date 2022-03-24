from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)      


# Create your models here.

class PhotoStory(models.Model):
    "to provide photo list of winners"
    name = models.CharField(max_length=100)
    photourl = models.ImageField(upload_to='uploadedimages', max_length=2500)
    description = models.TextField(null=True)
    dateadded = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "PhotoStory"
    def __unicode__(self):
          return self.name    

class VipWinner(models.Model):
      "DB table to save data for VIP title winners"
      name = models.CharField(max_length=100)
      email = models.EmailField()
      address = models.CharField(max_length=300)
      year = models.IntegerField(null=True)
      slogan = models.CharField(max_length=200, null=True)
      class Meta:
          verbose_name_plural = "VipWinner"
      
class RegisterVIP(AbstractUser):
      "to store login details in a custom user model preferred in real-world-apps, also removing username and using email/password for authentication."
      name = models.CharField(max_length=100)
      mobile_number = models.IntegerField(default=9988583997)
      email = models.EmailField(_('email address'), unique=True)
      USERNAME_FIELD = 'email'
      REQUIRED_FIELDS = []
      objects = UserManager()

class PersonalInfo(models.Model):
    "to save personal information of each user registered for VIP contest"
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=100)
    petname = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    mothername = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    pincode = models.IntegerField()
    mobilenumber = models.IntegerField()
    alternatenumber = models.IntegerField()
    gender = models.CharField(max_length=50)
    dateofbirth = models.DateField()
    weight = models.IntegerField()
    height = models.DecimalField(max_digits=3, decimal_places=2)  
    class Meta:
        verbose_name_plural = "PersonalINFO"
    def __unicode__(self):
          return self.email  

class PhotoPortfolio(models.Model):
    "to upload photos for user"
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    facephoto = models.ImageField(upload_to='uploadedimages', max_length=2500)
    standingposephoto = models.ImageField(upload_to='uploadedimages', max_length=2500)
    sideposephoto = models.ImageField(upload_to='uploadedimages', max_length=2500)
    stylishposephoto = models.ImageField(upload_to='uploadedimages', max_length=2500)  
    date_uploaded = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "PhotoPortFolio" 
    def __unicode__(self):
          return self.name       

class DescribeYourself(models.Model):
    "to save personality desc text submitted by user"  
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    selftext = models.TextField(max_length=2000)
    date_created = models.DateField(auto_now_add=True)          
    class Meta:
        verbose_name_plural = "DescribeYourself"
    def __unicode__(self):
          return self.name    

class ApplicantStatus(models.Model):
    "to save data regarding profile completeness, check status by admin and assigned applicant ID"       
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    registeredon = models.DateField(null=True)
    profilepercent = models.CharField(max_length=100, default='1%') 
    checkedbyadmin = models.CharField(max_length=50, default='No')
    checkedondate = models.DateField(null=True)
    applicantid = models.CharField(max_length=200, null=True)
    class Meta:
        verbose_name_plural = "ApplicantStatus"
    def __unicode__(self):
          return self.name    

class Messages(models.Model):
    "to save messages that can be seen by the user in his/her profile."
    email = models.EmailField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=2000)
    messagedate = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Messages"
    def __unicode__(self):
          return self.name    


from vipapi.signals import addnewapplicant 
def ready(self):
    import vipapi.signals 

@receiver(post_delete, sender=PhotoPortfolio)
def submission_delete(sender, instance, **kwargs):
    "to remove photo from the media folder when user account has been deleted by the admin"
    instance.facephoto.delete(False)
    instance.standingposephoto.delete(False)
    instance.sideposephoto.delete(False)
    instance.stylishposephoto.delete(False)           

          

              


