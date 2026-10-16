import pygame
import math
import random
from collections import deque

gravity =pygame.Vector2(0,0)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60


def main():
    ARENA_CENTER=pygame.Vector2(400,300)
    ARENA_RADIUS = 250

    class Ball:
        def __init__(self, x, y, vx, vy, color, weapon):
            self.pos = pygame.Vector2(x,y)
            self.vel = pygame.Vector2(vx,vy)
            self.radius = 10
            self.hp = 100
            self.color = color
            self.weapon = weapon
            self.pos_history = deque(maxlen=20)

        def update(self):
            self.vel += gravity
            self.pos += self.vel
            self.pos_history.append(self.pos.copy())

            to_center = self.pos - ARENA_CENTER
            dist = to_center.length()
            if dist + self.radius >= ARENA_RADIUS:
                if dist != 0:
                    normal = to_center.normalize()
                    self.pos = ARENA_CENTER + normal*(ARENA_RADIUS-self.radius)

                    if self.vel.dot(normal)>0:
                        reflected = self.vel.reflect(normal)
                        variation = random.uniform(-10, 10)  # random angle in degrees
                        changed = reflected.rotate(variation)

                        # Keep the ball moving back into the arena
                        self.vel = changed if changed.dot(normal) < 0 else reflected
        def draw(self,surface):
            pygame.draw.circle(surface,self.color,(int(self.pos.x),int(self.pos.y)),self.radius,2)
            points = list(self.pos_history)
            for start, end in zip(points,points[1:]):
                pygame.draw.line(surface,self.color,start,end,3)


        def collide_with(self,other):
            between = other.pos - self.pos
            min_dist = other.radius + self.radius
            distance_sq = between.length_squared()

            if distance_sq>= min_dist**2:
                return
            if distance_sq==0:
                normal = pygame.Vector2(1,0)
                distance=0
            else:
                distance=distance_sq**0.5
                normal = between / distance

            overlap = min_dist - distance
            self.pos -= normal*(overlap/2)
            other.pos += normal*(overlap/2)
            speed_toward_each_other = (self.vel-other.vel).dot(normal)
            if speed_toward_each_other>0:
                impulse = normal * speed_toward_each_other
                self.vel -= impulse
                other.vel += impulse
            
    ball1 = Ball(150,200,7,5,(18,162,219),None)
    ball2 = Ball(175,350,5,5,(235,19,48),None)
    ball3 = Ball(500,300,6,5,(23,189,8),None)
    Balls = [ball1,ball2,ball3]
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame Project")
    clock = pygame.time.Clock()

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))
    
        for b in Balls:
            b.update()
            b.draw(screen)

        for i in range(len(Balls)):
            for j in range(i+1, len(Balls)):
                Balls[i].collide_with(Balls[j])

        
        pygame.draw.circle(screen,(255,255,255),ARENA_CENTER,ARENA_RADIUS,5)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
