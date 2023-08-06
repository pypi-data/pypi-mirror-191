## Por que AllWhatsPy?
Como já sabemos, o Whatsapp é uma ferramenta que não podemos mais viver sem.
Seja para cunho profissional ou pessoal, é necessário o manuseio completo desta aplicação.

Então... por que não torná-lo ainda mais eficiente?

Depois de ter pensado nisso, comecei a pesquisar sobre Bots e APIs do Whatsapp, me inspirei em códigos como o do PyWhatsapp e PyWhatKit para a realização deste.

Após passar um tempo estudando e alternando entre o trabalho e o software, botei a mão na massa e comecei a minha jornada indo atrás da melhoria e da qualidade de Software. Continuo atualizando e desenvolvendo, fazendo isso  único e exclusivamente sozinho.

Foram usadas mais de 11 mil linhas de logs para o total funcionamento do código.

Com o AllWhatsPy, você consegue fazer o que quiser!


  
## O que você pode fazer com AllWhatsPy


##  Conectar

python
import AllWhatsPy as awp
awp.conexao()



## Desconectar
  
 
import AllWhatsPy as awp
awp.conexao()
awp.desconetar()


## Trabalhando com Chats/Contatos/Usuários

  ### encontrar_contato(contato)
 
  import AllWhatsPy as awp
    
  awp.conexao()
  awp.encontrar_contato('Lucas Lourenço')
   
  awp.desconectar()
  

  ### encontrar_usuario(numero)

  
    
    

  
  import AllWhatsPy as awp
    
  awp.conexao()
  awp.encontrar_usuario('21900000000')
   
  awp.desconectar()
 

  
 
  ### encontrar_primeira_conversa(ignorar_fixado = True)    

  
  import AllWhatsPy as awp
    
  awp.conexao()
  awp.encontrar_primeira_conversa()
   
  awp.desconectar()
 

  
 
  
  ### descer_conversa_origem_atual(quantidade: int = 1)

  
    
    

  
  import AllWhatsPy as awp
    
  awp.conexao()
  awp.encontrar_contato('Lucas Lourenço')
  awp.descer_conversa_origem_atual()
   
  awp.desconectar()
  
  
  
  ### subir_conversa_origem_atual(quantidade: int = 1)

  
    
    

  import AllWhatsPy as awp
    
  awp.conexao()
  awp.encontrar_contato('Lucas Lourenço')
  awp.subir_conversa_origem_atual()
   
  awp.desconectar()
 



  ### descer_chat_quantidade(quantidade: int)

  
    
  import AllWhatsPy as awp
    
  awp.conexao()
  awp.descer_chat_quantidade()
   
  awp.desconectar()
 



  ### sair_da_conversa()

  
    
  import AllWhatsPy as awp
    
  awp.conexao()
  awp.encontrar_usuario(21900000000)
  awp.enviar_mensagem()
  awp.sair_da_conversa()
  
 



  ### aplicar_filtro()

  
    
  import AllWhatsPy as awp
    
  awp.conexao()
  awp.aplicar_filtro()
   
  awp.desconectar()
 


  ### pegar_dados_contato()

  
    

  import AllWhatsPy as awp
    
  awp.conexao()
  dados = awp.pegar_dados_contato()
  



  ### apagar_conversa()

  
    
  import AllWhatsPy as awp
    
  awp.conexao()
  awp.encontrar_contato('Lucas Lourenço')
  awp.apagar_conversa()
  
  awp.desconectar()
  

  
  
  ### arquivar_conversa()

  
    
  import AllWhatsPy as awp
    
  awp.conexao()
  awp.encontrar_contato('Lucas Lourenço')
  awp.arquivar_conversa()
  
  awp.desconectar()
  

  
  
  ### marcar_como_nao_lida()

    
  import AllWhatsPy as awp
    
  awp.conexao()
  awp.encontrar_contato('Lucas Lourenço')
  awp.marcar_como_nao_lida()
  
  awp.desconectar()
  

  
