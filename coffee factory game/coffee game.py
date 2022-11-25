import pygame, pymunk
from random import randint
import math

pygame.init()
screen = pygame.display.set_mode((500, 500))
font = pygame.font.SysFont("consolas", 10, True)
uifont = pygame.font.SysFont("consolas", 45, True)
c = pygame.time.Clock()


def subfrom(point: tuple) -> tuple:
    return (point[0], point[1] + 15)


class Line:
    def __init__(self, points: list):
        self.points = points

    def draw(self, screen):

        pygame.draw.lines(screen, (0, 0, 0), False, self.points, 3)


class Cup:
    def __init__(self, pos: tuple, req: int, space: object):
        self.req = req
        self.pos = pos
        self.image = pygame.image.load("mug.png")
        self.rect = self.image.get_rect(center=self.pos)

        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        shape = pymunk.Poly(
            body, [(self.rect.topleft[0], self.rect.topleft[1] + 5),
                   (self.rect.topright[0] - 7, self.rect.topright[1] + 5),
                   (self.rect.bottomright[0], self.rect.bottomright[1] - 7),
                   self.rect.bottomleft])
        self.rect = pygame.Rect(0, 0, 18, 25)
        self.rect.center = pos
        space.add(body, shape)

    def check(
        self,
        shape,
    ) -> bool:
        out = False
        if self.rect.collidepoint(shape.body.position) and self.req > 0:

            out = True
            self.req -= 1
        return out

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        rtext = font.render(str(self.req), True, (0, 0, 0))
        screen.blit(rtext, rtext.get_rect(center=self.pos))


def create_segment(space, a, b):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, a, b, 2)
    shape.elasticity = 0.1

    space.add(body, shape)
    return shape


