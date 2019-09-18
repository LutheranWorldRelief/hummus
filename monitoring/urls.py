from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework import routers

from . import views
from . import dashboard
from . import api

router = routers.DefaultRouter()
router.register(r'opt/api-countries', api.CountryViewSet)
router.register(r'opt/api-types', api.ContactTypeViewSet)
router.register(r'opt/api-education', api.EducationViewSet)
router.register(r'opt/api-organizations', api.OrganizationViewSet)
router.register(r'opt/api-projects', api.ProjectViewSet)

app_name = 'monitoring'

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', views.ContactTableView.as_view()),
    path('project/', views.ProjectTableView.as_view()),
    path('subproject/', views.SubProjectTableView.as_view()),
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
    path('import/beneficiarios', TemplateView.as_view(template_name='import.html'), name='iframe_import'),
    path('report/proyectos', TemplateView.as_view(template_name='report.html'), name='iframe_report'),
    path('report/template-clean', views.DownloadTemplate.as_view(), name='template-clean'),
    path('validate/dupes-id', views.ValidateDupesId.as_view(), name='validate-dupes-ids'),
    path('opt/api-empty/', views.ContactEmpty.as_view(), ),
    path('opt/api-labels/', views.ContactLabels.as_view(), ),
    path('opt/api-docs/', views.ContactDocDupes.as_view(), ),
]
