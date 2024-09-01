import pygame
import time,re
import pandas as pd

pygame.init()
pygame.font.init()

class colors:  #set colors
   def __init__(self):
      self.white = (255,255,255)
      self.black = (0,0,0)
      self.blue = (0,0,255)
cor = colors()


class fontes:   #class for fonts
   def __init__(self) :
      pass
   def fonte(self,x):
      return pygame.font.SysFont("Arial",x)
fonte = fontes()   
             
class resolution: #class for resolution
   def __init__(self):
      self.x = 1024
      self.y = 720
      self.resolution = (self.x,self.y)
res = resolution()      


class rect_:   #class for create rects
   def __init__(self,x,y,w,h,name,num):
      self.x = x
      self.h = h
      self.y = y
      self.w = w
      self.rect = pygame.rect.Rect(self.x,self.y,self.w,self.h)
      self.center = self.rect.center
      self.cor = cor.white
      self.font2 = fonte.fonte(25)
      self.linha = 0
      self.num = num
           
      self.textlen = [0,0,0,0,0,0,0,0,0,0,0,0]
      if type(self.num )== bool:    #check if is not a check box
        if self.num == False: 
         self.text = ""
        else:
           self.text = "0" 
          
      else:
         self.text = "N"     
      self.name = name
      self.font = fonte.fonte(25)
      if self.name == "Anotações":  # check if anotation
         self.font = fonte.fonte(22)
       
   def show(self,tela):  # function in class to display rects
      
      pygame.draw.rect(tela,self.cor,self.rect) 
      pygame.draw.rect(tela,cor.black,self.rect,1) 
      self.textp = str(self.text)
      font = self.font
      
      text = font.render(f"{self.name}",0,cor.black)
      if type(self.num) == bool: #check if its not a check box
    
       text_center = text.get_rect(center=(self.x + (self.w/2),self.y - res.y*0.02))
       tela.blit(text,text_center)
       if self.name != "Anotações":  #check if is anotation

          self.inside_text = self.font2.render(self.textp[:int(self.w/12)],0,cor.black)
          tela.blit(self.inside_text,(self.x +2,self.y+1))
       else:
        
        
         t = font.render(self.textp,0,cor.black)
         textp_surface = t.get_rect()
         
         self.linha = int(textp_surface.w /800) 
         self.textlen[self.linha + 1] = len(self.text)
 
         for i in range(self.linha + 1):     #Jump lines
          
            if i >= len(self.textlen ) - 1:
               return

            if  self.linha > 0 and i < self.linha:
              
               self.inside_text = self.font2.render(self.textp[self.textlen[i]:self.textlen[i+1] ],0,cor.black)
            else:
               self.inside_text = self.font2.render(self.textp[self.textlen[i]:],0,cor.black)
            tela.blit(self.inside_text,(self.x +2,self.y +1 + (i*20) )) 
         
      else: 
     
        tela.blit(text,(self.x - len(self.name)*14,self.y -5 ) )
    
   def color_change(self):  #check box color change
      if self.cor == cor.white:
         self.cor = cor.blue
         self.text = "S"
      else:
         self.cor =cor.white
         self.text = "N"   
   

def get_text(caixas,tela,i): #get input
   box = caixas[i]
   font = pygame.font.Font(None,30)
   if type(box.num) != bool: # if its a check box
          box.color_change()
        
          return
   else:
    typing = True

    while True: #type looping
     
      box.show(tela)
      text_rect = box.inside_text.get_rect()
    
      if time.time() % 1 > 0.5:
            bar = pygame.Rect(box.x + text_rect.w + 2, box.y  +5 + (box.linha * 17),2,23)
            
            pygame.draw.rect(tela,(0,0,0),bar,) 

      if box.name == "Tipo de Negócio":   #create a drop box for "Tipo de Negocio"
      
           window_rect = pygame.rect.Rect(box.x,box.y + box.h,box.w + 1,box.h +1)
           pygame.draw.rect(tela,cor.white,window_rect)
           window_rect2 = pygame.rect.Rect(window_rect.x,window_rect.y + window_rect.h,window_rect.w,window_rect.h)
           pygame.draw.rect(tela,cor.white,window_rect)
           pygame.draw.rect(tela,cor.black,(window_rect.x - 1,window_rect.y -1,(window_rect.w ) + 2,(window_rect.h *2) ),2)
           
           text1 = font.render("Arrendamento",0,cor.black)
           text2 = font.render("Venda",0,cor.black)
           tela.blit(text1,(window_rect.x +2,window_rect.y+5) )
           tela.blit(text2,(window_rect2.x +2,window_rect2.y+5) )
           typing = False
               
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            pygame.quit()
         if event.type == pygame.MOUSEBUTTONDOWN:
            if typing == False:
             if window_rect.collidepoint(event.pos):
               box.text = "Arrendamento"
               return
             elif  window_rect2.collidepoint(event.pos):
               box.text = "Venda" 
               return  
            if not box.rect.collidepoint(event.pos):
               return 
            
         if event.type == pygame.KEYDOWN and typing == True:
            if event.key == pygame.K_TAB and i < 16:
               box.show(tela)
               text_rect = box.inside_text.get_rect()
               get_text(caixas,tela,i+1)
               return
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
              
               return 
           
            elif event.key==pygame.K_BACKSPACE:
                  box.text = str(box.text)
                  box.text = box.text [:-1]   
               
            elif box.num == True :
               if event.unicode.isdigit():
                  box.text = str(box.text)
                  box.text = int( box.text + event.unicode)
            
            else:  
                 if len(box.text) < 701: 
                  box.text = box.text + event.unicode
               
           
           
      pygame.time.wait(10)                       
      pygame.display.update()

