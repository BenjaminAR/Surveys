# widgets.py
from django import forms

class RangeSliderWidget(forms.Widget):
    def __init__(self, attrs=None, choices=()):
        self.choices = choices
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        input_form = f'<input type="hidden" id="{name}" >'
        output = [ input_form + '\n' +'<div class="range-container">']
        for choice in self.choices:
            output.append(
                f'<label class="range-marker-{name}" nv-val="{choice[0]}" for="{name}">'
                f'{choice[1]}</label>'
            )
        output.append('</div>')
        return '\n'.join(output)
'''

class RangeSliderWidget(forms.Widget):
    template_name = '../sx_widget/range_slider.html'

    def __init__(self, attrs=None, choices=()):
        self.choices = choices
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['choices'] = self.choices
        context['widget']['id'] = attrs['id']  # Utiliza el ID del campo
        return context

'''