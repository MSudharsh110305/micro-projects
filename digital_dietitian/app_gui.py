import threading
from datetime import date, timedelta

import matplotlib.pyplot as plt
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

from scanner import scan_barcode_from_camera
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
        self.geometry("800x720")
        # global font
        self.style.configure('.', font=('Segoe UI', 11))
        init_db()
        self._build_ui()
        self._load_profile()
        self._update_summary()

    def _build_ui(self):
        nb = tb.Notebook(self)
        nb.pack(fill=BOTH, expand=True, padx=12, pady=12)

        # ---- Profile Tab ----
        prof_tab = tb.Frame(nb)
        nb.add(prof_tab, text="👤 Profile")

        prof_frame = tb.Labelframe(prof_tab, text="Your Details", bootstyle="info")
        prof_frame.pack(fill=X, padx=20, pady=20)

        labels = ["Age", "Weight (kg)", "Height (cm)", "Gender", "Goal", "Preferences"]
        self.entries = {}
        for i, lbl in enumerate(labels):
            tb.Label(prof_frame, text=lbl).grid(row=i, column=0, sticky=E, padx=10, pady=8)
            ent = tb.Entry(prof_frame, width=30)
            ent.grid(row=i, column=1, sticky=W, padx=10, pady=8)
            self.entries[lbl.lower()] = ent

        btns = tb.Frame(prof_frame)
        btns.grid(row=6, column=0, columnspan=2, pady=15)
        tb.Button(btns, text="💾 Save",    bootstyle="success", width=14, command=self._save_profile).grid(row=0, column=0, padx=10)
        tb.Button(btns, text="🗑 Delete",  bootstyle="danger",  width=14, command=self._delete_profile).grid(row=0, column=1, padx=10)

        # ---- Scan Tab ----
        scan_tab = tb.Frame(nb)
        nb.add(scan_tab, text="🔍 Scan")

        scan_frame = tb.Labelframe(scan_tab, text="Scan & Log Food", bootstyle="warning")
        scan_frame.pack(fill=X, padx=20, pady=20)

        tb.Button(scan_frame, text="📷 Scan Barcode", bootstyle="primary", width=24,
                  command=self._threaded_scan).pack(pady=12)
        self.scan_result = tb.Label(scan_frame, text="No scan yet", bootstyle="secondary")
        self.scan_result.pack(pady=6)

        # ---- Summary Tab ----
        sum_tab = tb.Frame(nb)
        nb.add(sum_tab, text="📊 Summary")

        ctrl = tb.Frame(sum_tab)
        ctrl.pack(fill=X, padx=20, pady=10)
        tb.Button(ctrl, text="🔄 Refresh",      bootstyle="primary-outline", command=self._update_summary).pack(side=LEFT, padx=5)
        tb.Button(ctrl, text="❌ Clear Today",  bootstyle="danger-outline",  command=self._delete_today).pack(side=LEFT, padx=5)
        tb.Button(ctrl, text="🧹 Clear All",    bootstyle="warning-outline", command=self._delete_all_intake).pack(side=LEFT, padx=5)
        tb.Button(ctrl, text="📈 30-Day Graph", bootstyle="success-outline",  command=self._show_monthly_graph).pack(side=LEFT, padx=5)

        self.summary_frame = tb.Labelframe(sum_tab, text="Today's Totals", bootstyle="info")
        self.summary_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

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
            messagebox.showinfo("Success", "Profile saved successfully.")
        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid data: {e}")

    def _load_profile(self):
        prof = load_user()
        if prof:
            for key, ent in self.entries.items():
                ent.delete(0, tb.END)
                val = prof.get(key)
                ent.insert(0, str(val) if val is not None else "")

    def _delete_profile(self):
        if messagebox.askyesno("Confirm", "Delete profile?"):
            delete_user()
            for ent in self.entries.values():
                ent.delete(0, tb.END)
            messagebox.showinfo("Deleted", "Profile removed.")

    def _threaded_scan(self):
        threading.Thread(target=self._scan_and_log, daemon=True).start()

    def _scan_and_log(self):
        barcode = scan_barcode_from_camera()
        if not barcode:
            self.scan_result.config(text="❌ No barcode detected.")
            return
        self.scan_result.config(text=f"✅ Scanned: {barcode}")
        try:
            data = fetch_nutrition(barcode)
        except Exception as e:
            messagebox.showerror("Error", f"Data fetch failed: {e}")
            return

        log_intake(data)
        alts = suggest_alternatives(data['name'])
        msg = (
            f"{data['name']}\n"
            f"Calories: {data['calories']:.1f} kcal\n"
            f"Protein: {data['protein']:.1f} g   Fat: {data['fat']:.1f} g\n"
            f"Carbs: {data['carbs']:.1f} g    Sugar: {data['sugar']:.1f} g\n"
            f"Sodium: {data['sodium']:.1f} mg\n"
        )
        if alts:
            msg += "\nAlternatives:\n" + "\n".join(f"• {a}" for a in alts)
        messagebox.showinfo("Nutrition Details", msg)
        self._update_summary()

    def _update_summary(self):
        # clear old
        for w in self.summary_frame.winfo_children():
            w.destroy()
        totals = summarize_intake(get_daily_intake())
        colors = {
            'calories': 'danger', 'protein': 'success',
            'fat': 'warning', 'carbs': 'primary',
            'sugar': 'secondary', 'sodium': 'info'
        }
        for idx, (k, v) in enumerate(totals.items()):
            tb.Label(
                self.summary_frame,
                text=f"{k.title()}: {v:.1f}",
                bootstyle=f"{colors[k]}-inverse",
                width=28
            ).grid(row=idx//2, column=idx%2, padx=15, pady=12)

    def _delete_today(self):
        if messagebox.askyesno("Confirm", "Clear today's log?"):
            delete_intake_by_date(date.today().isoformat())
            self._update_summary()
            messagebox.showinfo("Deleted", "Today's data cleared.")

    def _delete_all_intake(self):
        if messagebox.askyesno("Confirm", "Delete ALL intake?"):
            delete_all_intake()
            self._update_summary()
            messagebox.showinfo("Deleted", "All data cleared.")

    def _show_monthly_graph(self):
        end = date.today()
        start = end - timedelta(days=29)
        data = get_intake_between(start.isoformat(), end.isoformat())
        idx = {d: c for d, c in data}
        days = [(start + timedelta(days=i)).isoformat() for i in range(30)]
        values = [idx.get(d, 0) for d in days]

        plt.figure(figsize=(9, 4))
        plt.plot(days, values, marker='o', linestyle='-', linewidth=2)
        plt.xticks(rotation=45, ha='right')
        plt.title("Last 30 Days: Daily Calories Intake")
        plt.xlabel("Date")
        plt.ylabel("Calories")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = DigitalDietitianApp()
    app.mainloop()
