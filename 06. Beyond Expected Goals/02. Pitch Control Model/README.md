## Generate Pitch Control Surface

* Get starting frame, team in possession and ball starting position(x and y).

* Break the pitch down into grids:

  ``` python
  n_grid_cell_x = 50 ## pixels(default)
  n_grid_cell_y = int(n_grid_cell_x * field_dims[1]) / field_dims[0]
  x_grid = np.linspace(-field_dims[0]/2, field_dims[0]/2, n_grid_cell_x)
  y_grid = np.linspace(-field_dims[1]/2, field_dims[1]/2, n_grid_cell_y)
  ```

* Initialize pitch control grids for both attacking as well as defending team

  ```pseudocode
  PPCF_a = numpy-zero array; dims = (y_grid.len, x_grid.len)
  PPCF_d = numpy-zero array; dims = (y_grid.len, x_grid.len)
  ```

* Initialize player positions and velocities for pitch control calculations:

  * Extract player ids from the tracking dataframe.

  * Create an empty list which will contain every player object.

  * For each and every player initialize an object of class Player.

    * Initialize:

      * player_id, player_name, team_name, velocity_max, reaction_time, sigma_value, position_of_player(x and y), inframe(True -- if postions are not NaN otherwise False), velocity(vx and vy), velocity=[0, 0] (if vx and vy is NaN).

    * Time to intercept function, will compute the time for a player to intercept the ball:

      ```pseudocode
      reaction = position + velocity * reaction_time
      time_to_intercept = reaction_time + normalize(final_pos - reaction) / v_max
      ## final_pos; time taken by the player to reach the final_position
      ```

    * Probability of intercepting the ball - function:

      * Will use a sigmoid function here

        ```pseudocode
        e = pi / sqrt(3) / sigma * (arr_time - time_to_intercept)
        probab = 1 / 1 + exp(-e)
        ```

  * If player is inframe, i.e. player position in not NaN i.e. inframe variable is True, append the object to the list(team_players).

    

    


