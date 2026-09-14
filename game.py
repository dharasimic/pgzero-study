import re
import random
from pathlib import Path

import pygame

WIDTH = 800
HEIGHT = 600

BACKGROUND_COLOR = (35, 45, 42)
TEXT_COLOR = (226, 190, 132)
HOVER_COLOR = (247, 218, 166)
OUTLINE_COLOR = (61, 39, 27)

ui_atlas = pygame.image.load("images/MediavelUI.png").convert_alpha()
books_atlas = pygame.image.load("images/UI books & more.png").convert_alpha()
floor_atlas = pygame.image.load("images/atlas_floor-16x16.png").convert_alpha()
walls_atlas = pygame.image.load("images/atlas_walls_low-16x16.png").convert_alpha()
click_sound = pygame.mixer.Sound("sounds/SFX/sfx_pressure_key_tp.mp3")
panel_source = ui_atlas.subsurface((0, 0, 80, 96))
panel = pygame.transform.scale(panel_source, (400, 480))
x_button_frames = tuple(
    pygame.transform.scale(ui_atlas.subsurface((80 + frame * 16, 32, 16, 16)), (40, 40))
    for frame in range(2)
)
music_button_frames = tuple(
    pygame.transform.scale(
        ui_atlas.subsurface((240, 80 + frame * 16, 16, 16)), (40, 40)
    )
    for frame in range(2)
)
paper_source = books_atlas.subsurface((608, 16, 48, 64))
paper_panel = pygame.transform.scale(paper_source, (720, 520))
fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
arrow_frames = tuple(
    tuple(
        pygame.transform.scale(
            ui_atlas.subsurface(
                (
                    144 + (frame % 2) * 32 + column * 16,
                    64 + (frame // 2) * 32 + row * 16,
                    16,
                    16,
                )
            ),
            (24, 24),
        )
        for row, column in ((0, 0), (0, 1), (1, 0), (1, 1))
    )
    for frame in range(4)
)

panel_position = (
    (WIDTH - panel.get_width()) // 2,
    (HEIGHT - panel.get_height()) // 2,
)
panel_inner = pygame.Rect(13, 31, 54, 53)
panel_scale_x = panel.get_width() / panel_source.get_width()
panel_scale_y = panel.get_height() / panel_source.get_height()
panel_inner_screen = pygame.Rect(
    panel_position[0] + round(panel_inner.x * panel_scale_x),
    panel_position[1] + round(panel_inner.y * panel_scale_y),
    round(panel_inner.width * panel_scale_x),
    round(panel_inner.height * panel_scale_y),
)
button_width = 220
button_height = 48
button_left = panel_inner_screen.left + (panel_inner_screen.width - button_width) // 2
button_gap = 16
button_group_height = button_height * 3 + button_gap * 2
button_top = (
    panel_inner_screen.top + (panel_inner_screen.height - button_group_height) // 2
)
button_positions = {
    "JOGAR": pygame.Rect((button_left, button_top), (button_width, button_height)),
    "COMO JOGAR": pygame.Rect(
        (button_left, button_top + button_height + button_gap),
        (button_width, button_height),
    ),
    "SAIR": pygame.Rect(
        (button_left, button_top + (button_height + button_gap) * 2),
        (button_width, button_height),
    ),
}
game_over_button_positions = {
    "JOGAR NOVAMENTE": pygame.Rect(
        (WIDTH - button_width) // 2,
        380,
        button_width,
        button_height,
    ),
    "MENU": pygame.Rect(
        (WIDTH - button_width) // 2,
        444,
        button_width,
        button_height,
    ),
}
pause_button_positions = {
    "COMO JOGAR": button_positions["COMO JOGAR"],
    "SAIR": button_positions["SAIR"],
}

hovered_button = None
hover_animation_time = 0
game_state = "menu"
previous_state = "menu"
controls_fade = 1.0
x_button_pressed = 0
music_muted = False
GAME_OVER_TEXT = "VOCE MORREU!"
PULSE_FRAMES = (0, 1, 2, 3, 2, 1)

controls_lines = (
    "USE W A S D PARA MOVER O PERSONAGEM",
    "USE O CURSOR DO MOUSE PARA MIRAR",
    "A BRUXINHA ATIRA AUTOMATICAMENTE NA DIRECAO DO CURSOR",
    "APERTE F PARA INTERAGIR COM BAUS",
    "PASSE POR CIMA DE BOTOES PARA ATIVA-LOS",
    "COLIDIR COM INIMIGOS FAZ VOCE PERDER VIDA",
    "PERCA AS TRES VIDAS E O JOGO ACABA",
    "APERTE ESC PARA PAUSAR",
)
controls_fontsize = 26
controls_start_y = 214
controls_line_gap = 40
controls_key_color = (156, 91, 42)
controls_text_font = pygame.font.Font("fonts/monogram.ttf", controls_fontsize)
x_button_rect = pygame.Rect(20, 20, 40, 40)
music_button_rect = pygame.Rect(WIDTH - 60, HEIGHT - 60, 40, 40)

ROOM_TILE_SIZE = 32
ROOM_COLUMNS = 17
ROOM_ROWS = 17
ROOM_OPENINGS = {
    "top": (4, 12),
    "bottom": (4, 12),
    "left": (4, 12),
    "right": (4, 12),
}
room_rect = pygame.Rect(
    (WIDTH - ROOM_COLUMNS * ROOM_TILE_SIZE) // 2,
    (HEIGHT - ROOM_ROWS * ROOM_TILE_SIZE) // 2,
    ROOM_COLUMNS * ROOM_TILE_SIZE,
    ROOM_ROWS * ROOM_TILE_SIZE,
)
floor_tile = pygame.transform.scale(
    floor_atlas.subsurface((0, 0, 16, 16)),
    (ROOM_TILE_SIZE, ROOM_TILE_SIZE),
)
wall_vertical = pygame.transform.scale(
    walls_atlas.subsurface((0, 16, 16, 16)),
    (ROOM_TILE_SIZE, ROOM_TILE_SIZE),
)
wall_horizontal = pygame.transform.scale(
    walls_atlas.subsurface((32, 48, 16, 16)),
    (ROOM_TILE_SIZE, ROOM_TILE_SIZE),
)
wall_top_left = pygame.transform.scale(
    walls_atlas.subsurface((16, 0, 16, 16)),
    (ROOM_TILE_SIZE, ROOM_TILE_SIZE),
)
wall_bottom_left = pygame.transform.scale(
    walls_atlas.subsurface((16, 32, 16, 16)),
    (ROOM_TILE_SIZE, ROOM_TILE_SIZE),
)
wall_top_right = pygame.transform.scale(
    walls_atlas.subsurface((48, 0, 16, 16)),
    (ROOM_TILE_SIZE, ROOM_TILE_SIZE),
)
wall_bottom_right = pygame.transform.scale(
    walls_atlas.subsurface((48, 32, 16, 16)),
    (ROOM_TILE_SIZE, ROOM_TILE_SIZE),
)
wall_collision_masks = []


def is_opening(side, position):
    return position // ROOM_TILE_SIZE in ROOM_OPENINGS[side]


def add_wall_collision_mask(image, x, y):
    wall_collision_masks.append((pygame.mask.from_surface(image), (x, y)))


add_wall_collision_mask(wall_top_left, 0, 0)
add_wall_collision_mask(wall_top_right, room_rect.width - ROOM_TILE_SIZE, 0)
add_wall_collision_mask(
    wall_bottom_left,
    0,
    room_rect.height - ROOM_TILE_SIZE,
)
add_wall_collision_mask(
    wall_bottom_right,
    room_rect.width - ROOM_TILE_SIZE,
    room_rect.height - ROOM_TILE_SIZE,
)
for position in range(ROOM_TILE_SIZE, room_rect.width - ROOM_TILE_SIZE, ROOM_TILE_SIZE):
    if not is_opening("top", position):
        add_wall_collision_mask(wall_horizontal, position, 0)
    if not is_opening("bottom", position):
        add_wall_collision_mask(
            wall_horizontal,
            position,
            room_rect.height - ROOM_TILE_SIZE,
        )
for position in range(
    ROOM_TILE_SIZE, room_rect.height - ROOM_TILE_SIZE, ROOM_TILE_SIZE
):
    if not is_opening("left", position):
        add_wall_collision_mask(wall_vertical, 0, position)
    if not is_opening("right", position):
        add_wall_collision_mask(
            wall_vertical,
            room_rect.width - ROOM_TILE_SIZE,
            position,
        )
wizzard_idle_frames = tuple(
    pygame.transform.scale(
        pygame.image.load(
            str(Path("images/frames") / f"wizzard_f_idle_anim_f{frame}.png")
        ).convert_alpha(),
        (32, 56),
    )
    for frame in range(4)
)
wizzard_run_frames = tuple(
    pygame.transform.scale(
        pygame.image.load(
            str(Path("images/frames") / f"wizzard_f_run_anim_f{frame}.png")
        ).convert_alpha(),
        (32, 56),
    )
    for frame in range(4)
)
ogre_run_frames = tuple(
    pygame.image.load(
        str(Path("images/frames") / f"ogre_run_anim_f{frame}.png")
    ).convert_alpha()
    for frame in range(4)
)
fireball_frames = tuple(
    pygame.image.load(
        str(Path("images/frames/fireball_12") / f"fireball_spritesheet{frame + 1}.png")
    )
    .convert_alpha()
    .subsurface((frame * 32, 0, 32, 32))
    .copy()
    for frame in range(12)
)
wizzard_frame = 0
wizzard_animation_time = 0
wizzard_x = 6.5 * ROOM_TILE_SIZE
wizzard_y = 6.5 * ROOM_TILE_SIZE
wizzard_facing_left = False
WIZZARD_SPEED = 160
WIZZARD_COLLISION_WIDTH = 12
WIZZARD_COLLISION_HEIGHT = 8
WIZZARD_COLLISION_BOTTOM = 28
WIZZARD_COLLISION_MASK = pygame.mask.Mask(
    (WIZZARD_COLLISION_WIDTH, WIZZARD_COLLISION_HEIGHT),
    fill=True,
)
OGRE_SPEED = 70
OGRE_COLLISION_WIDTH = 12
OGRE_COLLISION_HEIGHT = 8
OGRE_COLLISION_BOTTOM = 28
OGRE_COLLISION_MASK = pygame.mask.Mask(
    (OGRE_COLLISION_WIDTH, OGRE_COLLISION_HEIGHT),
    fill=True,
)
ogres = []
particles = []
ogre_spawn_timer = 0
OGRE_SPAWN_INTERVAL = 1.2
ogres_defeated = 0
health = 6
damage_cooldown = 0
survival_time = 0
heart_images = {
    6: pygame.transform.scale(
        pygame.image.load("images/frames/ui_heart_full.png").convert_alpha(),
        (26, 24),
    ),
    3: pygame.transform.scale(
        pygame.image.load("images/frames/ui_heart_half.png").convert_alpha(),
        (26, 24),
    ),
    0: pygame.transform.scale(
        pygame.image.load("images/frames/ui_heart_empty.png").convert_alpha(),
        (26, 24),
    ),
}
PROJECTILE_SPEED = 320
PROJECTILE_RADIUS = 5
PROJECTILE_INTERVAL = 0.25
FIREBALL_FRAME_RATE = 16
FIREBALL_HOLD_FRAME = 9
projectiles = []
projectile_timer = 0


def wizzard_collides(x, y):
    wizzard_left = round(x - WIZZARD_COLLISION_WIDTH / 2)
    wizzard_top = round(y + WIZZARD_COLLISION_BOTTOM - WIZZARD_COLLISION_HEIGHT)
    for wall_mask, (wall_x, wall_y) in wall_collision_masks:
        if wall_mask.overlap(
            WIZZARD_COLLISION_MASK,
            (wizzard_left - wall_x, wizzard_top - wall_y),
        ):
            return True
    return False


def ogre_collides(ogre, x, y):
    ogre_left = round(x - OGRE_COLLISION_WIDTH / 2)
    ogre_top = round(y + OGRE_COLLISION_BOTTOM - OGRE_COLLISION_HEIGHT)
    for wall_mask, (wall_x, wall_y) in wall_collision_masks:
        if wall_mask.overlap(
            OGRE_COLLISION_MASK,
            (ogre_left - wall_x, ogre_top - wall_y),
        ):
            return True
    return False


def projectile_hits_wall(x, y):
    projectile_mask = pygame.mask.Mask(
        (PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2),
        fill=True,
    )
    projectile_left = round(x - PROJECTILE_RADIUS)
    projectile_top = round(y - PROJECTILE_RADIUS)
    for wall_mask, (wall_x, wall_y) in wall_collision_masks:
        if wall_mask.overlap(
            projectile_mask,
            (projectile_left - wall_x, projectile_top - wall_y),
        ):
            return True
    return False


def projectile_hits_ogre(x, y):
    return any(projectile_hits_ogre_in_enemy(x, y, ogre) for ogre in ogres)


def projectile_hits_ogre_in_enemy(x, y, ogre):
    if not ogre["inside"]:
        return False
    projectile_rect = pygame.Rect(
        round(x - PROJECTILE_RADIUS),
        round(y - PROJECTILE_RADIUS),
        PROJECTILE_RADIUS * 2,
        PROJECTILE_RADIUS * 2,
    )
    ogre_rect = pygame.Rect(
        round(ogre["x"] - OGRE_COLLISION_WIDTH / 2),
        round(ogre["y"] + OGRE_COLLISION_BOTTOM - OGRE_COLLISION_HEIGHT),
        OGRE_COLLISION_WIDTH,
        OGRE_COLLISION_HEIGHT,
    )
    return projectile_rect.colliderect(ogre_rect)


def projectile_hits_ogre_swept(start_x, start_y, end_x, end_y, ogre):
    if not ogre["inside"]:
        return False

    ogre_rect = pygame.Rect(
        round(ogre["x"] - OGRE_COLLISION_WIDTH / 2),
        round(ogre["y"] + OGRE_COLLISION_BOTTOM - OGRE_COLLISION_HEIGHT),
        OGRE_COLLISION_WIDTH,
        OGRE_COLLISION_HEIGHT,
    )

    # Aumenta a hitbox somente para a detecção do projétil
    ogre_rect.inflate_ip(PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2)

    # Verifica todo o caminho percorrido pelo projétil
    return bool(
        ogre_rect.clipline(
            round(start_x),
            round(start_y),
            round(end_x),
            round(end_y),
        )
    )


def ogre_hits_wizzard(ogre):
    ogre_rect = pygame.Rect(
        round(ogre["x"] - OGRE_COLLISION_WIDTH / 2),
        round(ogre["y"] + OGRE_COLLISION_BOTTOM - OGRE_COLLISION_HEIGHT),
        OGRE_COLLISION_WIDTH,
        OGRE_COLLISION_HEIGHT,
    )
    wizzard_rect = pygame.Rect(
        round(wizzard_x - WIZZARD_COLLISION_WIDTH / 2),
        round(wizzard_y + WIZZARD_COLLISION_BOTTOM - WIZZARD_COLLISION_HEIGHT),
        WIZZARD_COLLISION_WIDTH,
        WIZZARD_COLLISION_HEIGHT,
    )
    return ogre_rect.colliderect(wizzard_rect)


def spawn_ogre():
    side = random.choice(tuple(ROOM_OPENINGS))
    opening = random.choice(ROOM_OPENINGS[side])
    position = opening * ROOM_TILE_SIZE + ROOM_TILE_SIZE / 2
    if side == "top":
        x, y, entry_target, facing_left = (
            position,
            -16,
            (position, ROOM_TILE_SIZE * 1.5),
            False,
        )
    elif side == "bottom":
        x, y, entry_target, facing_left = (
            position,
            room_rect.height + 16,
            (position, room_rect.height - ROOM_TILE_SIZE * 1.5),
            False,
        )
    elif side == "left":
        x, y, entry_target, facing_left = (
            -16,
            position,
            (ROOM_TILE_SIZE * 1.5, position),
            False,
        )
    else:
        x, y, entry_target, facing_left = (
            room_rect.width + 16,
            position,
            (room_rect.width - ROOM_TILE_SIZE * 1.5, position),
            True,
        )
    ogres.append(
        {
            "x": x,
            "y": y,
            "entry_target": entry_target,
            "inside": False,
            "frame": 0,
            "animation_time": random.random(),
            "facing_left": facing_left,
        }
    )


def create_death_particles(x, y):
    for _ in range(10):
        direction = pygame.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1),
        )

        if direction.length_squared() == 0:
            direction = pygame.Vector2(1, 0)

        direction.normalize_ip()

        particles.append(
            {
                "position": pygame.Vector2(x, y),
                "velocity": direction * random.uniform(40, 100),
                "life": random.uniform(0.25, 0.5),
                "size": random.randint(2, 4),
            }
        )


