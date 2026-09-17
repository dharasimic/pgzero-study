import random
import os
import sys
from pathlib import Path

from pgzero import music
import pygame

WIDTH = 800
HEIGHT = 600

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT))

BACKGROUND_COLOR = (35, 45, 42)
GAME_BACKGROUND_COLOR = (5, 5, 8)
TEXT_COLOR = (240, 238, 225)
HOVER_COLOR = (255, 253, 240)
OUTLINE_COLOR = (61, 39, 27)

ui_atlas = pygame.image.load("images/MediavelUI.png").convert_alpha()
walls_atlas = pygame.image.load("images/atlas_walls_low-16x16.png").convert_alpha()
menu_background = pygame.image.load("images/menu_background.jpg").convert()

menu_background = pygame.transform.scale(
    menu_background,
    (WIDTH, HEIGHT),
)

game_over_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
game_over_overlay.fill((0, 0, 0, 150))
click_sound = pygame.mixer.Sound("sounds/SFX/sfx_pressure_key_tp.mp3")
panel_source = ui_atlas.subsurface((0, 0, 80, 96))
panel = pygame.transform.scale(panel_source, (400, 480))
music_button_frames = tuple(
    pygame.transform.scale(
        ui_atlas.subsurface((240, 80 + frame * 16, 16, 16)), (40, 40)
    )
    for frame in range(2)
)

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
    100,
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

button_positions = {
    "JOGAR": pygame.Rect(
        (WIDTH - button_width) // 2,
        268,
        button_width,
        button_height,
    ),
    "SAIR": pygame.Rect(
        (WIDTH - button_width) // 2,
        316,
        button_width,
        button_height,
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
pause_panel_position = (
    (WIDTH - panel.get_width()) // 2,
    (HEIGHT - panel.get_height()) // 2,
)

pause_panel_inner = pygame.Rect(
    13,
    31,
    54,
    53,
)

pause_panel_scale_x = panel.get_width() / panel_source.get_width()
pause_panel_scale_y = panel.get_height() / panel_source.get_height()

pause_panel_inner_screen = pygame.Rect(
    pause_panel_position[0] + round(pause_panel_inner.x * pause_panel_scale_x),
    pause_panel_position[1] + round(pause_panel_inner.y * pause_panel_scale_y),
    round(pause_panel_inner.width * pause_panel_scale_x),
    round(pause_panel_inner.height * pause_panel_scale_y),
)

pause_button_width = 220
pause_button_height = 48
pause_button_gap = 16

pause_button_left = (
    pause_panel_inner_screen.left
    + (pause_panel_inner_screen.width - pause_button_width) // 2
)

pause_button_positions = {
    "CONTINUAR": pygame.Rect(
        pause_button_left,
        pause_panel_inner_screen.centery
        - pause_button_height
        - pause_button_gap // 2
        + 15,
        pause_button_width,
        pause_button_height,
    ),
    "SAIR": pygame.Rect(
        pause_button_left,
        pause_panel_inner_screen.centery + pause_button_gap // 2,
        pause_button_width,
        pause_button_height,
    ),
}

pause_overlay = pygame.Surface(
    (WIDTH, HEIGHT),
    pygame.SRCALPHA,
)
pause_overlay.fill((0, 0, 0, 150))

hovered_button = None
hover_animation_time = 0
game_state = "menu"
music_muted = False
MENU_MUSIC = "mystery"
GAME_MUSIC_1 = "haunted"
GAME_MUSIC_2 = "eglise_orgue"
GAME_OVER_MUSIC = "cave_tuto"


def play_game_music():
    music.play(GAME_MUSIC_1)
    music.queue(GAME_MUSIC_2)


GAME_OVER_TEXT = "VOCE MORREU!"
PULSE_FRAMES = (0, 1, 2, 3, 2, 1)

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
floor_tiles = tuple(
    pygame.transform.scale(
        pygame.image.load(f"images/frames/floor_{number}.png").convert_alpha(),
        (ROOM_TILE_SIZE, ROOM_TILE_SIZE),
    )
    for number in range(1, 9)
)

floor_layout = [
    [
        0 if random.random() < 0.90 else random.randint(1, 7)
        for column in range(ROOM_COLUMNS)
    ]
    for row in range(ROOM_ROWS)
]
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
        (24, 42),
    )
    for frame in range(4)
)
wizzard_run_frames = tuple(
    pygame.transform.scale(
        pygame.image.load(
            str(Path("images/frames") / f"wizzard_f_run_anim_f{frame}.png")
        ).convert_alpha(),
        (24, 42),
    )
    for frame in range(4)
)
ogre_run_frames = tuple(
    pygame.image.load(
        str(Path("images/frames") / f"ogre_run_anim_f{frame}.png")
    ).convert_alpha()
    for frame in range(4)
)

