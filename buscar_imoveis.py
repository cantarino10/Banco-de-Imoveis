import pygame
import time
import pandas as pd
import webbrowser

pygame.init()
pygame.font.init()

df = pd.read_csv("Dados de Imoveis.csv",index_col = False )   #load csv Data
diff = df.compare(df)

 
class Res:   #Define Resolution class
    def __init__ (self,x,y):
        self.x = x
        self.y = y
        self.Resolution = (self.x,self.y)


Resolution = Res(1024,720)
class icon:      #Icons Class
    def __init__(self):

        self.carrinho =  pygame.transform.scale(pygame.image.load(f"images/carrinho.jpg"),(25,25))
        self.banheiro = pygame.transform.scale(pygame.image.load("images/banheiro.png"),(23,23)) 
        self.quarto = pygame.transform.scale(pygame.image.load("images/quarto.png"),(25,25))
        self.suite = pygame.transform.scale(pygame.image.load("images/suite.png"),(25,25))
        self.elevador = pygame.transform.scale(pygame.image.load("images/elevador.png"),(25,25))
        self.pet = pygame.transform.scale(pygame.image.load("images/cao.png"),(25,25))
        self.areaconstruida = pygame.transform.scale(pygame.image.load("images/area.png"),(25,25))
        self.areaprivativa = pygame.transform.scale(pygame.image.load("images/areaprivativa.png"),(25,25))
        self.mobilia = pygame.transform.scale(pygame.image.load("images/mobilia.png"),(25,25))
        self.browser =  pygame.transform.scale(pygame.image.load("images/internet.png"),(25,25))
        self.local =  pygame.transform.scale(pygame.image.load("images/gps.png"),(25,25))
        self.fone = pygame.transform.scale(pygame.image.load("images/fone.jpg"),(25,25))
        self.lixeira = pygame.transform.scale(pygame.image.load("images/Lixeira.png"),(30,23))
        self.anotacoes = pygame.transform.scale(pygame.image.load("images/anotacoes_icone.png"),(25,25))
 
icone = icon()

white = (255,255,255)
blue = (0,0,255)
black = (0,0,0)         #Colors
rosa = (175,0,80)

class rect_:         #Class to create Result Rects
   def __init__(self,x,y,w,h):
      self.x = x
      self.y = y
      self.w = w
      self.h = h
      self.color = white
      self.colide = pygame.rect.Rect(self.x,self.y,self.w,self.h)
    
   def show(self,tela):   #Show Rects created
     
      pygame.draw.rect(tela,self.color,self.colide)
      pygame.draw.rect(tela,black,(self.x-1,self.y-1,self.w+1,self.h+1),2)

def create_rect_str(x):   #function to create input str Rects
   rec = []
   w = Resolution.x * 0.165
   h = Resolution.y * 0.04
   j = 0
   a = 0
   for i in range(x):
      r = rect_((Resolution.x * 0.01) , (Resolution.y * 0.005) +  (h + (Resolution.y * 0.1) * i),w,h  )
      rec.append(r)
      a+= 1
   return rec

def create_rect_int(x): #Funciton to create int input Rects
   rec = []
   y = Resolution.y * 0.45
   w = Resolution.x * 0.032
   h = Resolution.x * 0.032
   for i in range (x):
      r = rect_(Resolution.x * 0.143, y  +  (h + (Resolution.y * 0.05) * i),w,h  )
      rec.append(r)
   return rec

def creat_cbox(x): #Function to create checkbox rects
   rec =[]
   y = Resolution.y * 0.64
   w = Resolution.x * 0.015
   h = Resolution.x * 0.012
   for i in range(x):
      r = rect_(Resolution.x * 0.15,y  +  (h + (Resolution.y * 0.05) * i),w,h )
      rec.append(r)
   return rec   


def get_text(text,rect,tela,num = False):  #Get input text
   
    font = pygame.font.Font(None,30)
    typing = True
    while typing:
      
      pygame.draw.rect(tela,white,rect)
      text_toblit = font.render(f"{text}",1,(0,0,0))    #Display rect while typing
      text_rect = text_toblit.get_rect()
      tela.blit(text_toblit,(rect.x + 2, rect.y + 2))
 
      if time.time() % 1 > 0.5:
            bar = pygame.Rect(rect.x + text_rect.w + 2, rect.y + 2,2,25)      #typing bar
            pygame.draw.rect(tela,(0,0,0),bar,) 
     
     
      for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:       #Get Keyboard ipunts
                  return text
              if event.key == pygame.K_BACKSPACE:
                  text = text [:-1]
              elif text_rect.w < rect.w - 5:
                 if num == True:
                  if event.unicode.isdigit() and text_rect.w < rect.w -10: 
                     text = text +  event.unicode        
                 else:
                    text = text +  event.unicode  

          if event.type == pygame.MOUSEBUTTONDOWN:         #Get mouse input and go off typing mode
             if not rect.collidepoint(event.pos):
                 return text
          elif event.type == pygame.QUIT:
              pygame.quit()
      pygame.time.wait(15)       
      pygame.display.update()


