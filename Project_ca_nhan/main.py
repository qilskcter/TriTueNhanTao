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
COLOR_WALL = (70, 70, 80)
COLOR_TEXT, COLOR_PANEL = (240, 240, 240), (45, 45, 55)
COLOR_BTN, COLOR_BTN_ACTIVE = (60, 60, 80), (100, 100, 150)
COLOR_LOG_BG = (20, 20, 25)
COLOR_CLEANED = (50, 200, 120)

HAS_IMAGES = True
try:
    IMG_ROBOT = pygame.image.load("Assets/robot.png")
    IMG_DIRT = pygame.image.load("Assets/dirt.png")
    IMG_OBSTACLE = pygame.image.load("Assets/obstacle.png")
except pygame.error as e:
    HAS_IMAGES = False
    print(f"[Cảnh báo] Không tìm thấy file ảnh: {e}. Hệ thống sẽ dùng hình vẽ thay thế.")

class Visualizer:
    def __init__(self):
        self.grid_m = 3             
        self.grid_n = 3             
        self.active_input = None    
        self.input_text = ""        
        
        self.grid_data = [[0 for _ in range(self.grid_n)] for _ in range(self.grid_m)]
        
        self.algorithms = list(ALG_MAP.keys())
        self.current_algo = self.algorithms[0]
        self.dropdown_open = False
        self.dropdown_rect = pygame.Rect(30, 60, 220, 40)
        
        self.dropdown_scroll_index = 0
        self.dropdown_max_visible = 4  
        self.dropdown_item_h = 40
        self.dropdown_panel_rect = pygame.Rect(30, 100, 220, self.dropdown_max_visible * self.dropdown_item_h)
        
        self.box_m_rect = pygame.Rect(420, 60, 45, 40)
        self.box_n_rect = pygame.Rect(500, 60, 45, 40)
        
        self.grid_origin_x = 50
        self.grid_origin_y = 150
        self.grid_max_display_size = 300 

        self.logs = []
        self.log_scroll_index = 0
        self.log_panel_rect = pygame.Rect(400, 150, 460, 300)
        
        self.final_result = None
        self.running_simulation = False
        self.sim_index = 0
        self.current_sim_state = None
        
        self.path_scroll_index = 0
        self.path_panel_rect = pygame.Rect(30, 535, 840, 90)
        
        self.randomize_dirt()
        self.reset_env()

    def reset_env(self):
        self.logs = ["Click ô lưới để vẽ VẬT CẢN"]
        self.log_scroll_index = 0
        self.path_scroll_index = 0
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
        self.path_scroll_index = 0
        
        tuple_grid = tuple(tuple(row) for row in self.grid_data)
        start_state = (0, 0, tuple_grid)
        self.current_sim_state = start_state
        
        algo_instance = ALG_MAP[self.current_algo]
        path, algo_logs = algo_instance.solve(start_state)
        
        self.final_result = path if path is not None else "Khong tim thay duong di"
        self.logs = algo_logs 
        self.log_scroll_index = 999999
        
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
            visible_count = min(self.dropdown_max_visible, len(self.algorithms))
            for i in range(visible_count):
                algo_idx = self.dropdown_scroll_index + i
                item_rect = pygame.Rect(
                    self.dropdown_rect.x, 
                    self.dropdown_rect.y + (i + 1) * self.dropdown_item_h, 
                    self.dropdown_rect.width, 
                    self.dropdown_item_h
                )
                if item_rect.collidepoint(mx, my):
                    self.current_algo = self.algorithms[algo_idx]
                    self.dropdown_open = False
                    self.reset_env()
                    return
            
            if not self.dropdown_panel_rect.collidepoint(mx, my):
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

    def handle_scroll(self, button, mx, my):
        if self.log_panel_rect.collidepoint(mx, my):
            if button == 4:    
                self.log_scroll_index = max(0, self.log_scroll_index - 1)
            elif button == 5:  
                self.log_scroll_index += 1
                
        elif self.path_panel_rect.collidepoint(mx, my):
            if button == 4:
                self.path_scroll_index = max(0, self.path_scroll_index - 1)
            elif button == 5:
                self.path_scroll_index += 1

        elif self.dropdown_open and (self.dropdown_rect.collidepoint(mx, my) or self.dropdown_panel_rect.collidepoint(mx, my)):
            max_scroll = max(0, len(self.algorithms) - self.dropdown_max_visible)
            if button == 4:
                self.dropdown_scroll_index = max(0, self.dropdown_scroll_index - 1)
            elif button == 5:
                self.dropdown_scroll_index = min(max_scroll, self.dropdown_scroll_index + 1)

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
        
        lbl_size = FONT_LG.render("KICH THUOC", True, COLOR_TEXT)
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
        
        if HAS_IMAGES:
            scaled_robot = pygame.transform.scale(IMG_ROBOT, (cell_size - 10, cell_size - 10))
            scaled_dirt = pygame.transform.scale(IMG_DIRT, (cell_size // 2, cell_size // 2))
            scaled_obstacle = pygame.transform.scale(IMG_OBSTACLE, (cell_size, cell_size))

        for r in range(self.grid_m):
            for c in range(self.grid_n):
                cx = self.grid_origin_x + c * cell_size
                cy = self.grid_origin_y + r * cell_size
                
                if current_dirt[r][c] == 2:
                    if HAS_IMAGES:
                        surface.blit(scaled_obstacle, (cx, cy))
                    else:
                        pygame.draw.rect(surface, (100, 100, 110), (cx, cy, cell_size, cell_size))
                
                pygame.draw.rect(surface, COLOR_WALL, (cx, cy, cell_size, cell_size), width=1)
                
                if current_dirt[r][c] == 1:
                    if HAS_IMAGES:
                        dirt_x = cx + (cell_size - scaled_dirt.get_width()) // 2
                        dirt_y = cy + (cell_size - scaled_dirt.get_height()) // 2
                        surface.blit(scaled_dirt, (dirt_x, dirt_y))
                    else:
                        rad = cell_size // 4
                        pygame.draw.circle(surface, (200, 150, 80), (cx + cell_size//2, cy + cell_size//2), rad)
                
                if r == rx and c == ry:
                    if HAS_IMAGES:
                        robot_x = cx + 5
                        robot_y = cy + 5
                        surface.blit(scaled_robot, (robot_x, robot_y))
                    else:
                        pygame.draw.rect(surface, (50, 150, 250), (cx + 5, cy + 5, cell_size - 10, cell_size - 10), border_radius=5)

        lbl_log = FONT_LG.render("LOG:", True, COLOR_TEXT)
        surface.blit(lbl_log, (400, 120))
        pygame.draw.rect(surface, COLOR_LOG_BG, self.log_panel_rect, border_radius=5)
        pygame.draw.rect(surface, COLOR_WALL, self.log_panel_rect, width=1, border_radius=5)
        
        max_log_width = self.log_panel_rect.width - 30  
        log_lines_pool = []                   

        for log in self.logs:
            if HAS_FONT:
                words = log.split(' ')
                current_line = ""
                for word in words:
                    test_line = current_line + word + " "
                    if FONT_SM.size(test_line)[0] < max_log_width:
                        current_line = test_line
                    else:
                        log_lines_pool.append(current_line)
                        current_line = word + " "
                if current_line:
                    log_lines_pool.append(current_line)
            else:
                log_lines_pool.append(log)

        max_visible_lines = 12
        total_lines = len(log_lines_pool)
        
        if total_lines <= max_visible_lines:
            self.log_scroll_index = 0
        else:
            max_scroll = total_lines - max_visible_lines
            self.log_scroll_index = min(self.log_scroll_index, max_scroll)

        start_idx = self.log_scroll_index
        end_idx = start_idx + max_visible_lines
        display_lines = log_lines_pool[start_idx:end_idx]
        
        for idx, line_text in enumerate(display_lines):
            if HAS_FONT:
                txt_log = FONT_SM.render(line_text, True, (200, 200, 200))
                surface.blit(txt_log, (self.log_panel_rect.x + 15, self.log_panel_rect.y + 12 + idx * 23))
            else:
                pygame.draw.rect(surface, (100, 120, 100), (self.log_panel_rect.x + 15, self.log_panel_rect.y + 15 + idx * 23, 300, 4))
                
        if total_lines > max_visible_lines:
            scrollbar_h = max(20, int(self.log_panel_rect.height * (max_visible_lines / total_lines)))
            scrollbar_y = self.log_panel_rect.y + 5 + int((self.log_panel_rect.height - scrollbar_h - 10) * (self.log_scroll_index / (total_lines - max_visible_lines)))
            pygame.draw.rect(surface, (80, 80, 90), (self.log_panel_rect.right - 8, scrollbar_y, 4, scrollbar_h), border_radius=2)

        pygame.draw.rect(surface, COLOR_WALL, (30, 480, 840, 2))
        lbl_final = FONT_LG.render("DUONG DI:", True, COLOR_TEXT)
        surface.blit(lbl_final, (30, 500))
        
        pygame.draw.rect(surface, COLOR_PANEL, self.path_panel_rect, border_radius=5)
        pygame.draw.rect(surface, COLOR_WALL, self.path_panel_rect, width=1, border_radius=5)
        
        if self.final_result is not None:
            if HAS_FONT:
                if isinstance(self.final_result, list):
                    full_string = "Ket qua: [ " + " -> ".join(self.final_result) + " ]"
                else:
                    full_string = str(self.final_result)

                words = full_string.split(' ')
                path_lines_pool = []
                current_line = ""
                max_w = self.path_panel_rect.width - 30
                for word in words:
                    test_line = current_line + word + " "
                    if FONT_MD.size(test_line)[0] < max_w:
                        current_line = test_line
                    else:
                        path_lines_pool.append(current_line)
                        current_line = word + " "
                path_lines_pool.append(current_line)
                
                max_visible_path_lines = 3
                total_path_lines = len(path_lines_pool)
                
                if total_path_lines <= max_visible_path_lines:
                    self.path_scroll_index = 0
                else:
                    max_path_scroll = total_path_lines - max_visible_path_lines
                    self.path_scroll_index = min(self.path_scroll_index, max_path_scroll)

                start_p_idx = self.path_scroll_index
                end_p_idx = start_p_idx + max_visible_path_lines
                display_path_lines = path_lines_pool[start_p_idx:end_p_idx]

                for line_idx, line_text in enumerate(display_path_lines):
                    txt_line = FONT_MD.render(line_text, True, COLOR_CLEANED)
                    surface.blit(txt_line, (self.path_panel_rect.x + 15, self.path_panel_rect.y + 10 + line_idx * 24))

                if total_path_lines > max_visible_path_lines:
                    p_scrollbar_h = max(15, int(self.path_panel_rect.height * (max_visible_path_lines / total_path_lines)))
                    p_scrollbar_y = self.path_panel_rect.y + 5 + int((self.path_panel_rect.height - p_scrollbar_h - 10) * (self.path_scroll_index / (total_path_lines - max_visible_path_lines)))
                    pygame.draw.rect(surface, (80, 80, 90), (self.path_panel_rect.right - 8, p_scrollbar_y, 4, p_scrollbar_h), border_radius=2)
        else:
            txt_res = FONT_MD.render("Chua thuc hien...", True, (120, 120, 130))
            surface.blit(txt_res, (self.path_panel_rect.x + 15, self.path_panel_rect.y + 30))

        lbl_algo = FONT_LG.render("PHUONG PHAP", True, COLOR_TEXT)
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
            total_algos = len(self.algorithms)
            visible_count = min(self.dropdown_max_visible, total_algos)
            
            start_idx = self.dropdown_scroll_index
            end_idx = start_idx + visible_count
            display_algos = self.algorithms[start_idx:end_idx]

            pygame.draw.rect(surface, (40, 40, 50), self.dropdown_panel_rect, border_radius=5)
            pygame.draw.rect(surface, COLOR_WALL, self.dropdown_panel_rect, width=1, border_radius=5)

            for i, algo in enumerate(display_algos):
                item_rect = pygame.Rect(
                    self.dropdown_rect.x, 
                    self.dropdown_rect.y + (i + 1) * self.dropdown_item_h, 
                    self.dropdown_rect.width, 
                    self.dropdown_item_h
                )
                
                mx, my = pygame.mouse.get_pos()
                if item_rect.collidepoint(mx, my):
                    pygame.draw.rect(surface, (70, 70, 90), item_rect)
                else:
                    pygame.draw.rect(surface, (55, 55, 65), item_rect)
                    
                pygame.draw.rect(surface, (45, 45, 55), item_rect, width=1)
                
                if HAS_FONT:
                    txt_item = FONT_MD.render(algo, True, COLOR_TEXT)
                    surface.blit(txt_item, (item_rect.x + 10, item_rect.y + 7))

            if total_algos > self.dropdown_max_visible:
                panel_h = self.dropdown_panel_rect.height
                scrollbar_h = max(15, int(panel_h * (self.dropdown_max_visible / total_algos)))
                max_scroll_slots = total_algos - self.dropdown_max_visible
                scrollbar_y = self.dropdown_panel_rect.y + int((panel_h - scrollbar_h) * (self.dropdown_scroll_index / max_scroll_slots))
                
                pygame.draw.rect(surface, COLOR_CLEANED, (self.dropdown_panel_rect.right - 6, scrollbar_y, 4, scrollbar_h), border_radius=2)

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
                if event.button in (4, 5):
                    visualizer.handle_scroll(event.button, mx, my)
                else:
                    visualizer.handle_click(mx, my)
            elif event.type == pygame.KEYDOWN:
                visualizer.handle_keydown(event)
                    
        visualizer.update_simulation()
        visualizer.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()