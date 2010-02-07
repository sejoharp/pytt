from google.appengine.ext.db import djangoforms
from model.models import Property

class TimeForm(djangoforms.ModelForm):
    class Meta:
        model = Property
        exclude = ["userid"]

class PropertyForm(djangoforms.ModelForm):
    class Meta:
        model = Property
        exclude = ["email"]
