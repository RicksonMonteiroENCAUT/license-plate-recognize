<h1>Segmentação e Reconhecimento de placas de carro</h1>
<p>
    Pequeno projeto de segmentação e reconhecimento de placas de carro utilizando o OpenCV e a google Vision API.
    Antes de iniciar o projeto é necessário adicionar suas credencias do Google Vision para a utlização da API, Instruções para obter credenciais: <a href="https://cloud.google.com/vision/docs/setup" target="_blank">aqui</a>. 
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="[PATH].json"   
    
</p>
<p>Substitua "[PATH]" pelo caminho onde suas credencias estiverem salvas na sua máquina.</p>
  
<h2>Segmentação</h2>

<p>
    O processo de segmentação foi totalmente realizado com o auxílio da biblioteca de visão computacional OpenCV e foi dividido em 5 etapas.</br>
    -Inicialmente é feito a leitura da imagem e sua converção para GrayScale, temos o exemplo a abaixo:
    
</p>
    <div>
         <img src= "https://user-images.githubusercontent.com/62216467/103906599-eaf7c400-50de-11eb-803e-0dea5b9a464d.jpg" width=400> 
         <img src= "https://user-images.githubusercontent.com/62216467/103907114-9bfe5e80-50df-11eb-9f69-bf6f19c21c5c.png" width=400> 
    </div>
 
<p>
   Logo depois, aplicamos o cv2.bilateralFilter(), este filtro é bastante útil para remoção de ruídos com um ótima preservação de bordas.
   você pode encontrar mais informações sobre este método <a href="https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html" target="_blank">aqui</a>.    

</p>
    <div>
       <img src= "https://user-images.githubusercontent.com/62216467/103908997-eda7e880-50e1-11eb-9644-a1d0d473159b.png" width=600> 
    </div>
<p>
   É possível perceber como a imagem tem uma aparência mais "cartunista" após a aplicação do filtro. 
</p>
<p>
   Agora com a imagem já suavizada é aplicada uma transformação morfológica conhecida como Black-Hat, ela é basicamente a diferença entre a imagem de fechamento (Imagem após as operações de dilatação e erosão) e a imagem de entrada, no nosso caso, a imagem suavizada.
   Essa operação é muito útil para encontrar "coisas" escuras em fundos brancos, como é o caso dos digitos da placa. 
   Neste <a href="https://www.geeksforgeeks.org/top-hat-and-black-hat-transform-using-python-opencv/" target="_blank">link</a> tem mais infomações sobre a operação. Após sua aplicação chegamos no resultado abaixo.
</p>
       <div>
       <img src= "https://user-images.githubusercontent.com/62216467/103911205-82134a80-50e4-11eb-8007-fd6d86dbcc3c.png" width=600> 
    </div>
<p> 
    Em seguida aplicamos uma operação de fechamento afim de ressaltar os digitos da placa, pois após a operação black-hat eles obtiveram algumas falhas em seu interior e reduzir alguns ruídos externos. Neste <a href="https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html" target="_blank">link</a> é possível entender um pouco mais sobre o funcionamento das operações morfológicas. Também iremos realizar uma binarização na imagem.
    Após o operação e a binarização temos o seguinte resultado.    
</p>
     <div>
        <img src= "https://user-images.githubusercontent.com/62216467/103912857-91939300-50e6-11eb-891b-d1481a0a5cad.png" width=400> 
        <img src= "https://user-images.githubusercontent.com/62216467/103928950-4df75400-50fb-11eb-9f13-04b92a4f56e9.png" width=400>   
    </div>
<p> 
    Como a queremos detectar uma placa, precisamos de alguma forma destacar a placa entre os outros objetos da imagem, para isso iremos utilizar o método cv2.Sobel() 
    ele promove uma operação de alisamento gaussiano conjunto mais diferenciação, no nosso caso iremos usar a derivada na direção X afim de ressaltar os traços verticais (Isso mesmo, verticais! haha), pois são maioria na placa e em seus dígitos.
     No <a href="https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_gradients/py_gradients.html" target="_blank">link</a> é possível entender melhor seu funcionamento. Abaixo temos a imagem após o procedimento.
  
