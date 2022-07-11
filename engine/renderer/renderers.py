import pygame
RenderShape = {
    'rectangle': lambda pg, scr, sh: pg.draw.rect(scr, sh.get_color(), sh.get_parameters(),
                                                  width=sh.get_width()),
    'circle': lambda pg, scr, sh: pg.draw.circle(scr, sh.get_color(), sh.get_parameters()[0],
                                                 sh.get_parameters()[1],
                                                 width=sh.get_width()),
    'polygon': lambda pg, scr, sh: pg.draw.polygon(scr, sh.get_color(), sh.get_parameters(),
                                                   width=sh.get_width())}


# todo culling
# todo make this shit easier
#

def render(screen,renderBuffer,bg):
    screen.fill(bg)
    renderBufferSorted = sorted(renderBuffer, key=lambda i: i.get_depth(), reverse=True)
    renderBuffer.clear()
    for shape in renderBufferSorted:
        RenderShape[shape.get_type()](pygame, screen, shape)
    pygame.display.flip()


def render2(screen,renderBuffer,bg):
    screen.fill((255, 255, 255))
    for shape in renderBuffer:
        pass
            # todo do profiling
            # todo make z-bufferiing or some other way for uv mapping
            # todo use alpha channel to draw animated bg

            # todo https://www.youtube.com/watch?v=ih20l3pJoeU&list=PLrOv9FMX8xJE8NgepZR1etrsU63fDDGxO&index=22
