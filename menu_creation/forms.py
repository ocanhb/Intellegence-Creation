from django import forms
from .models import CreationEntry, ProblemFraming, ProjectManagement, SystemImplementation, DatasetRequest

class CreationEntryForm(forms.ModelForm):
    class Meta:
        model = CreationEntry
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'problem_name': forms.TextInput(attrs={'placeholder': 'Contoh: Prediksi Harga Rumah'}),
            'features': forms.TextInput(attrs={'placeholder': 'Contoh: Luas, Lokasi'}),
            'output': forms.TextInput(attrs={'placeholder': 'Contoh: Harga Rumah'}),
            'objective': forms.Textarea(attrs={'placeholder': 'Contoh: Prediksi harga rumah berdasarkan luas dan lokasi'}),
            'accuracy': forms.TextInput(attrs={'placeholder': 'Contoh: 92.5%'}),
            'refining_strategy': forms.TextInput(attrs={'placeholder': 'Contoh: Feature Tuning'}),
            'data_activity': forms.Textarea(attrs={'placeholder': 'Deskripsikan aktivitas pemrosesan data...'}),
        }

class ProblemFramingForm(forms.ModelForm):
    class Meta:
        model = ProblemFraming
        fields = '__all__'



class ProjectManagementForm(forms.ModelForm):
    class Meta:
        model = ProjectManagement
        fields = ['nama_kelompok', 'status_model', 'deskripsi_model']
        widgets = {
            'nama_kelompok': forms.TextInput(attrs={
                'placeholder': 'Nama Kelompok',
                'class': 'form-control'
            }),
            'status_model': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Status Model',
                'class': 'form-control'
            }),
            'deskripsi_model': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Deskripsi Model',
                'class': 'form-control'
            }),
        }



class SystemImplementationForm(forms.ModelForm):
    class Meta:
        model = SystemImplementation
        fields = ['no', 'nama_model', 'status_project', 'dokumentasi_model', 'laporan_model']
# 

class DatasetRequestForm(forms.ModelForm):
    class Meta:
        model = DatasetRequest
        fields = [ 'nama_model', 'kebutuhan', 'deskripsi']
        widgets = {
            'nama_model': forms.TextInput(attrs={'placeholder': 'Nama Model'}),
            'kebutuhan': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Kebutuhan dataset'}),
            'deskripsi': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Deskripsi kebutuhan'}),
        }