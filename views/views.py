from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView

# Views que renderizam páginas HTML
def home(request):
    return render(request, 'home.html')

def my_bots(request):
    return render(request, 'my_bots.html')

def bot_processar_classificar(request):
    return render(request, 'bot_processar_classificar.html')

def bot_consulta_cnpj(request):
    return render(request, 'bot_consulta_cnpj.html')

def bot_dividir_excel(request):
    return render(request, 'bot_dividir_excel.html')

def bot_limpar_formatos(request):
    return render(request, 'bot_limpar_formatos.html')

def bot_mover_esocial(request):
    return render(request, 'bot_mover_esocial.html')

def bot_organizar_xml(request):
    return render(request, 'bot_organizar_xml.html')

def bot_mover_extensao(request):
    return render(request, 'bot_mover_extensao.html')

def bot_unificar_excel(request):
    return render(request, 'bot_unificar_excel.html')

def bot_tabulador_xml_fiscal(request):
    return render(request, 'bot_tabulador_xml_fiscal.html')

def bot_organizador_pastas(request):
    return render(request, 'bot_organizador_pastas.html')

def bot_divisor_pag_pdf(request):
    return render(request, 'bot_divisor_pag_pdf.html')

def bot_tabulate_cfop(request):
    return render(request, 'bot_tabulate_cfop.html')
    
def bot_tabulate_darf(request):
    return (request, 'bot_tabulate_darf.html')
    
def bot_tabulate_dcomp(request):
    return (request, 'bot_tabulate_dcomp.html')
    
def bot_tabulate_dctf(request):
    return (request, 'bot_tabulate_dctf.html')
    
def bot_tabulate_fonte_pagadora(request):
    return (request, 'bot_tabulate_fonte_pagadora.html')

def bot_tabulate_ocr_free(request):
    return (request, 'bot_tabulate_ocr_free.html')

def bot_tabulate_recolhimentos(request):
    return (request, 'bot_tabulate_recolhimentos.html')

class TokenObtainPairWithIPView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            ip = self.get_client_ip(request)
            response.data['client_ip'] = ip
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
