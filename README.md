pygame_photobooth
=================

Rough Pygame Photobooth (but it's getting better)

You'll need to install the following (preferably as system packages):

* Pygame
 * libsdl-mixer
 * libsdl-ttf

The Arduino code sends a "Pressed!" event over the serial port. If you have configured the photo booth to accept input from the serial port you will need to ensure the program has access to the serial port.
* Arduino UNO shows up under /dev/ttyACM0. You'll need to add your user to the "dialout" group
* Arduino Duemilanove shows up under /dev/ttyUSB0.

The configuration file "config.yaml" has the default values in there for the application:
* ``camera_resolution_x/y``: The resolution of the camera hooked up
* ``offscreen_resolution_x/y``: The resolution of the screen
* ``serial_port``: The port for the Arduino button (/dev/ttyUSB0 or /dev/ttyACM0)
* ``serial_button``: Whether to check for the serial button or not (False will run without the button)
* ``photo_directory``: Where to store the photos (default: ./photos)
* ``fullscreen``: Whether to display fullscreen (default: True)
* ``theme``: Configuration specific to the theme
 * ``directory``: Where the theme is locted
 * ``overlay``: Image to overlay over the screen
 * ``attract_sound``: The sound to play every-so-often
 * ``font``: The font to use to display (TTF Font)
 * ``countdown sound``: The sound to use for the countdown

Doctor Who Theme:
* Font from http://www.dafont.com/ws-simple-gallifreyan.font
* Console Screen: http://girl-on-the-moon.deviantart.com/art/TARDIS-Monitor-Wallpaper-116295761

Camera skeleton code from http://www.pygame.org/docs/tut/camera/CameraIntro.html
