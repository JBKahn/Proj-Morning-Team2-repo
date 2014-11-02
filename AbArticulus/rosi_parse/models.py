from django.db import models

class Account(models.Model):
	student_num = models.CharField(max_length=9)
	password = models.CharField(max_length=200)
	user = models.ForeignKey('authentication.CustomUser')

	def save(self, *args, **kwargs):
		if self.student_num < 0 or self.student_num > 9:
			raise ValueError("student numbers must be 9 characters")
		super(Account, self).save(*args, **kwargs)
