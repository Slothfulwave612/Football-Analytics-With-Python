* Links to the videos from where these notes were made:
  * [Liverpool FC data scientist William Spearman's masterclass in pitch control](https://www.youtube.com/watch?v=X9PrwPyolyU)
  * [Advanced football analytics: building and applying a pitch control model in python](https://www.youtube.com/watch?v=5X1cSehLg6s&t=1239s)

## Content:
  * [Pitch Control](#pitch-control).
  * [Developing Pitch Control](#developing-pitch-control)
  * [Common Questions](#common-questions)
  * [Dynamic Control: Control Force](#dynamic-control-control-force)
  * [Dynamic Control: Intercepting](#dynamic-control-intercepting)
  * [Dynamic Pitch Control](#dynamic-pitch-control)
  * [Relevant Pitch Control](#relevant-pitch-control)
  * [Scoring Opportuinity](#scoring-opportuinity)
  * [Recap](#recap)
  * [Coding a Pitch Control Model: Overview](#coding-a-pitch-control-model-overview)
  * [Ball Time to Arrival](#Ball-Time-to-Arrival)
  * [Player Time To Arrival](#Player-Time-To-Arrival)
  * [Simple Approximation For Arrival Time](#Simple-Approximation-For-Arrival-Time)
  * [The Control Probability](#The-Control-Probability)
  * [Uncertain Player Arrival Times](#Uncertain-Player-Arrival-Times)
  * [Pitch Control Program](#Pitch-Control-Program)

# Pitch Control

* **Definition:** *Pitch control* (at a particular location) is the probability that a player could control the ball, assuming it were at that location.

![pitch_control](https://user-images.githubusercontent.com/33928040/80406400-a7a74d80-88e1-11ea-9e0f-769d9c709731.JPG)

  * The above was the model that was made by *William Spearman* and his team around 2015-16.

      * The plot displays a single frame of tracking data from a football game

      * The *red dots* are the home players, the *blue dots* are the away players and the *white dot* is the ball.

      * The *velocity vectors*(the arrows) are showing the direction in which the players are travelling in and that's computed from the tracking data.(may not be 100% accurate)

      * One can also see the region of control, e.g. around the home goal-keeper, the home team has complete control and similarly for the away team around the goalkeeper.

      * In the midfield, you can see it's a changing situation. One thing more that can be seen from the plot is that the player has bit more control in front of them(in the direction that they are running)

        

## Developing Pitch Control

* **Defining Control:**

  * The **player who is closest to the ball** is in *control of the ball.*

    ![control](https://user-images.githubusercontent.com/33928040/80406462-baba1d80-88e1-11ea-8bab-b1a7c905a86f.JPG)

  * In this plot here, we can see *three players*(two blue players and one red player)

  * So according to our definition, the player closest to the ball is in control of the ball, hence in this plot or example the *blue player* on the left is in control of the ball.

  * Extending this concept not just to the ball where it currently is but to the whole pitch, we can actually quantify the region that are controlled by the blue players and the red players using this definition of control.

    ![voronoi](https://user-images.githubusercontent.com/33928040/80406490-c7d70c80-88e1-11ea-89d1-d5e4921974a8.JPG)

  * This leads to **Voronoi Tessellation** of pitch control.
  
  * **Voronoi Tessellation:** This is a mathematical concept, which is used for the splitting of space into regions that are closest to one point or another.
  
  * In the above plot you can notice one thing, looking at the velocity vectors, we can see that the red player is moving towards the ball. So, even though the blue player is closer to the ball, the red player is moving in that direction.
  
  * So we can say one thing that since red player is moving in the direction of the ball, even though he is not closer to the ball, he can probably get there faster.
	
	* **Conclusion:** It's not **distance** that matters so much to controlling a region, it's the **time**.
	
	* So what we can do is, we can use very simple approximations like maximum speed and maximum acceleration for these players to compute how long will it take for each of these players with some starting speed and velocity vector to reach different location on the pitch.
	
	* So, here is what we get when we apply the above concept:
		
	![control_1](https://user-images.githubusercontent.com/33928040/80406554-dfae9080-88e1-11ea-8b9b-b08f3f88d1ef.JPG)
		
	* So, here we can see the ball is in red region of control. So by making Voronoi based on time instead of distance changes the dynamics of the system to be more realistic.
	
	* And as before we can quantify different region of control based on this time concept.
	
* **Adding Uncertainty:**

  * Like in physics, very less is certain in football. As such, we can never be 100% confident that a given area of the pitch is controlled by a player.

  * To account for this uncertainity in a data-driven way, we use the time it takes a player to be in a given location as the inputs and build a classifier that it fit to data to assign a probability of control.

  * So by looking at situation like when a ball is out of position on the pitch, then we can compute the control different players have on it and actually see which player ends up making the control touch using our event data. So that allows us to fit this probabilistic model, which then looks like this:

    ![uncertain](https://user-images.githubusercontent.com/33928040/80406598-f05f0680-88e1-11ea-9197-5d66e407a06c.JPG)

## Common Questions:

* *Aren't regions closer to the ball more important?*

  * Let's look at this following plot:

    ![pitch](https://user-images.githubusercontent.com/33928040/80406635-0076e600-88e2-11ea-80d0-aa665ead03dd.JPG)

  * In this situation the blue team is attacking from right to left, and the keeper here is in the huge amount of space which he is controlling. However that space is particularly not important because the team is not really doing with it. So the big space the keeper and the center backs of the attacking team are in is not particularly a good indicator of the quality of the possession or the quality of the attack, so it should not be used to measure anything about the teams performance.

  * So one way to quantify this is to say that, the pitch control we are interested in is the *pitch control that is closer to the ball*, because that is the relevant space to control. 

  * So we can build a model that we can call *Relevant Pitch Control* that highlights the control near the location that the players are occurring and that allows us to evaluate pitch control that's important.

* *What about while the ball is in motion?*

  * We can see that our model is not highlighting the relevant regions that are near the ball but furthermore it is not taking into account the fact that for the ball to reach more distant regions(it will take some time) so it's actually not computing the pitch control at some point far away the ball when it will take a few seconds for the ball to reach that point.

  * So to be able to deal with that we have to introduce kind of a dynamic control model for ball control.(*A Dynamic Pitch Control*)

    ![ball_motion](https://user-images.githubusercontent.com/33928040/80406686-17b5d380-88e2-11ea-9bd5-7aa22689546e.JPG)

* *Aren't some parts of the pitch are more valuable?*
  
   * Well we have hit on this point in our first question(the keeper example).
   
   * Obviously, the attacking team wants to get closer to their target goal and the space in those region will be much more important, so e.g. a striker is making a run in behind the defence then the striker will actually be exerting control behind the space on the defensive line while still being on side, and that space is very valuable even it is fairly small because that is creating a chance for the team to score.
   
   * So we have to be able to incorporate the information about the fact that all points of the pitch are not equally valuable.
   
   * So by incorporating that, we can incorporate the concept that *William Spearman* calls *Scoring Opportuinity*, which will allow us to compute the danger of a given situation.
   
     ![scoring](https://user-images.githubusercontent.com/33928040/80406769-3320de80-88e2-11ea-97f1-18e418fa489e.JPG)

## Dynamic Control: Control Force

* There is this fundamental principle that: *The more time you have on the ball, the more able  you are to make a control pass or a control touch*.

* So we can model this using a simple exponential, so the probability of control is just a rate parameter times the time interval that the player is in the vicinity of the ball.

* Let us consider that a controlled touch is a stochastic process with a fixed rate.

* For each time interval Δt that a player is in the vicinity of the ball, he/she has a probability of λ . Δt to make a controlled touch on the ball.

* On integrating this we get an exponential CDF(Cumulative Distribution Function); CDF gives you the probability that a random variable is less than or equal to a certain value.

  ![controlforce](https://user-images.githubusercontent.com/33928040/80406819-46cc4500-88e2-11ea-9ec0-33f2bfa08b62.JPG)

  * So the x-axis is the time a player is in the ball, and the y-axis is the probability that the player is able to make a control touch given that amount of time they are on the ball.
  * This is fit to data and one thing we can see is *90% time it takes less than a second to control the pass*.(as highlighted in the plot)

* Let's now look at a situation, where the ball is moving in one direction along the ground with a little bit of drag, so it is slowing down slightly at every time step and we are going to divide them into equal sized time steps, so let's say these time step are one-tenth of a second(i.e. 0.1 second) long. 

  ![space1](https://user-images.githubusercontent.com/33928040/80406859-58ade800-88e2-11ea-9617-f31ee5e8e914.JPG)

  * So, as the ball reaches this point where the *red* player is able to intercept it, and let's say that the pass probability per intercept vector is 10%, so **Line 1: 100% * 10% = 10%**.

  * Now when it moves to the next time step, we have to assume that the player was not able to make that control touch at the first time step, so there is now (100 %- 10%) = 90% chance to reach this next point and since 10% is the probability per intercept vector, so **Line 2: 90% * 10% = 9%**.

    ![space2](https://user-images.githubusercontent.com/33928040/80406885-62375000-88e2-11ea-9a1e-3d9988d59f84.JPG)

  * And for the third time step, then it will be **Line 3: (90% - 9%) * 10% = 81% * 10% = 8.1%**.

    ![space3](https://user-images.githubusercontent.com/33928040/80406909-6d8a7b80-88e2-11ea-846f-7e1026a8509b.JPG)

  * So what we are saying is there is 0.3 second of time step where the *red* player could make a control touch, i.e. could get to the the interception of the ball and make a control touch, and within those 0.3 seconds we give *red* player a total of **10% + 9% + 8.1% = 27.1%** probability of controlling  the pass.

    ![playera](https://user-images.githubusercontent.com/33928040/80406962-7f6c1e80-88e2-11ea-807d-531e21e65923.JPG)

  * Assuming *red* player doesn't intercept the ball, then the *blue* player gets a shot to make a control touch, and in first interval, we compute for *blue* player: **Line 1: (81% - 8.1) * 10% = 72.9 * 10% = 7.3%**

    ![palyer_b](https://user-images.githubusercontent.com/33928040/80407001-8d21a400-88e2-11ea-812b-57e49779c4d1.JPG)

  * For the second time step for *blue* player, **Line 2: (72.9% - 7.3%) * 10% = 65.6% * 10% = 6.6%**. 

    ![player_3](https://user-images.githubusercontent.com/33928040/80407052-9f9bdd80-88e2-11ea-92ff-516e8eb2d767.JPG)

  * And for the remaining:

    **Line 3: 59% * 10% = 5.9%**

    **Line 4: 53.1% * 10% = 5.3%**

    **Line 5: 47.8% * 10% = 4.8%**

    **Line 6: 43% * 10% = 4.3%**

    **Total: 34.2% probability of controlling the pass**

    ![player_4](https://user-images.githubusercontent.com/33928040/80407087-ad516300-88e2-11ea-946e-7e261b2b7493.JPG)

  * **Player A (Red):**

    * Not much *time to control* the ball.
    * Good *coordination* required to control pass.

  * **Player B (Blue):**

    * Cannot control pass *if player A received it* already.
    * Control region is large, i.e. there are *many intercept vectors* available.

  * So this model have nice features, it includes all information listed above(Player A and Player B information), and then this approach allows us to deals with the situation where the **control the region overlaps**, because those two players both have a chance to make a control touch, so by discretizing this integral into smaller and smaller timesteps. we can actually get the probability of each of the two players to make the control touch of the ball even when those control region overlap. 

## Dynamic Control: Intercepting

* Here what we can do is use some concepts from Physics to compute optimal time-to-intercept assuming a player's maximum speed and acceleration.

* Now what we have to do is convert this time taken by the player to intercept the pass or the ball into a probability. And this will encapsulate uncertainity in few different areas like the tracking data is never perfect.

* So, we take this time-to-intercept that we have computed and we effectively put it through a sigmoid distribution.

  ![sigmoid](https://user-images.githubusercontent.com/33928040/80407122-be9a6f80-88e2-11ea-9fdd-fc2826a7c7a1.JPG)

* So this will allow us to evaluate dynamic situation. So let's pick one dynamic situation is passing.

  ![dynamic](https://user-images.githubusercontent.com/33928040/80407144-cb1ec800-88e2-11ea-82fb-727925e22233.JPG)

  * So here in the plot the ball is moving from left to right(we have rotated into the reference frame of the ball, so x-axis represents the ball).
  * Player 0 is close to the trajectory of the ball, but he has to get to the ball very fast, so his control region is relatively small.
  * The dim line from each player represents a fixed time step. If let say the time step is each 0.1 second, then for player 0 there is 0.4 seconds to intercept the ball and has a probability of 17.8% to intercept it.
  * But player 2 and player 1 has larger time and spatial windows, so here player 1 has 56% chance of receiving it and player 2 has 26.2% chance.
  * Now what we can do it build a probability density function or cumulative distribution function of the probability of control at different points of time at a different point in space. So, basically this can give us the view of where these passes are going to be received, who is likely to receive these passes.

## Dynamic Pitch Control

* Now we can use the above concepts to make a dynamic pitch control by simply computing the dynamic control at different location on the pitch but only starting the integration when the ball should arrive there.

* In order to do that we need ball time-of-flight model, a simple one is *distance/ball_speed*.

  ![ballflight](https://user-images.githubusercontent.com/33928040/80407176-d83bb700-88e2-11ea-8ce8-b97db7900aad.JPG)

  * So here we have the ball time of flight model and you can see the region far from the ball takes about 4.5 seconds for the ball to reach there, for region close it is close to 0 second.

  * **Conclusion:** Using a simple model to approximate how long the ball should take to reach the target location, we can create a dynamic control model that is less certain about the control in regions far from the ball's current location.

    ![dynamicpitch](https://user-images.githubusercontent.com/33928040/80407207-e558a600-88e2-11ea-8ab3-9666c822b952.JPG)

## Relevant Pitch Control

* Now we will use the dynamic pitch control as an input into our relevant pitch control field.

* **Defining Relevance:** We define relevance as the probability that the next touch is at a given location at the pitch, also can be called as *transition probability*.

* And we can build a simple transition probability model using the pitch control(as input) of the team that is currently in position and the distance from the player who is currently in position.

  ![rpc](https://user-images.githubusercontent.com/33928040/80407244-f5708580-88e2-11ea-902f-43636c783984.JPG)

  * So this plot basically highlights the relevant region of the pitch for the blue team.

* Using our simple transition model, we can define our relevant pitch control by multiplying transition probability with the control probability.

  ![rpc2](https://user-images.githubusercontent.com/33928040/80407277-028d7480-88e3-11ea-9b46-5efe635bea72.JPG)

  * This is the relevant pitch control, which highlights the regions that the on ball player is likely to pass through(the blue region). 

  * So in this case, the most relevant region are the regions controlled by these two players(blue defence).

    

## Scoring Opportuinity

* Here in the model, we look at the probability of scoring given a control touch at a particular point on the pitch.

  ![score opp](https://user-images.githubusercontent.com/33928040/80407317-10db9080-88e3-11ea-8e0b-1f64cb6cfbaf.JPG)

  * Now here we can see this model, which represents a value 1 when you are at the goal mouth and becomes vanishingly small far from goal.

* Using our simple value model, we can define our scoring opportuinity by multiplying the relevant pitch control by the probability of scoring at each point on the pitch.

  ![off ball](https://user-images.githubusercontent.com/33928040/80407354-1f29ac80-88e3-11ea-93d5-d2caf42a91aa.JPG)

  * This *Off Ball Scoring Opportuinity* highlights the regions of the pitch where the next touch in a scoring chain is likely to come from.
  * So this is allowing us to basically weight the pitch control by how dangerous it is.
  * What's interesting about this is that the players who didn't seem to have very relevant pitch control actually have quite a bit of scoring opportuinity.

* **Off Ball Scoring Opportuinity: Match Analysis**

  * We can build various *scoring opportuinity maps* or a *scoring opportuinity vs time*, to highlight dangerous moment that may have occurred at a given moment in the match.

    ![obso](https://user-images.githubusercontent.com/33928040/80407410-349ed680-88e3-11ea-9778-8b46ea40aeb2.JPG)

  * Or how shots from both teams are correlated(Scoring Opportuinity Map), you can see the shots in the particular game(denoted by x) and the circles represents the shots that results in a goal.

  * Now what's interesting about this example is that both team actually scored one goals but one team took massively more shots(the red team), but both the team scored only one goal or have similar scoring opportuinity

* **Off Ball Scoring Opportuinity: Player Analysis**

  * So here are the scoring opportuinity maps for a given right back for three different games.
    ![rb](https://user-images.githubusercontent.com/33928040/80735126-dc0f4980-8b2d-11ea-8edf-e5838198207b.JPG)

  * So, you can generally see that his scoring opportuinity comes from wide right positions outside the penalty area, where he is clearly operating in space with the possibility of scoring. 

  * You can see that the player has not scored in these three games but you can still see that he is getting into those positions from where he can actually score.

  * And here you can see in the fourth match the player did score from those position, making two shots and converting them to goals.
    ![rb_scored](https://user-images.githubusercontent.com/33928040/80735133-df0a3a00-8b2d-11ea-9df7-93cbe18ebef1.JPG)

## Recap

* We have introduced pitch control which is itself a contextualizing of Voronoi Tessellation using the physical characteristics, i.e. the velocity and acceleration of players to develop a time to intercept and to render that as a probability of control.
* Additionally we have added some contextual features such as a transition probability model which allows us to build a relevant pitch control model.
* We have added the time of flight of the ball to allow us to see the dynamic pitch control model and then the same model can be used to evaluate passing situations.
* And then lastly we have incorporated a scoring value model alongside our transition and pitch control models to be able to build scoring opportuinity model that highlights the regions of the pitch that are controlled that are valuable and the ball is likely to transition to.

## Coding a Pitch Control Model: Overview

* So the basic question the pitch control model seek to answer is: *what options are available to the player on the ball?* or *where can that player pass the ball such that his team are allowed to retain possession of it.*

* Let's see an example:

  ![map](https://user-images.githubusercontent.com/33928040/80953065-6a2e4d00-8e18-11ea-971c-eb38105dcb95.JPG)

  * So here we a plot of an instance of a game.

  * The dot show the position where the players are and the little arrow are the velocity vectors(i.e. where they are running in that particular instance), the longer the arrow the faster they are moving.

  * Player 20 in the blue team is in the possession of the ball.

  * So in terms of passing options, given the motion from right to left, perhaps there are some passing options around player 23 around player 24.

  * The Pitch Control models enables you to quantify these options directly.

    ![pitch_map](https://user-images.githubusercontent.com/33928040/80953249-c42f1280-8e18-11ea-8d57-81c61d562078.JPG)

  *  So the red region in the field now indicate, the areas in which the red team are likely to gain control of the ball if player 20 was to pass the ball to those locations, whereas the blue regions indicate the areas in which the blue team were likely to retain control of the possession if the ball was passed to those location.

  * And the model captures not only the instantaneous positions of the players but also where they are running. So if a player is moving quickly they are much more likely to control the space they are moving into rather than the space that they currently occupy.

* **Building a pitch control model:**

  * If we want to build a pitch control model there are essentially three things that we need to calculate.

  * For a given location on a pitch:

    **1.** *How long would it take for the ball to arrive?*

    **2.** *How long would it take for each player to arrive?*

    **3.** *What is the total probability that each team will control the ball after it has arrived?*

  * And if we want to calculate a full pitch control surface like in the above figure, then we need to repeat these calculations for all locations on the pitch.

## Ball Time to Arrival

* Let's look at this figure:

  ![ball_time](https://user-images.githubusercontent.com/33928040/80953273-d14c0180-8e18-11ea-823e-2141c9496e04.JPG)

  * So the following figure shows that the player20(from the last figure) was in the possession of the ball at start position and lets imagine he want to move the ball to the end position, which is a distance of about 21 meters.
  * **Note:** In this model that we are building we are assuming that the ball moves with a constant speed of 15 m/s.
  * So it will take 1.4 second to arrive to the end position from the start position.

## Player Time To Arrival:

* Let's now look at how long it would take each of the players to arrive at the target position of the ball given their initial position and velocity at the moment that the pass is played.

* And in this model there are number of key assumption:

  * Players have a maximum speed of 5 m/s

  * Players have a maximum acceleration of 7 m/s<sup>2</sup>

  * Players take the fastest possible path

## Simple Approximation For Arrival Time

* Two-step process:

  * There is an initial *reaction time* of 0.7 seconds. During this time each player continues along their current trajectory.
  * After 0.7 seconds, the player runs directly towards the target location at their maximum speed of 5 m/s

* So let's see the two closest players to the target location in our example.

  ![two_closest](https://user-images.githubusercontent.com/33928040/80953364-fb9dbf00-8e18-11ea-8d7c-fc3a04964655.JPG)

  * We have player 4 on the red team and player 24 on the blue team, and again the arrow indicates the velocities of each player at the moment of the pass is played.

  * And so here are the trajectories the player would take under our simple approximate process.

    ![two_traj](https://user-images.githubusercontent.com/33928040/80953445-27b94000-8e19-11ea-904a-be38d8d956a1.JPG)

  * Here the little dots indicates the player would be after their initial reaction time, so for the first 0.7 second player 4 carries on along his initial trajectory and then after 0.7 second turns and runs at his maximum speed towards the target location.

  * Player 24 was moving along the right direction, so just continue along his path for the reaction period and then again moves on to the target location at his maximum speed.

  * And in this calculation it would take 2 seconds for player 4 to reach the target location and 1.5 seconds for player 24.

## The Control Probability

* So, we have calculated how long it will take a player and the ball to get to the target location, but how long it would take for each player to control the ball.

* In his paper, *William* assume that players that are in the vicinity of the ball within a given time interval Δt, the probability of controlling the ball is λ*Δt, where λ is a free parameter in his model that determines how quickly the player is tend to control the ball.

* In his model he suggests λ should be equal to 4.30 1/s, which is basically saying that it takes around 0.23 seconds for a player to control the ball.

  ![controlforce](https://user-images.githubusercontent.com/33928040/80953586-749d1680-8e19-11ea-85df-5883ea8a73a2.JPG)

## Ball Control: Exact Arrival Time

* So lets go back to our example and look again at the two players that start off closest to the target location, player 4 in the red team and player 24 in the red team.

  ![examplr](https://user-images.githubusercontent.com/33928040/80953638-8bdc0400-8e19-11ea-93e6-8ab8bdda34f7.JPG)

  * So we have already calculated that the ball will arrive at the target location after 1.4 seconds, player 24 after 1.5 seconds and player 4 by 2 seconds.

    ![pass_probab](https://user-images.githubusercontent.com/33928040/80953684-a615e200-8e19-11ea-8f15-2e222e3519e7.JPG)

  * So this chart above, shows you the probability that the ball is controlled by one of the two players as a function of time since the pass is played.

* Now, *William* described in his model incorporates some uncertainity in the player arrival time which he models using a sigmoid distribution with a standard deviation of 0.45 seconds.

  ![sigmoid](https://user-images.githubusercontent.com/33928040/80953769-cb0a5500-8e19-11ea-91aa-8e40c3115ea3.JPG)

## Uncertain Player Arrival Times

* Now if we incorporate this into our model we see that the probability that the ball is controlled by the either player changes significantly.

  ![sigmoid_probab](https://user-images.githubusercontent.com/33928040/80953799-d78ead80-8e19-11ea-8e8c-e7d80f714400.JPG)

  * And the reason for this is that the ball is assumed to have arrived exactly after 1.4 seconds but now there is some uncertainity in the arrival time of the players there is actually less window for player 24 to control the ball such that his final probability that he ends up controlling the ball reduced from 0.93 to 0.7 and the probability of player 4 controlling the ball increases correspondingly to about 0.3.

## Pitch Control Program

* So the way in which we calculate the full pitch control surface is by breaking down the field down into the grid of little pixels and within each pixel. 
* And within each pixel we calculate the time it will the ball to arrive from its current location, the time it will take all the players to arrive and then the probability that each player will be able to control the ball and therefore each team will be able to control the ball.
* And then we repeat that by moving across the grid and calculating it in every single pixel.
