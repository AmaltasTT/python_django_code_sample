from vipapi.models import RegisterVIP, ApplicantStatus
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.core.mail import EmailMessage

@receiver(post_save, sender=RegisterVIP)
def addnewapplicant(sender, **kwargs):
    "whenever new user is registered, some info is also saved into ApplicantStatus table so that admin can manage new registrants."
    print("signal - addnewapplicant is fired")
    if kwargs['created']:
        email = kwargs['instance'].email
        name = kwargs['instance'].name
        p1 = ApplicantStatus(email=email, name=name, registeredon=datetime.date.today())
        p1.save()
        subject = 'VIPNAMES - Registration'
        message = '<p><b>Hi '+name+',</b><br>We thank you for registrating for VIPNAMES contest.Please login to your account and complete your profile.<br><br>With warm regards,<br><b>VIPNAMES Select Community</b></p>'
        msg = EmailMessage(subject, message, to=[email], from_email='vipnamesmohali@gmail.com')
        msg.content_subtype = 'html'
        msg.send()
        
       