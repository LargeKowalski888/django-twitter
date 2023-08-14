from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#Create post sharing model to share your posts with other users
class Meep(models.Model):
	user = models.ForeignKey(
		User, related_name="meeps",
		on_delete=models.DO_NOTHING
		)
	body = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(User, related_name="meep_like", blank=True)

	#Keep track of the number of likes
	def number_of_likes(self):
		return self.likes.count()


	def __str__(self):
		return(
			f"{self.user} "
			f"({self.created_at:%Y-%m-%d %H:%M}): "
			f"{self.body}..."
		)

#from django.dispatch import receiver

#Create a User profile model. CASCADE means delete whole profile after deleting a user.
#OneToOneField allows 1 profile for 1 user. ManyToManyField allows multiple followers for 1 user.
#When you look up a follow, you reference follow by to see who you are followed by. Symmetrical allows you to follow someone without having them follow you back. Blank means you don't have to follow anyone.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank = True)

	date_modified = models.DateTimeField(User, auto_now=True)
	profile_image = models.ImageField(null=True, blank=True, upload_to="images/")

	profile_bio = models.CharField(null=True, blank=True, max_length=500)
	homepage_link = models.CharField(null=True, blank=True, max_length=100)
	facebook_link = models.CharField(null=True, blank=True, max_length=100)
	instagram_link = models.CharField(null=True, blank=True, max_length=100)
	linkedin_link = models.CharField(null=True, blank=True, max_length=100)

#Returns the username of the profile
	def __str__(self):
		return self.user.username

#Create profile when new user signs up
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()
		#Have the user follow themselves
		user_profile.follows.set([instance.profile.id])
		user_profile.save()

#Connects our signal 		@receiver(post_save, sender=User)
post_save.connect(create_profile, sender=User)