def update_particles(dt):
    for particle in particles[:]:
        particle["life"] -= dt

        if particle["life"] <= 0:
            particles.remove(particle)
            continue

        particle["position"] += particle["velocity"] * dt
        particle["velocity"] *= 0.92


def draw_particles(surface):
    for particle in particles:
        position = particle["position"]
        size = particle["size"]

        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (
                round(position.x),
                round(position.y),
            ),
            size,
        )


def reset_game():
    global game_state, wizzard_x, wizzard_y, wizzard_frame
    global wizzard_animation_time, wizzard_facing_left, projectile_timer
    global ogre_spawn_timer, ogres_defeated, health, damage_cooldown, survival_time

    ogres.clear()
    projectiles.clear()
    particles.clear()

    wizzard_x = 6.5 * ROOM_TILE_SIZE
    wizzard_y = 6.5 * ROOM_TILE_SIZE
    wizzard_frame = 0
    wizzard_animation_time = 0
    wizzard_facing_left = False

    projectile_timer = 0
    ogre_spawn_timer = 0
    ogres_defeated = 0
    health = 6
    damage_cooldown = 0
    survival_time = 0

    spawn_ogre()
    game_state = "game"


def create_projectile(mouse_position):
    direction = pygame.Vector2(
        mouse_position[0] - room_rect.left - wizzard_x,
        mouse_position[1] - room_rect.top - wizzard_y,
    )
    if direction.length_squared() == 0:
        return
    direction.normalize_ip()
    projectiles.append(
        {
            "position": pygame.Vector2(wizzard_x, wizzard_y),
            "direction": direction,
            "animation_time": 0,
        }
    )


