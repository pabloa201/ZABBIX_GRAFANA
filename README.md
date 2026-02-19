Este é um projeto meu em python,

É um projeto simples no qual tive a ideia para que fosse realizado um monitoramento diário dos nossos licenciamentos da empresa dos quais necessitam renovação.

Funciona da seguinte forma:

Há uma planilha que já utilizavamos para registrar as licenças que haviamos e suas datas de renovação, nessa mesma havia tambem uma contagem de dias.

Através da biblioteca XLWINGS, o app realiza uma consulta nas colunas e linhas que desejei que fossem lidas e coloca esses dados em uma varialvel dentro do Python.

Com esses dados lançados em variáveis dentro do codigo, realizei os seguintes passos.

1. Abre a planilha
2. Lê seus dados
3. Salva a mesma
4. Imprime no terminal os resultados com a quantidades de dia que cada está para vencer(e segura esse terminal aberto por 5 segundos)
5. Cria um arquivo de LOG em TXT com os mesmos dados que o mesmo imprimiu no terminal, gerando assim um log atual de quantos dias faltam para cada licença vencer
6. Faz uma verificação de cada uma das variáveis, nas quais se houver alguma licença que está faltando 40,30,20,15,10,5,3,1 dia(as) para expirar, ele dispara um e-mail informando que a mesma está com esses valores exatos para vencimento.

