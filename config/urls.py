from django.contrib import admin
from django.urls import path
from views.views import *

from views.views_auth import (
    cadastrar_usuario,
    confirmar_codigo,
    reenviar_codigo,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home", home, name="home"),
    path("my-bots/", my_bots, name="my_bots"),
    path("bots/processar-classificar/", bot_processar_classificar, name="bot_processar_classificar"),
    path("bots/consulta-cnpj/", bot_consulta_cnpj, name="bot_consulta_cnpj"),
    path("bots/dividir-excel/", bot_dividir_excel, name="bot_dividir_excel"),
    path("bots/limpar-formatos/", bot_limpar_formatos, name="bot_limpar_formatos"),
    path("bots/mover-esocial/", bot_mover_esocial, name="bot_mover_esocial"),
    path("bots/organizar-xml/", bot_organizar_xml, name="bot_organizar_xml"),
    path("bots/mover-extensao/", bot_mover_extensao, name="bot_mover_extensao"),
    path("bots/unificar-excel/", bot_unificar_excel, name="bot_unificar_excel"),
    path("bots/tabulador-xml-fiscal/", bot_tabulador_xml_fiscal, name="bot_tabulador_xml_fiscal"),
    path("bots/organizador-pastas/", bot_organizador_pastas, name="bot_organizador_pastas"),
    path("bots/divisor-pag-pdf/", bot_divisor_pag_pdf, name="bot_divisor_pag_pdf"),

    path("bots/bot_tabulate_cfop/", bot_tabulate_cfop, name="bot_tabulate_cfop"),
    path("bots/bot_tabulate_darf/", bot_tabulate_darf, name="bot_tabulate_darf"),
    path("bots/bot_tabulate_recolhimento/", bot_tabulate_recolhimentos, name="bot_tabulate_recolhimentos"),
    path("bots/bot_tabulate_dcomp/", bot_tabulate_dcomp, name="bot_tabulate_dcomp"),
    path("bots/bot_tabulate_dctf/", bot_tabulate_dctf, name="bot_tabulate_dctf"),
    path("bots/bot_tabulate_fonte_pagadora/", bot_tabulate_fonte_pagadora, name="bot_tabulate_fonte_pagadora"),
    path("bots/bot_tabulate_ocr_free/", bot_tabulate_ocr_free, name="bot_tabulate_ocr_free"),

    # JWT com IP
    path("api/token/", TokenObtainPairWithIPView.as_view(), name="token_obtain_pair_with_ip"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Rotas de autenticação
    path("auth/cadastrar/", cadastrar_usuario, name="cadastrar_usuario"),
    path("auth/confirmar/", confirmar_codigo, name="confirmar_codigo"),
    path("auth/reenviar-codigo/", reenviar_codigo, name="reenviar_codigo"),
]
