# Introduction To Tracking Data

## Content:
  * [Steps to create a football pitch](#editing-to-be-done).
  * [Analysis](#analysis).

## Steps to create a football pitch map:

* Here we will be discussing the step one can perform to make a plot of football pitch.

* This code was developed by [Laurie Shaw](https://twitter.com/EightyFivePoint).

* We here are actually discussing the function *plot_pitch* present in *utility_functions_viz.py*, i.e. the steps perfomed in the given funtion to plot the pitch map.

* In the function we are actually converting all the dimensions of pitch from yards to meters.(since field dimensions are typically defined in yards). We have used 105x68 meters^2 pitch area for our plot.

* **Note:** We will take the origin of the quadrant as the centre of our pitch that we will plot.

* So here are the steps:
  * **Code Line 25:** We have defined a plot of size (12,8).
  
  * **Code Line 28-30:** We have defined some of the parameters that we will use while plotting such as the color for our plot and linewidth.
  
  * **Code Line 33-37:** We have defined the field dimensions in meters. Pitch length and pitch width has been halved because we are using origin as the center for our pitch.
  
  * **Code Line 40-50:** Since the football dimensions are typically defined in yards so we have converted them into meters.
  
  * **Code Line 53:** Setting the background color, your plot now looks like this:
  ![Capture](https://user-images.githubusercontent.com/33928040/79645194-69b47600-81cb-11ea-9cdc-6a52f92aaee6.JPG)
    
  * **Code Line 56-57:** Plotting the half-way line of the pitch and the center circle of the pitch. The plot will look like:
  ![Capture](https://user-images.githubusercontent.com/33928040/79645289-10007b80-81cc-11ea-814e-4abb894e8f74.JPG)
  
  * **Code Line 60-61:** Here defining points for x and y to plot or circle. Let's see how this works, the circle whose center is at origin is basically derived by the formula: *x^2 + y^2 = r^2* and at *Line 60* we have our y coordinates and we have radius too with us so by using the given formula as x = sqrt(r^2 - y^2) we will find our x coordinates.
  
  * **Code Line 64-65:** Plotting our center circle, *Line 64* will plot the right hand side of the circle and *Line 65* will plot the left hand side of the circle. Here is our plot(note that the plot just has been magnified only to show the circle because everything in our plot is still empty):
    ![Capture](https://user-images.githubusercontent.com/33928040/79647367-d7fa3800-81cd-11ea-9abe-4afe6a69c9a8.JPG)
   
  * **Code Line 68:** First selecting s = -1 to show how the plotting works inside the for loop.
  
  * **Code Line 70-71:** Plotting the pitch boundary for left and bottom of the pitch. The plot now looks like this:
    ![Capture](https://user-images.githubusercontent.com/33928040/79655558-37f1de00-81d0-11ea-95b0-cc3c0a030fff.JPG)
    
  * **Code Line 74:** Plotting the goal post by using goal_line_width. The plot now looks like this:
    ![Capture](https://user-images.githubusercontent.com/33928040/79659930-7f2c9e80-81d1-11ea-8401-537fcd88a7a1.JPG)
  
  * **Code Line 77-79:** Plotting the six yard box line by line. First, plot after *Line 77*, second after *Line 77* and third after *Line 77*. Plots:
  
      ![Capture](https://user-images.githubusercontent.com/33928040/79667165-8d7bba00-81d3-11ea-8fc1-0a896b2915e1.JPG)
      ![Capture](https://user-images.githubusercontent.com/33928040/79667610-adab7900-81d3-11ea-9845-31a5f46d0a40.JPG)
      ![Capture](https://user-images.githubusercontent.com/33928040/79668482-ee0af700-81d3-11ea-9167-8abf0c59a8b9.JPG)
    
  * **Code Line 82-84:** Plotting the penalty box line by line. First, plot after *Line 82*, second after *Line 83* and third after *Line 84*. Plots:
  
    ![Capture](https://user-images.githubusercontent.com/33928040/79669063-a2a61800-81d6-11ea-8a3d-a636cba3abc1.JPG)
    ![Capture](https://user-images.githubusercontent.com/33928040/79669093-c5d0c780-81d6-11ea-85f2-f8f501f5de1f.JPG)
    ![Capture](https://user-images.githubusercontent.com/33928040/79669112-e3059600-81d6-11ea-9299-1f065465a961.JPG)

  * **Code Line 87:** Plotting the penalty spot. Here's how the plot looks like:
    ![Capture](https://user-images.githubusercontent.com/33928040/79669274-067d1080-81d8-11ea-95bc-5eca308aa811.JPG)
    
  * **Code Line 90-91:** Here defining the x and y points for our corner flag quadrant. y has been defined from 0 to 1 because we just need one circular quadrant.
  
  * **Code Line 92:** Plotting the first corner flag quadrant. Plot will now looks like this:
    ![Capture](https://user-images.githubusercontent.com/33928040/79681802-a8354980-823a-11ea-95a8-20e8a8c6f0b4.JPG)

  * **Code Line 93:** Plotting our second flag quadrant. Plot will now looks like this:
    ![Capture](https://user-images.githubusercontent.com/33928040/79681829-f21e2f80-823a-11ea-89a9-ab817c9932c4.JPG)

  * **Code Line 96-97:** Defining the x and y points for our D, here the D_length is the length of the chord that defines the D.
  
  * **Code Line 98:** Plotting the D:
    ![Capture](https://user-images.githubusercontent.com/33928040/79682105-53470280-823d-11ea-90a4-545eea98ca45.JPG)
  
  * Now the loop will run on more time for *sign = 1* and will plot the right hand side of the pitch. Plot:
    ![Capture](https://user-images.githubusercontent.com/33928040/79682212-0ca5d800-823e-11ea-88b2-bfa1666b7f0a.JPG)
  
  * **Code Line 101-104:** Removing all x ticks and y ticks as well as there labels. The plot will now look like:
    ![Capture](https://user-images.githubusercontent.com/33928040/79682295-a1a8d100-823e-11ea-94b3-48566a895484.JPG)
  
  * **Code 107-111:** Setting the axis limits for the plots. x coordinate will be from (-55.5, 55.5) and y coordinate will be from (-37, 37), the value 3 has been added to have a border around the pitch. So our final plot looks like:
    ![Capture](https://user-images.githubusercontent.com/33928040/79682393-7ecaec80-823f-11ea-9bb7-fb04a7f18333.JPG)

## Analysis:     

 * **Note:** In our pitch map, *home team* is attacking from *left to right* and away team is attacking from *right to left*.
 
 * Firstly we have drawn out the shot map for both the teams, from the plot we can see every kind of shots, i.e. shots which were on traget, blocked shots, shots which were saved, long range shots and of course the goals. The *home team's* two goals were from the edge of the six yard box having a good xG value and one of the shot that led to a goal was a long range shot with a low xG value. For *away team* the two goals were from inside the penalty box, they were trying many long range shots that end up either blocked or saved or of target. Here is the plot for shot-map:
   ![shot_map](https://user-images.githubusercontent.com/33928040/79694175-633a0300-828c-11ea-9d60-e1fff9aa6335.jpg)
 
 * Then we have plotted some of the event maps for the first three goals:
   * This is the event map for the first goal of the match scored by the *home team*.
   * We have numbered the events in the order.
   * Events from 1 to 8 were all *pass event* and the *9th event* was a shot that led to the first goal.
   * **Note:** Ball carry data is not present in the data set that is why the events sometime looks incomplete,
   * e.g. event from end point 3 to 4 starting point should be a carry event since it's not in the data set that why it's looking empty.
   ![event_map_goal_1](https://user-images.githubusercontent.com/33928040/79694177-646b3000-828c-11ea-9961-10c1c15eef43.jpg)
   
   * Next is the event map for the second goal of the match
     ![event_map_goal_2](https://user-images.githubusercontent.com/33928040/79879729-b6d35a80-840c-11ea-9a28-bfca66d9f733.jpg) 
   
   * And at last for the third goal of the match.
     ![event_map_goal_3](https://user-images.githubusercontent.com/33928040/79879715-b3d86a00-840c-11ea-9a4e-129a0c51c346.jpg)

 * Next we have plotted our tracking data:
   * Here at first we have plotted the position of all 22 players on the pitch at the start of the kick off:
     ![kick_off](https://user-images.githubusercontent.com/33928040/79694179-659c5d00-828c-11ea-9a77-caadd49d72c6.jpg)
   
   * Then we have plotted the tracking data when *home team* scored their first goal:
     ![home_team_first_goal](https://user-images.githubusercontent.com/33928040/79694178-6503c680-828c-11ea-9099-6d0f79eaf2d8.jpg)
   
   * Tracking plot when *away team* scored their first goal:
     ![away_team_first_goal](https://user-images.githubusercontent.com/33928040/79694176-63d29980-828c-11ea-8b47-ce427ee2a60c.jpg)   
   
   * Tracking plot when *home team* scored the last goal of the match
     ![last_goal](https://user-images.githubusercontent.com/33928040/79694172-61703f80-828c-11ea-8767-82cd2a03d6ce.jpg)
 
 * And then we went on and took *Player 9* for our analysis/plotting and plotted his shots on goal and tracking data when he scored the goal.
  ![player_9_shots](https://user-images.githubusercontent.com/33928040/79879721-b5099700-840c-11ea-99af-5b4524b39258.jpg)
  ![position_player9_goal](https://user-images.githubusercontent.com/33928040/79879725-b63ac400-840c-11ea-8330-c19891e54148.jpg)
  
