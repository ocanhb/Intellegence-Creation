from django.shortcuts import render, redirect
from .forms import CreationEntryForm , ProjectManagementForm,SystemImplementationForm,DatasetRequestForm
from .models import CreationEntry, ModelEntry, ModelActivity, ToExperience, ProjectManagement,SystemImplementation,DatasetRequest,DatasetSent
import requests
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from collections import Counter
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ModelEntry, DatasetRequest, ProjectManagement, SystemImplementation
from .serializers import ModelEntrySerializer, DatasetRequestSerializer,DatasetSentSerializer,ToExperienceSerializer, ProjectManagementSerializer, SystemImplementationSerializer
from rest_framework.generics import ListAPIView
from urllib.parse import urljoin
from rest_framework.reverse import reverse



 # atau pakai IP kalau beda mesin

def build_absolute_file_url(field_value):
    if field_value:
        if hasattr(field_value, 'url'):
            return urljoin(BASE_FILE_URL, field_value.url)
        elif isinstance(field_value, str) and not field_value.startswith('http'):
            return urljoin(BASE_FILE_URL, field_value)
        else:
            return field_value
    return ''


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import ModelEntry
from rest_framework import viewsets
from .serializers import ModelEntrySerializer

class CreationEntryView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = ModelEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Berhasil disimpan'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ModelEntryListAPIView(APIView):
    def get(self, request):
        entries = ModelEntry.objects.all()
        serializer = ModelEntrySerializer(entries, many=True)
        return Response(serializer.data)

class ToExperienceViewSet(viewsets.ModelViewSet):
    queryset = ToExperience.objects.all()
    serializer_class = ToExperienceSerializer

class DatasetRequestAPI(ListAPIView):
    queryset = DatasetRequest.objects.all()
    serializer_class = DatasetRequestSerializer


class DatasetSentListAPIView(APIView):
    def get(self, request):
        data = DatasetSent.objects.all()
        serializer = DatasetSentSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)

class ProjectManagementAPI(ListAPIView):
    queryset = ProjectManagement.objects.all()
    serializer_class = ProjectManagementSerializer

class SystemImplementationAPI(ListAPIView):
    queryset = SystemImplementation.objects.all()
    serializer_class = SystemImplementationSerializer


def index_view(request):
    return render(request, 'index.html')

def dashboard_view(request):
    activities = ModelEntry.objects.order_by('-created_at')[:5]
    status_list = ModelEntry.objects.values_list('status', flat=True)
    count = dict(Counter(status_list))
    status_data = {
        'success': count.get('success', 0),
        'Failed': count.get('Failed', 0),
        'ongoing': count.get('ongoing', 0)
    }
    print("STATUS_DATA:", status_data)  # Debug print

    context = {
        'activities': activities,
        'status_data': status_data
    }
    return render(request, 'dashboard.html', context)

def modeling_view(request):
    models = ModelEntry.objects.all().order_by('-id')
    data = [
        {
            "id": idx + 1,
            "title": m.title,
            "target": m.target,
            "accuracy": m.accuracy,
            "status": m.status,
            "from": "Dataset Upload",
            "features": m.features,
            "jenis": "Numerical",  # bisa kamu sesuaikan kalau ada field aslinya
            "category": m.category,
            "input": m.input,
            "process": m.process,
            "output": m.output,
            "algorithm": m.algorithm,
            "start": m.start.strftime("%Y-%m-%d") if m.start else '',
            "end": m.end.strftime("%Y-%m-%d") if m.end else '',
            "deployment": "no",  # bisa disesuaikan jika kamu punya field ini
            "activity": m.activity,
        }
        for idx, m in enumerate(models)
    ]
    return render(request, 'modeling.html', {'entries_json': data})

@require_http_methods(["DELETE"])
@csrf_exempt
def delete_model_entry(request, model_id):
    try:
        model = ModelEntry.objects.get(id=model_id)
        model.delete()
        return JsonResponse({'status': 'success'})
    except ModelEntry.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Model tidak ditemukan'}, status=404)

def modeling_api_view(request):
    models = ModelEntry.objects.all().order_by('-id')
    data = [m.to_dict() for m in models]
    return JsonResponse(data, safe=False)