def save(box,tela):  #save new register
   parametros = {}
   df_base = pd.read_csv("Dados de Imoveis.csv",index_col =False)
   ref_inicial = df_base["Ref"].iloc[-1] 
   parametros["Ref"] = [ref_inicial + 1]
 
   for i in box:
      if i.text == "":
         text = "-"
      else:
         text = i.text   
      
      parametros[i.name] = [text]
      
   df_novo = pd.DataFrame.from_dict(parametros)   
   df_novo = pd.concat([df_base,df_novo], ignore_index=True)
   df_novo.to_csv("Dados de Imoveis.csv", index = False)
   df_base = pd.read_csv("Dados de Imoveis.csv",index_col =False)
   check = df_novo.compare(df_base)

   background = pygame.image.load("images/back2.png")
   background = pygame.transform.scale(background,(res.x* 0.5,res.y * 0.3))
   ok_rect = pygame.rect.Rect(res.x * 0.35, res.y * 0.55,res.x *0.1,res.x*0.05)
   ok_rect.center = (res.x/2,res.y/2)
   
   back_center = background.get_rect(center=(res.x * 0.5,res.y * 0.5))
   font = pygame.font.Font(None,35)

   if not check.empty:   
    text = font.render("As informaçoes foram salvas",1,cor.black)
   else:
     text = font.render("Não foi possivel salvar as alteraçoes",1,cor.black)   
   text_surface = text.get_rect(center=(res.x/2,res.y*0.4))
    
   text_ok = font.render("OK",1,cor.black)
   ok_surface = text_ok.get_rect(center=(ok_rect.x + (ok_rect.w/2),ok_rect.y + (ok_rect.h/2)))
   
   while True:
   
      tela.blit(background,back_center)
      tela.blit(text,text_surface)
      if  check.empty:
         pygame.draw.rect(tela,cor.black,ok_rect,3)
         tela.blit(text_ok,ok_surface)
      else:
         tela.blit(background,back_center)
         tela.blit(text,text_surface)
         
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              return
          if event.type == pygame.MOUSEBUTTONDOWN:
              if event.button == 1:
                  if ok_rect.collidepoint(event.pos):
                      
                      return        
                 
                           
        
      pygame.time.wait(10)    
      pygame.display.update()   
      if not check.empty:
         pygame.time.wait(2000)
         return
  
  


