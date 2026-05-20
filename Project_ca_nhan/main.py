import pygame
import sys
import time
import random

import pygame.mouse
import pygame.draw
import pygame.display
import pygame.event

from algorithms import ALG_MAP

pygame.init()

HAS_FONT = True
try:
    import pygame.font
    pygame.font.init()
    FONT_SM = pygame.font.SysFont("Segoe UI", 16)
    FONT_MD = pygame.font.SysFont("Segoe UI", 20)
    FONT_LG = pygame.font.SysFont("Segoe UI", 24, bold=True)
except (NotImplementedError, ModuleNotFoundError, AttributeError):
    HAS_FONT = False
    print("[Hệ thống] Phát hiện lỗi SDL_ttf trên Mac. Kích hoạt bộ hiển thị văn bản giả lập...")

class FallbackFont:
    def __init__(self, size):
        self.size = size
    def render(self, text, antialias, color):
        width = len(text) * (self.size // 2)
        height = self.size
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (color[0], color[1], color[2], 40), (0, 0, width, height), border_radius=3)
        pygame.draw.line(surf, color, (5, height//2), (width - 5, height//2), 2)
        return surf

if not HAS_FONT:
    FONT_SM = FallbackFont(16)
    FONT_MD = FallbackFont(20)
    FONT_LG = FallbackFont(24)

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vacuum Cleaner Pathfinding Visualizer (With Obstacles)")

COLOR_BG, COLOR_GRID_BG = (30, 30, 40), (40, 40, 50)
COLOR_WALL, COLOR_DIRT = (70, 70, 80), (200, 150, 80)
COLOR_ROBOT, COLOR_CLEANED = (50, 150, 250), (50, 200, 120)
COLOR_TEXT, COLOR_PANEL = (240, 240, 240), (45, 45, 55)
COLOR_BTN, COLOR_BTN_ACTIVE = (60, 60, 80), (100, 100, 150)
COLOR_LOG_BG = (20, 20, 25)
COLOR_OBSTACLE = (100, 100, 110)

class Visualizer:
    def __init__(self):
        self.grid_m = 4             
        self.grid_n = 6             
        self.active_input = None    
        self.input_text = ""        
        
        self.grid_data = [[0 for _ in range(6)] for _ in range(4)]
        
        self.algorithms = list(ALG_MAP.keys())
        self.current_algo = self.algorithms[0]
        self.dropdown_open = False
        self.dropdown_rect = pygame.Rect(30, 60, 220, 40)
        
        self.box_m_rect = pygame.Rect(420, 60, 45, 40)
        self.box_n_rect = pygame.Rect(500, 60, 45, 40)
        
        self.grid_origin_x = 50
        self.grid_origin_y = 150
        self.grid_max_display_size = 300 

        self.logs = []
        self.final_result = None
        self.running_simulation = False
        self.sim_index = 0
        self.current_sim_state = None
        self.randomize_dirt()
        self.reset_env()

    def reset_env(self):
        self.logs = ["Click ô lưới để vẽ VẬT CẢN"]
        self.final_result = None
        self.running_simulation = False
        self.sim_index = 0
        tuple_grid = tuple(tuple(row) for row in self.grid_data)
        self.current_sim_state = (0, 0, tuple_grid)

    def apply_new_dimensions(self, new_m, new_n):
        self.grid_m = max(2, min(8, new_m))
        self.grid_n = max(2, min(8, new_n))
        self.grid_data = [[0 for _ in range(self.grid_n)] for _ in range(self.grid_m)]
        self.randomize_dirt()
        self.reset_env()

    def randomize_dirt(self):
        for r in range(self.grid_m):
            for c in range(self.grid_n):
                if r == 0 and c == 0:
                    self.grid_data[r][c] = 0
                elif self.grid_data[r][c] != 2: 
                    self.grid_data[r][c] = 1 if random.random() < 0.4 else 0
        self.reset_env()

    def run_algorithm(self):
        self.running_simulation = False
        self.sim_index = 0
        
        tuple_grid = tuple(tuple(row) for row in self.grid_data)
        start_state = (0, 0, tuple_grid)
        self.current_sim_state = start_state
        
        algo_instance = ALG_MAP[self.current_algo]
        path, algo_logs = algo_instance.solve(start_state)
        
        self.final_result = path if path is not None else "Khong tim thay duong di"
        self.logs = algo_logs[-12:] 
        
        if path and isinstance(path, list):
            self.running_simulation = True

    def update_simulation(self):
        if self.running_simulation and isinstance(self.final_result, list):
            if self.sim_index < len(self.final_result):
                action = self.final_result[self.sim_index]
                
                rx, ry, current_dirt = self.current_sim_state
                dirt_list = [list(row) for row in current_dirt]
                
                if action == "UP": rx -= 1
                elif action == "DOWN": rx += 1
                elif action == "LEFT": ry -= 1
                elif action == "RIGHT": ry += 1
                elif action == "CLEAN":
                    if 0 <= rx < self.grid_m and 0 <= ry < self.grid_n:
                        dirt_list[rx][ry] = 0
                
                tuple_grid = tuple(tuple(row) for row in dirt_list)
                self.current_sim_state = (rx, ry, tuple_grid)
                self.sim_index += 1
                time.sleep(0.4)
            else:
                self.running_simulation = False

    def handle_click(self, mx, my):
        if self.dropdown_rect.collidepoint(mx, my):
            self.dropdown_open = not self.dropdown_open
            self.active_input = None
            return

        if self.dropdown_open:
            for i in range(len(self.algorithms)):
                item_rect = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + (i + 1) * 40, self.dropdown_rect.width, 40)
                if item_rect.collidepoint(mx, my):
                    self.current_algo = self.algorithms[i]
                    self.dropdown_open = False
                    self.reset_env()
                    return
            self.dropdown_open = False

        if not self.running_simulation:
            if self.box_m_rect.collidepoint(mx, my):
                self.active_input = 'M'
                self.input_text = ""
                return
            elif self.box_n_rect.collidepoint(mx, my):
                self.active_input = 'N'
                self.input_text = ""
                return
            else:
                if not pygame.Rect(420, 60, 130, 40).collidepoint(mx, my):
                    self.active_input = None
        
        btn_rand = pygame.Rect(575, 60, 125, 40)
        if btn_rand.collidepoint(mx, my) and not self.running_simulation:
            self.randomize_dirt()
            return

        btn_run = pygame.Rect(715, 60, 155, 40)
        if btn_run.collidepoint(mx, my):
            self.active_input = None
            self.run_algorithm()
            return

        if not self.running_simulation:
            cell_size = self.grid_max_display_size // max(self.grid_m, self.grid_n)
            gx = mx - self.grid_origin_x
            gy = my - self.grid_origin_y
            if 0 <= gx < (self.grid_n * cell_size) and 0 <= gy < (self.grid_m * cell_size):
                col = gx // cell_size
                row = gy // cell_size
                if 0 <= row < self.grid_m and 0 <= col < self.grid_n:
                    if not (row == 0 and col == 0):
                        self.grid_data[row][col] = 2 if self.grid_data[row][col] != 2 else 0
                        self.reset_env()

    def handle_keydown(self, event):
        if not self.active_input:
            return
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            if self.input_text.isdigit():
                val = int(self.input_text)
                if self.active_input == 'M': self.apply_new_dimensions(val, self.grid_n)
                elif self.active_input == 'N': self.apply_new_dimensions(self.grid_m, val)
            self.active_input = None
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        else:
            if event.unicode.isdigit() and event.unicode in "2345678":
                self.input_text = event.unicode

    def draw(self, surface):
        surface.fill(COLOR_BG)
        
        lbl_size = FONT_LG.render("KICH THUOC M x N:", True, COLOR_TEXT)
        surface.blit(lbl_size, (420, 20))
        
        color_m = COLOR_BTN_ACTIVE if self.active_input == 'M' else COLOR_PANEL
        border_m = COLOR_CLEANED if self.active_input == 'M' else COLOR_WALL
        pygame.draw.rect(surface, color_m, self.box_m_rect, border_radius=5)
        pygame.draw.rect(surface, border_m, self.box_m_rect, width=1, border_radius=5)
        str_m = (self.input_text + "_") if self.active_input == 'M' else str(self.grid_m)
        txt_m = FONT_MD.render(str_m, True, COLOR_CLEANED)
        surface.blit(txt_m, (self.box_m_rect.x + (self.box_m_rect.width - txt_m.get_width())//2, self.box_m_rect.y + 7))
        
        txt_x = FONT_MD.render("X", True, COLOR_TEXT)
        surface.blit(txt_x, (473, 68))
        
        color_n = COLOR_BTN_ACTIVE if self.active_input == 'N' else COLOR_PANEL
        border_n = COLOR_CLEANED if self.active_input == 'N' else COLOR_WALL
        pygame.draw.rect(surface, color_n, self.box_n_rect, border_radius=5)
        pygame.draw.rect(surface, border_n, self.box_n_rect, width=1, border_radius=5)
        str_n = (self.input_text + "_") if self.active_input == 'N' else str(self.grid_n)
        txt_n = FONT_MD.render(str_n, True, COLOR_CLEANED)
        surface.blit(txt_n, (self.box_n_rect.x + (self.box_n_rect.width - txt_n.get_width())//2, self.box_n_rect.y + 7))

        btn_rand = pygame.Rect(575, 60, 125, 40)
        pygame.draw.rect(surface, (160, 110, 50), btn_rand, border_radius=5)
        pygame.draw.rect(surface, COLOR_TEXT, btn_rand, width=1, border_radius=5)
        txt_rand = FONT_MD.render("RANDOM BUI", True, COLOR_TEXT)
        surface.blit(txt_rand, (575 + (125 - txt_rand.get_width())//2, 60 + (40 - txt_rand.get_height())//2))

        btn_run = pygame.Rect(715, 60, 155, 40)
        pygame.draw.rect(surface, (50, 180, 100), btn_run, border_radius=5)
        txt_run = FONT_MD.render("RUN", True, COLOR_TEXT)
        surface.blit(txt_run, (715 + (155 - txt_run.get_width())//2, 60 + (40 - txt_run.get_height())//2))

        cell_size = self.grid_max_display_size // max(self.grid_m, self.grid_n)
        actual_width = self.grid_n * cell_size
        actual_height = self.grid_m * cell_size
        pygame.draw.rect(surface, COLOR_GRID_BG, (self.grid_origin_x, self.grid_origin_y, actual_width, actual_height))
        
        rx, ry, current_dirt = self.current_sim_state
        
        for r in range(self.grid_m):
            for c in range(self.grid_n):
                cx = self.grid_origin_x + c * cell_size
                cy = self.grid_origin_y + r * cell_size
                
                if current_dirt[r][c] == 2:
                    pygame.draw.rect(surface, COLOR_OBSTACLE, (cx, cy, cell_size, cell_size))
                
                pygame.draw.rect(surface, COLOR_WALL, (cx, cy, cell_size, cell_size), width=1)
                
                if current_dirt[r][c] == 1:
                    rad = cell_size // 4
                    pygame.draw.circle(surface, COLOR_DIRT, (cx + cell_size//2, cy + cell_size//2), rad)
                
                if r == rx and c == ry:
                    pygame.draw.rect(surface, COLOR_ROBOT, (cx + 5, cy + 5, cell_size - 10, cell_size - 10), border_radius=5)

        lbl_log = FONT_LG.render("LOG HOAT DONG:", True, COLOR_TEXT)
        surface.blit(lbl_log, (400, 120))
        log_panel = pygame.Rect(400, 150, 460, 300)
        pygame.draw.rect(surface, COLOR_LOG_BG, log_panel, border_radius=5)
        pygame.draw.rect(surface, COLOR_WALL, log_panel, width=1, border_radius=5)
        
        for idx, log in enumerate(self.logs):
            if HAS_FONT:
                txt_log = FONT_SM.render(log, True, (200, 200, 200))
                surface.blit(txt_log, (415, 160 + idx * 22))
            else:
                pygame.draw.rect(surface, (100, 120, 100), (415, 165 + idx * 22, 300, 4))

        pygame.draw.rect(surface, COLOR_WALL, (30, 480, 840, 2))
        lbl_final = FONT_LG.render("DUONG DI:", True, COLOR_TEXT)
        surface.blit(lbl_final, (30, 500))
        
        res_box = pygame.Rect(30, 535, 840, 90)
        pygame.draw.rect(surface, COLOR_PANEL, res_box, border_radius=5)
        pygame.draw.rect(surface, COLOR_WALL, res_box, width=1, border_radius=5)
        
        if self.final_result is not None:
            if HAS_FONT:
                if isinstance(self.final_result, list):
                    full_string = "Ket qua: [ " + " -> ".join(self.final_result) + " ]"
                else:
                    full_string = str(self.final_result)

                words = full_string.split(' ')
                lines = []
                current_line = ""
                max_w = 810
                for word in words:
                    test_line = current_line + word + " "
                    if FONT_MD.size(test_line)[0] < max_w:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word + " "
                lines.append(current_line)
                
                for line_idx, line_text in enumerate(lines):
                    if line_idx < 3:
                        txt_line = FONT_MD.render(line_text, True, COLOR_CLEANED)
                        surface.blit(txt_line, (45, 545 + line_idx * 24))
        else:
            txt_res = FONT_MD.render("Chua thuc hien...", True, (120, 120, 130))
            surface.blit(txt_res, (45, 565))

        lbl_algo = FONT_LG.render("LIST CHON PHUONG PHAP:", True, COLOR_TEXT)
        surface.blit(lbl_algo, (30, 20))
        
        pygame.draw.rect(surface, COLOR_BTN_ACTIVE if self.dropdown_open else COLOR_BTN, self.dropdown_rect, border_radius=5)
        pygame.draw.rect(surface, COLOR_TEXT, self.dropdown_rect, width=1, border_radius=5)
        
        if HAS_FONT:
            txt_curr = FONT_MD.render(self.current_algo, True, COLOR_TEXT)
            surface.blit(txt_curr, (self.dropdown_rect.x + 10, self.dropdown_rect.y + 7))
            txt_arrow = FONT_SM.render("V", True, COLOR_TEXT)
            surface.blit(txt_arrow, (self.dropdown_rect.right - 20, self.dropdown_rect.y + 10))
        else:
            pygame.draw.circle(surface, COLOR_CLEANED, (self.dropdown_rect.x + 20, self.dropdown_rect.y + 20), 6)

        if self.dropdown_open:
            for i, algo in enumerate(self.algorithms):
                item_rect = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + (i + 1) * 40, self.dropdown_rect.width, 40)
                pygame.draw.rect(surface, (55, 55, 65), item_rect)
                pygame.draw.rect(surface, COLOR_WALL, item_rect, width=1)
                if HAS_FONT:
                    txt_item = FONT_MD.render(algo, True, COLOR_TEXT)
                    surface.blit(txt_item, (item_rect.x + 10, item_rect.y + 7))

def main():
    clock = pygame.time.Clock()
    visualizer = Visualizer()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                visualizer.handle_click(mx, my)
            elif event.type == pygame.KEYDOWN:
                visualizer.handle_keydown(event)
                    
        visualizer.update_simulation()
        visualizer.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()