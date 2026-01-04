from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.decorators import login_required

# Views que renderizam páginas HTML
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/auth/login/')
def my_bots(request):
    return render(request, 'my_bots.html')

@login_required(login_url='/auth/login/')
def bot_processar_classificar(request):
    return render(request, 'bot_processar_classificar.html')

@login_required(login_url='/auth/login/')
def bot_consulta_cnpj(request):
    return render(request, 'bot_consulta_cnpj.html')

@login_required(login_url='/auth/login/')
def bot_dividir_excel(request):
    return render(request, 'bot_dividir_excel.html')

@login_required(login_url='/auth/login/')
def bot_limpar_formatos(request):
    return render(request, 'bot_limpar_formatos.html')

@login_required(login_url='/auth/login/')
def bot_mover_esocial(request):
    return render(request, 'bot_mover_esocial.html')

@login_required(login_url='/auth/login/')
def bot_organizar_xml(request):
    return render(request, 'bot_organizar_xml.html')

@login_required(login_url='/auth/login/')
def bot_mover_extensao(request):
    return render(request, 'bot_mover_extensao.html')

@login_required(login_url='/auth/login/')
def bot_unificar_excel(request):
    return render(request, 'bot_unificar_excel.html')

@login_required(login_url='/auth/login/')
def bot_tabulador_xml_fiscal(request):
    return render(request, 'bot_tabulador_xml_fiscal.html')

@login_required(login_url='/auth/login/')
def bot_organizador_pastas(request):
    return render(request, 'bot_organizador_pastas.html')

@login_required(login_url='/auth/login/')
def bot_divisor_pag_pdf(request):
    return render(request, 'bot_divisor_pag_pdf.html')

@login_required(login_url='/auth/login/')
def bot_tabulate_cfop(request):
    return render(request, 'bot_tabulate_cfop.html')

@login_required(login_url='/auth/login/')
def bot_tabulate_darf(request):
    return render(request, 'bot_tabulate_darf.html')

@login_required(login_url='/auth/login/')
def bot_tabulate_dcomp(request):
    return render (request, 'bot_tabulate_dcomp.html')

@login_required(login_url='/auth/login/')
def bot_tabulate_dctf(request):
    return render(request, 'bot_tabulate_dctf.html')

@login_required(login_url='/auth/login/')
def bot_tabulate_fonte_pagadora(request):
    return render(request, 'bot_tabulate_fonte_pagadora.html')

@login_required(login_url='/auth/login/')
def bot_tabulate_ocr_free(request):
    return render(request, 'bot_tabulate_ocr_free.html')

@login_required(login_url='/auth/login/')
def bot_tabulate_recolhimentos(request):
    return render(request, 'bot_tabulate_recolhimentos.html')

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