def update_projectiles(dt):
    global ogres_defeated

    for projectile in projectiles[:]:
        # Guarda onde o projétil estava antes de se mover
        previous_position = projectile["position"].copy()

        projectile["animation_time"] += dt
        projectile["position"] += projectile["direction"] * PROJECTILE_SPEED * dt

        position = projectile["position"]

        if projectile_hits_wall(position.x, position.y):
            projectiles.remove(projectile)
            continue

        for ogre in ogres[:]:
            if projectile_hits_ogre_swept(
                previous_position.x,
                previous_position.y,
                position.x,
                position.y,
                ogre,
            ):
                projectiles.remove(projectile)

                create_death_particles(
                    ogre["x"],
                    ogre["y"],
                )

                ogres.remove(ogre)
                ogres_defeated += 1
                break


def update_ogres(dt):
    global ogre_spawn_timer, health, damage_cooldown, game_state

    ogre_spawn_timer += dt
    while ogre_spawn_timer >= OGRE_SPAWN_INTERVAL:
        ogre_spawn_timer -= OGRE_SPAWN_INTERVAL
        spawn_ogre()

    damage_cooldown = max(0, damage_cooldown - dt)
    for ogre in ogres:
        if not ogre["inside"]:
            entry_direction = pygame.Vector2(
                ogre["entry_target"][0] - ogre["x"],
                ogre["entry_target"][1] - ogre["y"],
            )
            if entry_direction.length() <= OGRE_SPEED * dt:
                ogre["x"], ogre["y"] = ogre["entry_target"]
                ogre["inside"] = True
            else:
                entry_direction.normalize_ip()
                ogre["x"] += entry_direction.x * OGRE_SPEED * dt
                ogre["y"] += entry_direction.y * OGRE_SPEED * dt
                ogre["facing_left"] = entry_direction.x < 0
            ogre["animation_time"] += dt
            ogre["frame"] = int(ogre["animation_time"] * 6) % len(ogre_run_frames)
            continue

        direction = pygame.Vector2(wizzard_x - ogre["x"], wizzard_y - ogre["y"])
        if direction.length_squared() > 0:
            direction.normalize_ip()
            movement_x = direction.x * OGRE_SPEED * dt
            movement_y = direction.y * OGRE_SPEED * dt
            if not ogre_collides(ogre, ogre["x"] + movement_x, ogre["y"]):
                ogre["x"] += movement_x
            if not ogre_collides(ogre, ogre["x"], ogre["y"] + movement_y):
                ogre["y"] += movement_y
            ogre["facing_left"] = direction.x < 0
        ogre["animation_time"] += dt
        ogre["frame"] = int(ogre["animation_time"] * 6) % len(ogre_run_frames)

        if damage_cooldown == 0 and ogre_hits_wizzard(ogre):
            health -= 1
            damage_cooldown = 0.8
            if health <= 0:
                game_state = "game_over"
                return


