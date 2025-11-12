from django.shortcuts import render

def error_page(request):
    """
    Vista central de errores: renderiza un template genérico
    """
    code = request.GET.get("code", "Error")
    message = request.GET.get("message", "Ha ocurrido un problema inesperado.")
    return render(request, "error.html", {"code": code, "message": message})
