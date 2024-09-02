from django import forms
from .models import UploadedFile

class UploadTTLForm(forms.Form):
    ttl_file = forms.FileField(label="Upload Turtle (.ttl) File")

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('name', 'graph_id', 'size', 'file')
