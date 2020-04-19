# Introduction To Tracking Data

## Steps to create a football pitch map:

* Here we will be discussing the step one can perform to make a plot of football pitch.

* This code was developed by [Laurie Shaw](https://twitter.com/EightyFivePoint).

* We here are actually discussing the function *plot_pitch* present in *utility_functions_one.py*, i.e. the steps perfomed in the given funtion to plot the pitch map.

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
