Feature: identify if a User have access to a specific resource or service

Scenario: After recognizing a user, the system should identify if the user has access to a specific resource or service
  Given that the recognize environment was successfully set up
  When the picture /mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/elliot1.jpg is taken by the camera
  Then A Registered User must be recognized 
  When the User was identified
  Then Verify what kind of services and resources are available to him/her