def update(dt):
    global hover_animation_time, controls_fade, x_button_pressed, game_state
    global previous_state
    global wizzard_frame, wizzard_animation_time, wizzard_x, wizzard_y
    global wizzard_facing_left, projectile_timer
    global survival_time

    hover_animation_time += dt
    wizzard_animation_time += dt

    if game_state == "game":
        survival_time += dt

        projectile_timer += dt

        while projectile_timer >= PROJECTILE_INTERVAL:
            projectile_timer -= PROJECTILE_INTERVAL
            create_projectile(pygame.mouse.get_pos())

        update_projectiles(dt)
        update_particles(dt)

        is_moving = keyboard.w or keyboard.s or keyboard.a or keyboard.d

        if keyboard.a:
            wizzard_facing_left = True
        elif keyboard.d:
            wizzard_facing_left = False

        movement_x = 0
        movement_y = 0

        if keyboard.a:
            movement_x -= WIZZARD_SPEED * dt

        if keyboard.d:
            movement_x += WIZZARD_SPEED * dt

        if keyboard.w:
            movement_y -= WIZZARD_SPEED * dt

        if keyboard.s:
            movement_y += WIZZARD_SPEED * dt

        if not wizzard_collides(wizzard_x + movement_x, wizzard_y):
            wizzard_x += movement_x

        if not wizzard_collides(wizzard_x, wizzard_y + movement_y):
            wizzard_y += movement_y

        animation_frames = wizzard_run_frames if is_moving else wizzard_idle_frames

        wizzard_frame = int(wizzard_animation_time * 6) % len(animation_frames)

        wizzard_image = animation_frames[wizzard_frame]

        wizzard_x = max(
            WIZZARD_COLLISION_WIDTH / 2,
            wizzard_x,
        )

        wizzard_x = min(
            room_rect.width - WIZZARD_COLLISION_WIDTH / 2,
            wizzard_x,
        )

        wizzard_y = max(
            ROOM_TILE_SIZE - WIZZARD_COLLISION_BOTTOM + WIZZARD_COLLISION_HEIGHT,
            wizzard_y,
        )

        wizzard_y = min(
            room_rect.height - ROOM_TILE_SIZE - WIZZARD_COLLISION_BOTTOM,
            wizzard_y,
        )

        update_ogres(dt)

    if game_state == "controls":
        controls_fade = max(
            0.0,
            controls_fade - dt / 0.18,
        )

        if x_button_pressed:
            x_button_pressed = max(
                0.0,
                x_button_pressed - dt,
            )

            if x_button_pressed == 0:
                game_state = previous_state


