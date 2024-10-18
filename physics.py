class Physics3D:
    def __init__(self, width=800, height=800, depth=800, gravity=0.5, ball_radius=10):
        self.width = width
        self.height = height
        self.depth = depth  # Added depth for the 3D space
        self.gravity = gravity
        self.ball_radius = ball_radius
        self.balls = []  # List of balls in the simulation

    def add_ball(self, position, velocity=(0, 0, 0)):
        ball = {
            'pos': list(position),  # 3D position: [x, y, z]
            'velocity': list(velocity)  # 3D velocity: [vx, vy, vz]
        }
        self.balls.append(ball)

    def apply_gravity(self, ball):
        ball['velocity'][1] += self.gravity  # Gravity still affects only the y-axis

    def update_ball_position(self):
        """
        Update ball positions and handle collisions with the floor, walls, and depth boundaries.
        """
        for ball in self.balls:
            # Apply gravity
            self.apply_gravity(ball)
            
            # Update ball position in 3D
            ball['pos'][1] += ball['velocity'][1]  # Update y (vertical movement)
            ball['pos'][0] += ball['velocity'][0]  # Update x (horizontal movement)
            ball['pos'][2] += ball['velocity'][2]  # Update z (depth movement)
            
            # Handle floor collision
            if ball['pos'][1] + self.ball_radius > self.height:
                ball['pos'][1] = self.height - self.ball_radius
                ball['velocity'][1] = -ball['velocity'][1] * 0.7  # Bounce with damping

            # Handle left and right wall collisions (x-axis boundaries)
            if ball['pos'][0] - self.ball_radius < 0:
                ball['pos'][0] = self.ball_radius
                ball['velocity'][0] = -ball['velocity'][0] * 0.7
            elif ball['pos'][0] + self.ball_radius > self.width:
                ball['pos'][0] = self.width - self.ball_radius
                ball['velocity'][0] = -ball['velocity'][0] * 0.7
            
            # Handle front and back wall collisions (z-axis boundaries)
            if ball['pos'][2] - self.ball_radius < 0:
                ball['pos'][2] = self.ball_radius
                ball['velocity'][2] = -ball['velocity'][2] * 0.7
            elif ball['pos'][2] + self.ball_radius > self.depth:
                ball['pos'][2] = self.depth - self.ball_radius
                ball['velocity'][2] = -ball['velocity'][2] * 0.7

    def get_ball_position(self, index=0):
        """
        Returns the current 3D position of the ball at a given index.
        """
        return self.balls[index]['pos'] if len(self.balls) > 0 else None
