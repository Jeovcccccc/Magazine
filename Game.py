import pygame
from random import randint

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)

class Goods(pygame.sprite.Sprite):
    def __init__(self, x, speed, surf, score, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.score = score
        self.add(group)

    def update(self, *args):
        if self.rect.y < args[0] - 60:
            self.rect.y += self.speed
        else:
            self.kill()


w, h = 1600, 900
screen = pygame.display.set_mode((w, h))

#	Загружаются изображения, звуки и шрифты, используемые в игре
f = pygame.font.Font('fonts/Minecraft Rus NEW.otf', 30)
background = pygame.image.load('images/background.png').convert()
score = pygame.image.load('images/check.png').convert_alpha()
tel = pygame.image.load('images/tel.png')
end = pygame.image.load('images/end.png')
music = pygame.mixer.Sound('sounds/C418_-_Minecraft_30921694.mp3')
final_music = pygame.mixer.Sound('sounds/final.mp3')
t_rect = tel.get_rect(centerx=w//2, bottom=h-5)
k = 1

#   Задается скорость обновления экрана (FPS) и начальное значение счета игры.
clock = pygame.time.Clock()
FPS = 60
game_score = 0

#   Создается группа спрайтов goods.
goods_list = ({'path': 'apple.png', 'score': 100},
              {'path': 'banana.png', 'score': 150},
              {'path': 'orange.png', 'score': 200},
              {'path': 'strawberry.png', 'score': 250})
goods_surf = [pygame.image.load('images/'+data['path']).convert_alpha() for data in goods_list]
goods = pygame.sprite.Group()


#   выбирает изображение товара, устанавливает его позицию и скорость, возвращает объект Goods.
def createGoods(group):
    indx = randint(0, len(goods_surf)-1)
    x = randint(20, w-20)
    speed = randint(2, 8)

    return Goods(x, speed, goods_surf[indx], goods_list[indx]['score'], group)

speed = 15
createGoods(goods)


#   обрабатывает столкновение товаров с объектом tel и увеличивает счёт.
def collideGoods():
    global game_score
    for t in goods:
        if t_rect.collidepoint(t.rect.center):
            game_score += t.score
            t.kill()

while True:
    screen.blit(background, (0, 0))
    music.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT: #вызывает функцию createGoods.
            createGoods(goods)


#   перемещение объекта tel
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        t_rect.x -= speed
        if t_rect.x < 0:
            t_rect.x = 0
    elif keys[pygame.K_d]:
        t_rect.x += speed
        if t_rect.x > w-t_rect.width:
            t_rect.x = w-t_rect.width

#   окно победы
    if game_score > 5000:
        music.stop()
        if k == 1:
           final_music.play()
           k += 1


        background.blit(end, (500, 200))

    screen.blit(background, (0, 0))
    goods.draw(screen)
    screen.blit(score, (0, 0))
    sc_text = f.render(str(game_score), 1, ('black'))
    screen.blit(sc_text, (200, 10))
    screen.blit(tel, t_rect)
    pygame.display.update()

    clock.tick(FPS)

#методы update и collideGoods для обновления позиции товаров и обработки столкновений.
    goods.update(h)
    collideGoods()