# El Classico(2009)

* Here we are trying to analyze the event data from El Clasico held at the Estadio Santiago Bernabeu on May 2, 2009.

* The result ended in favour of **Barcelona** defeating **Real Madrid** by 6 goals to 2. This was one of the famous El Clasico ever played.

* The data has been taken from Statsbomb and it's there free data or the open data, which can be downloaded from this given link: [Statsbomb Open Data](https://github.com/statsbomb/open-data)
  
  ![statsbomb-logo](https://user-images.githubusercontent.com/33928040/79592082-140e9980-80f7-11ea-930b-5fdc9b0d9b3e.png)

* There are *five* Python files that are uploaded:
  * FCPython.py -- This Python file helps to draw the pitch map.
  * dribble_code.py -- This Python file creates the dribble map for any Barcelona player you will list.(that played in that El Clasico)
  * pass_map.py -- This Python file creates the pass map for any Barcelona player you will list.(that played in that El Clasico)
  * shot_map.py -- This Python file creates the shot map for both the teams.
  * shot_player.py -- This Python file creates a shot map for any Barcelona player you will list.(that played in that El Clasico)
  * touch_player.py -- This Python file creates a touch map for any Barcelona player you will list.(that played in that El Clasico)
  
## Shot Map:

* Here using shot_map.py we were able to create the shot map for each team.

* The shots are highlighted with circles. If the shot outcome was a goal then it's dark circle otherwise it's just a faded circle. The circle size tells the xG value i.e. if the shot has a high xG value then the circle size will be bigger else smaller.

* *Blue* color represents **Barcelona's** shots and *Red* represents **Real Madrid's** shots.

* Here is how the plot looks like:
  ![shots_pitch_map](https://user-images.githubusercontent.com/33928040/79593528-386b7580-80f9-11ea-9325-8e4737924a55.jpg)

* From this plot you can see how **Barcelona** dominated the shots department. **Barcelona** were having their shots with a good xG value and even both the shots from *Messi* that resulted in goal has a good xG value.

* The shot from *Puyol* that result in a goal have low xG value because it was a headed goal.

* The goal from *Thierry Henry* from outside the penalty box has a little bit high xG value then the xG value of the *Pique's* shot because *Iker Casillas* was out of position.

## Touch Map:

* Here using touch_player.py we were able to create the touch map for Lionel Messi, Xavi Hernandez and Andres Iniesta.

* Thorugh the plots we will see how *Pep Guardiola* used the trio for midfield domination and how he played *Lionel Messi* as a *False Nine*. Here are the plots:
  
  ![Lionel Andrés Messi Cuccittini's Touch Map vs Real Madrid](https://user-images.githubusercontent.com/33928040/79594973-ac0e8200-80fb-11ea-9607-7e2cec12de48.png)
  
![Xavier Hernández Creus's Touch Map vs Real Madrid](https://user-images.githubusercontent.com/33928040/79594974-add84580-80fb-11ea-839e-3b31d746ff8a.png)

![Andrés Iniesta Luján's Touch Map vs Real Madrid](https://user-images.githubusercontent.com/33928040/79594975-ae70dc00-80fb-11ea-9f2b-5d739e570a8f.png)

* From the plot above you can see how *Guardiola's* approach to control the midfield was performed by the trio and how he used them for attacking too. 

## Pass Map:

* Here using pass_map.py we were able to create the pass map for Lionel Messi, Xavi Hernandez and Andres Iniesta.

* Let's first see the plot the we will do some analysis based on the plots:
  
  ![Andrés Iniesta Luján pass map](https://user-images.githubusercontent.com/33928040/79595666-e0cf0900-80fc-11ea-940f-9dda78441d1a.jpg)
  
  ![Xavier Hernández Creus pass map](https://user-images.githubusercontent.com/33928040/79595654-de6caf00-80fc-11ea-8911-94ff4db9b04d.jpg)
  
  ![Lionel Andrés Messi Cuccittini pass map](https://user-images.githubusercontent.com/33928040/79595646-dc0a5500-80fc-11ea-9c77-967a4f898da9.jpg)
 
 * From these plot we can see that, how well *Andres Iniesta's* passing game was in that match as he achieved a 100% pass accuracy and *Xavi* and *Messi* were exceptional too achieving 96% and 98% percent respectively.
 
 * These plot show how the *Pep's* philosophy of the passing game was well demonstrated by the famous trio of *Xavi*, *Messi* and *Iniesta*.(well yes it was a collective effort from the whole team but I think this famous trio made everything easy and possible)

## Lionel Messi's Dribbles:

* Here using dribble_code.py we were able to create a dribble map for Lionel Messi.

* The dark circle represents the successful dribble and faded one represents the unsuccessful dribble.

* Here is the plot:
  
  ![Lionel Andrés Messi Cuccittini's Dribbles vs Real Madrid](https://user-images.githubusercontent.com/33928040/79599074-89cc3280-8102-11ea-895d-b24953913404.png)

## Lionel Messi's Shots:

* Here using shot_player.py we were able to create a shot map for Lionel Messi.

* Here is the plot:
  
  ![Lionel Andrés Messi Cuccittini's Shots vs Real Madrid](https://user-images.githubusercontent.com/33928040/79599493-35758280-8103-11ea-95c5-c20ea3747cfd.png)

* Here you can see that 4 shots that Messi took had a good xG values, and he converted two of them and it tells that he was really getting into the area of maximum possibility for scoring goals.

--> So this was my very shot analysis on few things that I noticed.

--> Thanks to [Friends of Tracking](https://www.youtube.com/channel/UCUBFJYcag8j2rm_9HkrrA7w/videos) for their lovely course.
