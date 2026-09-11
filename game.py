import re
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
	pygame.transform.scale(ui_atlas.subsurface((240, 80 + frame * 16, 16, 16)), (40, 40))
	for frame in range(2)
)
paper_source = books_atlas.subsurface((608, 16, 48, 64))
paper_panel = pygame.transform.scale(paper_source, (720, 520))
fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
arrow_frames = tuple(
	tuple(
		pygame.transform.scale(
			ui_atlas.subsurface(
				(144 + (frame % 2) * 32 + column * 16,
				 64 + (frame // 2) * 32 + row * 16,
				 16,
				 16)
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
button_left = panel_inner_screen.left + (
	panel_inner_screen.width - button_width
) // 2
button_gap = 16
button_group_height = button_height * 3 + button_gap * 2
button_top = panel_inner_screen.top + (
	panel_inner_screen.height - button_group_height
) // 2
button_positions = {
	"JOGAR": pygame.Rect((button_left, button_top), (button_width, button_height)),
	"COMO JOGAR": pygame.Rect((button_left, button_top + button_height + button_gap), (button_width, button_height)),
	"SAIR": pygame.Rect((button_left, button_top + (button_height + button_gap) * 2), (button_width, button_height)),
}

hovered_button = None
hover_animation_time = 0
game_state = "menu"
controls_fade = 1.0
x_button_pressed = 0
music_muted = False
PULSE_FRAMES = (0, 1, 2, 3, 2, 1)

controls_lines = (
	"USE W A S D PARA MOVER O PERSONAGEM",
	"USE O CURSOR DO MOUSE PARA MIRAR",
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
	add_wall_collision_mask(wall_horizontal, position, 0)
	add_wall_collision_mask(
		wall_horizontal,
		position,
		room_rect.height - ROOM_TILE_SIZE,
	)
for position in range(ROOM_TILE_SIZE, room_rect.height - ROOM_TILE_SIZE, ROOM_TILE_SIZE):
	add_wall_collision_mask(wall_vertical, 0, position)
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


def wizzard_collides(x, y):
	wizzard_left = round(x - WIZZARD_COLLISION_WIDTH / 2)
	wizzard_top = round(
		y + WIZZARD_COLLISION_BOTTOM - WIZZARD_COLLISION_HEIGHT
	)
	for wall_mask, (wall_x, wall_y) in wall_collision_masks:
		if wall_mask.overlap(
			WIZZARD_COLLISION_MASK,
			(wizzard_left - wall_x, wizzard_top - wall_y),
		):
			return True
	return False


def update(dt):
	global hover_animation_time, controls_fade, x_button_pressed, game_state
	global wizzard_frame, wizzard_animation_time, wizzard_x, wizzard_y
	global wizzard_facing_left

	hover_animation_time += dt
	wizzard_animation_time += dt
	if game_state == "game":
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
		wizzard_x = max(WIZZARD_COLLISION_WIDTH / 2, wizzard_x)
		wizzard_x = min(room_rect.width - WIZZARD_COLLISION_WIDTH / 2, wizzard_x)
		wizzard_y = max(
			ROOM_TILE_SIZE - WIZZARD_COLLISION_BOTTOM + WIZZARD_COLLISION_HEIGHT,
			wizzard_y,
		)
		wizzard_y = min(
			room_rect.height - ROOM_TILE_SIZE - WIZZARD_COLLISION_BOTTOM,
			wizzard_y,
		)
	if game_state == "controls":
		controls_fade = max(0.0, controls_fade - dt / 0.18)
		if x_button_pressed:
			x_button_pressed = max(0.0, x_button_pressed - dt)
			if x_button_pressed == 0:
				game_state = "menu"


def draw():
	screen.fill(BACKGROUND_COLOR)
	if game_state == "controls":
		draw_controls()
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

	room_surface.blit(wall_top_left, (0, 0))
	room_surface.blit(wall_top_right, (room_rect.width - ROOM_TILE_SIZE, 0))
	room_surface.blit(
		wall_bottom_left,
		(0, room_rect.height - ROOM_TILE_SIZE),
	)
	room_surface.blit(
		wall_bottom_right,
		(room_rect.width - ROOM_TILE_SIZE, room_rect.height - ROOM_TILE_SIZE),
	)
	draw_repeated_wall(room_surface, wall_horizontal, ROOM_TILE_SIZE, 0)
	draw_repeated_wall(
		room_surface,
		wall_horizontal,
		ROOM_TILE_SIZE,
		room_rect.height - ROOM_TILE_SIZE,
	)
	draw_repeated_wall(room_surface, wall_vertical, 0, ROOM_TILE_SIZE, vertical=True)
	draw_repeated_wall(
		room_surface,
		wall_vertical,
		room_rect.width - ROOM_TILE_SIZE,
		ROOM_TILE_SIZE,
		vertical=True,
	)

	is_moving = keyboard.w or keyboard.s or keyboard.a or keyboard.d
	animation_frames = wizzard_run_frames if is_moving else wizzard_idle_frames
	wizzard_image = animation_frames[wizzard_frame]
	if wizzard_facing_left:
		wizzard_image = pygame.transform.flip(wizzard_image, True, False)
	wizzard_position = (
		wizzard_x - wizzard_image.get_width() // 2,
		wizzard_y - wizzard_image.get_height() // 2,
	)
	room_surface.blit(wizzard_image, wizzard_position)
	screen.blit(room_surface, room_rect.topleft)


def draw_repeated_wall(surface, image, x, y, vertical=False):
	if image.get_width() > surface.get_width() - x:
		return
	if image.get_height() > surface.get_height() - y:
		return
	if vertical:
		for position_y in range(y, surface.get_height() - ROOM_TILE_SIZE, image.get_height()):
			surface.blit(image, (x, position_y))
	else:
		for position_x in range(x, surface.get_width() - ROOM_TILE_SIZE, image.get_width()):
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
			segments.append((text[last_token_end:token_match.start()], OUTLINE_COLOR))
		segments.append((token_match.group(), controls_key_color))
		last_token_end = token_match.end()
	if last_token_end < len(text):
		segments.append((text[last_token_end:], OUTLINE_COLOR))

	total_width = sum(
		controls_text_font.size(segment)[0]
		for segment, _ in segments
	)
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
	if game_state != "menu":
		hovered_button = None
		return

	hovered_button = None
	for label, button in button_positions.items():
		if button.collidepoint(pos):
			hovered_button = label
			break


def on_mouse_down(pos):
	global game_state, controls_fade, x_button_pressed, music_muted

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
		game_state = "controls"
		controls_fade = 1.0
		hovered_button = None
	elif button_positions["JOGAR"].collidepoint(pos):
		game_state = "game"
		hovered_button = None
	elif button_positions["SAIR"].collidepoint(pos):
		quit()



music.play("jardins")