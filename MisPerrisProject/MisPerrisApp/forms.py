from django import forms

from .models import Mascota, SolicitudContacto


class SolicitudContactoForm(forms.ModelForm):
    MASCOTAS = [
        ('', 'Selecciona un perrito'),
        ('Luna', 'Luna'),
        ('Max', 'Max'),
        ('Mora', 'Mora'),
    ]

    mascota_interes = forms.ChoiceField(
        choices=MASCOTAS,
        required=False,
        label='Perrito que te interesa',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tipo = self.data.get(
            self.add_prefix('tipo'),
            self.initial.get('tipo', 'adopcion'),
        )
        self.fields['mascota_interes'].required = tipo == 'adopcion'

    class Meta:
        model = SolicitudContacto
        fields = [
            'nombre',
            'email',
            'telefono',
            'tipo',
            'mascota_interes',
            'mensaje',
        ]
        widgets = {
            'tipo': forms.HiddenInput(),
            'mensaje': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'nombre': 'Nombre completo',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono (opcional)',
            'mensaje': 'Cuéntanos un poco más',
        }


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre']
        labels = {'nombre': 'Nombre de la mascota'}
        widgets = {'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Coco'})}