@csrf_exempt
def creation_entry_api(request):
    if request.method == 'POST':
        try:
            start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()

            model = ModelEntry.objects.create(
                title=request.POST.get('problem_name'),
                features=request.POST.get('features'),
                target=request.POST.get('output'),
                category=request.POST.get('dataset_type'),
                accuracy=request.POST.get('accuracy') or '0%',
                status=request.POST.get('training_status'),
                input=request.POST.get('features'),
                process=request.POST.get('refining_strategy'),
                output=request.POST.get('output'),
                algorithm = request.POST.get('algorithm'),
                activity=request.POST.get('data_activity'),
                start=start_date,
                end=end_date
            )
            return JsonResponse({'status': 'success', 'data': model.to_dict()})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})

def creation_entry(request):
    if request.method == 'POST':
        entry = CreationEntry(
            problem_name = request.POST.get('problem_name'),
            features = request.POST.get('features'),
            output = request.POST.get('output'),
            objective = request.POST.get('objective'),
            dataset_type = request.POST.get('dataset_type'),
            training_status = request.POST.get('training_status'),
            accuracy = request.POST.get('accuracy'),
            refining_strategy = request.POST.get('refining_strategy'),
            refining_status = request.POST.get('refining_status'),
            data_activity = request.POST.get('data_activity'),
            start_date = request.POST.get('start_date'),
            end_date = request.POST.get('end_date'),
            upload_csv = request.FILES.get('upload_csv')
        )
        entry.save()
        return redirect('modeling')  # redirect ke halaman modeling setelah submit
    return render(request, 'creation_entry.html')



#import requests
#from django.shortcuts import render

#def fetch_data(endpoint):
 #   base_url = "http://192.168.0.108:8000/"  # Ganti sesuai IP server
   # try:
    #    response = requests.get(f"{base_url}{endpoint}")
     #   if response.status_code == 200:
      #      return response.json()
       # else:
         #   return []
    #except requests.exceptions.RequestEx3ception:
     #   return []



