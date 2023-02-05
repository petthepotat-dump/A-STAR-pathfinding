import pygame

import sbv
from scripts import grid, user_input as ui


window = pygame.display.set_mode((800, 800), 0, 32)
clock = pygame.time.Clock()


g = grid.Grid(20, 20)


sch = sbv.StepVisScheduler({"freq": 10})
sch.start()
running = True
while running:
    window.fill((0, 0, 0))
    g.render(window)

    if ui.is_key_clicked(pygame.K_s):
        # set starting node
        mpos = ui.get_mouse_pos()
        g.start = (mpos[0] // grid.Grid.WIDTH, mpos[1] // grid.Grid.HEIGHT)
    elif ui.is_key_clicked(pygame.K_e):
        mpos = ui.get_mouse_pos()
        g.end = (mpos[0] // grid.Grid.WIDTH, mpos[1] // grid.Grid.HEIGHT)
    elif ui.is_key_pressed(pygame.K_d):
        mpos = ui.get_mouse_pos()
        g.grid[mpos[1] // grid.Grid.HEIGHT][mpos[0] // grid.Grid.WIDTH].ttype = grid.WA
    elif ui.is_key_pressed(pygame.K_a):
        mpos = ui.get_mouse_pos()
        g.grid[mpos[1] // grid.Grid.HEIGHT][mpos[0] // grid.Grid.WIDTH].ttype = grid.NN
    

    if ui.is_key_clicked(pygame.K_SPACE):
        sch.push_task(g.solve)
    elif ui.is_key_clicked(pygame.K_r):
        g.reset()
        sch._task_queue.clear()

    ui.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            ui.key_press(e)
        elif e.type == pygame.KEYUP:
            ui.key_release(e)
        elif e.type == pygame.MOUSEBUTTONDOWN:
            ui.mouse_button_press(e)
        elif e.type == pygame.MOUSEBUTTONUP:
            ui.mouse_button_release(e)
        elif e.type == pygame.MOUSEMOTION:
            ui.mouse_move_update(e)
    
    pygame.display.update()
    clock.tick(30)
pygame.quit()
sch.attempt_join()