## Enviando Mensagens

  ### enviar_mensagem(mensagem)

  
  
  import AllWhatsPy as awp

  awp.conexao()
  awp.encontrar_contato('Lucas Lourenço')
  awp.enviar_mensagem('Hello World!')

  awp.desconectar()
  



  ### enviar_mensagem_paragrafada(mensagem)


  import AllWhatsPy as awp

  awp.conexao()
  awp.encontrar_contato('Lucas Lourenço')
  awp.enviar_mensagem_paragrafada(
  '''
  Olá!
  Meu nome é Lucas Lourenco.
  Sou o Criador do AWP.
  '''
  )

  awp.desconectar()



  ### enviar_mensagem_por_link(numero, mensagem)
    
  import AllWhatsPy as awp

  awp.conexao()
  awp.enviar_mensagem_por_link(21900000000 ,'E ai, tudo bem?')

  awp.desconectar()

   

   

   ### enviar_mensagem_direta(contato, mensagem, selecionar_funcao, salvo):  
  
  Para número salvo:
  
      
  import AllWhatsPy as awp

  awp.conexao()
  awp.enviar_mensagem_direta('Lucas Lourenco','Olá! Tudo bem?',1 ,True)

  awp.desconectar()
   

 
    
  Para número não salvo:
  
  

  import AllWhatsPy as awp

  awp.conexao()
  awp.enviar_mensagem_direta(21900000000,'Olá! Tudo bem?',1 ,False)

  awp.desconectar()

  
  
  
## Voltar ao último contato que parou

  
  

import AllWhatsPy as awp
  
awp.conexao()
awp.contato_registrar()
  
awp.desconectar()
```
 
  
 

import AllWhatsPy as awp
  
awp.conexao()
awp.contato_abrir_registrado(2)
  
awp.desconectar()
```



## Agendamento


import AllWhatsPy as awp
  
awp.conexao()
awp.agendamento('20', '08', '30')
awp.encontrar_contato('Lucas Lourenço')
awp.enviar_mensagem('Hello World')
  
awp.desconectar()

## Enviando Arquivos, Vídeos e Imagens

  ### enviar_imagem(nome_imagem)
  

    


    
    import AllWhatsPy as awp

    awp.conexao()
    awp.encontrar_contato('Lucas Lourenço')
    awp.enviar_imagem('AlgumaImagem.png')

    awp.desconectar()
   

   


  ### enviar_video(nome_video)
  

    
    
    

    
    import AllWhatsPy as awp

    awp.conexao()
    awp.encontrar_contato('Lucas Lourenço')
    awp.enviar_video('nome_video.mp4')

    awp.desconectar()
   

   


  ### enviar_arquivo(nome_arquivo)
  

    
    

    
    import AllWhatsPy as awp

    awp.conexao()
    awp.encontrar_contato('Lucas Lourenço')
    awp.enviar_arquivo('nome_arquivo.ext')

    awp.desconectar()
   

   

## Listando as Ultimas Mensagens e Contatos Aparentes
  
  ### lista_ultimas_mensagens_recebidas_de_contatos(quantidade: int = 1)
   
    
    import AllWhatsPy as awp

    awp.conexao()
    dados = awp.lista_ultimas_mensagens_recebidas_de_contatos()

   
    
   


## Mensagens de Conversas
  
  ### ultimas_mensagens_conversa()
  
    
                                                                                                                                                                                                                                                                                                                    
     Em seu início, ela subirá para ser possível de captar mais inforamções e, logo após, irá retornar tudo em um dicionário separado por índices. E os valores desses      índices serão mais um dicionário contendo todas as informações daquela conversa.
    
    
    import AllWhatsPy as awp

    awp.conexao()
    awp.encontrar_contato('Lucas Lourenço')
    dados = awp.ultimas_mensagens_conversa()
   
     
    `output:`
    
    
   
    Como é possível reparar, será trazido informações com o índice. Os `values` deles serão outra dicionário onde você pode estar trabalhando. 
    
   


## Acesso ao Código
Se quiser ter acesso ao código, basta [Clicar Aqui](https://github.com/devlucaslourenco/AllWhatsPy)



## Notas do Criador

Para a criação deste código, foram usadas mais de 11 mil linhas de log




## Autor


http://linkedin.com/in/lucas-lourenco0312




https://www.instagram.com/lucaslourencoo__/



Email: dev.lucaslourenco@gmail.com



## Problemas com o AllWhatsPy
Ainda não foi encontrado problemas no código. 

Caso você tenha percebido algo, sinta-se à vontade para descrevê-lo na aba `Issues`!

E também para você que está tendo dificuldades em trabalhar com esta lib, basta descrevê-la que irei ajudá-lo!


## Contribuição

Pull Requests são muito bem vindas!

Caso seja uma grande mudança, por favor, abra uma discussão na aba `Issues` para maior compreensão do seu caso.