def draw():
    screen.fill(BACKGROUND_COLOR)
    if game_state == "controls":
        draw_controls()
        return
    if game_state == "game_over":
        draw_game_over()
        return
    if game_state == "paused":
        draw_pause()
        return
    if game_state == "game":
        draw_game()
        return

    screen.blit(panel, panel_position)

    for label, button in button_positions.items():
        color = HOVER_COLOR if label == hovered_button else TEXT_COLOR
        screen.draw.text(
            label,
            center=button.center,
            fontname="monogram",
            fontsize=38,
            color=color,
            owidth=1,
            ocolor=OUTLINE_COLOR,
        )

        if label == hovered_button:
            draw_hover_arrows(button)

    if game_state == "menu":
        music_frame = 1 if music_muted else 0
        screen.blit(music_button_frames[music_frame], music_button_rect.topleft)


def draw_game():
    room_surface = pygame.Surface(room_rect.size, pygame.SRCALPHA)

    for row in range(ROOM_ROWS):
        for column in range(ROOM_COLUMNS):
            room_surface.blit(
                floor_tile,
                (column * ROOM_TILE_SIZE, row * ROOM_TILE_SIZE),
            )

    # Paredes
    room_surface.blit(wall_top_left, (0, 0))
    room_surface.blit(
        wall_top_right,
        (room_rect.width - ROOM_TILE_SIZE, 0),
    )
    room_surface.blit(
        wall_bottom_left,
        (0, room_rect.height - ROOM_TILE_SIZE),
    )
    room_surface.blit(
        wall_bottom_right,
        (
            room_rect.width - ROOM_TILE_SIZE,
            room_rect.height - ROOM_TILE_SIZE,
        ),
    )

    draw_wall_with_openings(
        room_surface,
        wall_horizontal,
        "top",
    )
    draw_wall_with_openings(
        room_surface,
        wall_horizontal,
        "bottom",
    )
    draw_wall_with_openings(
        room_surface,
        wall_vertical,
        "left",
        vertical=True,
    )
    draw_wall_with_openings(
        room_surface,
        wall_vertical,
        "right",
        vertical=True,
    )

    # Projéteis
    draw_projectiles(room_surface)

    # Ogros
    for ogre in ogres:
        if not ogre["inside"]:
            continue

        ogre_image = ogre_run_frames[ogre["frame"]]

        if ogre["facing_left"]:
            ogre_image = pygame.transform.flip(
                ogre_image,
                True,
                False,
            )

        ogre_position = (
            ogre["x"] - ogre_image.get_width() // 2,
            ogre["y"] - ogre_image.get_height() // 2,
        )

        room_surface.blit(
            ogre_image,
            ogre_position,
        )

    # Partículas
    draw_particles(room_surface)

    # Bruxinha
    is_moving = keyboard.w or keyboard.s or keyboard.a or keyboard.d

    animation_frames = wizzard_run_frames if is_moving else wizzard_idle_frames

    wizzard_image = animation_frames[wizzard_frame]

    if wizzard_facing_left:
        wizzard_image = pygame.transform.flip(
            wizzard_image,
            True,
            False,
        )

    wizzard_position = (
        wizzard_x - wizzard_image.get_width() // 2,
        wizzard_y - wizzard_image.get_height() // 2,
    )

    # Pisca durante a invencibilidade após tomar dano
    if damage_cooldown <= 0 or int(damage_cooldown * 12) % 2 == 0:
        room_surface.blit(
            wizzard_image,
            wizzard_position,
        )

    screen.blit(
        room_surface,
        room_rect.topleft,
    )

    draw_hud()


