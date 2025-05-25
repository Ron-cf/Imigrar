# Imigrar
Projeto Integrador III - Univesp

Com a crescente demanda global por profissionais qualificados, os jovens adultos recebem propostas de emprego de diversos países. Estas propostas apresentam remunerações em diversos patamares. Levando se em conta que os sistemas de tributação têm regras diferentes nos diversos issional. O processamento dos países, a renda líquida recebida pelo trabalhador passa a ser um elemento de difícil aferição no processo de seleção da melhor oferta de emprego.
Neste projeto foi desenvolvido um sistema para o cálculo da renda líquida, a partir do fornecimento de dados básicos como: valor do salário bruto e cidade em que será exercida a atividade profdados de entrada ocorre no servidor com um programa utilizando a linguagem python.
A passagem de dados entre o front-end e o back-end é feita com o uso de flask.

O arquivo p_3.service é o arquivo que permite que a aplicação python rode como um serviço no servidor de aplicação.
É utilizado como parâmetro para o comando no systemctl no linux.
Comando para ativar: systemctl start p_3.service
Comando para verificar: systemctl status p_3.service
Comando para parar o serviço (Utilizado quando foi feita alguma modificação no arquivo .py): systemctl stop p_3.service

Os arquivos 2025-05-21_13h36m58s.json e 2025-05-24_12h28m59s.json são exemplos do arquivo do tipo json gerado com o processamento dos dados iniciais.

O arquivo resultado.txt também é gerado pelo programa python e possibilita a visualização dos resultados no front-end.
