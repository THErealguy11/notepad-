import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import requests
import os
import subprocess

class NotepadApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Notepad+++")
        self.master.geometry("800x600")

        self.create_menu()
        self.create_text_area()

        self.check_for_updates()  # Check for updates when the application starts

    def create_menu(self):
        self.menu_bar = tk.Menu(self.master)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Update", command=self.check_for_updates)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Settings menu
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.settings_menu.add_command(label="Change Theme", command=self.change_theme)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        self.master.config(menu=self.menu_bar)

    def create_text_area(self):
        self.text_area = tk.Text(self.master, wrap="word")
        self.text_area.pack(fill="both", expand=True)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        content = self.text_area.get(1.0, tk.END)
        if content.strip() != "":
            file_path = filedialog.asksaveasfilename(defaultextension=".txt")
            if file_path:
                with open(file_path, "w") as file:
                    file.write(content)
                    messagebox.showinfo("Success", "File saved successfully!")
        else:
            messagebox.showerror("Error", "Cannot save an empty file!")

    def check_for_updates(self):
        try:
            latest_release_info = self.get_latest_release_info()
            if latest_release_info:
                latest_version = latest_release_info['tag_name']
                if self.is_newer_version_available(latest_version):
                    self.download_and_install_update(latest_release_info['assets'][0]['browser_download_url'])
                else:
                    messagebox.showinfo("Update", "Your application is up to date.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while checking for updates: {e}")

    def get_latest_release_info(self):
        try:
            response = requests.get('https://api.github.com/repos/THErealguy11/notepad-/releases/latest')
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", "Failed to fetch latest release information.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None

    def is_newer_version_available(self, latest_version):
        current_version = '1.0.0'  # Replace with your current version
        return latest_version != current_version

    def download_and_install_update(self, download_url):
        try:
            response = requests.get(download_url)
            if response.status_code == 200:
                update_package_path = 'update.zip'  # Path to temporarily store the update package
                with open(update_package_path, 'wb') as file:
                    file.write(response.content)
                # Extract the update package and replace existing application files
                # Perform necessary setup or initialization tasks after updating
                subprocess.run(['unzip', update_package_path])
                os.remove(update_package_path)  # Clean up the temporary update package
                messagebox.showinfo("Update", "Update installed successfully. Please restart the application.")
            else:
                messagebox.showerror("Error", "Failed to download update package.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def cut_text(self):
        self.master.clipboard_clear()
        selected_text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.master.clipboard_append(selected_text)
        self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def copy_text(self):
        self.master.clipboard_clear()
        selected_text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        if selected_text:
            self.master.clipboard_append(selected_text)
            self.edit_menu.entryconfig("Paste", state="normal")
        else:
            self.edit_menu.entryconfig("Paste", state="disabled")

    def paste_text(self):
        clipboard_content = self.master.clipboard_get()
        if clipboard_content:
            self.text_area.insert(tk.INSERT, clipboard_content)
            self.edit_menu.entryconfig("Paste", state="normal")
        else:
            self.edit_menu.entryconfig("Paste", state="disabled")

    def change_theme(self):
        theme_color = colorchooser.askcolor()[1]
        if theme_color:
            self.text_area.config(bg=theme_color)

def main():
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
