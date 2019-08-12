from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def proyecto(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def cantidadProyectos(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def cantidadEventos(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoActividades(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def paises(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def rubros(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoOrganizaciones(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def proyectosMetas(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoAnioFiscal(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoEdad(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoEducacion(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoEventos(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoTipoParticipante(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoSexoParticipante(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoNacionalidad(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoPaisEventos(request):
    return JsonResponse({'foo':'bar'})
