import pygame
import pygame.image
import buscar_imoveis,cadastro

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial",30)
class resolution:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.resolution = (self.x,self.y)

res = resolution(1024,720)
tela = pygame.display.set_mode(res.resolution)
class icone:
   def __init__(self,path,x,y,w,h,text) :
      self.icon = pygame.transform.scale(pygame.image.load(path),(w,h))
      self.x = x
      self.y = y
      self.text = text
      self.rect = pygame.rect.Rect(self.x,self.y,w,h)
   def display(self):
   
      tela.blit(self.icon,(self.x,self.y))
      text = font.render(self.text,0,(255,255,255))
     
      text_surface = text.get_rect(center= (self.x + (self.rect.w/2),self.y + self.rect.w + 5 ))
      tela.blit(text,text_surface)
def main():

  sair = icone("images/sair_button.png",res.x*0.7,res.y*0.25,80,80,"Sair")
  adicionar = icone("images/adicao.png",res.x * 0.48,res.y*0.25,80,80,"Adicionar Imoveis")
  background = pygame.transform.scale(pygame.image.load("images/background.png"),res.resolution)
  procurar = icone("images/buscar_casa.png",res.x*0.26,res.y*0.25,80,80,"Procurar Imoveis")
  hand_cursor = pygame.transform.scale(pygame.image.load("images/hand_cursor.png"),(23,23))
  pygame.display.set_caption("Banco de Imoveis by Vinicius")
  mouse = True
  while True:  
    tela.blit(background,(0,0))  
    sair.display()  
    adicionar.display()
    procurar.display()

    for event in pygame.event.get():
      pos = pygame.mouse.get_pos()
      mouse = True
      if event.type == pygame.QUIT:
          return
      if procurar.rect.collidepoint(pygame.mouse.get_pos()):
         mouse = False
         if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
               pygame.mouse.set_visible(True)
               buscar_imoveis.main()
      if adicionar.rect.collidepoint(pygame.mouse.get_pos()):
         mouse = False   
         if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
               pygame.mouse.set_visible(True)
               cadastro.main()
      if sair.rect.collidepoint(pygame.mouse.get_pos()):
         mouse = False   
         if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
               return
  
    pygame.mouse.set_visible(mouse)
    if not mouse:
       tela.blit(hand_cursor,(pos[0] - 5,pos[1] - 2)) 
   
          
    pygame.time.wait(10)  
    pygame.display.update()  
      
if __name__ == "__main__":
   main()