def create_ball(space, pos):
    body = pymunk.Body(.1, 999, pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(
        body,
        3,
    )

    shape.elasticity = 0.1

    space.add(body, shape)
    return shape


def create_wall(space, dim, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Poly.create_box(body, dim)
    space.add(body, shape)
    return shape


def draw_box(box):
    k = list(
        map(
            lambda x:
            (x[0] + box.body.position[0], x[1] + box.body.position[1]),
            box.get_vertices()))
    k.append(k[0])
    pygame.draw.polygon(screen, (200, 100, 0), k, 0)
    pygame.draw.circle(screen, (255, 255, 0), box.body.position, 3, 1)


def draw_ball(ball):
    pygame.draw.circle(screen, (103, 71, 54), ball.body.position, 3)


def rem_illegal(cline, rlist):
    for item in cline:
        for rect in rlist:
            if rect.collidepoint(item):
                cline.remove(item)
                break


def physics_mode(cuplist,
                 startpos,
                 space,
                 wlist,
                 stoplist=[],
                 fliplist=[],
                 dpipe=True,
                 message="press r to move to the next level"):
    held = False
    llist = []
    cline = []
    lmp = [(0, 0)]

    blist = []
    cooldown = 0
    pipe = pygame.image.load("pipe.png")
    prect = pipe.get_rect(center=startpos)
    endmess = font.render(message, True, (75, 75, 75))
    for item in llist:
        for i in range(len(item.points) - 1):
            create_segment(space, item.points[i], item.points[i + 1])
    c = pygame.time.Clock()

    done = False
    while not done:

        if cooldown <= 0 and c.get_time() <= 17:

            blist.append(
                create_ball(space,
                            (startpos[0] + randint(-1, 1), startpos[1])))
            cooldown = 5
        else:
            cooldown -= 1
        c.tick(60)
        space.step(0.01)
        screen.fill((255, 255, 255))

        space.step(0.01)
        go = True
        for item in stoplist:
            if item.collidepoint(pygame.mouse.get_pos()):
                go = False
        if not go and held:
            held = False
            rem_illegal(cline, stoplist)
            if len(cline) > 1:
                llist.append(Line(cline))
            cline = []

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and go:
                held = True
                cline = [pygame.mouse.get_pos()]

            elif (event.type == pygame.MOUSEBUTTONUP and (go)) and held:
                held = False
                create_segment(space, cline[-1], pygame.mouse.get_pos())
                llist.append(Line(cline + [pygame.mouse.get_pos()]))
                cline = []
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                done = True

        if not pygame.mouse.get_focused() and held:
            held = False
            create_segment(space, cline[-1], pygame.mouse.get_pos())
            llist.append(Line(cline + [pygame.mouse.get_pos()]))
            cline = []
        if len(cline) > 0:
            pygame.draw.lines(screen, (0, 0, 0), False,
                              cline + [pygame.mouse.get_pos()], 3)
        if held:
            mp = pygame.mouse.get_pos()
            mouse_vec = (mp[0] - lmp[-1][0], mp[1] - lmp[-1][1])
            line_vec = (lmp[-1][0] - lmp[-2][0], lmp[-1][1] - lmp[-2][1])
            normalise_length = math.hypot(mouse_vec[0],
                                          mouse_vec[1]) * math.hypot(
                                              line_vec[0], line_vec[1])
            if normalise_length != 0:
                if (mouse_vec[0] * line_vec[0] + mouse_vec[1] *
                        line_vec[1]) / normalise_length < 0.95 or math.hypot(
                            mp[0] - cline[-1][0], mp[1] - cline[-1][1]) > 75:

                    create_segment(space, cline[-1], pygame.mouse.get_pos())
                    cline.append(pygame.mouse.get_pos())
        for item in stoplist:
            pygame.draw.rect(screen, (75, 100, 200), item)
        for item in fliplist:
            pygame.draw.rect(screen, (175, 10, 100), item)
        for item in blist:
            draw_ball(item)
            for cup in cuplist:
                if cup.check(item):
                    blist.remove(item)
                    space._remove_shape(item)
                    space._remove_body(item.body)
                    break
            for flip in fliplist:
                if flip.collidepoint(item.body.position):
                    item.body.velocity = (item.body.velocity[0], -400)
            if item.body.position[1] > 500:
                item.body.position = (item.body.position[0], 0)
            elif item.body.position[1] < 0:
                item.body.position = (item.body.position[0], 500)
            if item.body.position[0] > 500:
                item.body.position = (0, item.body.position[1])
            elif item.body.position[0] < 0:
                item.body.position = (500, item.body.position[1])
        if dpipe:
            screen.blit(pipe, prect)
        for item in wlist:
            draw_box(item)
        for item in llist:
            item.draw(screen)
        for cup in cuplist:
            cup.draw(screen)
        if sum(list(map(lambda x: x.req, cuplist))) <= 0:
            screen.blit(endmess, endmess.get_rect(center=(250, 150)))
        pygame.draw.circle(screen, (0, 0, 0), pygame.mouse.get_pos(), 5, 2)
        pygame.display.flip()

        if lmp[-1] != pygame.mouse.get_pos():
            lmp.append(pygame.mouse.get_pos())
        if len(lmp) > 2:
            lmp = lmp[-2:]
    if sum(list(map(lambda x: x.req, cuplist))) > 0:
        return False
    else:
        return True


def level_1():
    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    cuplist = [Cup((35, 350), 50, space)]
    wall_list = [
        create_wall(space, (500, 10), (250, 5)),
        create_wall(space, (500, 10), (250, 495)),
        create_wall(space, (10, 500), (495, 250)),
        create_wall(space, (10, 500), (5, 250)),
        create_wall(space, (100, 10), (15, 368))
    ]
    return physics_mode(cuplist, (450, 30), space, wall_list)


def level_2():
    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    cuplist = [Cup((465, 350), 50, space), Cup((465, 450), 50, space)]
    wall_list = [
        create_wall(space, (500, 10), (250, 5)),
        create_wall(space, (500, 10), (250, 495)),
        create_wall(space, (10, 500), (495, 250)),
        create_wall(space, (10, 500), (5, 250)),
        create_wall(space, (100, 10), (485, 368)),
        create_wall(space, (100, 10), (485, 468))
    ]
    return physics_mode(cuplist, (30, 30), space, wall_list)


def level_3():
    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    cuplist = [Cup((350, 100), 50, space)]
    wall_list = [
        create_wall(space, (400, 10), (200, 5)),
        create_wall(space, (400, 10), (200, 495)),
        create_wall(space, (10, 500), (495, 250)),
        create_wall(space, (10, 500), (5, 250)),
        create_wall(space, (10, 200), (250, 390)),
        create_wall(space, (10, 200), (250, 110)),
        create_wall(space, (30, 10), (475, 5)),
        create_wall(space, (30, 10), (475, 495)),
        create_wall(space, (175, 10), (412, 118))
    ]
    return physics_mode(cuplist, (30, 30), space, wall_list)


def level_4():
    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    cuplist = [
        Cup((400, 478), 25, space),
        Cup((100, 478), 25, space),
        Cup((350, 358), 25, space),
        Cup((150, 358), 25, space),
        Cup((300, 243), 25, space),
        Cup((200, 243), 25, space)
    ]
    wall_list = [
        create_wall(space, (500, 10), (250, 5)),
        create_wall(space, (500, 10), (250, 495)),
        create_wall(space, (10, 500), (495, 250)),
        create_wall(space, (10, 500), (5, 250)),
        create_wall(space, (200, 10), (390, 375)),
        create_wall(space, (200, 10), (110, 375)),
        create_wall(space, (200, 10), (390, 260)),
        create_wall(space, (200, 10), (110, 260))
    ]
    return physics_mode(cuplist, (250, 45), space, wall_list)


def level_5():

    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    cuplist = [Cup((80, 277), 50, space), Cup((80, 157), 50, space)]
    wall_list = [
        create_wall(space, (300, 10), (250, 5)),
        create_wall(space, (300, 10), (250, 495)),
        create_wall(space, (10, 200), (495, 100)),
        create_wall(space, (10, 200), (5, 100)),
        create_wall(space, (10, 200), (495, 400)),
        create_wall(space, (10, 200), (5, 400)),
        create_wall(space, (125, 10), (63, 295)),
        create_wall(space, (125, 10), (63, 175)),
        create_wall(space, (125, 10), (437, 350)),
        create_wall(space, (10, 370), (379, 160)),
        create_wall(space, (10, 290), (120, 150)),
    ]
    return physics_mode(cuplist, (200, 45), space, wall_list)


def level_6():
    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    cuplist = [Cup((35, 350), 50, space)]
    rlist = [pygame.Rect(250, 0, 75, 500)]
    wall_list = [
        create_wall(space, (500, 10), (250, 5)),
        create_wall(space, (500, 10), (250, 495)),
        create_wall(space, (10, 500), (495, 250)),
        create_wall(space, (10, 500), (5, 250)),
        create_wall(space, (100, 10), (15, 368))
    ]
    return physics_mode(cuplist, (450, 30), space, wall_list, stoplist=rlist)


def level_7():
    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    cuplist = [Cup((465, 350), 50, space)]
    rlist = [pygame.Rect(250, 0, 250, 500)]
    wall_list = [
        create_wall(space, (500, 10), (250, 5)),
        create_wall(space, (500, 10), (250, 495)),
        create_wall(space, (10, 500), (495, 250)),
        create_wall(space, (10, 500), (5, 250)),
        create_wall(space, (100, 10), (480, 368))
    ]
    return physics_mode(cuplist, (50, 30), space, wall_list, stoplist=rlist)


def level_8():
    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    cuplist = [Cup((35, 150), 5, space)]
    rlist = [pygame.Rect(250, 0, 250, 250)]
    wall_list = [
        create_wall(space, (370, 10), (185, 5)),
        create_wall(space, (370, 10), (185, 495)),
        create_wall(space, (10, 500), (495, 250)),
        create_wall(space, (10, 500), (5, 250)),
        create_wall(space, (100, 10), (15, 168))
    ]
    return physics_mode(cuplist, (450, 30),
                        space,
                        wall_list,
                        stoplist=rlist,
                        dpipe=False)


def level_9():

    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    cuplist = [Cup((35, 200), 50, space)]
    fliplist = [pygame.Rect(100, 480, 100, 20)]
    wall_list = [
        create_wall(space, (500, 10), (250, 5)),
        create_wall(space, (500, 10), (250, 495)),
        create_wall(space, (10, 500), (495, 250)),
        create_wall(space, (10, 500), (5, 250)),
        create_wall(space, (100, 10), (15, 218)),
        create_wall(space, (10, 300), (250, 150)),
        create_wall(space, (10, 150), (250, 500))
    ]
    return physics_mode(cuplist, (450, 30),
                        space,
                        wall_list,
                        fliplist=fliplist)


def level_10():

    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    cuplist = [Cup((465, 400), 50, space)]
    fliplist = [pygame.Rect(100, 230, 100, 20)]
    wall_list = [
        create_wall(space, (300, 10), (350, 5)),
        create_wall(space, (300, 10), (350, 495)),
        create_wall(space, (10, 500), (495, 250)),
        create_wall(space, (10, 500), (5, 250)),
        create_wall(space, (100, 10), (485, 418)),
        create_wall(space, (500, 10), (250, 250))
    ]
    return physics_mode(cuplist, (450, 30),
                        space,
                        wall_list,
                        fliplist=fliplist)


def level_11():

    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    rlist = [pygame.Rect(350, 0, 150, 300), pygame.Rect(0, 0, 200, 500)]
    cuplist = [Cup((35, 200), 50, space)]
    fliplist = [pygame.Rect(255, 480, 100, 20)]
    wall_list = [
        create_wall(space, (500, 10), (250, 5)),
        create_wall(space, (500, 10), (250, 495)),
        create_wall(space, (10, 500), (495, 250)),
        create_wall(space, (10, 500), (5, 250)),
        create_wall(space, (100, 10), (15, 218)),
        create_wall(space, (10, 400), (250, 300))
    ]
    physics_mode(cuplist, (450, 30),
                 space,
                 wall_list,
                 stoplist=rlist,
                 fliplist=fliplist,
                 message="thanks for playing, you win")


def level_12():
    space = pymunk.Space()
    space.gravity = (0, 40)
    space = pymunk.Space()
    space.gravity = (0, 40)
    rlist = [pygame.Rect(350, 0, 150, 150)]
    cuplist = [Cup((35, 100), 100, space)]
    fliplist = []
    wall_list = [
        create_wall(space, (350, 10), (175, 5)),
        create_wall(space, (350, 10), (175, 495)),
        create_wall(space, (10, 500), (495, 250)),
        create_wall(space, (10, 500), (5, 250)),
        create_wall(space, (1000, 10), (15, 218)),
        create_wall(space, (100, 10), (15, 118)),
    ]
    return physics_mode(cuplist, (85, 300),
                        space,
                        wall_list,
                        stoplist=rlist,
                        fliplist=fliplist)


levels = [
    level_1, level_2, level_4, level_3, level_5, level_6, level_7, level_8,
    level_12, level_9, level_10, level_11
]


def game_manage(start):
    for item in levels[start:]:
        out = False
        while not out:
            out = item()


def ui():
    rlist = []
    uicov = pygame.Surface((500, 500))
    k = 0
    im = uifont.render("choose level", True, (255, 255, 255))
    uicov.blit(im, im.get_rect(center=(250, 50)))
    for y in range(3):
        for x in range(4):
            k += 1
            rlist.append(pygame.Rect(x * 115 + 28, y * 115 + 85, 100, 100))
            pygame.draw.rect(uicov, (255, 0, 78), rlist[-1])
            im = uifont.render(str(k), True, (0, 0, 0))
            uicov.blit(im, im.get_rect(center=rlist[-1].center))
    done = False
    while not done:
        screen.blit(uicov, (0, 0))
        pygame.draw.circle(screen, (250, 255, 250), pygame.mouse.get_pos(), 5,
                           2)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for x, rect in enumerate(rlist):
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        done = True
                        game_manage(x)


ui()
