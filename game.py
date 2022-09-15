import json
import random
import string
import threading
import pygame
import os
from Personagem import Personagem
from Udp import udp
from toJson import toJason

LARGURA, ALTURA = 480, 320
#LARGURA, ALTURA = 680, 420

JANELA = pygame.display.set_mode((LARGURA,ALTURA+100))
WHITE = (255,255,255)
BLACK = (0,0,0)
FPS = 15

CENARIO1_PNG=pygame.image.load(os.path.join('Recursos','City1','Bright','City1.png'))
CENARIO1 = pygame.transform.scale(CENARIO1_PNG, (LARGURA, ALTURA-ALTURA*0.15))
PAINEL01_PNG=pygame.image.load(os.path.join('Recursos','UI','Frames_Overlay_01.png'))
PAINEL01= pygame.transform.scale(PAINEL01_PNG, (LARGURA, 120))
PER_W=LARGURA*15//100
PER_H=ALTURA*15//100

#SPRITES_SHEET.PNG
sprite0 =pygame.image.load(os.path.join('Recursos','Dude_Monster','Rock1.png')).convert_alpha()
pedra_rect = sprite0.get_rect()
sprite0 =pygame.transform.scale(sprite0,(pedra_rect.w*3,pedra_rect.h*3))
sprite0_1 =pygame.image.load(os.path.join('Recursos','UI','heart.png')).convert_alpha()
sprite0_1 =pygame.transform.scale(sprite0_1,(pedra_rect.w*3,pedra_rect.h*3))

#Sprites Player1
sprite1 = pygame.image.load(os.path.join('Recursos','Dude_Monster','Dude_Monster_Idle_4.png')).convert_alpha() 
sprite2 = pygame.image.load(os.path.join('Recursos','Dude_Monster','Dude_Monster_Walk_6.png')).convert_alpha() 
sprite3 = pygame.image.load(os.path.join('Recursos','Dude_Monster','Dude_Monster_Run_6.png')).convert_alpha() 
sprite4_1 = pygame.image.load(os.path.join('Recursos','Dude_Monster','Dude_Monster_Attack1_4.png')).convert_alpha()
sprite4_2 = pygame.image.load(os.path.join('Recursos','Dude_Monster','Dude_Monster_Throw_4.png')).convert_alpha()
sprite4_3 = pygame.image.load(os.path.join('Recursos','Dude_Monster','Dude_Monster_Hurt_4.png')).convert_alpha()

#Sprites Player2
sprite1_2 = pygame.image.load(os.path.join('Recursos','Pink_Monster','Pink_Monster_Idle_4.png')).convert_alpha() 
sprite2_2 = pygame.image.load(os.path.join('Recursos','Pink_Monster','Pink_Monster_Walk_6.png')).convert_alpha() 
sprite3_2 = pygame.image.load(os.path.join('Recursos','Pink_Monster','Pink_Monster_Run_6.png')).convert_alpha() 
sprite4_1_2 = pygame.image.load(os.path.join('Recursos','Pink_Monster','Pink_Monster_Attack1_4.png')).convert_alpha()
sprite4_2_2 = pygame.image.load(os.path.join('Recursos','Pink_Monster','Pink_Monster_Throw_4.png')).convert_alpha()
sprite4_3_2 = pygame.image.load(os.path.join('Recursos','Pink_Monster','Pink_Monster_Hurt_4.png')).convert_alpha()

#Sprites Zombie
sprite5 = pygame.image.load(os.path.join('Recursos','Zombies','Male_Idle_15.png')).convert_alpha()
sprite6 = pygame.image.load(os.path.join('Recursos','Zombies','Male_Walk_10.png')).convert_alpha()
sprite7 = pygame.image.load(os.path.join('Recursos','Zombies','Male_Attack_8.png')).convert_alpha()
sprite8 = pygame.image.load(os.path.join('Recursos','Zombies','Male_Hurt_4.png')).convert_alpha()

pygame.font.init()
font = pygame.font.SysFont("comics sans ms",40)

class Pedras():
    
    def __init__(self,objeto,area):
        self.objeto=objeto
        self.area=area
        self.inicio=0
        self.final=ALTURA
        self.acel=1.25
    
    def get_dictio(self):        
        dict= {
                        
            'acel':self.acel,
            'area.x':self.area.x,
            'area.y':self.area.y,
            'area.w':self.area.w,
            'area.h':self.area.h,
            'inicio':self.inicio,            
            'final':self.final
            
        }
        json_dict=json.dumps(dict, indent=4)
        return json_dict
        
        
