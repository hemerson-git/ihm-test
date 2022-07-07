Feature: recognize a user by his/her picture

Scenario: A user turn on the TV and must be recognized by a camera
  Given that the recognize environment was successfully set up
  When the picture /mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/elliot1.jpg is taken by the camera
  Then A Registered User must be recognized 


Scenario: A Unregistered user turn on the TV and must not be recognized by a camera
  Given that the recognize environment was successfully set up
  When the picture /mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/price1.jpg is taken by the camera
  Then A Unregistered User must not to be recognized 
