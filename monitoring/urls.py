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
    path('contact/', views.ContactTableView.as_view()),
    path('project/', views.ProjectTableView.as_view()),
    path('subproject/', views.SubProjectTableView.as_view()),
    path('contact/<int:pk>/', views.ContactDetailView.as_view(), name='contact'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project'),
    path('subproject/<int:pk>/', views.SubProjectDetailView.as_view(), name='subproject'),

    # dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('graphic/proyecto/', dashboard.get_proyecto, name='graphic-proyecto'),
    path('graphic/cantidad-paises/', dashboard.cantidad_paises, name='cantidad-paises'),
    path('graphic/cantidad-proyectos/', dashboard.cantidad_proyectos, name='cantidad-proyectos'),
    path('graphic/cantidad-participantes/',
         dashboard.cantidad_participantes, name='cantidad-participantes'),
    path('graphic/paises/', dashboard.get_paises, name='graphic-paises'),
    path('graphic/rubros/', dashboard.get_rubros, name='graphic-rubros'),
    path('graphic/grafico-organizaciones/', dashboard.grafico_organizaciones,
         name='grafico-organizaciones'),
    path('graphic/proyectos-metas/', dashboard.proyectos_metas, name='proyectos-metas'),
    path('graphic/grafico-anio-fiscal/', dashboard.grafico_anio_fiscal, name='grafico-anio-fiscal'),
    path('graphic/grafico-edad/', dashboard.grafico_edad, name='grafico-edad'),
    path('graphic/grafico-educacion/', dashboard.grafico_educacion, name='grafico-educacion'),
    path('graphic/grafico-eventos/', dashboard.grafico_eventos, name='grafico-eventos'),
    path('graphic/grafico-tipo-participante/', dashboard.grafico_tipo_participante,
         name='grafico-tipo-participante'),
    path('graphic/grafico-sexo-participante/', dashboard.grafico_sexo_participante,
         name='grafico-sexo-participante'),
    path('graphic/grafico-nacionalidad/', dashboard.grafico_nacionalidad,
         name='grafico-nacionalidad'),
    path('graphic/grafico-pais-eventos/', dashboard.grafico_pais_eventos,
         name='grafico-pais-eventos'),

    # import
    path('import/participants/step1', TemplateView.as_view(template_name='import/step1.html',
                                                           extra_context={'short_date_format': settings.SHORT_DATE_FORMAT}), name='import-step1'),
    path('import/participants/step2', views.ValidateExcel.as_view(), name='import-step2'),
    path('import/participants/step3', views.ImportParticipants.as_view(), name='import-step3'),
    path('import/capture/', views.Capture.as_view(), name='capture'),
    path('import/capture/<int:pk>/', DetailView.as_view(model=models.Request)),

    # export
    path('export/participants', views.ProjectContactTableView.as_view(), name='export'),
    path('export/template-clean/', views.DownloadTemplate.as_view(), name='template-clean'),

    # dupes
    path('validate/dupes-doc/', views.ValidateDupesDoc.as_view(), name='validate-dupes-doc'),
    path('validate/dupes-name/', views.ValidateDupesName.as_view(), name='validate-dupes-name'),

    # APIs misc
    path('opt/api-fusion/', jsonviews.ContactFusion.as_view(), ),
    path('opt/api-contact/<int:id>/', jsonviews.ContactImportDupes.as_view(), ),
    path('opt/api-name-values/', jsonviews.ContactNameValues.as_view(), ),
    path('opt/api-doc-values/', jsonviews.ContactNameValues.as_view(), ),
    path('opt/api-empty/', jsonviews.ContactEmpty.as_view(), ),
    path('opt/api-labels/', jsonviews.ContactLabels.as_view(), ),
    path('opt/api-docs/', jsonviews.ContactDocDupes.as_view(), ),
    path('opt/api-names/', jsonviews.ContactNameDupes.as_view(), ),
    path('opt/api-doc/<str:document>/', jsonviews.ContactDocDupesDetails.as_view(), ),
    path('opt/api-name/<str:name>/', jsonviews.ContactNameDupesDetails.as_view(), ),
    path('opt/api-organizations/', jsonviews.JsonIdName.as_view(
        queryset=models.Organization.objects.filter(projectcontact__isnull=False).distinct())),
    path('opt/api-countries/',
         jsonviews.JsonIdName.as_view(queryset=models.Country.objects.filter(
             project__isnull=False).distinct())),
    path('opt/api-projects/',
         jsonviews.JsonIdName.as_view(queryset=models.Project.objects.filter(status='Active'))),
    path('opt/api-types/', jsonviews.JsonIdName.as_view(queryset=models.ContactType.objects.all())),
    path('opt/api-education/',
         jsonviews.JsonIdName.as_view(queryset=models.Education.objects.all()), )

]
