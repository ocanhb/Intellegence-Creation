from django.urls import path, include
from . import views 
from .views import (
    terima_creation_entry,
    CreationEntryView,
    ModelEntryListAPIView,
    DatasetRequestAPI,
    DatasetSentListAPIView,
    ProjectManagementAPI,
    SystemImplementationAPI,
    integrasi_view, 
    download_view
)
from rest_framework.routers import DefaultRouter
from .views import ToExperienceViewSet

# Router untuk ViewSet
router = DefaultRouter()
router.register(r'engineering', ToExperienceViewSet, basename='engineering')

urlpatterns = [
    # Halaman frontend
    path('index/', views.index_view, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('modeling/', views.modeling_view, name='modeling'),
    path('creation/', views.creation_entry, name='creation_entry'),
    path('creation/api/', views.creation_entry_api, name='creation_entry_api'),
    path('integrasi/', views.integrasi_view, name='integrasi'),

    # APIView / Function-based view
    path('api/get_all_models/', views.modeling_api_view, name='get_all_models'),
    path('api/creation_entries/', terima_creation_entry, name='terima_creation_entry'),
    path('api/delete_model/<int:model_id>/', views.delete_model_entry, name='delete_model_entry'),
    path('api/model_entries/', ModelEntryListAPIView.as_view(), name='model-entry-list'),
    path('api/dataset-request/', DatasetRequestAPI.as_view(), name='dataset-request-api'),
    path('api/dataset-response/', DatasetSentListAPIView.as_view(), name='dataset-response-api'),
    path('api/Project-Management/', ProjectManagementAPI.as_view(), name='project-models-api'),
    path('api/System-Implementation/', SystemImplementationAPI.as_view(), name='system-implementation-api'),

    # Gunakan router di sini
    path('api/', include(router.urls)),
    path('integrasi/', integrasi_view, name='integrasi'),
    path('download/<path:path>', download_view, name='download'),
    
    path('problem-framing/', views.problem_framing_page, name='problem_framing'),
    path('problem-framing-form/', views.problem_framing_form, name='problem_framing_form'),
    path('problem-framing-form/<int:pk>/edit/', views.problem_framing_form, name='problem_framing_edit'),
    # API Endpoints
    path('api/problem-framing/', views.api_problem_framing_list),
    path('api/problem-framing/<int:pk>/', views.api_problem_framing_delete),

    path('submit-system-implementation/', views.submit_System_Implementation, name='submit_System_Implementation'),
    path('submit-dataset-request/', views.submit_dataset_request, name='submit_dataset_request'),
    path('submit-project-management/', views.submit_Project_Management, name='submit_Project_Management'),

    path('integrasi/form-request/', views.submit_dataset_request, name='form_dataset_request'),
    path('integrasi/form-project/', views.submit_Project_Management, name='form_project_management'),
    path('integrasi/form-implement/', views.submit_System_Implementation, name='form_system_implementation'),

    path('api/laporan-integrasi-json/', views.laporan_integrasi_json, name='laporan_integrasi_json'),
    path('api/submit-system-implementation/', views.api_list_system_implementation, name='api_submit_final_model'),
    path('api/dataset-request/', views.api_list_dataset_request, name='api_dataset_request'),
    path('api/project-management/', views.api_list_project_management, name='api_project_management'),
    path('api/dataset-response/', views.api_list_dataset_response, name='api_list_dataset_response'),
    path('api/engineering-data/', views.api_list_engineering_data, name='api_list_engineering_data'),

]

