import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.font import Font
import json
import os

class MountTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WoW Mount Tracker")
        self.mounts = []
        self.dark_mode = True  # Start in dark mode

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Auto-save on exit

        self.setup_theme()
        self.create_widgets()
        self.load_mounts()  # Auto-load on startup

    def setup_theme(self):
        if self.dark_mode:
            self.bg_color = "#1e1b18"
            self.fg_color = "#ffd100"
            self.accent_color = "#2e2a26"
            self.button_color = "#3a312a"
            self.select_color = "#665544"
        else:
            self.bg_color = "#f6f2e9"
            self.fg_color = "#1a0e00"
            self.accent_color = "#ffffff"
            self.button_color = "#ddd4c0"
            self.select_color = "#c4b79c"

        self.font_family = "Georgia"  # Replace with 'Morpheus' if installed
        self.custom_font = Font(family=self.font_family, size=10, weight="bold")

    def create_widgets(self):
        self.root.configure(bg=self.bg_color)

        self.frame = tk.Frame(self.root, bg=self.bg_color)
        self.frame.pack(padx=10, pady=10)

        self.mount_listbox = tk.Listbox(
            self.frame,
            width=80,
            selectmode=tk.SINGLE,
            bg=self.accent_color,
            fg=self.fg_color,
            font=self.custom_font,
            highlightbackground=self.bg_color,
            selectbackground=self.select_color,
            selectforeground=self.fg_color
        )
        self.mount_listbox.pack()

        btn_frame = tk.Frame(self.frame, bg=self.bg_color)
        btn_frame.pack(pady=5)

        self._make_button(btn_frame, "Add Mount", self.add_mount, 0)
        self._make_button(btn_frame, "Remove", self.remove_mount, 1)
        self._make_button(btn_frame, "Farmed ✅", self.mark_farmed, 2)
        self._make_button(btn_frame, "Refresh", self.refresh_all, 3)
        self._make_button(btn_frame, "Toggle Theme", self.toggle_theme, 4)
        self._make_button(btn_frame, "💾 Save", self.save_mounts, 5)
        self._make_button(btn_frame, "📂 Load", self.load_mounts, 6)

    def _make_button(self, frame, text, command, column):
        btn = tk.Button(
            frame,
            text=text,
            command=command,
            bg=self.button_color,
            fg=self.fg_color,
            activebackground=self.select_color,
            activeforeground=self.fg_color,
            relief=tk.FLAT,
            font=self.custom_font
        )
        btn.grid(row=0, column=column, padx=5, pady=5)

    def refresh_ui(self):
        current_mounts = self.mounts.copy()
        self.frame.destroy()
        self.setup_theme()
        self.create_widgets()
        for entry, farmed in current_mounts:
            self.mounts.append((entry, farmed))
            self.mount_listbox.insert(tk.END, entry)
            index = self.mount_listbox.size() - 1
            color = "gray" if "✅" in entry else self.fg_color
            self.mount_listbox.itemconfig(index, {'fg': color})

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.refresh_ui()

    def add_mount(self):
        mount_name = simpledialog.askstring("Mount Name", "Enter mount name:")
        if not mount_name: return
        raid_name = simpledialog.askstring("Raid Name", "Enter raid name:")
        if not raid_name: return
        difficulty = simpledialog.askstring("Raid Difficulty", "e.g., Normal, Heroic, Mythic:")
        if not difficulty: return
        size = simpledialog.askstring("Raid Size", "10-man, 25-man, or N/A:")
        if not size: return

        entry = f"{mount_name} - {raid_name} - {difficulty} - {size}"
        self.mount_listbox.insert(tk.END, entry)
        self.mounts.append((entry, False))

    def remove_mount(self):
        selected = self.mount_listbox.curselection()
        if not selected:
            messagebox.showinfo("No selection", "Select a mount to remove.")
            return
        self.mount_listbox.delete(selected)
        del self.mounts[selected[0]]

    def mark_farmed(self):
        selected = self.mount_listbox.curselection()
        if not selected:
            messagebox.showinfo("No selection", "Select a mount to mark as farmed.")
            return
        index = selected[0]
        current_text = self.mount_listbox.get(index)
        if "✅" not in current_text:
            self.mount_listbox.delete(index)
            grayed = f"{current_text} ✅"
            self.mount_listbox.insert(index, grayed)
            self.mount_listbox.itemconfig(index, {'fg': 'gray'})
            self.mounts[index] = (grayed, True)

    def refresh_all(self):
        self.mount_listbox.delete(0, tk.END)
        for i, (entry, farmed) in enumerate(self.mounts):
            clean_entry = entry.replace(" ✅", "")
            self.mount_listbox.insert(tk.END, clean_entry)
            self.mount_listbox.itemconfig(i, {'fg': self.fg_color})
            self.mounts[i] = (clean_entry, False)

    def save_mounts(self):
        try:
            with open("mounts.json", "w") as f:
                json.dump(self.mounts, f)
            messagebox.showinfo("Saved", "Mount list saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {e}")

    def load_mounts(self):
        if os.path.exists("mounts.json"):
            try:
                with open("mounts.json", "r") as f:
                    self.mounts = json.load(f)
                self.mount_listbox.delete(0, tk.END)
                for entry, farmed in self.mounts:
                    self.mount_listbox.insert(tk.END, entry)
                    index = self.mount_listbox.size() - 1
                    color = "gray" if "✅" in entry else self.fg_color
                    self.mount_listbox.itemconfig(index, {'fg': color})
            except Exception as e:
                messagebox.showerror("Error", f"Could not load: {e}")

    def on_close(self):
        self.save_mounts()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MountTrackerApp(root)
    root.mainloop()
