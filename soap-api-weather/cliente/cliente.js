const soap = require('soap');
const readline = require('readline');

// URL para o arquivo WSDL fornecido pelo seu serviço SOAP em Python
const url = 'http://127.0.0.1:8000/?wsdl';

// Cria uma interface para ler a entrada do terminal
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Pergunta ao usuário o nome da cidade
rl.question('Escreva o nome da cidade: ', function(cityName) {
    // Cria um cliente para interagir com o serviço SOAP
    soap.createClient(url, function(err, client) {
        if (err) {
            console.error('Erro ao criar cliente SOAP:', err);
            rl.close();
            return;
        }

        // Chama o método get_weather no serviço SOAP
        client.get_weather({ city_name: cityName }, function(err, result) {
            if (err) {
                console.error('Erro ao chamar o método SOAP:', err);
                rl.close();
                return;
            }

            // Exibe o resultado
            console.log('Informações do tempo para ' + cityName + ':');
            console.log(result);
            rl.close(); // Fecha a interface readline
        });
    });
});
