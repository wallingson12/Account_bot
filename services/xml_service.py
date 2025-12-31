from account_tools.utils.decorators import log_de_erro
from services.mover_xml.mover_arquivos_esocial import (
    mover_arquivos_xml_metade,
    organizar_xml_por_data,
)


class XmlService:

    @log_de_erro
    def mover_esocial(self, *args, **kwargs):
        return mover_arquivos_xml_metade(*args, **kwargs)

    @log_de_erro
    def organizar_por_data(self, *args, **kwargs):
        return organizar_xml_por_data(*args, **kwargs)