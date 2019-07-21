import time
import random

import constants as cfg
from engine import render
from engine import bitmasks
from engine import colours
from engine.vec import Vec
from engine.io import (progress_leds,
                       pi_controller,
                       musical_buzzer,
                       score_py_glow,
                       diagnostics)

class Pong:

    GAME_STATES = {
        "left_win":     0,
        "right_win":    1,
        "loop":         2,
        "left_serve":   3,
        "right_serve":  4
    }

    def __init__(self, auto_start_loop=True):
        self.width = cfg.GAME_WIDTH
        self.height = cfg.GAME_HEIGHT
        self.renderer = render.Renderer(self.width, self.height)
        # startup screen
        x = 10
        y = 5
        self.renderer.draw_bitmask(x, y,
                                   bitmasks.loading_bats["general_bat_border"],
                                   colours.BLACK)
        self.renderer.draw_bitmask(x, y,
                                   bitmasks.loading_bats["bat_filler"],
                                   colours.BLUE)
        x = 60
        self.renderer.draw_bitmask(x, y,
                                   bitmasks.loading_bats["general_bat_border"],
                                   colours.BLACK)
        self.renderer.draw_bitmask(x, y,
                                   bitmasks.loading_bats["bat_filler"],
                                   colours.RED)
        self.renderer.draw_string("pong",
                                  self.width // 2, 7,
                                  colours.CYAN,
                                  centered=True)
        self.renderer.rerender()
        musical_buzzer.play_intro_song()
        # setup remaining things
        self.fps = cfg.FPS
        self.tps = cfg.TPS
        self.balls = [Ball(self, Vec(0, 0), Vec(0, 0)) \
                      for _ in range(cfg.BALL_N)]
        # both players will be controlled by the same controller for now
        self.left_player  = Player(self,
                                   Vec(3, 10),
                                   pi_controller,
                                   musical_buzzer.SOUND_A)
        self.right_player = Player(self,
                                   Vec(self.width - 4, 5),
                                   pi_controller,
                                   musical_buzzer.SOUND_B)
        self.left_player_score = 0
        self.right_player_score = 0
        self.diagnostics = {
            "adc_value": 0,
            "serve_button_state": 0,
            "super_button_state": 0,
            "bat_left_pos_x": 0,
            "bat_left_pos_y": 0,
            "bat_right_pos_x": 0,
            "bat_right_pos_y": 0,
            "ball_pos_x": 0,
            "ball_pos_y": 0
        }
        if random.random() < 0.5:
            self.serving_player = self.left_player
            self.game_state = self.GAME_STATES['left_serve']
        else:
            self.serving_player = self.right_player
            self.game_state = self.GAME_STATES['right_serve']
        if auto_start_loop:
            self.start_loop()

    def start_loop(self):
        ITERATIONS_PER_SECOND = max(self.fps, self.tps)
        iterations = 0
        try:
            while True:
                # separate frames per second (fps) from ticks per second (tps)
                if iterations % (ITERATIONS_PER_SECOND // self.tps) == 0:
                    self.tick()
                if iterations % (ITERATIONS_PER_SECOND // self.fps) == 0:
                    self.repaint()
                iterations += 1
                time.sleep(1 / ITERATIONS_PER_SECOND)
        except KeyboardInterrupt:
            exit()

    def tick(self):
        # check if any player has won
        if self.left_player_score >= cfg.WINNING_SCORE:
            self.game_state = self.GAME_STATES['left_win']
            return
        elif self.right_player_score >= cfg.WINNING_SCORE:
            self.game_state = self.GAME_STATES['right_win']
            return

        self.left_player.tick()
        self.diagnostics["bat_left_pos_x"] = self.left_player.pos.x
        self.diagnostics["bat_left_pos_y"] = self.left_player.pos.y
        self.right_player.tick()
        self.diagnostics["bat_right_pos_x"] = self.right_player.pos.x
        self.diagnostics["bat_right_pos_y"] = self.right_player.pos.y
        progress_leds.led_on(int((self.balls[-1].pos.x / self.width) * 7 + 0.5))

        if self.game_state == self.GAME_STATES["loop"]:
            for ball in self.balls:
                ball.tick()
        elif self.game_state == self.GAME_STATES["left_serve"]:
            self.diagnostics["ball_pos_x"] = self.balls[-1].pos.x
            self.diagnostics["ball_pos_y"] = self.balls[-1].pos.y
            self.balls[-1].pos.x = self.left_player.pos.x + 1
            self.balls[-1].pos.y = self.left_player.pos.y + (
                                   self.left_player.size // 2)
            self.balls[-1].vel = Vec(cfg.BALL_SPEED / self.tps, 0)

        elif self.game_state == self.GAME_STATES["right_serve"]:
            self.diagnostics["ball_pos_x"] = self.balls[-1].pos.x
            self.diagnostics["ball_pos_y"] = self.balls[-1].pos.y
            self.balls[-1].pos.x = self.right_player.pos.x - 1
            self.balls[-1].pos.y = self.right_player.pos.y + (
                                   self.right_player.size // 2)
            self.balls[-1].vel = Vec(-cfg.BALL_SPEED / self.tps, 0)


    def repaint(self):
        # draw scores
        left_player_score_width = self.renderer.get_label_width(
            str(self.left_player_score))
        self.renderer.draw_string(str(self.left_player_score),
                                  self.width // 2 - 8 - left_player_score_width,
                                  1,
                                  cfg.SCORE_COLOUR)
        self.renderer.draw_string(str(self.right_player_score),
                                  self.width // 2 + 9,
                                  1,
                                  cfg.SCORE_COLOUR)
        # draw net
        for y in range(self.height):
            if not (y // 2) % 2:
                self.renderer.draw_pixel(self.width // 2, y + 1, cfg.NET_COLOR)
        # draw balls
        for ball in self.balls:
            ball.repaint()
        # draw players
        self.left_player.repaint()
        self.right_player.repaint()
        # render win messages if applicable
        if self.game_state == self.GAME_STATES['left_win']:
            self.renderer.draw_string("left wins!",
                                      self.width // 2,
                                      self.height // 2 - 4,
                                      cfg.WIN_MESSAGE_COLOUR,
                                      centered=True)
        elif self.game_state == self.GAME_STATES['right_win']:
            self.renderer.draw_string("right wins!",
                                      self.width // 2,
                                      self.height // 2 - 4,
                                      cfg.WIN_MESSAGE_COLOUR,
                                      centered=True)
        # rerender screen
        self.renderer.rerender()
        # diagnostics Display
        render.move_cursor(0, self.height + 10)
        diagnostics.write_display(self.diagnostics)


class Player:

    def __init__(self, game, pos, controller, sound):
        self.game = game
        self.pos = pos
        self.size = cfg.BAT_SIZE
        self.super_size_countdown = 0
        self.super_size_count = 0
        self.controller = controller
        self.sound = sound
        self.serves = 0

    def tick(self):
        # adc value: height of bat
        adc_value = self.controller.get_value_1()
        self.pos.y = adc_value * (self.game.height - self.size)
        self.game.diagnostics["adc_value"] = adc_value
        # btn 1: serve
        btn_1_state = self.controller.button_1_check()
        self.game.diagnostics["serve_button_state"] = btn_1_state
        if btn_1_state:
            if self.game.game_state != self.game.GAME_STATES["loop"]:
                # serve
                self.game.game_state = self.game.GAME_STATES["loop"]
                self.serves += 1
                # for serve 5 rule
                # this can be executed regardless of whether the serve 5 rule
                # is actually used or not since it would not impact the game
                # flow anyways
                if self.serves > 5:
                    # toggle self.game.serving_player between left- and right
                    # player
                    if self.game.serving_player == self.game.right_player:
                        self.game.serving_player = self.game.left_player
                    else:
                        self.game.serving_player = self.game.right_player
                    # reset own serve count
                    self.serves = 0
        # btn 2: Super size
        btn_2_state = self.controller.button_2_check()
        self.game.diagnostics["super_button_state"] = btn_2_state
        if btn_2_state and \
           self.super_size_countdown <= 0 and \
           self.super_size_count < cfg.MAX_SUPER_SIZE_COUNT:
            self.super_size_count += 1
            self.super_size_countdown = cfg.SUPER_SIZE_LENGTH * self.game.tps
            self.size = cfg.SUPER_SIZE_BAT_SIZE
        if self.super_size_countdown <= 0:
            self.size = cfg.BAT_SIZE
        else:
            self.super_size_countdown -= 1

    def repaint(self):
        for dy in range(self.size):
            x = self.pos.x
            y = self.pos.y + dy
            self.game.renderer.draw_pixel(x, y, cfg.BAT_COLOUR)

    def play_sound(self):
        musical_buzzer.sing_note(self.sound)


class Ball:

    def __init__(self, game, pos, vel, colour=cfg.BALL_COLOUR):
        self.game = game
        self.pos = pos # the ball's position
        self.vel = vel # the balls velocity
        self.colour = colour
        self.next_pos = self.pos

    def tick(self):
        # first naive prediciton where the ball is going to be in the next tick.
        self.next_pos = self.pos + self.vel
        # check wall collisions...
        if self.next_pos.x < 0:
            # collision with left wall -> right player scores
            # self.vel.x *= -1
            # self.next_pos = self.pos + self.vel
            self.game.right_player_score += 1
            score_py_glow.play_animation()
            if cfg.USE_5_SERVE:
                # determine who will serve next based on the 'serve 5 rule'
                if self.game.serving_player == self.game.right_player:
                    self.game.game_state = self.game.GAME_STATES["right_serve"]
                else:
                    self.game.game_state = self.game.GAME_STATES["left_serve"]
            else:
                self.game.game_state = self.game.GAME_STATES["right_serve"]
        elif self.next_pos.x >= self.game.width:
            # collision with right wall -> left player scores
            # self.vel.x *= -1
            # self.next_pos = self.pos + self.vel
            self.game.left_player_score += 1
            score_py_glow.play_animation()
            if cfg.USE_5_SERVE:
                # determine who will serve next based on the 'serve 5 rule'
                if self.game.serving_player == self.game.right_player:
                    self.game.game_state = self.game.GAME_STATES["right_serve"]
                else:
                    self.game.game_state = self.game.GAME_STATES["left_serve"]
            else:
                self.game.game_state = self.game.GAME_STATES["left_serve"]
        if self.next_pos.y < 0 or self.next_pos.y >= self.game.height:
            self.vel.y *= -1
            self.next_pos = self.pos + self.vel
        else:
            self.handle_collision(self.game.left_player)
            self.handle_collision(self.game.right_player)
        self.pos = self.next_pos
        self.game.diagnostics["ball_pos_x"] = self.pos.x
        self.game.diagnostics["ball_pos_y"] = self.pos.y

    def handle_collision(self, player):
        u_left, v_left = Vec.intersection_scalars(self.pos,
                                                  self.vel,
                                                  Vec(player.pos.x,
                                                      player.pos.y - 1),
                                                  Vec(0, player.size + 1))
        if 0 <= u_left <= 1. and 0 <= v_left <= 1.:
            # collision detected
            if self.game.game_state == self.game.GAME_STATES['loop']:
                player.play_sound()
            self.vel.x *= -1
            # -1 <= spin <= +1
            # if the ball hits the bat exactly in the middle, spin will be 0
            # if it hits the bat at the top or bottom, spin will be -1 or +1
            # respectively.
            spin = (v_left - 0.5) * 2
            self.vel.y = spin * cfg.SPIN_STRENGTH
            # normalize the ball's velocity so that it does not change when
            # it hits the bat (only in direction, not in length => speed).
            if cfg.RANDOM_SPEEDS:
                self.vel.set_length(((0.7 + random.random()) * 1.4) * \
                    cfg.BALL_SPEED / self.game.tps)
            else:
                self.vel.set_length(cfg.BALL_SPEED / self.game.tps)
            self.next_pos = self.pos + self.vel

    def repaint(self):
        self.game.renderer.draw_pixel(self.pos.x, self.pos.y, self.colour)
