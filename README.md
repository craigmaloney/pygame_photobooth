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
* ``serial_button``: Whether to check for the serial button or not (default: False will run without the button)
* ``serial_port``: The port for the Arduino button (/dev/ttyUSB0 or /dev/ttyACM0)
* ``photo_directory``: Where to store the photos (default: ./photos)
* ``fullscreen``: Whether to display fullscreen (default: True)
* ``max_alpha``: Alpha range from 0-255, with 0 being invisible and 255 being completely opaque
* ``alpha_step``: How quickly to remove the overlay. Larger numbers are faster. 0 will not display the overlay.
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


pygame_photobooth hardware
==========================

Main components:
* Computer running Ubuntu (or another Linux distribution)
* V4L compatible web camera (we used a Logitech Web Cam)
* External screen
* 2+ shelf cart/stand
  * The shelf we used is from IKEA, MULIG Shelf unit, black http://www.ikea.com/us/en/catalog/products/70241044/ 
* we have mount with a standard tripod screw for the webcam which attaches to the pole for the monitor, this can be done differently based on your setup

For the optional button:
* The button we use is Large Arcade Button with LED - 60mm White https://www.adafruit.com/products/1192
* Arduino (we have used Arduino Uno and Duemilanove but others should be compatible) 
* Housing for button - we used a project box from an electronics store).
  * The button and Arduino can be mounted in the same box with a cutout for the USB cable.
* USB cable for Arduino 
* Wire to connect the button to the Arduino
* (optional, recommended) proto shield for Arduino and wire connectors to make the connection between button and Arduino more robust