masked_orc_run_frames = tuple(
    pygame.image.load(
        str(Path("images/frames") / f"masked_orc_run_anim_f{frame}.png")
    ).convert_alpha()
    for frame in range(4)
)

orc_warrior_run_frames = tuple(
    pygame.image.load(
        str(Path("images/frames") / f"orc_warrior_run_anim_f{frame}.png")
    ).convert_alpha()
    for frame in range(4)
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

OGRE_COLLISION_WIDTH = 12
OGRE_COLLISION_HEIGHT = 8
OGRE_COLLISION_BOTTOM = 28
OGRE_COLLISION_MASK = pygame.mask.Mask(
    (OGRE_COLLISION_WIDTH, OGRE_COLLISION_HEIGHT),
    fill=True,
)
ENEMY_TYPES = {
    "ogre": {
        "frames": ogre_run_frames,
        "speed": 40,
        "health": 2,
    },
    "masked_orc": {
        "frames": masked_orc_run_frames,
        "speed": 80,
        "health": 1,
    },
    "orc_warrior": {
        "frames": orc_warrior_run_frames,
        "speed": 100,
        "health": 1,
    },
}
ogres = []
particles = []
HORDE_START_SIZE = 6
HORDE_SIZE_INCREMENT = 2

HORDE_SPAWN_INTERVAL = 0.30
HORDE_BREAK = 1.5

horde_number = 1
horde_queue = []
horde_spawn_timer = 0
horde_break_timer = 0
horde_lane_index = 0
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
skull_image = pygame.image.load("images/frames/skull.png").convert_alpha()

skull_image = pygame.transform.scale(
    skull_image,
    (42, 42),
)
PROJECTILE_SPEED = 320
PROJECTILE_RADIUS = 5
PROJECTILE_INTERVAL = 0.25
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


def projectile_hits_ogre_swept(start_x, start_y, end_x, end_y, ogre):
    if not ogre["inside"]:
        return False

    ogre_rect = pygame.Rect(
        round(ogre["x"] - 14),
        round(ogre["y"] - 14),
        28,
        28,
    )

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


SPAWN_LANES = (
    ("top", 4),
    ("top", 12),
    ("bottom", 4),
    ("bottom", 12),
    ("left", 4),
    ("left", 12),
    ("right", 4),
    ("right", 12),
)


def create_horde():
    size = HORDE_START_SIZE + (horde_number - 1) * HORDE_SIZE_INCREMENT

    if horde_number == 1:
        enemy_queue = ["ogre"] * size

    else:
        masked_count = max(1, size // 3)
        warrior_count = max(1, size // 6)
        ogre_count = size - masked_count - warrior_count

        enemy_queue = (
            ["ogre"] * ogre_count
            + ["masked_orc"] * masked_count
            + ["orc_warrior"] * warrior_count
        )

    random.shuffle(enemy_queue)

    return enemy_queue


def start_horde():
    global horde_queue
    global horde_spawn_timer
    global horde_break_timer

    horde_queue = create_horde()
    horde_spawn_timer = HORDE_SPAWN_INTERVAL
    horde_break_timer = 0


def spawn_ogre(enemy_type="ogre", lane=None):
    if lane is None:
        lane = random.choice(SPAWN_LANES)

    side, opening = lane
    position = opening * ROOM_TILE_SIZE + ROOM_TILE_SIZE / 2

    if side == "top":
        x, y = (
            position,
            -16,
        )
        entry_target = (
            position,
            ROOM_TILE_SIZE * 1.5,
        )
        facing_left = False

    elif side == "bottom":
        x, y = (
            position,
            room_rect.height + 16,
        )
        entry_target = (
            position,
            room_rect.height - ROOM_TILE_SIZE * 1.5,
        )
        facing_left = False

    elif side == "left":
        x, y = (
            -16,
            position,
        )
        entry_target = (
            ROOM_TILE_SIZE * 1.5,
            position,
        )
        facing_left = False

    else:
        x, y = (
            room_rect.width + 16,
            position,
        )
        entry_target = (
            room_rect.width - ROOM_TILE_SIZE * 1.5,
            position,
        )
        facing_left = True

    stats = ENEMY_TYPES[enemy_type]

    ogres.append(
        {
            "type": enemy_type,
            "x": x,
            "y": y,
            "entry_target": entry_target,
            "inside": False,
            "frame": 0,
            "animation_time": random.random(),
            "facing_left": facing_left,
            "speed": stats["speed"],
            "health": stats["health"],
            "frames": stats["frames"],
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
    global horde_number, horde_queue, horde_spawn_timer
    global horde_break_timer, horde_lane_index
    global ogres_defeated, health, damage_cooldown, survival_time

    ogres.clear()
    projectiles.clear()
    particles.clear()

    wizzard_x = 6.5 * ROOM_TILE_SIZE
    wizzard_y = 6.5 * ROOM_TILE_SIZE
    wizzard_frame = 0
    wizzard_animation_time = 0
    wizzard_facing_left = False

    projectile_timer = 0
    ogres_defeated = 0
    health = 6
    damage_cooldown = 0
    survival_time = 0

    horde_number = 1
    horde_queue = []
    horde_spawn_timer = 0
    horde_break_timer = 0
    horde_lane_index = 0
    start_horde()
    game_state = "game"
    play_game_music()


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
        }
    )


def update_projectiles(dt):
    global ogres_defeated

    for projectile in projectiles[:]:
        # Guarda onde o projétil estava antes de se mover
        previous_position = projectile["position"].copy()

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
    global health, damage_cooldown, game_state
    global horde_spawn_timer, horde_break_timer, horde_number, horde_lane_index

    horde_spawn_timer += dt

    if horde_queue:
        while horde_queue and horde_spawn_timer >= HORDE_SPAWN_INTERVAL:
            horde_spawn_timer -= HORDE_SPAWN_INTERVAL

            enemy_type = horde_queue.pop(0)

            lane = SPAWN_LANES[horde_lane_index % len(SPAWN_LANES)]
            horde_lane_index += 1

            spawn_ogre(enemy_type, lane)

    else:
        horde_break_timer += dt

        if horde_break_timer >= HORDE_BREAK:

            horde_number += 1
            start_horde()

    damage_cooldown = max(0, damage_cooldown - dt)
    for ogre in ogres:
        if not ogre["inside"]:
            entry_direction = pygame.Vector2(
                ogre["entry_target"][0] - ogre["x"],
                ogre["entry_target"][1] - ogre["y"],
            )
            if entry_direction.length() <= ogre["speed"] * dt:
                ogre["x"], ogre["y"] = ogre["entry_target"]
                ogre["inside"] = True
            else:
                entry_direction.normalize_ip()
                ogre["x"] += entry_direction.x * ogre["speed"] * dt
                ogre["y"] += entry_direction.y * ogre["speed"] * dt
                ogre["facing_left"] = entry_direction.x < 0
            ogre["animation_time"] += dt
            ogre["frame"] = int(ogre["animation_time"] * 6) % len(ogre["frames"])
            continue

        direction = pygame.Vector2(wizzard_x - ogre["x"], wizzard_y - ogre["y"])
        if direction.length_squared() > 0:
            direction.normalize_ip()
            movement_x = direction.x * ogre["speed"] * dt
            movement_y = direction.y * ogre["speed"] * dt
            if not ogre_collides(ogre, ogre["x"] + movement_x, ogre["y"]):
                ogre["x"] += movement_x
            if not ogre_collides(ogre, ogre["x"], ogre["y"] + movement_y):
                ogre["y"] += movement_y
            ogre["facing_left"] = direction.x < 0
        ogre["animation_time"] += dt
        ogre["frame"] = int(ogre["animation_time"] * 6) % len(ogre["frames"])

        if damage_cooldown == 0 and ogre_hits_wizzard(ogre):
            health -= 1
            damage_cooldown = 0.8
            if health <= 0:
                game_state = "game_over"
                music.play(GAME_OVER_MUSIC)
                return


def update(dt):
    global hover_animation_time, game_state
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


def draw():
    pygame.draw.rect(
        screen.surface,
        BACKGROUND_COLOR,
        (0, 0, WIDTH, HEIGHT),
    )

    if game_state == "game_over":
        draw_game_over()
        return

    if game_state == "game" or game_state == "paused":
        pygame.draw.rect(
            screen.surface,
            GAME_BACKGROUND_COLOR,
            (0, 0, WIDTH, HEIGHT),
        )

        draw_game()

        if game_state == "paused":
            draw_pause()

            music_frame = 1 if music_muted else 0
            screen.surface.blit(
                music_button_frames[music_frame],
                music_button_rect.topleft,
            )

        return

    screen.surface.blit(menu_background, (0, 0))

    screen.draw.text(
        "Dungeon Survival",
        center=(WIDTH // 2, 150),
        fontname="monogram",
        fontsize=68,
        color=TEXT_COLOR,
        owidth=2,
        ocolor=OUTLINE_COLOR,
    )

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

    if game_state in ("menu", "paused"):
        music_frame = 1 if music_muted else 0
        screen.surface.blit(
            music_button_frames[music_frame],
            music_button_rect.topleft,
        )


def draw_game():
    room_surface = pygame.Surface(room_rect.size, pygame.SRCALPHA)

    for row in range(ROOM_ROWS):
        for column in range(ROOM_COLUMNS):
            tile_index = floor_layout[row][column]

            room_surface.blit(
                floor_tiles[tile_index],
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

        ogre_image = ogre["frames"][ogre["frame"]]

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

    screen.surface.blit(
        room_surface,
        room_rect.topleft,
    )

    draw_hud()


def draw_projectiles(surface):
    for projectile in projectiles:
        position = projectile["position"]

        x = round(position.x)
        y = round(position.y)

        # Sombra
        pygame.draw.circle(
            surface,
            (70, 35, 25),
            (x + 2, y + 3),
            PROJECTILE_RADIUS,
        )

        # Borda
        pygame.draw.circle(
            surface,
            (120, 35, 20),
            (x, y),
            PROJECTILE_RADIUS,
        )

        # Corpo
        pygame.draw.circle(
            surface,
            (255, 90, 25),
            (x, y),
            PROJECTILE_RADIUS - 2,
        )

        # Núcleo luminoso
        pygame.draw.circle(
            surface,
            (255, 170, 60),
            (x - 1, y - 1),
            2,
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
        screen.surface.blit(heart, (20 + heart_number * 30, 20))

    screen.blit(skull_image, (18, 49))

    screen.draw.text(
        str(ogres_defeated),
        midleft=(52, 74),
        fontname="monogram",
        fontsize=24,
        color=TEXT_COLOR,
        owidth=1,
        ocolor=OUTLINE_COLOR,
    )


def draw_game_over():
    center_x = WIDTH // 2

    screen.surface.blit(
        menu_background,
        (0, 0),
    )
    screen.blit(game_over_overlay, (0, 0))

    screen.draw.text(
        GAME_OVER_TEXT,
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
        f"INIMIGOS: {ogres_defeated}",
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
        screen.surface.blit(image, position)


def draw_pause():
    screen.surface.blit(
        panel,
        pause_panel_position,
    )

    center_x = pause_panel_inner_screen.centerx

    # Título
    screen.draw.text(
        "Pausado",
        center=(center_x, pause_panel_inner_screen.top + 65),
        fontname="monogram",
        fontsize=52,
        color=TEXT_COLOR,
        owidth=2,
        ocolor=OUTLINE_COLOR,
    )

    # Botão CONTINUAR
    screen.draw.text(
        "CONTINUAR",
        center=pause_button_positions["CONTINUAR"].center,
        fontname="monogram",
        fontsize=38,
        color=(HOVER_COLOR if hovered_button == "CONTINUAR" else TEXT_COLOR),
        owidth=1,
        ocolor=OUTLINE_COLOR,
    )

    if hovered_button == "CONTINUAR":
        draw_hover_arrows(pause_button_positions["CONTINUAR"])

    # Botão SAIR
    screen.draw.text(
        "SAIR",
        center=pause_button_positions["SAIR"].center,
        fontname="monogram",
        fontsize=38,
        color=(HOVER_COLOR if hovered_button == "SAIR" else TEXT_COLOR),
        owidth=1,
        ocolor=OUTLINE_COLOR,
    )

    if hovered_button == "SAIR":
        draw_hover_arrows(pause_button_positions["SAIR"])


def format_survival_time():
    minutes = int(survival_time) // 60
    seconds = int(survival_time) % 60
    return f"{minutes:02d}:{seconds:02d}"


def draw_hover_arrows(button):
    frame = PULSE_FRAMES[int(hover_animation_time * 4) % len(PULSE_FRAMES)]
    positions = (
        ((button.left, button.top), arrow_frames[frame][0]),
        ((button.right - 24, button.top), arrow_frames[frame][1]),
        ((button.left, button.bottom - 24), arrow_frames[frame][2]),
        ((button.right - 24, button.bottom - 24), arrow_frames[frame][3]),
    )

    for position, image in positions:
        screen.surface.blit(image, position)


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
    global game_state, music_muted

    if game_state == "game":
        return

    if game_state == "game_over":
        if game_over_button_positions["JOGAR NOVAMENTE"].collidepoint(pos):
            click_sound.play()
            reset_game()

        elif game_over_button_positions["MENU"].collidepoint(pos):
            click_sound.play()
            game_state = "menu"
            music.play(MENU_MUSIC)

        return

    if game_state == "paused":
        if music_button_rect.collidepoint(pos):
            click_sound.play()
            music_muted = not music_muted
            music.set_volume(0 if music_muted else 1)

        elif pause_button_positions["CONTINUAR"].collidepoint(pos):
            click_sound.play()
            game_state = "game"
            hovered_button = None

        elif pause_button_positions["SAIR"].collidepoint(pos):
            click_sound.play()
            game_state = "menu"
            music.play(MENU_MUSIC)
            hovered_button = None

        return

    if game_state != "menu":
        return

    if music_button_rect.collidepoint(pos):
        click_sound.play()
        music_muted = not music_muted
        music.set_volume(0 if music_muted else 1)
        return

    if button_positions["JOGAR"].collidepoint(pos):
        click_sound.play()
        reset_game()
        hovered_button = None

    elif button_positions["SAIR"].collidepoint(pos):
        click_sound.play()
        quit()


def on_key_down(key):
    global game_state, hovered_button
    if key == keys.ESCAPE:
        if game_state == "game":
            game_state = "paused"
            hovered_button = None
        elif game_state == "paused":
            game_state = "game"


music.play(MENU_MUSIC)

import pgzrun

pgzrun.go()
