"""
Ping-Pong (Pong) game - Tool A version (ChatGPT-style)
Minimal requirements:
- Game environment setup (field, paddles, ball)
- Player input (W/S for left, Up/Down for right)
- Ball movement + collisions (walls + paddles)
- Score keeping (top of screen)
Library: Python standard library only (turtle)
"""

import turtle
import time

# -------------------------
# Config
# -------------------------
WIDTH, HEIGHT = 800, 500
PADDLE_W, PADDLE_H = 14, 100
BALL_SIZE = 14
PADDLE_STEP = 25

# Ball speed settings (increase over time a bit)
BALL_DX_INIT = 4
BALL_DY_INIT = 3
SPEEDUP_FACTOR = 1.03  # small speed increase after paddle hits


def make_paddle(x: int, y: int) -> turtle.Turtle:
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color("white")
    paddle.shapesize(stretch_wid=PADDLE_H / 20, stretch_len=PADDLE_W / 20)
    paddle.penup()
    paddle.goto(x, y)
    return paddle


def make_ball() -> turtle.Turtle:
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("square")
    ball.color("white")
    ball.shapesize(stretch_wid=BALL_SIZE / 20, stretch_len=BALL_SIZE / 20)
    ball.penup()
    ball.goto(0, 0)
    ball.dx = BALL_DX_INIT
    ball.dy = BALL_DY_INIT
    return ball


def make_scoreboard() -> turtle.Turtle:
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, HEIGHT // 2 - 50)
    return pen


def clamp_paddle(paddle: turtle.Turtle) -> None:
    top_limit = HEIGHT // 2 - PADDLE_H // 2
    bottom_limit = -HEIGHT // 2 + PADDLE_H // 2
    if paddle.ycor() > top_limit:
        paddle.sety(top_limit)
    if paddle.ycor() < bottom_limit:
        paddle.sety(bottom_limit)


def update_score(pen: turtle.Turtle, left_score: int, right_score: int) -> None:
    pen.clear()
    pen.write(
        f"Left: {left_score}   Right: {right_score}",
        align="center",
        font=("Arial", 20, "normal"),
    )


def main():
    # Screen setup
    wn = turtle.Screen()
    wn.title("Ping-Pong (Tool A)")
    wn.bgcolor("black")
    wn.setup(width=WIDTH, height=HEIGHT)
    wn.tracer(0)

    # Middle line (optional visual)
    mid = turtle.Turtle()
    mid.speed(0)
    mid.color("gray")
    mid.penup()
    mid.goto(0, HEIGHT // 2)
    mid.setheading(270)
    mid.pendown()
    mid.hideturtle()
    for _ in range(25):
        mid.forward(10)
        mid.penup()
        mid.forward(10)
        mid.pendown()

    # Paddles and ball
    left_paddle = make_paddle(-WIDTH // 2 + 40, 0)
    right_paddle = make_paddle(WIDTH // 2 - 40, 0)
    ball = make_ball()

    # Score
    left_score = 0
    right_score = 0
    pen = make_scoreboard()
    update_score(pen, left_score, right_score)

    # Controls
    def left_up():
        left_paddle.sety(left_paddle.ycor() + PADDLE_STEP)
        clamp_paddle(left_paddle)

    def left_down():
        left_paddle.sety(left_paddle.ycor() - PADDLE_STEP)
        clamp_paddle(left_paddle)

    def right_up():
        right_paddle.sety(right_paddle.ycor() + PADDLE_STEP)
        clamp_paddle(right_paddle)

    def right_down():
        right_paddle.sety(right_paddle.ycor() - PADDLE_STEP)
        clamp_paddle(right_paddle)

    wn.listen()
    wn.onkeypress(left_up, "w")
    wn.onkeypress(left_down, "s")
    wn.onkeypress(right_up, "Up")
    wn.onkeypress(right_down, "Down")

    # Main loop
    while True:
        wn.update()
        time.sleep(1 / 120)  # smooth-ish

        # Move ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Wall collision (top/bottom)
        if ball.ycor() > HEIGHT // 2 - BALL_SIZE:
            ball.sety(HEIGHT // 2 - BALL_SIZE)
            ball.dy *= -1

        if ball.ycor() < -HEIGHT // 2 + BALL_SIZE:
            ball.sety(-HEIGHT // 2 + BALL_SIZE)
            ball.dy *= -1

        # Score check (left/right out of bounds)
        if ball.xcor() > WIDTH // 2:
            left_score += 1
            update_score(pen, left_score, right_score)
            ball.goto(0, 0)
            ball.dx = -BALL_DX_INIT
            ball.dy = BALL_DY_INIT

        if ball.xcor() < -WIDTH // 2:
            right_score += 1
            update_score(pen, left_score, right_score)
            ball.goto(0, 0)
            ball.dx = BALL_DX_INIT
            ball.dy = BALL_DY_INIT

        # Paddle collision
        # Right paddle
        if (
            ball.xcor() > right_paddle.xcor() - 20
            and ball.xcor() < right_paddle.xcor() + 20
            and abs(ball.ycor() - right_paddle.ycor()) < (PADDLE_H / 2 + BALL_SIZE / 2)
            and ball.dx > 0
        ):
            ball.setx(right_paddle.xcor() - 20)
            ball.dx *= -1
            ball.dx *= SPEEDUP_FACTOR
            ball.dy *= SPEEDUP_FACTOR

        # Left paddle
        if (
            ball.xcor() < left_paddle.xcor() + 20
            and ball.xcor() > left_paddle.xcor() - 20
            and abs(ball.ycor() - left_paddle.ycor()) < (PADDLE_H / 2 + BALL_SIZE / 2)
            and ball.dx < 0
        ):
            ball.setx(left_paddle.xcor() + 20)
            ball.dx *= -1
            ball.dx *= SPEEDUP_FACTOR
            ball.dy *= SPEEDUP_FACTOR


if __name__ == "__main__":
    main()
