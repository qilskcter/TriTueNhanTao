import json
import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection

from shapely.geometry import Polygon

from backtracking import BacktrackingSolver
from forward_checking import ForwardCheckingSolver


PROVINCE_FILE = "./DATA/provNew.geojson"
WARD_FILE = "./DATA/Wards.json"


def load_geojson(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    polygons = []

    for feature in data["features"]:
        geom = feature["geometry"]

        if geom["type"] == "Polygon":
            polygons.append(geom["coordinates"][0])

        elif geom["type"] == "MultiPolygon":
            for polygon in geom["coordinates"]:
                polygons.append(polygon[0])

    return polygons


def get_center_point(coords):
    lon_sum = 0
    lat_sum = 0

    for lon, lat in coords:
        lon_sum += lon
        lat_sum += lat

    return lon_sum / len(coords), lat_sum / len(coords)


def load_topojson(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        topo = json.load(f)

    arcs = topo["arcs"]
    geometries = topo["objects"]["collection"]["geometries"]

    def get_arc(index):
        if index >= 0:
            return arcs[index]
        return list(reversed(arcs[-index - 1]))

    def join_arcs(arc_indices):
        coords = []

        for index in arc_indices:
            arc = get_arc(index)

            if coords and coords[-1] == arc[0]:
                coords.extend(arc[1:])
            else:
                coords.extend(arc)

        if coords and coords[0] != coords[-1]:
            coords.append(coords[0])

        return coords

    ward_polygons = []
    ward_names = []
    label_points = []
    shapely_polygons = []

    for i, geom in enumerate(geometries):
        name = geom["properties"].get("Tên", f"Ward {i}")

        if geom["type"] == "Polygon":
            coords = join_arcs(geom["arcs"][0])
            ward_polygons.append(coords)
            ward_names.append(name)
            label_points.append(get_center_point(coords))
            shapely_polygons.append(Polygon(coords).buffer(0))

        elif geom["type"] == "MultiPolygon":
            for polygon in geom["arcs"]:
                coords = join_arcs(polygon[0])
                ward_polygons.append(coords)
                ward_names.append(name)
                label_points.append(get_center_point(coords))
                shapely_polygons.append(Polygon(coords).buffer(0))

    return ward_polygons, ward_names, label_points, shapely_polygons


def build_neighbors(shapely_polygons):
    neighbors = defaultdict(set)
    n = len(shapely_polygons)

    for i in range(n):
        for j in range(i + 1, n):
            inter = shapely_polygons[i].boundary.intersection(
                shapely_polygons[j].boundary
            )

            if not inter.is_empty and inter.length > 0.000001:
                neighbors[i].add(j)
                neighbors[j].add(i)

    return neighbors


class MapColoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Coloring CSP Visualizer")
        self.root.geometry("1500x900")

        self.province_polygons = []
        self.ward_polygons = []
        self.ward_names = []
        self.label_points = []
        self.shapely_polygons = []
        self.neighbors = {}

        self.solver = None
        self.generator = None
        self.assignment = {}

        self.running = False
        self.press = None
        self.current_xlim = None
        self.current_ylim = None

        self.algorithm_var = tk.StringVar(value="fc")

        self.setup_ui()
        self.load_data()
        self.draw_map(first_time=True)

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(main_frame, width=460)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        menu_frame = tk.LabelFrame(right_frame, text="Chọn thuật toán")
        menu_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Radiobutton(
            menu_frame,
            text="Backtracking thường",
            variable=self.algorithm_var,
            value="bt"
        ).pack(anchor="w")

        tk.Radiobutton(
            menu_frame,
            text="Backtracking + Forward Checking",
            variable=self.algorithm_var,
            value="fc"
        ).pack(anchor="w")

        button_frame = tk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=5)

        tk.Button(button_frame, text="Bắt đầu", command=self.start).pack(side=tk.LEFT, padx=3)
        tk.Button(button_frame, text="Bước tiếp", command=self.next_step).pack(side=tk.LEFT, padx=3)
        tk.Button(button_frame, text="Tự động", command=self.auto_run).pack(side=tk.LEFT, padx=3)
        tk.Button(button_frame, text="Dừng", command=self.stop).pack(side=tk.LEFT, padx=3)
        tk.Button(button_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=3)

        self.log_box = scrolledtext.ScrolledText(
            right_frame,
            width=55,
            font=("Arial", 10)
        )
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.fig, self.ax = plt.subplots(figsize=(10, 8), dpi=90)
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=left_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas.mpl_connect("scroll_event", self.zoom)
        self.canvas.mpl_connect("button_press_event", self.pan_start)
        self.canvas.mpl_connect("button_release_event", self.pan_end)
        self.canvas.mpl_connect("motion_notify_event", self.pan_move)

    def load_data(self):
        try:
            self.province_polygons = load_geojson(PROVINCE_FILE)

            result = load_topojson(WARD_FILE)
            self.ward_polygons = result[0]
            self.ward_names = result[1]
            self.label_points = result[2]
            self.shapely_polygons = result[3]

            self.neighbors = build_neighbors(self.shapely_polygons)

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def start(self):
        self.assignment = {}

        if self.algorithm_var.get() == "bt":
            self.solver = BacktrackingSolver(
                len(self.ward_polygons),
                self.ward_names,
                self.neighbors
            )
            algo_name = "Backtracking thường"
        else:
            self.solver = ForwardCheckingSolver(
                len(self.ward_polygons),
                self.ward_names,
                self.neighbors
            )
            algo_name = "Backtracking + Forward Checking"

        self.generator = self.solver.solve_generator()
        self.running = False

        self.log_box.delete("1.0", tk.END)

        self.log("Biểu diễn dưới dạng CSP:")
        self.log("- Biến: các phường/xã")
        self.log("- Miền giá trị: red, lime, blue, yellow")
        self.log("- Ràng buộc: hai phường kề nhau không được cùng màu")
        self.log("")
        self.log(f"Thuật toán đang dùng: {algo_name}")
        self.log("Assignment = {}")
        self.log("")

        self.draw_map()

    def next_step(self):
        if self.generator is None:
            self.start()

        try:
            step = next(self.generator)
        except StopIteration:
            self.log("Đã kết thúc thuật toán.")
            return

        action = step[0]
        ward_index = step[1]
        color = step[2]
        self.assignment = step[3]

        removed_list = []
        if len(step) > 4:
            removed_list = step[4]

        if action == "choose":
            self.log(f"Chọn biến: {self.ward_names[ward_index]}")

        elif action == "try":
            self.log(f"- Thử gán {self.ward_names[ward_index]} = {color}")

        elif action == "valid":
            self.log("- Kiểm tra ràng buộc: hợp lệ")
            self.log(self.assignment_to_text())

        elif action == "invalid":
            self.log("- Kiểm tra ràng buộc: không hợp lệ")

        elif action == "fc":
            self.log("- Forward Checking:")

            if not removed_list:
                self.log("  Không loại màu nào khỏi hàng xóm.")
            else:
                for neighbor, removed_color in removed_list:
                    self.log(
                        f"  Loại màu {removed_color} khỏi "
                        f"{self.ward_names[neighbor]}"
                    )

        elif action == "domain_empty":
            self.log("- Forward Checking phát hiện có phường hết màu khả dụng")
            self.log("- Nhánh này bị loại sớm")

        elif action == "backtrack":
            self.log(
                f"- Backtrack: bỏ màu {color} của "
                f"{self.ward_names[ward_index]}"
            )

        elif action == "done":
            self.log("Hoàn thành tô màu bản đồ.")
            self.log(self.assignment_to_text())

        self.draw_map()

    def auto_run(self):
        self.running = True
        self.run_auto_step()

    def run_auto_step(self):
        if not self.running:
            return

        self.next_step()
        self.root.after(40, self.run_auto_step)

    def stop(self):
        self.running = False

    def reset(self):
        self.assignment = {}
        self.solver = None
        self.generator = None
        self.running = False
        self.log_box.delete("1.0", tk.END)
        self.draw_map()

    def assignment_to_text(self):
        items = []

        for index, color in self.assignment.items():
            items.append(f"{self.ward_names[index]}={color}")

        return "Assignment = {" + ", ".join(items) + "}"

    def draw_map(self, first_time=False):
        if not first_time:
            self.current_xlim = self.ax.get_xlim()
            self.current_ylim = self.ax.get_ylim()

        self.ax.clear()

        province_patches = []
        ward_patches = []
        ward_colors = []

        for coords in self.province_polygons:
            province_patches.append(MplPolygon(coords, closed=True))

        for i, coords in enumerate(self.ward_polygons):
            ward_patches.append(MplPolygon(coords, closed=True))
            ward_colors.append(self.assignment.get(i, "white"))

        province_collection = PatchCollection(
            province_patches,
            facecolor="#eeeeee",
            edgecolor="black",
            linewidth=1.2,
            alpha=1.0
        )

        ward_collection = PatchCollection(
            ward_patches,
            facecolor=ward_colors,
            edgecolor="black",
            linewidth=0.35,
            alpha=0.9
        )

        self.ax.add_collection(province_collection)
        self.ax.add_collection(ward_collection)

        for name, point in zip(self.ward_names, self.label_points):
            lon, lat = point
            self.ax.text(lon, lat, name, fontsize=4, ha="center", va="center")

        if first_time or self.current_xlim is None or self.current_ylim is None:
            center_lon = 106.7009
            center_lat = 10.7769
            zoom_width = 0.10
            zoom_height = 0.075

            self.ax.set_xlim(center_lon - zoom_width, center_lon + zoom_width)
            self.ax.set_ylim(center_lat - zoom_height, center_lat + zoom_height)
        else:
            self.ax.set_xlim(self.current_xlim)
            self.ax.set_ylim(self.current_ylim)

        self.ax.set_aspect("equal", adjustable="box")
        self.ax.axis("off")
        self.canvas.draw_idle()

    def log(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

        line_count = int(self.log_box.index("end-1c").split(".")[0])
        if line_count > 500:
            self.log_box.delete("1.0", "100.0")

    def zoom(self, event):
        if event.xdata is None or event.ydata is None:
            return

        scale = 1.2
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()

        x = event.xdata
        y = event.ydata

        if event.button == "up":
            factor = 1 / scale
        else:
            factor = scale

        new_width = (cur_xlim[1] - cur_xlim[0]) * factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * factor

        self.ax.set_xlim(x - new_width / 2, x + new_width / 2)
        self.ax.set_ylim(y - new_height / 2, y + new_height / 2)

        self.canvas.draw_idle()

    def pan_start(self, event):
        if event.button == 1:
            self.press = (
                event.xdata,
                event.ydata,
                self.ax.get_xlim(),
                self.ax.get_ylim()
            )

    def pan_end(self, event):
        self.press = None

    def pan_move(self, event):
        if self.press is None:
            return

        if event.xdata is None or event.ydata is None:
            return

        x0, y0, xlim, ylim = self.press

        dx = event.xdata - x0
        dy = event.ydata - y0

        self.ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
        self.ax.set_ylim(ylim[0] - dy, ylim[1] - dy)

        self.canvas.draw_idle()


if __name__ == "__main__":
    root = tk.Tk()
    app = MapColoringApp(root)
    root.mainloop()