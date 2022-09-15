
import pygame
import json

from Gen_img import gen_image

BLACK=(0,0,0)

class Personagem:

    MS=200 #millisegundos

    def __init__(self):
        
        self.idle=[]
        self.walk=[]
        self.run=[]
        self.attack=[]
        self.throw=[]
        self.hurt=[]
        self.frame=0
        self.estado="idle"
        self.acao="idle"              
        self.z=False
        self.acel=1
        self.acelMax=3
        self.acelfact=1.04
        self.vel=3
        self.area = pygame.Rect(0,0,0,0)
        self.pedra=0
        self.aux=0
        self.gatilho = pygame.Rect(0,0,0,0)
        self.frame_atk_ini=2
        self.frame_atk=0
        self.health_max=100
        self.health=self.health_max
        self.alvo=0
        self.id=""
        
    def get_dictio(self):
        
        dict= {
            'estado':self.estado,
            'z':self.z,
            'acel':self.acel,
            'area.x':self.area.x,
            'area.y':self.area.y,
            'area.w':self.area.w,
            'area.h':self.area.h,
            'pedra':self.pedra,
            'gatilho.x':self.gatilho.x,
            'gatilho.y':self.gatilho.y,
            'gatilho.w':self.gatilho.w,
            'gatilho.h':self.gatilho.h,
            'frame_atk_ini':self.frame_atk_ini,
            'frame_atk':self.frame_atk,
            'health_max':self.health_max,
            'health':self.health,
            'id':self.id
            
        }
        json_dict=json.dumps(dict, indent=4)
        return json_dict
    
    def dict_to_atrib(self,_json):
        
        dict=_json
        
        self.estado=dict['estado']
        self.z=dict['z']
        self.acel=dict['acel']
        self.area.x=dict['area.x']
        self.area.y=dict['area.y']
        self.area.w=dict['area.w']
        self.area.h=dict['area.h']
        self.pedra=dict['pedra']
        self.gatilho.x=dict['gatilho.x']
        self.gatilho.y=dict['gatilho.y']
        self.gatilho.w=dict['gatilho.w']
        self.gatilho.h=dict['gatilho.h']
        self.frame_atk_ini=dict['frame_atk_ini']
        self.frame_atk=dict['frame_atk']
        self.health_max=dict['health_max']
        self.health=dict['health']
        self.id=dict['id']
    
    def keys(self,teclado,largura,altura):
        
        if self.estado != "attack" and self.estado != "throw":
            if teclado[pygame.K_RIGHT]:                
                self.z=False #false para flip
                #onde quero ir nao ultrapassa os limites da tela, x nao pode ser maior que a largura da tela
                if  not (self.area.x+self.vel * self.acel)>largura - self.area.w: #deve se considerar W que é a largura do personagem
                    if (self.acel < self.acelMax): self.acel *= self.acelfact
                    self.area.x+=self.vel * self.acel

            if teclado[pygame.K_LEFT]:
                self.z=True #true para flipar(inverter horizontal)
                #onde quero ir nao ultrapassa os limites da tela, x nao pode ser menor que 0
                if not (self.area.x-self.vel *self.acel)<0:
                    if (self.acel < self.acelMax): self.acel *= self.acelfact
                    self.area.x-=self.vel *self.acel
            
            if teclado[pygame.K_UP]:
                #onde quero ir nao ultrapassa os limites da area na tela
                if not(self.area.y-self.vel*self.acel)<(altura-altura/3)-self.area.h:#uma margem ate onde posso subir
                    if(self.acel <self.acelMax):self.acel *= self.acelfact
                    self.area.y-=self.vel*self.acel
            
            if teclado[pygame.K_DOWN]:
                if not(self.area.y+self.vel*self.acel)>altura-100+self.area.h+10:#onde quero ir nao ultrapassa os limites da tela
                    if(self.acel <self.acelMax):self.acel *= self.acelfact
                    self.area.y+=self.vel*self.acel
    
    #set para carregar na memoria os arquivos sprite sheet png
    def set_idle(self,sheet,max_step,l,h,rgb):
        for step in range(max_step):
            self.idle.append(gen_image(sheet,step,l,h,rgb))
        
        
    def set_walk(self,sheet,max_step,l,h,rgb):
        for step in range(max_step):
            self.walk.append(gen_image(sheet,step,l,h,rgb))
       
            
    def set_run(self,sheet,max_step,l,h,rgb):
        try:
            for step in range(max_step):
                self.run.append(gen_image(sheet,step,l,h,rgb))
        except:
            print("No possui run Sheet...")
            
    def set_attack(self,sheet,max_step,l,h,rgb):
        try:
            for step in range(max_step):
                self.attack.append(gen_image(sheet,step,l,h,rgb))
                self.frame_atk_fim=len(self.attack)-1
        except:
            print("No possui ATTACK Sheet...")
    
    def set_throw(self,sheet,max_step,l,h,rgb):
        try:
            for step in range(max_step):
                self.throw.append(gen_image(sheet,step,l,h,rgb))
        except:
            print("No possui THROW Sheet...")
    
    def set_hurt(self,sheet,max_step,l,h,rgb):
        try:
            for step in range(max_step):
                self.hurt.append(gen_image(sheet,step,l,h,rgb))
        except:
            print("No possui Hurt Sheet...")
    
    def resize(self,Lar,Alt,flip_x,flip_y):
        
        #idle
        temp=[]
        for x in self.idle:
            temp.append(pygame.transform.flip(pygame.transform.scale(x, (Lar, Alt)).convert_alpha(),flip_x,flip_y))            
        self.idle = temp.copy()
        temp.clear()
        
        #walk
        for x in self.walk:
            temp.append(pygame.transform.flip(pygame.transform.scale(x, (Lar, Alt)).convert_alpha(),flip_x,flip_y))            
        self.walk = temp.copy()
        temp.clear()
            
        #run
        try:
            for x in self.run:
                temp.append(pygame.transform.flip(pygame.transform.scale(x, (Lar, Alt)).convert_alpha(),flip_x,flip_y))            
            self.run = temp.copy()
            temp.clear()
        except:
            print("No possui RUN anim...")
            
        #Attack
        try:
            for x in self.attack:
                temp.append(pygame.transform.flip(pygame.transform.scale(x, (Lar, Alt)).convert_alpha(),flip_x,flip_y))            
            self.attack = temp.copy()
            temp.clear()
        except:
            print("No possui ATTACK anim...")
            
        #Throw
        try:
            for x in self.throw:
                temp.append(pygame.transform.flip(pygame.transform.scale(x, (Lar, Alt)).convert_alpha(),flip_x,flip_y))            
            self.throw = temp.copy()
            temp.clear()
        except:
            print("No possui ATTACK anim...")
            
        #Hurt
        try:
            for x in self.hurt:
                temp.append(pygame.transform.flip(pygame.transform.scale(x, (Lar, Alt)).convert_alpha(),flip_x,flip_y))            
            self.hurt = temp.copy()
            temp.clear()
        except:
            print("No possui ATTACK anim...")
    
    def get_img(self,last_time,time):
        
        #Dictionary de estados
        if self.estado != "attack" and self.estado != "throw" and self.estado != "hurt":

            if self.acel > 1: 
                    if self.acel>2: self.estado="run"
                    else:self.estado="walk"
            else : self.estado="idle"
        
        try:
            
            if self.estado =="hurt":
                if time-last_time >= self.MS:
                    self.frame +=1 
                self.mod = self.frame % len(self.hurt)                
                self.acel=1
                if( self.frame == len(self.hurt)):
                    self.frame = 0
                    self.estado="idle"
                return self.hurt[self.mod]
            
            elif self.estado =="attack":
                
                if time-last_time >= self.MS:
                    
                    self.frame +=1 
                    self.frame_atk +=1 #contador de frame para sincronizar o gatilho do colisor de atk
                    self.frame_atk %= len(self.attack)                    
                    self.mod = self.frame % len(self.attack)
                if( self.frame == len(self.attack)):
                    self.frame = 0
                    self.frame_atk =0
                    self.estado="idle"
                #sincroniza o gatilho do colisor de atk
                if self.frame_atk == self.frame_atk_ini: 
                    if not self.z:self.gatilho = pygame.Rect(self.area.x+self.area.w,self.area.centery,(self.area.w*0.30),(self.area.h*0.25))
                    else: self.gatilho = pygame.Rect(self.area.x-10,self.area.centery,(self.area.w*0.30),(self.area.h*0.25))
                elif self.frame_atk == self.frame_atk_fim:
                    self.gatilho = pygame.Rect(self.area.centerx,self.area.centery,0,0)
                return self.attack[self.mod]
            
            elif self.estado =="throw":
                if time-last_time >= self.MS:
                    self.frame +=1 
                self.mod = self.frame % len(self.throw)
                if( self.frame == len(self.throw)):
                    self.frame = 0
                    self.estado="idle"
                return self.throw[self.mod]
    
            elif self.estado =="idle":  
                    if time-last_time >= self.MS:
                        self.frame +=1
                    self.mod = self.frame % len(self.idle)
                    return self.idle[self.mod]
            elif self.estado =="walk":
                    if time-last_time >= self.MS:
                        self.frame +=1
                    self.mod = self.frame % len(self.walk)
                    return self.walk[self.mod]
            elif self.estado =="run":
                    if time-last_time >= self.MS:
                        self.frame +=1
                    self.mod = self.frame % len(self.run)
                    return self.run[self.mod]
        except:
            print("anima padrao, algum frame nao pode ser exibido")
            return self.idle[1]
    
    def patch_finder(self):
        
        
        if not(self.area.colliderect(self.alvo.area)) and not self.estado=="attack" and not self.estado=="hurt":
            
            if (self.area.x - self.alvo.area.x) >0 :
                self.acel = 2
                self.area.x -= self.vel 
                self.z=True                       
            elif not (self.area.x - self.alvo.area.x) ==0: 
                self.acel = 2
                self.area.x += self.vel
                self.z=False
            
            if (self.area.y - self.alvo.area.y +self.alvo.area.h) >0 :
                self.area.y -= self.vel                        
            else: 
                self.area.y += self.vel
    
        elif not self.estado== "hurt":
           
            #inicio da anima de atk
            self.estado="attack"
            if self.acao != "cd":
                self.frame,self.frame_atk=0,0            
            self.acao="cd"
    
            if self.gatilho.colliderect(self.alvo.area):
                if self.aux == 0:
                    self.alvo.frame=0                                                                              
                    
            #fim            
            if self.frame_atk == len(self.attack)-1:
                self.frame,self.frame_atk=0,0
                self.acao="idle"
                self.estado="idle"                
                self.aux=0