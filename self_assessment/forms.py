from django import forms

LEVELS = ((-1, '— Select your level —'),
          (0, 'None'),
          (1, 'Basic'),
          (2, 'Middle'),
          (3, 'Professional'),
          (4, 'Expert')
          )


class MainForm(forms.Form):
    field = forms.ChoiceField(choices=LEVELS, required=True)

    def __init__(self, label, _class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = label
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = _class
