"""Основной класс приложения JSON/XML Viewer."""

import tkinter as tk
from tkinter import ttk, filedialog, font, messagebox
import os

from config import CONFIG
from parser import DataParser
from widgets import TaggedTreeview, ClosableNotebook


class JSONXMLViewer:
    def __init__(self, root):
        self.root = root
        self.root.title(CONFIG["window"]["title"])
        self.root.geometry(
            f"{CONFIG['window']['width']}x{CONFIG['window']['height']}"
        )

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.files = {}  # {frame_id: {'tree': widget, 'path': str, 'frame': widget}}
        self.search_results = []
        self.current_result_index = -1

        self._setup_ui()
        self._setup_styles()
        self._setup_bindings()

    def _setup_ui(self):
        self._create_toolbar()
        self._create_main_area()
        self._create_statusbar()

    def _create_toolbar(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side="top", fill="x", padx=10, pady=8)

        ttk.Button(top_frame, text="📂 Открыть", command=self.open_files).pack(
            side="left", padx=2
        )
        ttk.Button(top_frame, text="✕ Закрыть", command=self.close_current_tab).pack(
            side="left", padx=2
        )

        ttk.Label(top_frame, text="|").pack(side="left", padx=10)

        ttk.Label(top_frame, text="Поиск:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(top_frame, width=40)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda e: self.perform_search())

        ttk.Button(top_frame, text="Найти", command=self.perform_search).pack(
            side="left", padx=5
        )
        ttk.Button(top_frame, text="Очистить", command=self.clear_search).pack(
            side="left", padx=2
        )

        ttk.Label(top_frame, text="|").pack(side="left", padx=10)

        ttk.Label(top_frame, text="Шрифт:").pack(side="left", padx=5)
        self.font_size_var = tk.StringVar(value=str(CONFIG["font_size"]))
        spin = ttk.Spinbox(
            top_frame,
            from_=8,
            to=24,
            width=4,
            textvariable=self.font_size_var,
            command=self.change_font_size,
        )
        spin.pack(side="left")

    def _create_main_area(self):
        main_paned = ttk.PanedWindow(self.root, orient="vertical")
        main_paned.pack(fill="both", expand=True, padx=5, pady=5)

        # Верхняя часть - вкладки
        top_pane = ttk.Frame(main_paned)
        main_paned.add(top_pane, weight=CONFIG["layout"]["editor_weight"])

        self.notebook = ClosableNotebook(top_pane)
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind("<ButtonPress-2>", self.on_middle_click)
        self.notebook.context_menu.add_command(
            label="Закрыть вкладку", command=self.close_current_tab
        )
        self.notebook.context_menu.add_command(
            label="Закрыть все", command=self.close_all_tabs
        )

        # Нижняя часть - результаты
        bottom_pane = ttk.Frame(main_paned)
        main_paned.add(bottom_pane, weight=CONFIG["layout"]["results_weight"])

        ttk.Label(
            bottom_pane, text="🔍 Результаты поиска", font=(CONFIG["font_family"], 11, "bold")
        ).pack(pady=5)

        result_frame = ttk.Frame(bottom_pane)
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.results_tree = TaggedTreeview(result_frame, columns=("path",), show="tree")
        self.results_tree.heading("#0", text="Найдено")
        self.results_tree.column("#0", width=300)
        self.results_tree.column("path", width=200)

        vsb = ttk.Scrollbar(result_frame, orient="vertical", command=self.results_tree.yview)
        hsb = ttk.Scrollbar(result_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.results_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

        self.results_tree.bind("<Double-1>", self.on_result_double_click)

    def _create_statusbar(self):
        self.status_label = ttk.Label(self.root, text="Готов", relief="sunken", anchor="w")
        self.status_label.pack(side="bottom", fill="x", padx=5, pady=2)

    def _setup_styles(self):
        colors = CONFIG["colors"]
        self.style.configure(
            "Treeview",
            background=colors["bg"],
            foreground=colors["fg"],
            fieldbackground=colors["bg"],
            rowheight=22,
        )
        self.style.configure("Treeview.Heading", background=colors["heading_bg"])
        self.style.map(
            "Treeview",
            foreground=[("selected", "white")],
            background=[("selected", colors["selection"])],
        )

    def _setup_bindings(self):
        self.root.bind("<Control-o>", lambda e: self.open_files())
        self.root.bind("<Control-f>", lambda e: self.search_entry.focus())
        self.root.bind("<Control-w>", lambda e: self.close_current_tab())
        self.root.bind("<F3>", lambda e: self.find_next())

    def open_files(self):
        filetypes = [("JSON/XML files", "*.json *.xml"), ("All files", "*.*")]
        paths = filedialog.askopenfilenames(title="Открыть файлы", filetypes=filetypes)
        for path in paths:
            self.load_file(path)

    def load_file(self, path):
        filename = os.path.basename(path)
        ext = os.path.splitext(path)[1].lower()

        try:
            if ext == ".json":
                data = DataParser.parse_json(path)
                parse_func = self._build_json_tree
            elif ext == ".xml":
                data = DataParser.parse_xml(path)
                parse_func = self._build_xml_tree
            else:
                messagebox.showwarning("Warning", f"Неподдерживаемый формат: {ext}")
                return

            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=f" {filename} ")

            tree = TaggedTreeview(frame, selectmode="browse")
            vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

            tree.grid(row=0, column=0, sticky="nsew")
            vsb.grid(row=0, column=1, sticky="ns")
            hsb.grid(row=1, column=0, sticky="ew")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            parse_func(tree, "", data)

            frame_id = str(frame)
            self.files[frame_id] = {"tree": tree, "path": path, "frame": frame}
            self.notebook.select(frame)
            self.status_label.config(text=f"Открыт: {filename}")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _build_json_tree(self, tree, parent, data, path=""):
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, (dict, list)):
                    node = tree.insert(
                        parent, "end", text=key, open=False, tags=("key",), values=(new_path,)
                    )
                    self._build_json_tree(tree, node, value, new_path)
                else:
                    tag = DataParser.get_tag_by_type(value)
                    text = f"{key}: {value}"
                    tree.insert(parent, "end", text=text, tags=(tag,), values=(new_path,))
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                if isinstance(item, (dict, list)):
                    node = tree.insert(
                        parent, "end", text=f"[{i}]", open=False, tags=("key",), values=(new_path,)
                    )
                    self._build_json_tree(tree, node, item, new_path)
                else:
                    tag = DataParser.get_tag_by_type(item)
                    text = f"[{i}]: {item}"
                    tree.insert(parent, "end", text=text, tags=(tag,), values=(new_path,))

    def _build_xml_tree(self, tree, parent, element, path=""):
        tag = element.tag
        new_path = f"{path}/{tag}" if path else tag

        node = tree.insert(
            parent, "end", text=tag, open=False, tags=("key",), values=(new_path,)
        )

        if element.attrib:
            for attr_key, attr_value in element.attrib.items():
                attr_path = f"{new_path}/@{attr_key}"
                text = f"@{attr_key}: {attr_value}"
                tree.insert(node, "end", text=text, tags=("xml_attr",), values=(attr_path,))

        if element.text and element.text.strip():
            text_path = f"{new_path}/#text"
            text_content = element.text.strip()
            display_text = (
                text_content if len(text_content) < 50 else text_content[:47] + "..."
            )
            tree.insert(
                node, "end", text=f"#text: {display_text}", tags=("string",), values=(text_path,)
            )

        for child in element:
            self._build_xml_tree(tree, node, child, new_path)

    def on_middle_click(self, event):
        frame_id = self._get_frame_id_from_event(event)
        if frame_id and frame_id in self.files:
            self.close_tab(frame_id)

    def _get_frame_id_from_event(self, event):
        index = self.notebook.index(f"@{event.x},{event.y}")
        if index >= 0:
            tabs = self.notebook.tabs()
            if index < len(tabs):
                return tabs[index]
        return None

    def close_tab(self, frame_id):
        if frame_id in self.files:
            tree = self.files[frame_id]["tree"]
            for item in tree.get_children(""):
                tree.delete(item)
            del self.files[frame_id]

        self.notebook.forget(frame_id)
        self.clear_search()

        if not self.files:
            self.status_label.config(text="Нет открытых файлов")

    def close_current_tab(self):
        current_tab_id = self.notebook.select()
        if current_tab_id and current_tab_id in self.files:
            self.close_tab(current_tab_id)

    def close_all_tabs(self):
        for frame_id in list(self.files.keys()):
            self.close_tab(frame_id)

    def change_font_size(self):
        try:
            size = int(self.font_size_var.get())
            CONFIG["font_size"] = size
            new_font = font.Font(family=CONFIG["font_family"], size=size)
            for info in self.files.values():
                info["tree"].configure(font=new_font)
            self.results_tree.configure(font=new_font)
        except ValueError:
            pass

    def perform_search(self):
        self.clear_search()
        query = self.search_entry.get().strip().lower()
        if not query:
            return

        count = 0
        for frame_id, info in self.files.items():
            tree = info["tree"]
            for item in tree.get_children(""):
                count += self._search_recursive(tree, item, query, frame_id)

        self.search_results.sort(key=lambda x: x[2])
        self.status_label.config(text=f"Найдено: {count} совпадений")
        self._update_results_panel()

    def _search_recursive(self, tree, item, query, frame_id):
        count = 0
        text = tree.item(item, "text").lower()
        values = tree.item(item, "values")
        path = values[0] if values else ""

        if query in text:
            current_tags = tree.item(item, "tags")
            if "highlight" not in current_tags:
                tree.item(item, tags=tuple(set(current_tags) | {"highlight"}))

            parent = tree.parent(item)
            while parent:
                tree.item(parent, open=True)
                parent = tree.parent(parent)

            self.search_results.append((frame_id, item, path, text))
            count += 1

        for child in tree.get_children(item):
            count += self._search_recursive(tree, child, query, frame_id)
        return count

    def clear_search(self):
        for info in self.files.values():
            tree = info["tree"]
            for item in tree.get_children(""):
                self._clear_highlight(tree, item)
        self.search_results = []
        self.current_result_index = -1
        for item in self.results_tree.get_children(""):
            self.results_tree.delete(item)
        self.status_label.config(text="Готов")

    def _clear_highlight(self, tree, item):
        tags = tree.item(item, "tags")
        if "highlight" in tags:
            tree.item(item, tags=tuple(t for t in tags if t != "highlight"))
        for child in tree.get_children(item):
            self._clear_highlight(tree, child)

    def _update_results_panel(self):
        for item in self.results_tree.get_children(""):
            self.results_tree.delete(item)

        for i, (frame_id, item_id, path, text) in enumerate(self.search_results):
            filename = os.path.basename(self.files[frame_id]["path"])
            display = (
                f"{filename}: {text[:50]}..." if len(text) > 50 else f"{filename}: {text}"
            )
            self.results_tree.insert(
                "", "end", iid=f"result_{i}", text=display, values=(path,)
            )

    def on_result_double_click(self, event):
        selection = self.results_tree.selection()
        if not selection:
            return

        item_id = selection[0]
        try:
            index = int(item_id.split("_")[1])
            if 0 <= index < len(self.search_results):
                frame_id, tree_item, path, text = self.search_results[index]

                if frame_id not in self.files:
                    return

                self.notebook.select(frame_id)

                tree = self.files[frame_id]["tree"]
                tree.selection_set(tree_item)
                tree.focus(tree_item)
                tree.see(tree_item)

                self.status_label.config(text=f"Переход: {path}")
        except (IndexError, ValueError):
            pass

    def find_next(self):
        if not self.search_results:
            return
        self.current_result_index = (self.current_result_index + 1) % len(
            self.search_results
        )
        frame_id, tree_item, path, text = self.search_results[self.current_result_index]

        if frame_id not in self.files:
            return

        self.notebook.select(frame_id)
        tree = self.files[frame_id]["tree"]
        tree.selection_set(tree_item)
        tree.focus(tree_item)
        tree.see(tree_item)
        self.status_label.config(
            text=f"Результат {self.current_result_index + 1}/{len(self.search_results)}: {path}"
        )