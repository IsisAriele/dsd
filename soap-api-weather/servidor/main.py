from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from weather import get_weather

class WeatherService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def get_weather(ctx, city_name):
        previsao = get_weather(city_name)
        if previsao is None:
            return "Não foi possível encontrar cidade."

        return f"{previsao['cidade']} - {previsao['regiao']}, {previsao['pais']} - Temperatura atual: {previsao['temperatura']}°C - Umidade: {previsao['umidade']}% (Hora atual: {previsao['hora_atual']})"

application = Application(
    [WeatherService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    import logging
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.INFO)
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://127.0.0.1:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()