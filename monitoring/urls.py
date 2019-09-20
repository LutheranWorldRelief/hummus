from django.urls import include, path
from django.views.generic import TemplateView

from . import views
from . import jsonviews
from . import dashboard
from . import models

app_name = 'monitoring'

urlpatterns = [
    path('contact/', views.ContactTableView.as_view()),
    path('project/', views.ProjectTableView.as_view()),
    path('subproject/', views.SubProjectTableView.as_view()),
    path('contact/<int:pk>/', views.ContactDetailView.as_view(), name='contact'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project'),
    path('subproject/<int:pk>/', views.SubProjectDetailView.as_view(), name='subproject'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('graphic/proyecto/', dashboard.proyecto, name='graphic-proyecto'),
    path('graphic/cantidad-proyectos/', dashboard.cantidadProyectos, name='cantidad-proyectos'),
    path('graphic/cantidad-eventos/', dashboard.cantidadEventos, name='cantidad-eventos'),
    path('graphic/grafico-actividades/', dashboard.graficoActividades, name='grafico-actividades'),
    path('graphic/paises/', dashboard.paises, name='graphic-paises'),
    path('graphic/rubros/', dashboard.rubros, name='graphic-rubros'),
    path('graphic/grafico-organizaciones/', dashboard.graficoOrganizaciones, name='grafico-organizaciones'),
    path('graphic/proyectos-metas/', dashboard.proyectosMetas, name='proyectos-metas'),
    path('graphic/grafico-anio-fiscal/', dashboard.graficoAnioFiscal, name='grafico-anio-fiscal'),
    path('graphic/grafico-edad/', dashboard.graficoEdad, name='grafico-edad'),
    path('graphic/grafico-educacion/', dashboard.graficoEducacion, name='grafico-educacion'),
    path('graphic/grafico-eventos/', dashboard.graficoEventos, name='grafico-eventos'),
    path('graphic/grafico-tipo-participante/', dashboard.graficoTipoParticipante, name='grafico-tipo-participante'),
    path('graphic/grafico-sexo-participante/', dashboard.graficoSexoParticipante, name='grafico-sexo-participante'),
    path('graphic/grafico-nacionalidad/', dashboard.graficoNacionalidad, name='grafico-nacionalidad'),
    path('graphic/grafico-pais-eventos/', dashboard.graficoPaisEventos, name='grafico-pais-eventos'),
    path('import/beneficiarios/', TemplateView.as_view(template_name='import.html'), name='iframe_import'),
    path('report/proyectos/', TemplateView.as_view(template_name='report.html'), name='iframe_report'),
    path('report/template-clean/', views.DownloadTemplate.as_view(), name='template-clean'),
    path('report/export/', views.ReportExport.as_view(), name='report-export'),
    path('validate/dupes-doc/', views.ValidateDupesDoc.as_view(), name='validate-dupes-doc'),
    path('validate/dupes-name/', views.ValidateDupesName.as_view(), name='validate-dupes-name'),
    path('opt/api-fusion/', jsonviews.ContactFusion.as_view(), ),
    path('opt/api-name-values/', jsonviews.ContactNameValues.as_view(), ),
    path('opt/api-doc-values/', jsonviews.ContactNameValues.as_view(), ),
    path('opt/api-empty/', jsonviews.ContactEmpty.as_view(), ),
    path('opt/api-labels/', jsonviews.ContactLabels.as_view(), ),
    path('opt/api-docs/', jsonviews.ContactDocDupes.as_view(), ),
    path('opt/api-names/', jsonviews.ContactNameDupes.as_view(), ),
    path('opt/api-doc/<str:document>/', jsonviews.ContactDocDupesDetails.as_view(), ),
    path('opt/api-name/<str:name>/', jsonviews.ContactNameDupesDetails.as_view(), ),
    path('opt/api-organizations/', jsonviews.JsonIdName.as_view(queryset=models.Organization.objects.filter(projectcontact__isnull=False).distinct())),
    path('opt/api-countries/', jsonviews.JsonIdName.as_view(queryset=models.Country.objects.filter(project__isnull=False).distinct())),
    path('opt/api-projects/', jsonviews.JsonIdName.as_view(queryset=models.Project.objects.filter(status='Active'))),
    path('opt/api-types/', jsonviews.JsonIdName.as_view(queryset=models.ContactType.objects.all())),
    path('opt/api-education/', jsonviews.JsonIdName.as_view(queryset=models.Education.objects.all()),)
]
