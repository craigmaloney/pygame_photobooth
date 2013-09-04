import pygame
import pygame.camera
from pygame.locals import *
from datetime import datetime

TIMER_TICK = USEREVENT
SNAPSHOT = USEREVENT + 1
NINJA_SNAPSHOT = USEREVENT + 2

class Counter(pygame.sprite.Sprite):

    def __init__(self):
        self.countdown_in_progress = False
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.seconds = 0
        self.image = pygame.Surface([200, 200])
        self.rect = self.image.get_rect()
        self.rect.center = ((800, 150))

    def update(self):
        self.font = pygame.font.Font(('./ws_simple_gallifreyan.ttf'), 160)
        base = self.font.render(str(self.seconds), 1, (0, 0, 0))
        self.image = base
        top = self.font.render(str(self.seconds), 1, (0x66, 0x88, 0xbb))
        self.image.blit(top, (-3, -3))

    def initialize_snapshot(self):
        if self.countdown_in_progress is False:
            self.countdown_in_progress = True
            pygame.time.set_timer(TIMER_TICK, 1000)
            self.seconds = 3
            self.rect.center = ((350, 150))

    def countdown(self):
        self.seconds = self.seconds - 1
        if self.seconds <= 0:
            pygame.time.set_timer(TIMER_TICK, 0)
            self.countdown_in_progress = False
            self.seconds = 0
            self.rect.center = ((800, 150))
            pygame.event.post(pygame.event.Event(SNAPSHOT))


class Flash(pygame.sprite.Sprite):

    def __init__(self):
        self.countdown = 255
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.color = [255, 255, 255]
        self.image = pygame.Surface([640, 480], SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = ((0, 0))

    def update(self):
        if self.countdown >= 0:
            self.color = [self.countdown, self.countdown, self.countdown]
            self.image.fill(self.color)
            self.image.set_alpha(self.countdown)
            self.countdown = self.countdown - 10
        else:
            self.kill()


class Capture(object):
    def __init__(self):
        self.size = (640, 480)
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
        # if the camera has an image ready.  note that while this works on most
        # cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0, 0))
        all.update()
        dirty = all.draw(self.display)
        pygame.display.update(dirty)
        pygame.display.flip()

    def take_snapshot(self):
        filename = "screenshot_{datetime}.jpg".format(
            datetime=datetime.now().strftime('%s.%f'))
        pygame.image.save(self.display, filename)

    def main(self):
        going = True

        counter = pygame.sprite.Group()
        flash = pygame.sprite.Group()
        all = pygame.sprite.OrderedUpdates()

        Counter.containers = all, counter
        Flash.containers = all, flash

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

                if (e.type == TIMER_TICK):
                    countdown.countdown()

                # Flash photo
                if (e.type == SNAPSHOT):
                    self.take_snapshot()
                    Flash()
                    pygame.time.set_timer(NINJA_SNAPSHOT, 1000)

                # Ninja photo
                if (e.type == NINJA_SNAPSHOT):
                    self.take_snapshot()
                    pygame.time.set_timer(NINJA_SNAPSHOT, 0)

            self.get_and_flip(all)

if __name__ == "__main__":
    pygame.init()
    pygame.camera.init()
    a = Capture()
    a.main()
