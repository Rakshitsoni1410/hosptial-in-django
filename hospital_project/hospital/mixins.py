class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            w = field.widget.__class__.__name__
            if w in ('TextInput','EmailInput','PasswordInput','NumberInput','DateInput','TimeInput'):
                field.widget.attrs['class'] = 'form-control'
            elif w == 'Textarea':
                field.widget.attrs['class'] = 'form-control'
            elif w == 'Select':
                field.widget.attrs['class'] = 'form-select'