def busca(parameters,*text):    #Search Function
    global df
    text = list(text)
    final = df
    b = 0

    for i in text:   #text = text = filters
      if i != "":
          if type(i) == str :
            final  = final[final[parameters[b]].str.contains(i, regex=False)]        #filter by str boxes
                 
          elif parameters[b] == "Valor":          
               final = final[final[parameters[b]] < i]
               print(parameters[b],final)
       
          elif  type(i) == bool:      #Check box Filtering
              if i == True:
                  if parameters[b] == "Venda":
                     final = final[final["Tipo de Negócio"] == "Venda"] 
                  elif parameters[b] == "Arrendamento":
                     final = final[final["Tipo de Negócio"] == "Arrendamento"]    
                  else:
                     final = final[final[parameters[b]] != "N"]        
          else:
               final = final[final[parameters[b]] >= i]       #text Filter

      if final.empty:
                return final    #Return if no results  
      b+=1  
        
    return final

def create_icon_rect(size,x):  #rect for icones on result boxes
   rect = []
  
   for  a in range(size):
      y = (Resolution.y * 0.12) + (a *(Resolution.y * 0.16)) + 5
      r = rect_(x,y,25,25)
      rect.append(r)
   return rect   
   
def show_result(df,tela,browser_rect,local_rect,lixeira_rect,anotacoes_rect):
      font = pygame.font.Font(None, 25)
       
      for i in range(len(df.index)):
        pygame.draw.rect(tela,white,pygame.rect.Rect(Resolution.x * 0.2, Resolution.y * 0.015 + (i * (Resolution.y * 0.16) ),Resolution.x *0.79,Resolution.y *0.155))  #display Results
      
        info = df.iloc[i]
     
        text = font.render(f"Ref : {info.loc["Ref"]}",1,black)
        tela.blit(text,((Resolution.x * 0.2) + 5, (Resolution.y * 0.015 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f"Tipo : {info.loc["Tipo"]}",1,black)
        tela.blit(text,((Resolution.x * 0.3) + 5, (Resolution.y * 0.015 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f"Condomínio : {info.loc["Condomínio"]}",1,black)
        tela.blit(text,((Resolution.x * 0.6) + 5, (Resolution.y * 0.015 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f"Endereço : {info.loc["Endereço"]}, {info.loc["Freguesia"]} - {info.loc["Cidade"]}",1,black)
        tela.blit(text,((Resolution.x * 0.2) + 5, (Resolution.y * 0.05 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f"€ {info.loc["Valor"]}",1,black)
        tela.blit(text,((Resolution.x * 0.85) + 5, (Resolution.y * 0.05 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f"Locador : {info.loc["Locador"]}",1,black)
        tela.blit(text,((Resolution.x * 0.2) + 5, (Resolution.y * 0.085 + (i *(Resolution.y * 0.16))) + 5))
        tela.blit(icone.fone,((Resolution.x * 0.6) + 5, (Resolution.y * 0.082 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f" {info.loc["Fone"]}",1,black)
        tela.blit(text,((Resolution.x * 0.6) + 40, (Resolution.y * 0.092 + (i *(Resolution.y * 0.16))) + 5))

        tela.blit(icone.carrinho,((Resolution.x * 0.2) + 5, (Resolution.y * 0.12 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f"{info.loc["Garagem"]}",1,black)
        tela.blit(text,((Resolution.x * 0.2) + 30, (Resolution.y * 0.13 + (i *(Resolution.y * 0.16))) + 5))
        tela.blit(icone.banheiro,((Resolution.x * 0.25) + 5, (Resolution.y * 0.12 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f"{info.loc["Banheiros"]}",1,black)
        tela.blit(text,((Resolution.x * 0.25) + 30, (Resolution.y * 0.13 + (i *(Resolution.y * 0.16))) + 5))
        tela.blit(icone.quarto,((Resolution.x * 0.30) + 5, (Resolution.y * 0.12 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f"T{info.loc["T"]}",1,black)
        tela.blit(text,((Resolution.x * 0.3) + 30, (Resolution.y * 0.13 + (i *(Resolution.y * 0.16))) + 5))
        tela.blit(icone.areaconstruida,((Resolution.x * 0.35) + 5, (Resolution.y * 0.12 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f"{info.loc["Area Privativa"]}m²",1,black)
        tela.blit(text,((Resolution.x * 0.35) + 30, (Resolution.y * 0.13 + (i *(Resolution.y * 0.16))) + 5))
        tela.blit(icone.areaconstruida,((Resolution.x * 0.42) + 5, (Resolution.y * 0.12 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f"{info.loc["Area Construida"]}m²",1,black)
        tela.blit(text,((Resolution.x * 0.42) + 30, (Resolution.y * 0.13 + (i *(Resolution.y * 0.16))) + 5))
        
        if info.loc["Suite"] > 0:
           tela.blit(icone.suite,((Resolution.x * 0.5) + 5, (Resolution.y * 0.12 + (i *(Resolution.y * 0.16))) + 5))
           text = font.render(f"{info.loc["Suite"]}",1,black)
           tela.blit(text,((Resolution.x * 0.5) + 30, (Resolution.y * 0.13 + (i *(Resolution.y * 0.16))) + 5))
        if info.loc["Elevador"] == "S":
           tela.blit(icone.elevador,((Resolution.x * 0.55) + 5, (Resolution.y * 0.12 + (i *(Resolution.y * 0.16))) + 5))
        if info.loc["Pet Friendly"] == "S":
            tela.blit(icone.pet,((Resolution.x * 0.6) + 5, (Resolution.y * 0.12 + (i *(Resolution.y * 0.16))) + 5))
        if info.loc["Mobiliado"] != "N":
           tela.blit(icone.mobilia,((Resolution.x * 0.65) + 5, (Resolution.y * 0.12 + (i *(Resolution.y * 0.16))) + 5))
           text = font.render(f"{info.loc["Mobiliado"]}",1,black)
           tela.blit(text,((Resolution.x * 0.65) + 35, (Resolution.y * 0.13 + (i *(Resolution.y * 0.16))) + 5))
        text = font.render(f"{info.loc["Tipo de Negócio"]}",1,black)
        tela.blit(text,((Resolution.x * 0.85) + 5, (Resolution.y * 0.09 + (i *(Resolution.y * 0.16))) + 5))
  
        tela.blit(icone.browser,(browser_rect[i].x,browser_rect[i].y))
        tela.blit(icone.local,(local_rect[i].x,local_rect[i].y))
        tela.blit(icone.lixeira,(lixeira_rect[i].x,lixeira_rect[i].y))
        tela.blit(icone.anotacoes,(anotacoes_rect[i].x,anotacoes_rect[i].y))
        
        
def save_ask(tela):  #Display save window when close
    background = pygame.image.load("images/background.png")
    background = pygame.transform.scale(background,(Resolution.x* 0.4,Resolution.y * 0.3))
    sim_rect = pygame.rect.Rect(Resolution.x * 0.35, Resolution.y * 0.55,Resolution.x *0.1,Resolution.x*0.05)
    
    nao_rect = pygame.rect.Rect(Resolution.x * 0.55, Resolution.y * 0.55,Resolution.x *0.1,Resolution.x*0.05)
    back_center = background.get_rect(center=(Resolution.x * 0.5,Resolution.y * 0.5))
    font = pygame.font.Font(None,35)
    text = font.render("Deseja salvar as alterações ?",1,black)
    text_surface = text.get_rect(center=(Resolution.x/2,Resolution.y*0.4))
    
    text_sim = font.render("Sim",1,white)
    text_nao = font.render("Nao",1,white)
    sim_surface = text_sim.get_rect(center=(sim_rect.x + (sim_rect.w/2),sim_rect.y + (sim_rect.h/2)))
    nao_surfcae = text_sim.get_rect(center=(nao_rect.x + (nao_rect.w/2),nao_rect.y + (nao_rect.h/2)))
    while True:
      tela.blit(background,back_center)
      tela.blit(text,text_surface)
      pygame.draw.rect(tela,black,sim_rect,3)
      pygame.draw.rect(tela,black,nao_rect,3)
      tela.blit(text_sim,sim_surface)
      tela.blit(text_nao,nao_surfcae)
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              return
          if event.type == pygame.MOUSEBUTTONDOWN:
              if event.button == 1:
                  if sim_rect.collidepoint(event.pos):
                      df.to_csv("Dados de Imoveis.csv")
                      return        
                  elif nao_rect.collidepoint(event.pos):
                      return
                           
        
      pygame.time.wait(10)    
      pygame.display.update()


   
def main(): #Main funciton
  global df
  final = df #save dataframe in other variable
  tela = pygame.display.set_mode(Resolution.Resolution, pygame.RESIZABLE)
  pygame.display.set_caption("Banco de Imoveis by Vinicius")    #set screen properties
  background = pygame.image.load("images/background.png")
  background = pygame.transform.scale(background,Resolution.Resolution)   #background

  fonte = pygame.font.Font(None,30)    #input Box Font
  fonte_int = pygame.font.Font(None,25)#result Font and Annotations
  fonte2 = pygame.font.SysFont("Arial",50,italic= True) #italic font
  changes = False # see changes to save
 

  check_box = [False,False,False,False,False]    #check box declarations
  text_search = ["","","","","","","","",]       #search box declaration   
  search_rect = create_rect_str(5)
  search_rect.extend(create_rect_int(3))
  search_rect.extend(creat_cbox(5))              #create all rects
  
  

  filtros = ["Tipo","Cidade","Freguesia","Locador","Valor","Garagem", "Banheiros","T","Elevador","Pet Friendly","Mobiliado","Venda","Arrendamento"] #Boxes titles

  botao_busca = pygame.image.load("images/Busca_icone.png")
  botao_busca = pygame.transform.scale(botao_busca,(40,40))  #search button
  busca_rect = rect_(Resolution.x * 0.01,Resolution.y * 0.9,40,40) #search butao rect
  botao_reset = pygame.image.load("images/reset_button.png")
  botao_reset = pygame.transform.scale(botao_reset,(60,60))        # reset button
  reset_rect = rect_(busca_rect.x + busca_rect.w + 10,Resolution.y * 0.885,60,60) #reset rect
  bota_sair = pygame.transform.scale(pygame.image.load("images\sair_button.png"),(40,40))
  sair_rect = rect_(reset_rect.x + reset_rect.w +10,busca_rect.y,40,40)
  sem_resultado = pygame.rect.Rect(Resolution.x * 0.2,0,Resolution.x * 0.8,Resolution.y) #no result text rect
   
  hand_cursor = pygame.image.load("images/hand_cursor.png")
  hand_cursor = pygame.transform.scale(hand_cursor,(23,23))

  min = 0
  max = 6   #min and max rect to display
  mouse = True
  runing = True
  while runing == True:
   
   pos = pygame.mouse.get_pos() #get mouse position
   tela.blit(background,(0,0)) #blit background
   tela.blit(botao_busca,(busca_rect.x,busca_rect.y))  # blit buttons
   tela.blit(botao_reset,(reset_rect.x,reset_rect.y))
   tela.blit(bota_sair,(sair_rect.x,sair_rect.y))
   if not final.empty:  # print result if there is any result
           
      final_show = final[min:max] 
      browser_rect = create_icon_rect(len(final_show.index),Resolution.x * 0.92)
      lixeira_rect = create_icon_rect(len(final_show.index),Resolution.x * 0.95)
      local_rect = create_icon_rect(len(final_show.index),Resolution.x * 0.88)
      anotacoes_rect = create_icon_rect(len(final_show.index),Resolution.x*0.84)
      show_result(final_show,tela,browser_rect,local_rect,lixeira_rect,anotacoes_rect)       
   else :
     if time.time() % 1 > 0.5: 
      text = fonte2.render("Nenhum resultado encontrado",1,black)
      text_rect = text.get_rect(center = ((sem_resultado.x + sem_resultado.w +100)/2, (sem_resultado.y + sem_resultado.h - 200)/2))
      tela.blit(text,text_rect)
   z = 0
   a = 0
   for i in search_rect:   #display all filter rects
       if a <= 4:
      
         text = fonte.render(f"{filtros[a]}",1,white)
         text_surface = text.get_rect(center = ((i.x + i.w)/2,i.y - (i.h / 2)))
         tela.blit(text,text_surface)
         i.show(tela)
         text_toblit = fonte.render(f"{text_search[a]}",1,(0,0,0))
         tela.blit(text_toblit,(i.x + 2, i.y + 2))
     
       elif a <= 7:
          text = fonte_int.render(f"{filtros[a]}",1,white)
          tela.blit(text,(Resolution.x * 0.01, i.y + 4))
          i.show(tela) 
          text_toblit = fonte.render(f"{text_search[a]}",1,(0,0,0))
          tela.blit(text_toblit,(i.x + 2, i.y + 2))
       else: 
          text = fonte_int.render(f"{filtros[a]}",1,white)    
          tela.blit(text,(Resolution.x * 0.01, i.y  ))
          i.show(tela) 
   
       a+= 1
     
   for event in pygame.event.get():     #Get events
        mouse = True
        pos = pygame.mouse.get_pos()
       
        for i in range(len(browser_rect)):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if browser_rect[i].colide.collidepoint(pos):
                      
                       mouse = False                     
                       
            elif local_rect[i].colide.collidepoint(pos):
                       mouse = False
            elif lixeira_rect[i].colide.collidepoint(pos):
                  mouse = False      
            elif  anotacoes_rect[i].colide.collidepoint(pos):
                            
                  txt = final_show.iloc[i].loc["Anotações"]
                  if type(txt) == str:    #check if theres any text to show
                     txtall = []
                     txtsurface = []
                     mouse = False
                     show = True
                     line = int(len(txt) / 80)
                                         
                     for x in range(line + 1): #split text in lines
                         txtall.append(txt[x*80:(x+1)*80])
                         txtsurface.append(fonte_int.render(txt[x*80:(x+1)*80],0,white))

                     rect_wide = txtsurface[0].get_rect()
                     anot_rect  = pygame.rect.Rect(0,0,rect_wide.w + 10,((Resolution.y* 0.04) * line) + 10 ) # gets text length to set rectangle width
                     anot_rect.center = (Resolution.x/2,Resolution.y/2) 
                     back = pygame.transform.scale(pygame.image.load("images/back2.png"),(anot_rect.w,anot_rect.h)) 
                     pygame.draw.rect(tela,white,anot_rect)
                     tela.blit(back,(anot_rect.x,anot_rect.y))
                     pygame.draw.rect(tela,black,(anot_rect.x-1,anot_rect.y-1,anot_rect.w+2,anot_rect.h+2),3)
                     

                     for x in range(len(txtsurface)):
                         tela.blit(txtsurface[x],(anot_rect.x + 5,(anot_rect.y + 5) + (Resolution.y*0.03 * x)) )  #blit text

                     while show == True:  #shwo anotations while mouse is in position
                       for event in pygame.event.get():
                           if not anotacoes_rect[i].colide.collidepoint(pygame.mouse.get_pos()):  
                               show = False
                                     
                        
                       pygame.time.wait(10)
                       pygame.display.update()
           
        if event.type == pygame.MOUSEBUTTONDOWN:  # get mouse click
            if event.button == 1:
                a = 0
                for i in search_rect:
                    if i.colide.collidepoint(event.pos):
                       if a <=3:
                           text_search[a] = get_text(text_search[a],i.colide,tela)
                       elif a <=7:
                           text_search[a] = get_text(str(text_search[a]),i.colide,tela,True) 
                        
                           if text_search[a].isdigit():
                               text_search[a] = int(text_search[a])
                     
                       else:    
                          if i.colide.collidepoint(event.pos):
                              check_box[a - 8] =  not check_box[a - 8 ]
                              if i.color == white:
                                 i.color = blue
                              else:
                                 i.color = white 
                    a+= 1


                for i in range(len(browser_rect)):
                   if browser_rect[i].colide.collidepoint(event.pos):
                       url = final_show.iloc[i]["Link"]
                       webbrowser.open(url)
                   if local_rect[i].colide.collidepoint(event.pos):
                      urlmap = final_show.iloc[i]["Local"]
                      webbrowser.open(urlmap)
                   if lixeira_rect[i].colide.collidepoint(event.pos):
                      posdrop = i+min
                                  
                      df.drop([posdrop], axis=0,inplace = True  )
                      final = df
                      changes = True
                      pygame.time.wait(20)
                  
                   
                if busca_rect.colide.collidepoint(event.pos):
                  
                   final = busca(filtros,*text_search,*check_box)
                
            
                elif reset_rect.colide.collidepoint(event.pos):    #reset variables
                    text_search = ["","","","","","","","",]             
                    check_box = [False,False,False,False,False]
                    final = df
                elif sair_rect.colide.collidepoint(event.pos):
                    return
                    
            elif event.button == 4:
               if min > 0:
                min -= 1
                max -=1
            elif event.button == 5:
              if max < len(final.index):
               min +=1
               max +=1
                  
                        
        elif event.type == pygame.QUIT:
            if changes == True:         #ask for saving
                save_ask(tela)
            runing = False
   if not mouse:
        
          pygame.mouse.set_visible(False)
          tela.blit(hand_cursor,(pos[0] - 5,pos[1] - 2))    
   else:
           pygame.mouse.set_visible(True) 
         
   pygame.time.wait(10)
   pygame.display.update()

  pygame.quit()




if __name__ == "__main__":
  main()