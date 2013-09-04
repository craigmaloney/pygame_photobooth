import pygame
import pygame.camera
from pygame.locals import *
from datetime import datetime

TIMER_TICK = USEREVENT
SNAPSHOT = USEREVENT + 1
NINJA_SNAPSHOT = USEREVENT + 2
ATTRACT_MODE = USEREVENT + 3
RESOLUTION = (640, 480)
OFFSCREEN = (800, 480)


class Counter(pygame.sprite.Sprite):

    def __init__(self):
        self.countdown_in_progress = False
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.seconds = 0
        self.image = pygame.Surface([200, 200])
        self.rect = self.image.get_rect()
        self.rect.center = (OFFSCREEN)

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
            self.rect.center = (OFFSCREEN)
            pygame.event.post(pygame.event.Event(SNAPSHOT))


class Status(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface([200, 200])
        self.rect = self.image.get_rect()
        self.original_position = (640, 630)
        self.rect.bottomright = (self.original_position)

    def update(self):
        text = datetime.now().strftime("%s")
        self.font = pygame.font.Font(('./ws_simple_gallifreyan.ttf'), 20)
        base = self.font.render(str(text), 1, (0, 0, 0))
        self.image = base
        top = self.font.render(str(text), 1, (0x66, 0x88, 0xbb))
        self.image.blit(top, (-1, -1))

    def attract(self):
        self.rect.bottomright = (self.original_position)

    def hide(self):
        self.rect.topleft = (OFFSCREEN)


class Flash(pygame.sprite.Sprite):

    def __init__(self):
        self.countdown = 255
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.color = (255, 255, 255, 128)
        self.image = pygame.Surface(RESOLUTION, SRCALPHA)
        self.image.fill(self.color)
        self.image.set_alpha(self.countdown)
        self.rect = self.image.get_rect()
        self.rect.topleft = ((0, 0))

    def update(self):
        if self.countdown >= 0:
            self.color = (255,255,255,self.countdown)
            self.image.fill(self.color)
            self.image.set_alpha(self.countdown)
            self.countdown = self.countdown - 10
        else:
            self.kill()


class LastImage(pygame.sprite.Sprite):

    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.countdown = 255
        new_image = pygame.transform.smoothscale(image, (640 / 4, 480 / 4))
        self.image = new_image
        self.image.set_alpha(self.countdown)
        self.rect = self.image.get_rect()
        self.rect.topleft = ((0, 0))

    def update(self):
        if self.countdown >= 0:
            self.image.set_alpha(self.countdown)
            self.countdown = self.countdown - .1
        else:
            self.kill()

class ConsoleOverlay(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.alpha_channel = 60
        self.counter = 0
        console_image = \
            pygame.image.load(
                'TARDIS_Monitor_Wallpaper_by_Girl_on_the_Moon_overlay.png').convert()
        self.image = pygame.transform.smoothscale(
                console_image, (RESOLUTION))
        
        self.image.set_alpha(self.alpha_channel)
        self.rect = self.image.get_rect()
        self.rect.topleft = ((0, 0))

    def update(self):
        pass

    def hide(self):
        self.rect.topleft = (OFFSCREEN)

    def attract(self):
        self.rect.topleft = ((0, 0))
        

class Capture(object):
    def __init__(self):
        self.size = RESOLUTION
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, DOUBLEBUF | HWSURFACE)

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
        return self.display

    def main(self):
        going = True

        counter = pygame.sprite.Group()
        flash = pygame.sprite.Group()
        status = pygame.sprite.Group()
        last_image = pygame.sprite.Group()
        console_overlay = pygame.sprite.Group()
        all = pygame.sprite.OrderedUpdates()

        Counter.containers = all, counter
        LastImage.containers = all, last_image
        Flash.containers = all, flash
        Status.containers = all, status
        ConsoleOverlay.containers = all, console_overlay

        countdown = Counter()
        status = Status()
        console = ConsoleOverlay()

        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False
                if (e.type == KEYDOWN and e.key == K_SPACE):
                    console.hide()
                    countdown.initialize_snapshot()

                if (e.type == TIMER_TICK):
                    countdown.countdown()

                # Flash photo
                if (e.type == SNAPSHOT):
                    # Fake a last_image group collision to kill the last image sprite
                    pygame.sprite.groupcollide(last_image, last_image, True, True)

                    status.hide()
                    self.get_and_flip(all)
                    prev_image = self.take_snapshot()
                    Flash()
                    pygame.time.set_timer(NINJA_SNAPSHOT, 1000)

                # Ninja photo
                if (e.type == NINJA_SNAPSHOT):
                    ninja_image = self.take_snapshot()
                    pygame.time.set_timer(NINJA_SNAPSHOT, 0)
                    pygame.time.set_timer(ATTRACT_MODE, 1000)

                # Start up Attract Mode
                if (e.type == ATTRACT_MODE):
                    status.attract()
                    console.attract()
                    LastImage(prev_image)
                    pygame.time.set_timer(ATTRACT_MODE, 0)

            self.get_and_flip(all)

if __name__ == "__main__":
    pygame.init()
    pygame.camera.init()
    a = Capture()
    a.main()