def draw_projectiles(surface):
    for projectile in projectiles:
        position = projectile["position"]
        frame = min(
            int(projectile["animation_time"] * FIREBALL_FRAME_RATE),
            FIREBALL_HOLD_FRAME,
        )
        image = fireball_frames[frame]
        surface.blit(
            image,
            (
                round(position.x - image.get_width() / 2),
                round(position.y - image.get_height() / 2),
            ),
        )


def draw_wall_with_openings(surface, image, side, vertical=False):
    x = room_rect.width - ROOM_TILE_SIZE if side == "right" else 0
    y = room_rect.height - ROOM_TILE_SIZE if side == "bottom" else 0
    for position in (
        range(ROOM_TILE_SIZE, room_rect.width - ROOM_TILE_SIZE, ROOM_TILE_SIZE)
        if not vertical
        else range(ROOM_TILE_SIZE, room_rect.height - ROOM_TILE_SIZE, ROOM_TILE_SIZE)
    ):
        if is_opening(side, position):
            continue
        if vertical:
            surface.blit(image, (x, position))
        else:
            surface.blit(image, (position, y))


def draw_hud():
    for heart_number in range(3):
        remaining_health = health - heart_number * 2
        heart = heart_images[
            6 if remaining_health >= 2 else 3 if remaining_health == 1 else 0
        ]
        screen.blit(heart, (20 + heart_number * 30, 20))
    screen.draw.text(
        f"OGROS: {ogres_defeated}",
        (20, 52),
        fontname="monogram",
        fontsize=24,
        color=TEXT_COLOR,
        owidth=1,
        ocolor=OUTLINE_COLOR,
    )


