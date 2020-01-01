"""
monitoring URL Configuration. Included as root ''
"""
from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView, DetailView

from . import views
from . import jsonviews
from . import dashboard
from . import models

app_name = 'monitoring'

urlpatterns = [

    # misc
    # path('',TemplateView.as_view(template_name='index.html')),
    path('helloworld', TemplateView.as_view(template_name='modular_template/helloworld.html')),
    path('contact/', views.ContactTableView.as_view()),
    path('project/', views.ProjectTableView.as_view()),
    path('subproject/', views.SubProjectTableView.as_view()),
    path('contact/<int:pk>/', views.ContactDetailView.as_view(), name='contact'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project'),
    path('subproject/<int:pk>/', views.SubProjectDetailView.as_view(), name='subproject'),
    path('city/<int:pk>/', DetailView.as_view(model=models.City), name='city_id'),
    path('city/<str:name>/', views.CityDetailView.as_view(), name='city_name'),
    path('city/<str:name>/<str:country_id>/', views.CityDetailView.as_view(), name='city_country'),

    # dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('graphic/proyecto/', dashboard.get_proyecto, name='graphic-proyecto'),
    path('graphic/cantidad-paises/', dashboard.cantidad_paises, name='cantidad-paises'),
    path('graphic/cantidad-proyectos/', dashboard.cantidad_proyectos, name='cantidad-proyectos'),
    path('graphic/cantidad-subproyectos/', dashboard.cantidad_subproyectos,
         name='cantidad-subproyectos'),
    path('graphic/cantidad-participantes/',
         dashboard.cantidad_participantes, name='cantidad-participantes'),
    path('graphic/rubros/', dashboard.get_rubros, name='graphic-rubros'),
    path('graphic/grafico-organizaciones/', dashboard.grafico_organizaciones,
         name='grafico-organizaciones'),
    path('graphic/proyectos-metas/', dashboard.proyectos_metas, name='proyectos-metas'),
    path('graphic/grafico-anio-fiscal/', dashboard.grafico_anio_fiscal, name='grafico-anio-fiscal'),
    path('graphic/grafico-edad/', dashboard.grafico_edad, name='grafico-edad'),
    path('graphic/grafico-educacion/', dashboard.grafico_educacion, name='grafico-educacion'),
    path('graphic/grafico-tipo-participante/', dashboard.grafico_tipo_participante,
         name='grafico-tipo-participante'),
    path('graphic/grafico-sexo-participante/', dashboard.grafico_sexo_participante,
         name='grafico-sexo-participante'),
    path('graphic/grafico-nacionalidad/', dashboard.grafico_nacionalidad,
         name='grafico-nacionalidad'),
    path('graphic/grafico-pais-eventos/', dashboard.grafico_pais_eventos,
         name='grafico-pais-eventos'),

    # import
    path('import/participants/step1', views.GetExcelToImport.as_view(), name='import-step1'),
    path('import/participants/step2', views.ValidateExcel.as_view(), name='import-step2'),
    path('import/participants/step3', views.ImportParticipants.as_view(), name='import-step3'),
    path('import/capture/', views.Capture.as_view(), name='capture'),
    path('import/capture/<int:pk>/', DetailView.as_view(model=models.Request)),

    # export
    path('export/participants', views.ProjectContactTableView.as_view(), name='export'),
    path('export/template-clean/', views.DownloadTemplate.as_view(), name='template-clean'),

    # API dupes
    path('dupes/doc/', views.ValidateDupesDoc.as_view(), name='dupes-doc'),
    path('dupes/name/', views.ValidateDupesName.as_view(), name='dupes-name'),
    path('dupes/name-fuzzy/', views.ValidateDupesNameFuzzy.as_view(), name='dupes-name-fuzzy'),

    # API dupes - merge
    path('api/fusion/', jsonviews.ContactFusion.as_view(), ),
    path('api/contact/<int:id>/', jsonviews.ContactImportDupes.as_view(), ),
    path('api/name-values/', jsonviews.ContactNameValues.as_view(), ),
    path('api/doc-values/', jsonviews.ContactNameValues.as_view(), ),
    path('api/empty/', jsonviews.ContactEmpty.as_view(), ),
    path('api/labels/', jsonviews.ContactLabels.as_view(), ),
    path('api/docs/', jsonviews.ContactDocDupes.as_view(), ),
    path('api/names/', jsonviews.ContactNameDupes.as_view(), ),
    path('api/names-fuzzy/', jsonviews.ContactNameFuzzyDupes.as_view(), ),
    path('api/doc/<str:document>/', jsonviews.ContactDocDupesDetails.as_view(), ),
    path('api/name/<str:name>/', jsonviews.ContactNameDupesDetails.as_view(), ),
    path('api/ids/<int:id1>/<int:id2>/', jsonviews.ContactIdsDupesDetails.as_view(), ),

    # Participants counter API
    path('api/participants/', jsonviews.ProjectContactCounter.as_view()),
    path('graphic/paises/', jsonviews.Countries.as_view(), name='graphic-paises'),

    # Projects API
    path('api/years/', jsonviews.YearsAPI.as_view()),
    path('api/projects/', jsonviews.ProjectAPIListView.as_view(), name="api-projects"),
    path('api/projects/<int:project_id>/', jsonviews.ProjectAPIListView.as_view()),

    # subprojects API
    path('api/subprojects/', jsonviews.SubProjectAPIListView.as_view(), name="api-subproject"),
    path('api/subprojects/<int:subproject_id>/', jsonviews.SubProjectAPIListView.as_view()),
    path('api/subprojects/project/<int:project_id>/', jsonviews.SubProjectAPIListView.as_view(),
         name="api-subprojects-project"),

    # APIs dumping lists of data
    path('api/organizations/', jsonviews.JsonIdName.as_view(
        queryset=models.Organization.objects.all())),
    path('api/types/', jsonviews.JsonIdName.as_view(queryset=models.ContactType.objects.all())),
    path('api/education/',
         jsonviews.JsonIdName.as_view(queryset=models.Education.objects.all()), ),
    path('api/lwrregions/', jsonviews.LWRRegions.as_view(), name="api-lwrregions"),
]
