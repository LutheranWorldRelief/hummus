from django.urls import path

from . import views
from . import graphic
from django.views.generic import TemplateView

app_name = 'monitoring'

urlpatterns = [
    path('contact/', views.ContactTableView.as_view()),
    path('project/', views.ProjectTableView.as_view()),
    path('subproject/', views.SubProjectTableView.as_view()),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project'),
    path('subproject/<int:pk>/', views.SubProjectDetailView.as_view(), name='subproject'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('graphic/proyecto/', graphic.proyecto, name='graphic-proyecto'),
    path('graphic/cantidad-proyectos/', graphic.cantidadProyectos, name='cantidad-proyectos'),
    path('graphic/cantidad-eventos/', graphic.cantidadEventos, name='cantidad-eventos'),
    path('graphic/grafico-actividades/', graphic.graficoActividades, name='grafico-actividades'),
    path('graphic/paises/', graphic.paises, name='graphic-paises'),
    path('graphic/rubros/', graphic.rubros, name='graphic-rubros'),
    path('graphic/grafico-organizaciones/', graphic.graficoOrganizaciones, name='grafico-organizaciones'),
    path('graphic/proyectos-metas/', graphic.proyectosMetas, name='proyectos-metas'),
    path('graphic/grafico-anio-fiscal/', graphic.graficoAnioFiscal, name='grafico-anio-fiscal'),
    path('graphic/grafico-edad/', graphic.graficoEdad, name='grafico-edad'),
    path('graphic/grafico-educacion/', graphic.graficoEducacion, name='grafico-educacion'),
    path('graphic/grafico-eventos/', graphic.graficoEventos, name='grafico-eventos'),
    path('graphic/grafico-tipo-participante/', graphic.graficoTipoParticipante, name='grafico-tipo-participante'),
    path('graphic/grafico-sexo-participante/', graphic.graficoSexoParticipante, name='grafico-sexo-participante'),
    path('graphic/grafico-nacionalidad/', graphic.graficoNacionalidad, name='grafico-nacionalidad'),
    path('graphic/grafico-pais-eventos/', graphic.graficoPaisEventos, name='grafico-pais-eventos'),
    path('import/beneficiarios', TemplateView.as_view(template_name='import.html'), name='iframe_import'),
    path('report/proyectos', TemplateView.as_view(template_name='report.html'), name='iframe_report'),
]