def main():
  tipo = rect_(res.x*0.04,res.y*0.12,res.x*0.2,res.y*0.05,"Tipo",False)
  t = rect_(tipo.x + 10 + tipo.w,tipo.y,res.x*0.05,res.y*0.05,"T",False)
  condominio = rect_(t.x + t.w+ 10,tipo.y,res.x*0.2,res.y*0.05,"Condomínio",False)
  cidade = rect_(condominio.x + condominio.w+ 10,tipo.y,res.x*0.2,res.y*0.05,"Cidade",False)
  freguesia = rect_(cidade.x + cidade.w+ 10,tipo.y,res.x*0.2,res.y*0.05,"Freguesia",False)
  endereco = rect_(res.x*0.04,tipo.y + 35 + tipo.h,res.x*0.47,res.y*0.05,"Endereço",False)
  locador =  rect_(condominio.x + condominio.w+ 10,endereco.y,res.x*0.2,res.y*0.05,"Locador",False)
  fone = rect_(cidade.x + cidade.w+ 10,endereco.y,res.x*0.2,res.y*0.05,"Fone",False)
  valor = rect_(tipo.x,endereco.y + 35 + endereco.h,res.x*0.2,res.y*0.05,"Valor",True)
  negociacao = rect_(t.x,valor.y,res.x*0.2,res.y*0.05,"Tipo de Negócio",False)
  maps = rect_(negociacao.x + negociacao.w + 10,valor.y,res.x*0.47,res.y*0.05,"Local",False)
  link = rect_(tipo.x,valor.y+valor.h+35,res.x*0.89,res.y*0.05,"Link",False)
  banhos = rect_(res.x * 0.06,link.y + link .h + 35,res.x*0.05,res.y*0.05,"Banheiros",True)
  suites = rect_(banhos.x + res.x*0.19,banhos.y,res.x*0.05,res.y*0.05,"Suite",True)
  garagem = rect_(suites.x+ res.x*0.19,banhos.y,res.x*0.05,res.y*0.05,"Garagem",True)
  apv = rect_(garagem.x + res.x*0.19,banhos.y,res.x*0.05,res.y*0.05,"Area Privativa",True)
  acn = rect_(apv.x + res.x*0.19,banhos.y,res.x*0.05,res.y*0.05,"Area Construida",True)
  pet = rect_(res.x * 0.35,banhos.y + banhos.w + 20,res.x*0.015,res.x*0.015,"Pet Friendly","Box") 
  elevador = rect_(pet.x + res.x* 0.2,banhos.y + banhos.w + 20,res.x*0.015,res.x*0.015,"Elevador","Box") 
  mobilia = rect_(elevador.x + res.x* 0.2,banhos.y + banhos.w + 20,res.x*0.015,res.x*0.015,"Mobiliado","Box")
  anotacao = rect_(tipo.x,res.y*0.7,res.x*0.9,res.y*0.27,"Anotações",False)  
  caixas = [tipo,t,condominio,cidade,freguesia,endereco,locador,fone,valor,negociacao,maps,link,banhos,suites,garagem,apv,acn,pet,elevador,mobilia,anotacao]
  
  salvar_icone = pygame.transform.scale(pygame.image.load("images/salvar.png"),(50,50))
  salvar_rect = pygame.rect.Rect(res.x * 0.04,res.y * 0.01,50,50)
  reset_icone = pygame.transform.scale(pygame.image.load("images/reset_button.png"),(60,60))
  reset_rect = pygame.rect.Rect(res.x * 0.1,res.y * 0.009,60,60)
  sair_icone = pygame.transform.scale(pygame.image.load("images/sair_button.png"),(60,60))
  sair_rect = pygame.rect.Rect(res.x * 0.87,res.y * 0.009,60,60)
  borracha_icone = pygame.transform.scale(pygame.image.load("images/Borracha.png"),(60,60))
  borracha_rect = pygame.rect.Rect(anotacao.w + anotacao.x + 2,anotacao.y,60,60)

  tela = pygame.display.set_mode(res.resolution,pygame.RESIZABLE)
  pygame.display.set_caption("Dados Imobiliarios")
  background = pygame.transform.scale(pygame.image.load("images/background.png"),res.resolution)
  
  while True:  
   
    tela.blit(background,(0,0))
    tela.blit(salvar_icone,salvar_rect)
    tela.blit(reset_icone,reset_rect)
    tela.blit(sair_icone,sair_rect)
    tela.blit(borracha_icone,borracha_rect)
    pygame.draw.rect(tela,cor.white,anotacao.rect)
    for i in caixas:
        i.show(tela)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
           if event.key== pygame.K_ESCAPE:
              return
        if event.type == pygame.QUIT:
            return
        if event.type==pygame.MOUSEBUTTONDOWN:
           if event.button == 1:
              if reset_rect.collidepoint(event.pos):
                 for i in caixas:
                    if type(i.num) == bool:
                     i.text = ""
                    else:
                       i.cor = cor.white 
                       i.text = "N"
              elif salvar_rect.collidepoint(event.pos):
                 save(caixas,tela)
                 main()
                 return
              elif borracha_rect.collidepoint(event.pos):
                 anotacao.text = ""
              elif sair_rect.collidepoint(event.pos)   :
                 return
              for i in range(len(caixas)):
                 if caixas[i].rect.collidepoint(event.pos):
                  
                    get_text(caixas,tela,i)
                  


    pygame.time.wait(10)    
    pygame.display.update()

if __name__ == "__main__":
    main()