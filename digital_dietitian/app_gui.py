import threading
from datetime import date, timedelta

import cv2
import matplotlib.pyplot as plt
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pyzbar import pyzbar

from api_fetcher import fetch_nutrition
from user_profile import (
    init_db, save_user, load_user, log_intake,
    get_daily_intake, delete_user, delete_intake_by_date,
    delete_all_intake, get_intake_between
)
from tracker import summarize_intake
from suggestions import suggest_alternatives

class DigitalDietitianApp(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("🍏 Digital Dietitian")
        self.geometry("900x900")
        # global font
        self.style.configure('.', font=('Segoe UI', 11))
        init_db()

        self.cap = None
        self.scanning = False
        self.scanned_barcodes = set()

        self._build_ui()
        self._load_profile()
        self._update_summary()
        self._update_graph()

    def _build_ui(self):
        notebook = tb.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Profile Tab ---
        prof_tab = tb.Frame(notebook)
        notebook.add(prof_tab, text="👤 Profile")

        prof_frame = tb.Labelframe(prof_tab, text="Your Details", bootstyle="info")
        prof_frame.pack(fill=tk.X, padx=20, pady=20)

        labels = ["Age", "Weight (kg)", "Height (cm)", "Gender", "Goal", "Preferences"]
        self.entries = {}
        for i, lbl in enumerate(labels):
            tb.Label(prof_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=10, pady=4)
            ent = tb.Entry(prof_frame, width=30)
            ent.grid(row=i, column=1, sticky=tk.W, padx=10, pady=4)
            self.entries[lbl.lower()] = ent

        btns = tb.Frame(prof_frame)
        btns.grid(row=6, column=0, columnspan=2, pady=10)
        tb.Button(btns, text="💾 Save",   bootstyle="success", width=12, command=self._save_profile).grid(row=0, column=0, padx=5)
        tb.Button(btns, text="🗑 Delete", bootstyle="danger",  width=12, command=self._delete_profile).grid(row=0, column=1, padx=5)

        # --- Scan Tab ---
        scan_tab = tb.Frame(notebook)
        notebook.add(scan_tab, text="🔍 Scan")

        scan_frame = tb.Labelframe(scan_tab, text="Camera & Scan", bootstyle="warning")
        scan_frame.pack(fill=tk.X, padx=20, pady=10)

        self.video_label = tb.Label(scan_frame)
        self.video_label.pack(padx=10, pady=10)

        self.scan_btn = tb.Button(scan_frame, text="▶ Start Scanning", bootstyle="primary", width=24,
                                  command=self._toggle_scanning)
        self.scan_btn.pack(pady=5)

        tree_frame = tb.Labelframe(scan_tab, text="Scanned Items", bootstyle="info")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        cols = ("barcode","name","calories","protein","fat","carbs","sugar","sodium")
        self.tree = tb.Treeview(tree_frame, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=100, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Summary Tab ---
        sum_tab = tb.Frame(notebook)
        notebook.add(sum_tab, text="📊 Summary")

        filter_frame = tb.Frame(sum_tab)
        filter_frame.pack(fill=tk.X, padx=20, pady=10)
        tb.Label(filter_frame, text="Show last:").pack(side=tk.LEFT)
        self.period_cb = tb.Combobox(filter_frame, values=["7 days","14 days","21 days","28 days","30 days"],
                                     state="readonly", width=12)
        self.period_cb.current(4)
        self.period_cb.pack(side=tk.LEFT, padx=5)
        self.period_cb.bind("<<ComboboxSelected>>", lambda e: (self._update_summary(), self._update_graph()))

        self.summary_frame = tb.Labelframe(sum_tab, text="Today's Totals", bootstyle="info")
        self.summary_frame.pack(fill=tk.X, padx=20, pady=10)

        self.graph_frame = tb.Labelframe(sum_tab, text="30-Day Calorie Trend", bootstyle="secondary")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # -- Profile Methods --
    def _save_profile(self):
        data = {k: self.entries[k].get() for k in self.entries}
        try:
            profile = {
                'age': int(data['age']),
                'weight': float(data['weight (kg)']),
                'height': float(data['height (cm)']),
                'gender': data['gender'],
                'goal': data['goal'],
                'preferences': data['preferences']
            }
            save_user(profile)
            messagebox.showinfo("Success", "Profile saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid data: {e}")

    def _load_profile(self):
        prof = load_user()
        if prof:
            for key, ent in self.entries.items():
                ent.delete(0, tk.END)
                val = prof.get(key)
                ent.insert(0, str(val) if val is not None else "")

    def _delete_profile(self):
        if messagebox.askyesno("Confirm", "Delete profile?"):
            delete_user()
            for ent in self.entries.values():
                ent.delete(0, tk.END)
            messagebox.showinfo("Deleted", "Profile removed.")

    # -- Scanning Methods --
    def _toggle_scanning(self):
        if not self.scanning:
            self.cap = cv2.VideoCapture(0)
            self.scanning = True
            self.scan_btn.config(text="■ Stop Scanning", bootstyle="danger")
            self._video_loop()
        else:
            self.scanning = False
            self.scan_btn.config(text="▶ Start Scanning", bootstyle="primary")
            if self.cap:
                self.cap.release()

    def _video_loop(self):
        if not self.scanning:
            return
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame).resize((600,360))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)

            barcodes = pyzbar.decode(frame)
            for bc in barcodes:
                code = bc.data.decode('utf-8')
                if code not in self.scanned_barcodes:
                    self.scanned_barcodes.add(code)
                    self._handle_scan(code)
                break

        self.after(30, self._video_loop)

    def _handle_scan(self, barcode):
        try:
            data = fetch_nutrition(barcode)
        except Exception as e:
            messagebox.showerror("Error", f"Lookup failed: {e}")
            return
        log_intake(data)
        self.tree.insert("", "end", values=(
            barcode,
            (data['name'][:15] + '…') if len(data['name'])>15 else data['name'],
            f"{data['calories']:.1f}",
            f"{data['protein']:.1f}",
            f"{data['fat']:.1f}",
            f"{data['carbs']:.1f}",
            f"{data['sugar']:.1f}",
            f"{data['sodium']:.1f}"
        ))
        self._update_summary()
        self._update_graph()

    # -- Summary Methods --
    def _update_summary(self):
        for w in self.summary_frame.winfo_children():
            w.destroy()
        days = int(self.period_cb.get().split()[0])
        end = date.today()
        start = end - timedelta(days=days-1)
        rows = []
        for single in (start + timedelta(n) for n in range(days)):
            rows.extend(get_daily_intake(single.isoformat()))
        total = summarize_intake(rows)

        colors = {
            'calories': 'danger', 'protein': 'success',
            'fat': 'warning', 'carbs': 'primary',
            'sugar': 'secondary', 'sodium': 'info'
        }
        for idx, (k, v) in enumerate(total.items()):
            tb.Label(
                self.summary_frame,
                text=f"{k.title()}: {v:.1f}",
                bootstyle=f"{colors[k]}-inverse",
                width=32
            ).grid(row=idx//2, column=idx%2, padx=15, pady=6)

    def _update_graph(self):
        for w in self.graph_frame.winfo_children():
            w.destroy()
        days = int(self.period_cb.get().split()[0])
        end = date.today()
        start = end - timedelta(days=days-1)
        data = get_intake_between(start.isoformat(), end.isoformat())
        idx = {d: c for d, c in data}
        x = [(start + timedelta(i)).strftime("%m-%d") for i in range(days)]
        y = [idx.get((start + timedelta(i)).isoformat(), 0) for i in range(days)]

        fig = plt.Figure(figsize=(8, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y, marker='o', color='green')
        ax.set_title(f"Last {days} Days: Daily Calories")
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _delete_today(self):
        if messagebox.askyesno("Confirm", "Clear today's intake?"):
            delete_intake_by_date(date.today().isoformat())
            self._update_summary()
            self._update_graph()

    def _delete_all_intake(self):
        if messagebox.askyesno("Confirm", "Delete ALL intake?"):
            delete_all_intake()
            self._update_summary()
            self._update_graph()

if __name__ == "__main__":
    DigitalDietitianApp().mainloop()
