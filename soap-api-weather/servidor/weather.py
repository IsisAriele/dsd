import requests

api_key = ""
base_url = "http://api.weatherapi.com/v1/current.json?"

def get_weather(city_name):
    complete_url = base_url + "key=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if "error" in x.keys():
        return None
    
    return {
        "cidade": x["location"]["name"],
        "regiao": x["location"]["region"],
        "pais": x["location"]["country"],
        "hora_atual": x["location"]["localtime"],
        "temperatura": x["current"]["temp_c"],
        "umidade": x["current"]["humidity"],
        "condicao": x["current"]["condition"]["text"],
    }