class Enemies(Personagem):
        
            
        def __init__(self):
            super().__init__()
            self.set_idle(sprite5,15,432,521,WHITE)
            self.set_walk(sprite6,10,432,521,BLACK)
            self.set_attack(sprite7,8,432,521,BLACK)
            self.set_hurt(sprite8,4,432,521,BLACK)
            self.resize(PER_W*1.05,PER_H*2,False,False)
            self.area=self.idle[0].get_rect()
            self.area=self.area.inflate(-20, -5)
            self.area.x=LARGURA-(PER_W*1.5)
            self.area.y=ALTURA-(PER_H*1.5)
            self.vel=1
            self.frame_atk_ini=2
            self.frame_atk_fim=5
            self.health_max=3
            self.health=3
            
        
        
        
        
con=udp()
terreno = pygame.Rect(0,ALTURA-100,LARGURA,100)
enemies=[]
objetos=[]
inventorio=[]
disparado=[]
def Renderizar():
    
    
    JANELA.fill((25,25,25))
    JANELA.blit(CENARIO1,(0,0))    
    
    a=0
    for obj in objetos:        
        JANELA.blit(obj.objeto,obj.area)
        
        
             
     
def main():
        
    batida = pygame.time.Clock()
    last_time = pygame.time.get_ticks()
    last_cd_time=pygame.time.get_ticks()
    cd_time=last_time
    
    
    #Configurações do player 1    
    p1 = Personagem()
    p1.set_idle(sprite1,4,32,32,BLACK)
    p1.set_walk(sprite2,6,32,32,BLACK)
    p1.set_run(sprite3,6,32,32,BLACK)
    p1.set_attack(sprite4_1,4,32,32,BLACK)
    p1.set_throw(sprite4_2,4,32,32,BLACK)
    p1.set_hurt(sprite4_3,4,32,32,BLACK)
    p1.resize(PER_W,PER_H,False,False)
    
    p1.vel=2
    p1.acelMax=4
    p1.acelfact=1.25
    p1.health_max=3
    p1.health =3
    p1.frame_atk_ini=1
    p1.frame_atk_fim=2      
    player=p1.idle[0]
    p1.area=player.get_rect()        
    p1.area=p1.area.inflate(-20, -5)       
    p1.area.center = terreno.center
    
    #Configurações do player 2    
    p2 = Personagem()
    p2.set_idle(sprite1_2,4,32,32,BLACK)
    p2.set_walk(sprite2_2,6,32,32,BLACK)
    p2.set_run(sprite3_2,6,32,32,BLACK)
    p2.set_attack(sprite4_1_2,4,32,32,BLACK)
    p2.set_throw(sprite4_2_2,4,32,32,BLACK)
    p2.set_hurt(sprite4_3_2,4,32,32,BLACK)
    p2.resize(PER_W,PER_H,False,False)
    
    p2.vel=2
    p2.acelMax=4
    p2.acelfact=1.25
    p2.health_max=3
    p2.health =3
    p2.frame_atk_ini=1
    p2.frame_atk_fim=2      
    player2=p2.idle[0]
    p2.area=player.get_rect()        
    p2.area=p2.area.inflate(-20, -5)       
    p2.area.center = terreno.center    
    
     
    desafio =1
    
    PEDRAS = pygame.event.custom_type()
    pygame.time.set_timer(PEDRAS, random.randrange(4000,10000))
    RESPAW = pygame.event.custom_type()
    t0=1000
    t1=3000
    pygame.time.set_timer(RESPAW,random.randrange(t0,t1))
    p1.acao="idle"
    rodar = True 
    
    comeco = True
    respaw=True 
    
    t2 = threading.Thread(target=con.conectar)
    
    try:t2.start()
    except:print("Server fora de alcance")
    listona=[]    
    while rodar:
        
        batida.tick(FPS)
        
        if con.pareado:
            #SERIALIZA OS OBJTOS PARA SEREM ENVIADOS
            toJ = toJason()
            p1_json=p1.get_dictio()
            send_json=toJ.list_obj_not__dict(enemies,"enemies")
            send_json=toJ.list_obj_not__dict(objetos,"objetos")
            send_json=toJ.add_to_list(p1_json,"player")
            try:con.send(send_json)
            except:print("Peer desconectou")
            #PEGA A ULTIMA MSG RECEBIDA DESERIALIZA PARA OS OBJETOS
            
            try:
                listona = toJ.dic_list(con.last_msg,('enemies','objetos','player'))
                p2.dict_to_atrib(listona[2])
            except:pass
            
   
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                rodar = False 
            elif eventos.type ==PEDRAS:
                aleatorio = random.randrange(terreno.x,terreno.w)
                pedra_sprite=sprite0
                pedra_area=pedra_sprite.get_rect()
                pedra_area.x=aleatorio
                pedra= Pedras(pedra_sprite,pedra_area)
                pedra.final = random.randrange(terreno.top+pedra_area.h,terreno.bottom-pedra_area.h)
                objetos.append(pedra)
            elif eventos.type ==RESPAW:
                    
                    aleatorio = random.randrange(0,2)                    
                    if aleatorio == 0:
                        _x=terreno.x+PER_W*1.05
                    else:  _x=terreno.w-PER_W*1.05
                    
                    e = Enemies()
                    e.area.x=_x
                    e.alvo=p1
                    for _ in range(5):
                        e.id+=random.choice(string.ascii_letters)
                        e.id+=str(random.randrange(0,10))
                    #e.area.y= random.randrange((terreno.y+e.area.h),(terreno.h-e.area.h))
                    if len(enemies)<desafio and respaw:
                        enemies.append(e)
                        comeco = False
                    
                    if con.pareado:
                        
                        repetido = False
                        try:
                            for peer in listona[0]:
                                d = json.loads(peer)                            
                                for each in enemies:
                                    if d['id'] == each.id:
                                        repetido = True
                                if not repetido:                                
                                    e = Enemies()
                                    e.dict_to_atrib(d)                                
                                    e.alvo=p2
                                    enemies.append(e)
                        except:pass
                                     
                        
                    elif len(enemies)==0:respaw = True
                    else:respaw=False 
                    
                        
                
                
            elif eventos.type==pygame.KEYDOWN:
                if eventos.key==pygame.K_SPACE:                    
                    pass
            
            elif eventos.type == pygame.KEYUP:
                if eventos.key==pygame.K_SPACE:
                    
                    if p1.acao != "cd":
                        p1.frame,p1.frame_atk=0,0
                        p1.estado="attack"                       
                        if not p1.z:
                            p1.gatilho = pygame.Rect(p1.area.x+p1.area.w,p1.area.centery,(p1.area.w*0.10),(p1.area.h*0.25))
                        else:p1.gatilho = pygame.Rect(p1.area.x-10,p1.area.centery,(p1.area.w*0.10),(p1.area.h*0.25))
                        for each in enemies:
                            if p1.gatilho.colliderect(each.area) or p1.gatilho.colliderect(each.gatilho):                            
                                each.frame=0
                                each.estado="hurt"
                                p1.frame,p1.frame_atk=0,0
                                p1.estado="attack" 
                                each.health -=1
                                p1.acao="cd"
                                last_cd_time=pygame.time.get_ticks()
                        
                    
                    #cata pedras
                    for each in objetos:
                        if p1.area.colliderect(each.area):
                            p1.estado = "attack"
                            p1.acao="cd"
                            last_cd_time=pygame.time.get_ticks()
                            inventorio.append(each)
                            objetos.remove(each)
                    
                        
                    if len(inventorio)>0 and p1.acao !="cd":
                        p1.frame=0
                        p1.estado="throw"
                        obj=inventorio.pop(0)
                        obj.area.center=p1.area.center
                        obj.inicio=obj.area.x
                        if p1.z == False: obj.final=LARGURA
                        else: obj.final=0
                        disparado.append(obj)
                        p1.acao="cd"
                        last_cd_time = pygame.time.get_ticks()
                                           
        teclado = pygame.key.get_pressed()
        

        if p1.acao=="cd":
            cd_time=pygame.time.get_ticks()
        if p1.acao!="idle" and cd_time - last_cd_time >= 1000  :
            p1.acao ="idle"
            last_cd_time = cd_time 
               
        if not any(pygame.key.get_pressed()):
            if p1.acel>1 : p1.acel=1
        else: 
            p1.keys(teclado,LARGURA,ALTURA)            
            pass 
  
        time =pygame.time.get_ticks()

        player=p1.get_img(last_time,time)
        player2=p2.get_img(last_time,time)
                        
        try:
            Renderizar()
                
            #pedras caindo
            for obj in objetos:
                
                if obj.area.y +3 * obj.acel < obj.final:
                    obj.acel *=1.15
                    obj.area.y +=3 * obj.acel
                else :obj.acel = 1.25
                
                if obj.acel > 1.25:
                    if obj.area.colliderect(p1.area):
                        p1.frame=0
                        p1.estado="hurt"
                        objetos.remove(obj)
                        p1.health -=1
                    else:
                        for each in enemies:
                            if obj.area.colliderect(each.area):
                                each.frame=0
                                each.estado="hurt"
                                each.health -=1
                                objetos.remove(obj)
                
            for each in disparado:#movimentação do projetil horizontalmente
                
                if not each.inicio == each.area.x: #Sincroniza dando um atraso no render do projetil 
                    JANELA.blit(each.objeto,each.area)
                    each.acel *=1.15
                    if each.final == LARGURA:each.area.x +=4* each.acel
                    else:each.area.x -=4* each.acel
                    if each.area.x > LARGURA: disparado.remove(each)
                else:                
                    if p1.frame >=2: #primeiro quadro a ser desenhado do projetil apartir do segundo frame da animação
                        JANELA.blit(each.objeto,each.area)
                        each.acel *=1.15
                        if each.final == LARGURA:each.area.x +=4* each.acel
                        else:each.area.x -=4* each.acel
                
                for enemy in enemies: #verifica colisão 
                    if each.area.colliderect(enemy.area):
                        enemy.frame=0
                        enemy.estado="hurt"
                        enemy.health -=1
                        disparado.remove(each)

            if len(enemies)==0 and not comeco:                
                desafio +=1
                p1.health_max +=1
                p1.health = p1.health_max
                if t1-desafio*100 == t0:t1=2000
                else:t1-=desafio*100
                comeco = True
            for each in enemies: #renderiza todos inimigos da lista
                JANELA.blit(pygame.transform.flip(each.get_img(last_time,time), each.z, False),(each.area.inflate(20,10)))#"desenha o inimigo"
                pygame.draw.rect(JANELA, (0,255,0), (each.gatilho), 1)#colisor da "mão"
                pygame.draw.rect(JANELA, (255,0,0), (each.area), 1)#colisor zoombie 
                each.patch_finder()
                if p1.area.colliderect(each.gatilho):
                    if each.aux==0:
                        p1.frame =0
                        p1.health -=1  
                        p1.estado="hurt"
                        each.aux=1
                        
                    
                if  each.health == 0:                    
                    enemies.remove(each)
            pygame.draw.rect(JANELA, (0,255,0), (p1.gatilho), 1)#colisor do gatilho de ação do personagem        
            pygame.draw.rect(JANELA, (0,255,0), (p1.area), 1)#colisor_personagem
            #O inflate na definição da area(-20,-5) e no blit(20,10) faz com que ajuste a area no tamanho envolta do personagem
            
            #PLayer2
            if con.pareado:
                JANELA.blit(pygame.transform.flip(player2, p2.z, False),(p2.area.inflate(20,10)))#Personagem desenhado na tela com flip se Z for true
            #Player1
            JANELA.blit(pygame.transform.flip(player, p1.z, False),(p1.area.inflate(20,10)))#Personagem desenhado na tela com flip se Z for true
            
            if time - last_time >= p1.MS :last_time = time        
            
            painel_area=PAINEL01.get_rect()
            painel_area.x=0
            painel_area.y=ALTURA
            JANELA.blit(PAINEL01,(painel_area))
            heart_area=sprite0_1.get_rect()
            heart_area.centery = painel_area.centery
            heart_area.x=painel_area.x+heart_area.w
            heart_area.y-=heart_area.h
            for x in range(p1.health):
                heart_area.x=x*(heart_area.w+5)+5
                JANELA.blit(sprite0_1,heart_area)
            

            texto ="" + str(len(inventorio))
            texto=font.render(texto, 1,(0,0,255))
            pedra_ico =pygame.transform.scale(sprite0, (pedra_rect.w*4,pedra_rect.h*4) )
            pedra_ico_rect =pedra_ico.get_rect()
            pedra_ico_rect.center = painel_area.center
            texto_rect = texto.get_rect()
            texto_rect.center = pedra_ico_rect.center
            JANELA.blit( pedra_ico,pedra_ico_rect)
            JANELA.blit(texto, (texto_rect))
            pygame.draw.rect(JANELA,(WHITE),(p1.gatilho.w,p1.gatilho.h,1,1),100)
        except:
            print("ops! algum erro no main")
        pygame.display.update() 
    pygame.quit()
   
if __name__ == "__main__": 
    main()

        
    
    
    
    
    



