from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from weather import get_weather

class WeatherService(ServiceBase):
    # Decorator para definir o tipo de dado de entrada e saída
    # Unicode = string
    @rpc(Unicode, _returns=Unicode)
    def get_weather(ctx, city_name):
        previsao = get_weather(city_name)
        if previsao is None:
            return "Não foi possível encontrar cidade."

        return (
            f"{previsao['cidade']} - {previsao['regiao']}, {previsao['pais']}\n"
            f"Temperatura atual: {previsao['temperatura']}°C\n"
            f"Umidade: {previsao['umidade']}%\n"
            f"Condição: {previsao['condicao']}\n"
            f"Hora atual: {previsao['hora_atual']}"
        )
# O application define o serviço SOAP e gera automaticamente o WSDL
# O servidor ESGI serve o aplicativo SOAP
application = Application(
    [WeatherService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# O servidor WSGI serve o aplicativo SOAP
wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    import logging
    # Importa o servidor WSGI
    from wsgiref.simple_server import make_server

    # Configuração do log
    logging.basicConfig(level=logging.INFO)
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://127.0.0.1:8000/?wsdl")

    # Inicializa o servidor
    server = make_server('172.21.32.1', 8000, wsgi_application)
    server.serve_forever()