def draw_game_over():
    center_x = WIDTH // 2

    screen.draw.text(
        "Game over :(",
        center=(center_x, 180),
        fontname="monogram",
        fontsize=58,
        color=TEXT_COLOR,
        owidth=2,
        ocolor=OUTLINE_COLOR,
    )

    screen.draw.text(
        f"TEMPO SOBREVIVIDO: {format_survival_time()}",
        center=(center_x, 270),
        fontname="monogram",
        fontsize=30,
        color=TEXT_COLOR,
    )

    screen.draw.text(
        f"OGROS MORTOS: {ogres_defeated}",
        center=(center_x, 315),
        fontname="monogram",
        fontsize=30,
        color=TEXT_COLOR,
    )

    screen.draw.text(
        "JOGAR NOVAMENTE",
        center=game_over_button_positions["JOGAR NOVAMENTE"].center,
        fontname="monogram",
        fontsize=38,
        color=(HOVER_COLOR if hovered_button == "JOGAR NOVAMENTE" else TEXT_COLOR),
        owidth=1,
        ocolor=OUTLINE_COLOR,
    )

    if hovered_button == "JOGAR NOVAMENTE":
        draw_game_over_hover_arrows(game_over_button_positions["JOGAR NOVAMENTE"])

    screen.draw.text(
        "MENU",
        center=game_over_button_positions["MENU"].center,
        fontname="monogram",
        fontsize=38,
        color=(HOVER_COLOR if hovered_button == "MENU" else TEXT_COLOR),
        owidth=1,
        ocolor=OUTLINE_COLOR,
    )

    if hovered_button == "MENU":
        draw_hover_arrows(game_over_button_positions["MENU"])


def draw_game_over_hover_arrows(button):
    frame = PULSE_FRAMES[int(hover_animation_time * 4) % len(PULSE_FRAMES)]

    arrow_gap = 12

    positions = (
        (
            (button.left - arrow_gap, button.top),
            arrow_frames[frame][0],
        ),
        (
            (button.right + arrow_gap - 24, button.top),
            arrow_frames[frame][1],
        ),
        (
            (button.left - arrow_gap, button.bottom - 24),
            arrow_frames[frame][2],
        ),
        (
            (
                button.right + arrow_gap - 24,
                button.bottom - 24,
            ),
            arrow_frames[frame][3],
        ),
    )

    for position, image in positions:
        screen.blit(image, position)


