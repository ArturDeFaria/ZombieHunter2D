import pygame
def gen_image(sheet,frame,w,h,rgb):
        img = pygame.Surface((w,h)).convert_alpha()    
        img.blit(sheet,(0,0), ((frame*w),0,w,h))
        img.set_colorkey(rgb)
        return img