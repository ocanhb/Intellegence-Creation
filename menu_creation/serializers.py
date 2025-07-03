# serializers.py
from rest_framework import serializers
from .models import ModelEntry, ToExperience, DatasetRequest, DatasetSent, ProjectManagement, SystemImplementation


class ModelEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelEntry
        fields = '__all__'

class ToExperienceSerializer(serializers.ModelSerializer):
    meaningful_path = serializers.SerializerMethodField()
    experience_path = serializers.SerializerMethodField()
    implementasi_path = serializers.SerializerMethodField()
    batasan_path = serializers.SerializerMethodField()
    perencanaan_path = serializers.SerializerMethodField()

    class Meta:
        model = ToExperience
        fields = [
            'id', 'namaProjek',
            'meaningful_path', 'experience_path',
            'implementasi_path', 'batasan_path', 'perencanaan_path'
        ]

    def get_meaningful_path(self, obj):
        request = self.context.get('request')
        if request and obj.meaningful:
            return request.build_absolute_uri(obj.meaningful.url)
        return None

    def get_experience_path(self, obj):
        request = self.context.get('request')
        if request and obj.experience:
            return request.build_absolute_uri(obj.experience.url)
        return None

    def get_implementasi_path(self, obj):
        request = self.context.get('request')
        if request and obj.implementasi:
            return request.build_absolute_uri(obj.implementasi.url)
        return None

    def get_batasan_path(self, obj):
        request = self.context.get('request')
        if request and obj.batasan:
            return request.build_absolute_uri(obj.batasan.url)
        return None

    def get_perencanaan_path(self, obj):
        request = self.context.get('request')
        if request and obj.perencanaan:
            return request.build_absolute_uri(obj.perencanaan.url)
        return None

class DatasetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetRequest
        fields = '__all__'


class DatasetSentSerializer(serializers.ModelSerializer):
    data_file_path = serializers.SerializerMethodField()

    class Meta:
        model = DatasetSent
        fields = [
            'id', 'sender_name', 'nama_model', 'kebutuhan',
            'dataset_name', 'dataset_description', 'dataset_status',
            'data_file', 'status_pilihan',
            'data_file_path'
        ]

    def get_data_file_path(self, obj):
        request = self.context.get('request')
        if request and obj.data_file:
            return request.build_absolute_uri(obj.data_file.url)
        return None


class ProjectManagementSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        request = self.context.get('request')
        if request and obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None

    class Meta:
        model = ProjectManagement  # Ganti kalau nama model berbeda
        fields = '__all__'


class SystemImplementationSerializer(serializers.ModelSerializer):
    laporan_model = serializers.SerializerMethodField()

    def get_laporan_model(self, obj):
        request = self.context.get('request')
        if request and obj.laporan_model:
            return request.build_absolute_uri(obj.laporan_model.url)
        return None

    class Meta:
        model = SystemImplementation  # Ganti kalau nama model berbeda
        fields = '__all__'

from rest_framework import serializers
from .models import ProblemFraming

class ProblemFramingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemFraming
        fields = '__all__'
