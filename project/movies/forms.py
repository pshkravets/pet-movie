from django import forms


class SearchMovieForm(forms.Form):
    search_field = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Film name',
            'aria-label': 'Film name',
            'aria-describedby': 'button-addon2',

        }
    ))
