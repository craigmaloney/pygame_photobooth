import pygame
import pygame.camera
from pygame.locals import *

class Counter(pygame.sprite.Sprite):

    def __init__(self):
        self.countdown_in_progress = False
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.seconds = 0
        self.image = pygame.Surface([200,200])
        self.rect = self.image.get_rect()
        self.rect.center = ((800,150))

    def update(self):
        self.font = pygame.font.Font(('./ws_simple_gallifreyan.ttf'), 160)
        self.image = self.font.render(str(self.seconds), 1, (0,0,0))

    def initialize_snapshot(self):
        if self.countdown_in_progress is False:
            self.countdown_in_progress = True
            pygame.time.set_timer(USEREVENT, 1000)
            self.seconds = 3
            self.rect.center = ((350,150))

    def countdown(self):
        print self.seconds
        self.seconds = self.seconds - 1
        if self.seconds <= 0:
            pygame.time.set_timer(USEREVENT, 0)
            self.countdown_in_progress = False
            self.seconds = 0
            self.rect.center = ((800,150))
            pygame.event.post(pygame.event.Event(USEREVENT + 1))

class Capture(object):
    def __init__(self):
        self.size = (640,480)
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)
        
        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()

        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self, all):
        # if you don't want to tie the framerate to the camera, you can check 
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        all.update()
        dirty = all.draw(self.display)
        pygame.display.update(dirty)
        pygame.display.flip()

    def take_snapshot(self):
        pygame.image.save(self.display, "screenshot.jpeg")


    def main(self):
        going = True

        counter = pygame.sprite.Group()
        all = pygame.sprite.OrderedUpdates()

        Counter.containers = all, counter

        countdown = Counter()
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False
                if (e.type == KEYDOWN and e.key == K_SPACE):
                    countdown.initialize_snapshot()

                if (e.type == USEREVENT):
                    countdown.countdown()

                if (e.type == USEREVENT+1):
                    self.take_snapshot()

            self.get_and_flip(all)

if __name__ == "__main__":
    pygame.init()
    pygame.camera.init()
    a = Capture()
    a.main()
