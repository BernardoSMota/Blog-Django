from site_setup.models import SiteSetup

def site_setup(request):
    dados = SiteSetup.objects.order_by('-id').first()

    return {
        'site_setup' : dados
    } 