</p>
      <div>
       <img src= "https://user-images.githubusercontent.com/62216467/103915374-e2f15180-50e9-11eb-8437-4744bea070ef.png" width=600> 
    </div>
 
<p> 
     No entanto a imagem acima perdeu sua formatação dos valores, seus valores não estão mais entre [0-255] e seu "type" não é mais uint8, como de padrão nas imagens por esse         fator a imagem acima aparece com tanto ruído. Dessa forma, é necessario realizar uma normalização para resgatar este intevalo de valores e seu type padrão. Após isso temos uma resultado melhor na imagem, como pode ser visto
</p>
    <div>
       <img src= "https://user-images.githubusercontent.com/62216467/103916395-24363100-50eb-11eb-89aa-10b99a37a626.png" width=600> 
    </div>
<p>
  Com a imagem já normalizada aplicamos um filtro gaussiano com kernel (9x9), afim de reduzir os ruídos restantes, seguida de outra operação de fechamento com o mesmo intuito     da aplicada anteriormente. Assim chegamos no resultado abaixo:
</p>
    <div>
         <img src= "https://user-images.githubusercontent.com/62216467/103927444-1d161f80-50f9-11eb-8d41-b2c2b2e3fd4e.png" width=600> 
    </div>
<p>
    Por fim, é realizada outra operação de binarização na imagem. Com a imagem já binarizada aplicamos uma operação de erosão com 3 iterações seguida de uma operação de dilatação de com 9 iterações (Valores obtidos empíricamente). Com a erosão tentaremos reduzir os restantes dos ruídos, porém iremos perder parte da informação da placa, com a dilatação tentaremos recuperar parte dessa informação perdida.     
</p>
    <div>
         <img src= "(https://user-images.githubusercontent.com/62216467/103930048-ea6e2600-50fc-11eb-9785-7dfb5adfc03a.png" width=400> 
         <img src= "(https://user-images.githubusercontent.com/62216467/103930061-efcb7080-50fc-11eb-8f36-5ee3f31ce588.png" width=400> 
    </div>
<p>
    Após os procedimentos iremos enviar a imagem para a função crop que desenvolvi. Ela recebe a imagem após os últimos procedimento(imagem A) e a imagem em escala de              cinza(Imagem B). A imagem "A" é submetida ao método cv2.findContourns(), com ela iremos conseguir todos os contornos da imagem e com o auxílio da cv2.boudingRect()             conseguimos obter os vértices dos retangulos encontrados. A proporção das placas mercosul são de 40x13, assim temos uma proporção de 3.07. Dessa forma, considerei que apenas os retângulos encontrados que respeitassem uma proporção de valores entre [2-5]. Assim, com os vértices obtidos pude realizar um recorte na imagem em escala de cinza e obter a placa. Atualmente esse algoritimo de segmentação obteve uma acurácia de apenas 70%, porém acredito ser possível aumentar esse valor com a utilização de mais técnicas de processamento de imagem.  
    vértices para 
</p>
    <div>   
         <img src= "https://user-images.githubusercontent.com/62216467/103930077-f528bb00-50fc-11eb-99eb-3e9ca43c1b56.png" width=700> 
    </div>
<h2>
    Reconhecimento
</h2>
<p>
    O Reconhecimento da placa é realizado através da API Google Vision utilizando técnicas de Reconhecimento Óptico de Caracteres (OCR). Neste <a           href="https://cloud.google.com/vision/docs/ocr" target="_blank">link</a> tem a explicação de como utilizar.
</p>

<h2>Contatos</h2>
<p>
    <a href="https://www.instagram.com/rickson_gm/" target="_blank">Instagram</a></br>
    <a href="https://www.gmail.com" target="_blank">ricksonencaut@gmail.com</a></br>
    <a href="https://www.linkedin.com/in/rickson-gomes-monteiro-411a2a1a1/" target="_blank">LinkedIN</a></br>
</p>