def draw_pause():
    screen.blit(panel, panel_position)
    screen.draw.text(
        "PAUSADO",
        center=(WIDTH // 2, panel_inner_screen.top + 34),
        fontname="monogram",
        fontsize=38,
        color=TEXT_COLOR,
        owidth=1,
        ocolor=OUTLINE_COLOR,
    )
    for label, button in pause_button_positions.items():
        color = HOVER_COLOR if label == hovered_button else TEXT_COLOR
        screen.draw.text(
            label,
            center=button.center,
            fontname="monogram",
            fontsize=38,
            color=color,
            owidth=1,
            ocolor=OUTLINE_COLOR,
        )
        if label == hovered_button:
            draw_hover_arrows(button)
    screen.blit(music_button_frames[1 if music_muted else 0], music_button_rect.topleft)


def format_survival_time():
    minutes = int(survival_time) // 60
    seconds = int(survival_time) % 60
    return f"{minutes:02d}:{seconds:02d}"


def draw_repeated_wall(surface, image, x, y, vertical=False):
    if image.get_width() > surface.get_width() - x:
        return
    if image.get_height() > surface.get_height() - y:
        return
    if vertical:
        for position_y in range(
            y, surface.get_height() - ROOM_TILE_SIZE, image.get_height()
        ):
            surface.blit(image, (x, position_y))
    else:
        for position_x in range(
            x, surface.get_width() - ROOM_TILE_SIZE, image.get_width()
        ):
            surface.blit(image, (position_x, y))


def draw_controls():
    screen.blit(paper_panel, ((WIDTH - paper_panel.get_width()) // 2, 40))
    screen.draw.text(
        "COMO JOGAR",
        center=(WIDTH // 2, 154),
        fontname="monogram",
        fontsize=42,
        color=OUTLINE_COLOR,
        owidth=1,
        ocolor=TEXT_COLOR,
    )

    for line_number, text in enumerate(controls_lines):
        draw_control_line(text, controls_start_y + line_number * controls_line_gap)

    frame = 1 if x_button_pressed else 0
    screen.blit(x_button_frames[frame], x_button_rect.topleft)
    if controls_fade:
        fade_surface.fill((0, 0, 0, round(255 * controls_fade)))
        screen.blit(fade_surface, (0, 0))


def draw_control_line(text, y):
    segments = []
    last_token_end = 0
    for token_match in re.finditer(r"\b(?:W|A|S|D|F|ESC)\b", text):
        if token_match.start() > last_token_end:
            segments.append((text[last_token_end : token_match.start()], OUTLINE_COLOR))
        segments.append((token_match.group(), controls_key_color))
        last_token_end = token_match.end()
    if last_token_end < len(text):
        segments.append((text[last_token_end:], OUTLINE_COLOR))

    total_width = sum(controls_text_font.size(segment)[0] for segment, _ in segments)
    segment_left = (WIDTH - total_width) / 2
    for segment, color in segments:
        segment_width = controls_text_font.size(segment)[0]
        segment_surface = controls_text_font.render(segment, True, color)
        screen.blit(
            segment_surface,
            (segment_left, y - segment_surface.get_height() / 2),
        )
        segment_left += segment_width


def draw_hover_arrows(button):
    frame = PULSE_FRAMES[int(hover_animation_time * 4) % len(PULSE_FRAMES)]
    positions = (
        ((button.left, button.top), arrow_frames[frame][0]),
        ((button.right - 24, button.top), arrow_frames[frame][1]),
        ((button.left, button.bottom - 24), arrow_frames[frame][2]),
        ((button.right - 24, button.bottom - 24), arrow_frames[frame][3]),
    )

    for position, image in positions:
        screen.blit(image, position)


def on_mouse_move(pos):
    global hovered_button
    if game_state == "menu":
        buttons = button_positions
    elif game_state == "paused":
        buttons = pause_button_positions
    elif game_state == "game_over":
        buttons = game_over_button_positions
    else:
        hovered_button = None
        return

    hovered_button = None
    for label, button in buttons.items():
        if button.collidepoint(pos):
            hovered_button = label
            break


def on_mouse_down(pos, button):
    global game_state, controls_fade, x_button_pressed, music_muted, previous_state

    if game_state == "game":
        return

    if game_state == "game_over":
        if game_over_button_positions["JOGAR NOVAMENTE"].collidepoint(pos):
            click_sound.play()
            reset_game()
        elif game_over_button_positions["MENU"].collidepoint(pos):
            click_sound.play()
            game_state = "menu"
        return

    if game_state == "paused":
        if music_button_rect.collidepoint(pos):
            click_sound.play()
            music_muted = not music_muted
            music.set_volume(0 if music_muted else 1)
        elif pause_button_positions["COMO JOGAR"].collidepoint(pos):
            previous_state = "paused"
            game_state = "controls"
            controls_fade = 1.0
        elif pause_button_positions["SAIR"].collidepoint(pos):
            click_sound.play()
            game_state = "menu"
        return

    if game_state == "controls":
        if x_button_rect.collidepoint(pos):
            click_sound.play()
            x_button_pressed = 0.08
        return

    if game_state != "menu":
        return

    if music_button_rect.collidepoint(pos):
        click_sound.play()
        music_muted = not music_muted
        music.set_volume(0 if music_muted else 1)
        return

    if any(button.collidepoint(pos) for button in button_positions.values()):
        click_sound.play()

    if button_positions["COMO JOGAR"].collidepoint(pos):
        previous_state = "menu"
        game_state = "controls"
        controls_fade = 1.0
        hovered_button = None
    elif button_positions["JOGAR"].collidepoint(pos):
        reset_game()
        hovered_button = None
    elif button_positions["SAIR"].collidepoint(pos):
        quit()


def on_key_down(key):
    global game_state, hovered_button
    if key == keys.ESCAPE:
        if game_state == "game":
            game_state = "paused"
            hovered_button = None
        elif game_state == "paused":
            game_state = "game"


music.play("jardins")