from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import ModelEntry
from .serializers import ModelEntrySerializer
import traceback


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def terima_creation_entry(request):
    try:
        print("DATA MASUK:", request.data)
        serializer = ModelEntrySerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                "success": True,
                "message": "Data berhasil disimpan.",
                "data": ModelEntrySerializer(instance).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(traceback.format_exc())
        return Response({
            "success": False,
            "message": f"Terjadi kesalahan: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import os
import requests
from urllib.parse import urlparse

from django.shortcuts import render
from django.http import FileResponse, Http404
from django.conf import settings

from urllib.parse import urlparse

def extract_path_from_url(field_value):
    try:
        # Jika field adalah FieldFile
        if hasattr(field_value, 'url'):
            return field_value.url
        # Jika string tapi bukan full URL
        elif isinstance(field_value, str) and not field_value.startswith('http'):
            return f'/media/{field_value.lstrip("/")}'
        # Jika sudah URL penuh
        elif isinstance(field_value, str):
            return field_value
    except:
        pass
    return ''



def integrasi_view(request):
    data = {
        "toexperience": ToExperience.objects.all().order_by('-id'),
        "dataset_request": DatasetRequest.objects.all().order_by('-id'),
        "dataset_response": DatasetSent.objects.all().order_by('-id'),
        "project_models": ProjectManagement.objects.all().order_by('-id'),
        "final_models": SystemImplementation.objects.all().order_by('-id'),
    }

    for d in data.get('system_implementation', []):
        d.laporan_model_path = extract_path_from_url(d.laporan_model)

    for d in data.get('dataset_response', []):
        d.data_file_path = extract_path_from_url(d.data_file)

    for d in data.get('project_models', []):
        d.file_path = extract_path_from_url(d.file)

    for d in data.get('toexperience', []):
        d.meaningful_path = extract_path_from_url(d.meaningful)
        d.experience_path = extract_path_from_url(d.experience)
        d.implementasi_path = extract_path_from_url(d.implementasi)
        d.batasan_path = extract_path_from_url(d.batasan)
        d.perencanaan_path = extract_path_from_url(d.perencanaan)

    return render(request, 'integrasi.html', data | {
        'MEDIA_URL_ABS': 'https://ocanhb.pythonanywhere.com/media/'
    })


# 🧾 DOWNLOAD VIEW
def download_view(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    raise Http404("File tidak ditemukan")

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ProblemFraming
from .forms import ProblemFramingForm
import json

def problem_framing_page(request):
    return render(request, 'problem_framing.html')

def problem_framing_form(request, pk=None):
    if pk:
        instance = get_object_or_404(ProblemFraming, pk=pk)
    else:
        instance = None

    if request.method == 'POST':
        form = ProblemFramingForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('problem_framing')
    else:
        form = ProblemFramingForm(instance=instance)

    return render(request, 'problem_framing_form.html', {'form': form})

# API untuk mengambil data JSON
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ProblemFraming
from .serializers import ProblemFramingSerializer

@api_view(['GET'])
def api_problem_framing_list(request):
    items = ProblemFraming.objects.all()
    serializer = ProblemFramingSerializer(items, many=True)
    return Response(serializer.data)


@csrf_exempt
def api_problem_framing_delete(request, pk):
    if request.method == 'DELETE':
        obj = get_object_or_404(ProblemFraming, pk=pk)
        obj.delete()
        return JsonResponse({'message': 'deleted'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import requests
import traceback  # Tambahan

from django.shortcuts import render, redirect
import os, requests
from .forms import SystemImplementationForm

def submit_System_Implementation(request):
    if request.method == 'POST':
        form = SystemImplementationForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()

            data = {
                "no": instance.no,
                "nama_model": instance.nama_model,
                "status_project": instance.status_project,
                "dokumentasi_model": instance.dokumentasi_model,
            }

            files = {}
            if instance.laporan_model:
                laporan_path = instance.laporan_model.path
                laporan_nama = os.path.basename(laporan_path)

                try:
                    with open(laporan_path, "rb") as file:
                        files["laporan_model"] = (laporan_nama, file, "application/pdf")

                        response = requests.post(
                            "http://192.168.0.115:8000/api/terima-model/",
                            data=data,
                            files=files,
                            timeout=10
                        )

                        if response.status_code == 201:
                            print("✅ Berhasil dikirim ke teman.")
                        else:
                            print("⚠️ Gagal kirim:", response.status_code, response.text)

                except requests.exceptions.RequestException as e:
                    print("❌ Error koneksi:", str(e))

            return redirect('integrasi')

        else:
            # ❗ KEMBALIKAN form dgn error
            print("❌ Form tidak valid:", form.errors)
            return render(request, 'form_system_implementation.html', {
                'System_Implementation_form': form
            })

    else:
        form = SystemImplementationForm()

    return render(request, 'form_system_implementation.html', {
        'System_Implementation_form': form
    })

from django.utils.dateparse import parse_datetime
from django.utils import timezone
from .forms import DatasetRequestForm
import requests, json


def submit_dataset_request(request):
    if request.method == 'POST':
        form = DatasetRequestForm(request.POST)
        if form.is_valid():
            instance = form.save()

            data = {
                "nama_model": instance.nama_model,
                "kebutuhan": instance.kebutuhan,
                "deskripsi": instance.deskripsi,
                "timestamp": instance.timestamp.isoformat()
            }

            try:
                response = requests.post(
                    "http://192.168.0.115/api/dataset-request/",
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )

                if response.status_code == 201:
                    print("✅ Dataset juga dikirim ke teman.")
                else:
                    print("⚠️ Gagal kirim:", response.status_code, response.text)

            except requests.exceptions.RequestException as e:
                print("❌ Error koneksi:", str(e))

            return redirect('integrasi')

    else:
        form = DatasetRequestForm()

    return render(request, 'form_dataset_request.html', {
        'Dataset_Request_form': form
    })

from .forms import ProjectManagementForm


def submit_Project_Management(request):
    if request.method == 'POST':
        form = ProjectManagementForm(request.POST)
        if form.is_valid():
            instance = form.save()

            data = {
                "nama_kelompok": instance.nama_kelompok,
                "status_model": instance.status_model,
                "deskripsi_model": instance.deskripsi_model,
            }

            try:
                response = requests.post(
                    "https://nzurulhaqii.pythonanywhere.com/api/project-management/",
                    data=data,
                    timeout=5
                )

                if response.status_code == 201:
                    print("✅ Project juga dikirim ke teman.")
                else:
                    print("⚠️ Gagal kirim:", response.status_code, response.text)

            except requests.exceptions.RequestException as e:
                print("❌ Error koneksi:", str(e))

            return redirect('integrasi')

    else:
        form = ProjectManagementForm()

    return render(request, 'form_project_management.html', {
        'Project_Management_form': form
    })

from .models import SystemImplementation, DatasetRequest, ProjectManagement


@api_view(['GET'])
def api_list_system_implementation(request):
    data = SystemImplementation.objects.all().order_by('-id')
    serializer = SystemImplementationSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_list_dataset_request(request):
    data = DatasetRequest.objects.all().order_by('-timestamp')
    serializer = DatasetRequestSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_list_project_management(request):
    data = ProjectManagement.objects.all().order_by('-id')
    serializer = ProjectManagementSerializer(data, many=True)
    return Response(serializer.data)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DatasetRequest, ProjectManagement, SystemImplementation, DatasetSent, ToExperience
from .serializers import DatasetRequestSerializer, ProjectManagementSerializer, SystemImplementationSerializer, DatasetSentSerializer, ToExperienceSerializer

@api_view(['GET'])
def laporan_integrasi_json(request):
    return Response({
        "dataset_requests": DatasetRequestSerializer(DatasetRequest.objects.all(), many=True, context={"request": request}).data,
        "project_management": ProjectManagementSerializer(ProjectManagement.objects.all(), many=True, context={"request": request}).data,
        "system_implementation": SystemImplementationSerializer(SystemImplementation.objects.all(), many=True, context={"request": request}).data,
        "dataset_responses": DatasetSentSerializer(DatasetSent.objects.all(), many=True, context={"request": request}).data,
        "toexperience": ToExperienceSerializer(ToExperience.objects.all(), many=True, context={"request": request}).data,
    })

@api_view(['GET'])
def api_list_dataset_response(request):
    data = DatasetSent.objects.all().order_by('-id')
    serializer = DatasetSentSerializer(data, many=True, context={"request": request})
    return Response(serializer.data)

@api_view(['GET'])
def api_list_engineering_data(request):
    data = ToExperience.objects.all().order_by('-id')
    serializer = ToExperienceSerializer(data, many=True, context={"request": request})
    return Response(serializer.data)

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import DatasetSent
from .serializers import DatasetSentSerializer  # INI WAJIB ADA
import traceback

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])  # <--- INI WAJIB
def terima_dataset_api(request):
    try:
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"success": False, "message": "File CSV tidak ditemukan."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        final_data = {
            "sender_name": data.get("sender_name", "Anonim"),
            "nama_model": data.get("nama_model"),
            "kebutuhan": data.get("kebutuhan"),
            "dataset_name": data.get("name"),
            "dataset_description": data.get("description"),
            "dataset_status": data.get("status"),
            "data_file": uploaded_file,
            "status_pilihan": "Sudah Dipilih",
        }

        serializer = DatasetSentSerializer(data=final_data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({
                "success": True,
                "message": "Dataset berhasil diterima.",
                "data": DatasetSentSerializer(instance).data
            }, status=status.HTTP_201_CREATED)


        print("ERROR SERIALIZER:", serializer.errors)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(traceback.format_exc())
        return Response({
            "success": False,
            "message": f"Terjadi kesalahan: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.shortcuts import get_object_or_404, redirect
from .models import (
    ToExperience,
    DatasetRequest,
    DatasetSent,
    ProjectManagement,
    SystemImplementation
)

def delete_toexperience(request, id):
    obj = get_object_or_404(ToExperience, id=id)
    obj.delete()
    return redirect('integrasi')

def delete_request_dataset(request, id):
    obj = get_object_or_404(DatasetRequest, id=id)
    obj.delete()
    return redirect('integrasi')

def delete_response_dataset(request, id):
    obj = get_object_or_404(DatasetSent, id=id)
    obj.delete()
    return redirect('integrasi')

def delete_project_management(request, id):
    obj = get_object_or_404(ProjectManagement, id=id)
    obj.delete()
    return redirect('integrasi')

def delete_system_implementation(request, id):
    obj = get_object_or_404(SystemImplementation, id=id)
    obj.delete()
    return redirect('integrasi')
