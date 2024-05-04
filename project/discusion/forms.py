from django import forms

class Comments(forms.Form):
    comment = forms.CharField(max_length=200, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'id': 'exampleFormControlTextarea1',
            'rows': '3',
        }
    ))