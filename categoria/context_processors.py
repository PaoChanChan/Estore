from .models import Categoria

def menu_links(request):
    """Función para generar los distintos links para cada categoría"""
    links = Categoria.objects.all()
    return dict(links=links)
