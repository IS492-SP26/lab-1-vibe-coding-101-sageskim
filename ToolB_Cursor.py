"""
Two-player Ping-Pong (Pong) game using Python's built-in turtle module.

Controls:
  Left paddle:  W (up), S (down)
  Right paddle: Up Arrow (up), Down Arrow (down)
  Quit:         Esc
  Reset score:  R
"""

from __future__ import annotations

import time
import turtle


WIDTH = 900
HEIGHT = 600

PADDLE_W = 20
PADDLE_H = 110
PADDLE_STEP = 28

BALL_SIZE = 18  # visual size (approx)
BALL_SPEED_START = 6.5
BALL_SPEED_MAX = 13.0

WALL_Y = (HEIGHT // 2) - 10


def clamp(v: float, lo: float, hi: float) -> float:
    return lo if v < lo else hi if v > hi else v


class Paddle:
    def __init__(self, x: int) -> None:
        self.t = turtle.Turtle(visible=False)
        self.t.speed(0)
        self.t.shape("square")
        self.t.shapesize(stretch_wid=PADDLE_H / 20, stretch_len=PADDLE_W / 20)
        self.t.color("white")
        self.t.penup()
        self.t.goto(x, 0)
        self.t.showturtle()

    @property
    def x(self) -> float:
        return self.t.xcor()

    @property
    def y(self) -> float:
        return self.t.ycor()

    def move(self, dy: float) -> None:
        new_y = clamp(
            self.t.ycor() + dy,
            -HEIGHT / 2 + PADDLE_H / 2 + 5,
            HEIGHT / 2 - PADDLE_H / 2 - 5,
        )
        self.t.sety(new_y)


class Ball:
    def __init__(self) -> None:
        self.t = turtle.Turtle(visible=False)
        self.t.speed(0)
        self.t.shape("circle")
        self.t.shapesize(stretch_wid=BALL_SIZE / 20, stretch_len=BALL_SIZE / 20)
        self.t.color("white")
        self.t.penup()
        self.t.goto(0, 0)
        self.t.showturtle()

        self.vx = BALL_SPEED_START
        self.vy = BALL_SPEED_START * 0.62

    def reset(self, direction: int) -> None:
        # direction: +1 -> to the right, -1 -> to the left
        self.t.goto(0, 0)
        self.vx = BALL_SPEED_START * direction
        self.vy = BALL_SPEED_START * 0.62

    def speed_up(self) -> None:
        # Increase speed slightly, but keep bounded.
        sx = min(abs(self.vx) * 1.04, BALL_SPEED_MAX)
        sy = min(abs(self.vy) * 1.03, BALL_SPEED_MAX)
        self.vx = sx if self.vx >= 0 else -sx
        self.vy = sy if self.vy >= 0 else -sy


class Scoreboard:
    def __init__(self) -> None:
        self.left = 0
        self.right = 0
        self.t = turtle.Turtle(visible=False)
        self.t.speed(0)
        self.t.color("white")
        self.t.penup()
        self.t.goto(0, HEIGHT // 2 - 70)
        self.draw()

    def draw(self) -> None:
        self.t.clear()
        self.t.write(
            f"{self.left}    :    {self.right}",
            align="center",
            font=("Courier", 32, "bold"),
        )

    def reset(self) -> None:
        self.left = 0
        self.right = 0
        self.draw()


def main() -> None:
    screen = turtle.Screen()
    screen.title("Ping-Pong (Pong) - Python Turtle")
    screen.bgcolor("black")
    screen.setup(width=WIDTH, height=HEIGHT)
    screen.tracer(0)  # manual redraw

    # Center line (dashed)
    line = turtle.Turtle(visible=False)
    line.speed(0)
    line.color("gray")
    line.penup()
    line.goto(0, HEIGHT / 2 - 20)
    line.setheading(270)
    for _ in range(26):
        line.pendown()
        line.forward(12)
        line.penup()
        line.forward(12)

    left_paddle = Paddle(x=-(WIDTH // 2) + 60)
    right_paddle = Paddle(x=(WIDTH // 2) - 60)
    ball = Ball()
    score = Scoreboard()

    # Input handlers
    screen.listen()

    screen.onkeypress(lambda: left_paddle.move(+PADDLE_STEP), "w")
    screen.onkeypress(lambda: left_paddle.move(-PADDLE_STEP), "s")
    screen.onkeypress(lambda: right_paddle.move(+PADDLE_STEP), "Up")
    screen.onkeypress(lambda: right_paddle.move(-PADDLE_STEP), "Down")
    screen.onkeypress(lambda: score.reset(), "r")
    screen.onkeypress(screen.bye, "Escape")

    last = time.perf_counter()

    while True:
        # Keep turtle responsive and render next frame
        screen.update()

        now = time.perf_counter()
        dt = now - last
        last = now

        # Simple fixed-ish timestep feel; cap dt so pauses don't teleport ball.
        dt = min(dt, 0.03)

        # Move ball
        ball.t.setx(ball.t.xcor() + ball.vx * (dt * 60))
        ball.t.sety(ball.t.ycor() + ball.vy * (dt * 60))

        bx, by = ball.t.xcor(), ball.t.ycor()

        # Wall collisions (top/bottom)
        if by > WALL_Y:
            ball.t.sety(WALL_Y)
            ball.vy *= -1
        elif by < -WALL_Y:
            ball.t.sety(-WALL_Y)
            ball.vy *= -1

        # Paddle collisions
        # Left paddle: near its x, and y within paddle height range
        if (
            bx < left_paddle.x + (PADDLE_W / 2) + 14
            and bx > left_paddle.x
            and abs(by - left_paddle.y) < (PADDLE_H / 2) + 10
            and ball.vx < 0
        ):
            ball.t.setx(left_paddle.x + (PADDLE_W / 2) + 14)
            ball.vx *= -1
            # Add a bit of "english" depending on hit position
            offset = (by - left_paddle.y) / (PADDLE_H / 2)
            ball.vy = clamp(ball.vy + offset * 4.2, -BALL_SPEED_MAX, BALL_SPEED_MAX)
            ball.speed_up()

        # Right paddle
        if (
            bx > right_paddle.x - (PADDLE_W / 2) - 14
            and bx < right_paddle.x
            and abs(by - right_paddle.y) < (PADDLE_H / 2) + 10
            and ball.vx > 0
        ):
            ball.t.setx(right_paddle.x - (PADDLE_W / 2) - 14)
            ball.vx *= -1
            offset = (by - right_paddle.y) / (PADDLE_H / 2)
            ball.vy = clamp(ball.vy + offset * 4.2, -BALL_SPEED_MAX, BALL_SPEED_MAX)
            ball.speed_up()

        # Scoring: ball goes past left/right edge
        if bx > (WIDTH / 2) - 10:
            score.left += 1
            score.draw()
            ball.reset(direction=-1)
            time.sleep(0.35)
        elif bx < -(WIDTH / 2) + 10:
            score.right += 1
            score.draw()
            ball.reset(direction=+1)
            time.sleep(0.35)

        # Small sleep to reduce CPU usage
        time.sleep(0.001)


if __name__ == "__main__":
    main()

