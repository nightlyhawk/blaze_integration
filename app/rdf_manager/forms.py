from django import forms

class UploadTTLForm(forms.Form):
    ttl_file = forms.FileField(label="Upload Turtle (.ttl) File")