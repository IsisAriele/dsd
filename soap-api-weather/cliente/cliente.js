const soap = require('soap');
const readline = require('readline');

const url = 'http://172.21.32.1:8000/?wsdl';

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('Escreva o nome da cidade: ', function(cityName) {
    soap.createClient(url, function(err, client) {
        if (err) {
            console.error('Erro ao criar cliente SOAP:', err);
            rl.close();
            return;
        }

        client.get_weather({ city_name: cityName }, function(err, result) {
            if (err) {
                console.error('Erro ao chamar o método SOAP:', err);
                rl.close();
                return;
            }
            console.log('Informações do clima para ' + cityName + ':');
            console.log(result.get_weatherResult);
            rl.close(); 
        });
    });
});
