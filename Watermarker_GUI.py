import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import json
import os
import threading
from watermarker import watermark_adder

USERS_LIST = "users.json"
OUTPUT_FOLDER = "C:\OTPUT_FOLDER" #Change this to the desired output folder


def add_files_from_dnd(event) -> None:
    """Add files to the selected_files list when they are dragged and dropped."""
    files = file_listbox.tk.splitlist(event.data)
    selected_files.extend(files)
    update_file_list()


def load_users() -> list:
    """Returns the list of users from the file."""
    if os.path.exists(USERS_LIST):
        with open(USERS_LIST, "r") as file:
            return sorted(json.load(file))
    return []


def save_users(users) -> None:
    """Save the list of users to the file."""
    with open(USERS_LIST, "w") as file:
        json.dump(users, file, indent=4)


def add_user() -> None:
    """Add a user to the list of users."""
    user = user_entry.get().strip()
    if user and user not in users:
        users.append(user)
        users.sort()
        save_users(users)
        update_user_list()
        user_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "The user already exists or the field is empty.")


def delete_user() -> None:
    """Delete the selected user(s) from the list of users."""
    selected_indices = users_listbox.curselection()
    if selected_indices:
        for index in reversed(selected_indices):
            actual_index = users.index(display_users[index])
            del users[actual_index]
        users.sort()
        save_users(users)
        update_user_list()
    else:
        messagebox.showwarning("Warning", "Select the user(s) to delete.")


def update_user_list(display_users=None) -> None:
    """Update the list of users in the listbox."""
    if display_users is None:
        display_users = users

    # Save the current selection
    current_selection = users_listbox.curselection()
    selected_users = [users_listbox.get(i) for i in current_selection]

    users_listbox.delete(0, tk.END)
    for user in display_users:
        users_listbox.insert(tk.END, user)

    # Restore the selection
    for idx, user in enumerate(display_users):
        if user in selected_users:
            users_listbox.selection_set(idx)


def search_users(event=None) -> None:
    """Search for users in the list of users."""
    search_query = user_entry.get().strip().lower()
    global display_users
    if search_query:
        display_users = [user for user in users if search_query in user.lower()]
    else:
        display_users = users
    update_user_list(display_users)


def select_files() -> None:
    """Open the file dialog to select files."""
    # Save the current selection of users
    current_user_selection = users_listbox.curselection()

    # Open the file dialog to select files
    files = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.mov")])
    print(files)
    if files:
        selected_files.extend(files)
        update_file_list()

    # Restore the selection of users
    for index in current_user_selection:
        users_listbox.selection_set(index)


def update_file_list() -> None:
    """Update the list of files in the listbox."""
    file_listbox.delete(0, tk.END)
    for file in selected_files:
        file_listbox.insert(tk.END, os.path.basename(file))


def clear_file_list() -> None:
    """Clear the list of selected files."""
    selected_files.clear()
    update_file_list()


def delete_selected_files(event=None) -> None:
    """Delete the selected file(s) from the list of files."""
    selected_indices = file_listbox.curselection()
    if selected_indices:
        for index in reversed(selected_indices):
            del selected_files[index]
        update_file_list()
    else:
        messagebox.showwarning("Warning", "Select the file(s) to delete.")


def start_watermarker() -> None:
    """Start the watermarking process and provide feedback to the user."""
    selected_user_indices = users_listbox.curselection()
    if not selected_user_indices or not selected_files:
        messagebox.showwarning("Warning", "The list of selected users or files is empty.")
        return

    selected_users = [display_users[i] for i in selected_user_indices]
    mapping = [(user, file) for user in selected_users for file in selected_files]

    def thread_target():
        watermark_adder(mapping, OUTPUT_FOLDER)

    thread = threading.Thread(target=thread_target)
    thread.start()


if __name__ == "__main__":

    users = load_users()
    selected_files = []
    display_users = users  # The list of users to display in the listbox

    root = TkinterDnD.Tk()
    root.title("Watermarker")

    user_frame = ttk.LabelFrame(root, text="Users")
    user_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    users_listbox = tk.Listbox(user_frame, height=20, width=25, selectmode=tk.EXTENDED)
    users_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    user_scrollbar = ttk.Scrollbar(user_frame, orient=tk.VERTICAL, command=users_listbox.yview)
    users_listbox.config(yscrollcommand=user_scrollbar.set)
    user_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    user_entry = ttk.Entry(root)
    user_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    user_entry.bind("<KeyRelease>", search_users)
    add_user_button = ttk.Button(root, text="Add user", command=add_user)
    add_user_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    delete_user_button = ttk.Button(root, text="Delete user", command=delete_user)
    delete_user_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    file_frame = ttk.LabelFrame(root, text="Files")
    file_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    file_listbox = tk.Listbox(file_frame, height=20, width=40, selectmode=tk.EXTENDED)
    file_listbox.bind("<BackSpace>", delete_selected_files)
    file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    file_scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=file_listbox.yview)
    file_listbox.config(yscrollcommand=file_scrollbar.set)
    file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    file_listbox.drop_target_register(DND_FILES)
    file_listbox.dnd_bind('<<Drop>>', add_files_from_dnd)

    select_files_button = ttk.Button(root, text="Select files", command=select_files)
    select_files_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    clear_files_button = ttk.Button(root, text="Clear file list", command=clear_file_list)
    clear_files_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    generate_button = ttk.Button(root, text="Start Watermarker", command=start_watermarker)
    generate_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    update_user_list()

    root.mainloop()
