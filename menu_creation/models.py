from django.db import models
from datetime import date, datetime



class ProblemFraming(models.Model):
    problem_name = models.CharField(max_length=255)
    problem_statement = models.TextField()
    input_features = models.TextField()
    planned_process = models.TextField()
    expected_output = models.CharField(max_length=255)
    dataset_needed = models.TextField()

    def __str__(self):
        return self.problem_name

class ModelActivity(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('On Going', 'On Going')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class CreationEntry(models.Model):
    problem_name = models.CharField(max_length=255)
    features = models.TextField()
    output = models.CharField(max_length=255)
    objective = models.TextField()

    dataset_type = models.CharField(max_length=50, choices=[
        ('regresi', 'Regresi'),
        ('klasifikasi', 'Klasifikasi'),
        ('forecasting', 'Forecasting'),
    ])

    training_status = models.CharField(max_length=50, choices=[
        ('belum', 'Belum Dilatih'),
        ('proses', 'Proses'),
        ('sudah', 'Sudah Dilatih'),
    ])

    accuracy = models.CharField(max_length=50, blank=True, null=True)
    refining_strategy = models.CharField(max_length=255, blank=True, null=True)

    refining_status = models.CharField(max_length=50, choices=[
        ('belum', 'Belum'),
        ('proses', 'Proses'),
        ('sudah', 'Sudah'),
    ])

    data_activity = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    upload_csv = models.FileField(upload_to='uploads/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.problem_name

class History(models.Model):
    title = models.CharField(max_length=200)
    from_field = models.CharField(max_length=200)
    target = models.CharField(max_length=100)
    features = models.TextField()
    jenis_data = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    accuracy = models.CharField(max_length=20)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    deployment = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ToExperience(models.Model):
    namaProjek = models.CharField(max_length=100)
    meaningful = models.FileField(upload_to='laporan/')
    experience = models.FileField(upload_to='laporan/')
    implementasi = models.FileField(upload_to='laporan/')
    batasan = models.FileField(upload_to='laporan/')
    perencanaan = models.FileField(upload_to='laporan/')

    def __str__(self):
        return self.namaProjek

class DatasetRequest(models.Model):
    nama_model = models.CharField(max_length=100)
    kebutuhan = models.TextField()
    deskripsi = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class DatasetSent(models.Model):
    sender_name = models.CharField(max_length=100, default="Anonim")
    nama_model = models.CharField(max_length=100)
    kebutuhan = models.CharField(max_length=255)

    dataset_name = models.CharField(max_length=255)
    dataset_description = models.TextField(blank=True, null=True)
    dataset_status = models.CharField(max_length=50)

    data_file = models.FileField(upload_to='uploads/', null=True, blank=True)

    status_pilihan = models.CharField(max_length=50, default="Sudah Dipilih")

    def __str__(self):
        return f"{self.dataset_name} oleh {self.sender_name}"

class ProjectManagement(models.Model):
    nama_kelompok = models.CharField(max_length=100)
    nama_model = models.CharField(max_length=100, default="default_model")
    status_model = models.CharField(max_length=100)
    deskripsi_model = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='uploaded_files/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_model


class SystemImplementation(models.Model):
    no = models.IntegerField()
    nama_model = models.CharField(max_length=100, default="default_model")
    status_project = models.CharField(max_length=50)

    # Dulu: final_model = models.CharField(max_length=100)
    dokumentasi_model = models.URLField(help_text="Link ke Google Colab")

    # Dulu: dokumentasi_link = models.URLField()
    laporan_model = models.FileField(upload_to='laporan/', null=True, blank=True, help_text="Upload PDF laporan model")

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama_model} - {self.status_project}"

class ModelEntry(models.Model):
    title = models.CharField(max_length=200)
    features = models.TextField(blank=True, null=True)

    target = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    accuracy = models.CharField(max_length=20)
    status = models.CharField(max_length=100)
    input = models.TextField()
    process = models.TextField()
    output = models.CharField(max_length=100)
    algorithm = models.TextField()
    activity = models.TextField()
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "features": self.features,
            "target": self.target,
            "category": self.category,
            "accuracy": self.accuracy,
            "status": self.status,
            "input": self.input,
            "process": self.process,
            "output": self.output,
            "algorithm": self.algorithm,
            "activity": self.activity,
            "start": self.start.strftime('%Y-%m-%d') if self.start else '',
            "end": self.end.strftime('%Y-%m-%d') if self.end else '',
            "from": "Dataset Upload",
            "jenis": "Numerical",  # ubah sesuai kebutuhan
            "deployment": "no"     # default sementara
        }
