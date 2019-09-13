from django.urls import path

from . import views
from . import dashboard
from django.views.generic import TemplateView

app_name = 'monitoring'

urlpatterns = [
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
]
