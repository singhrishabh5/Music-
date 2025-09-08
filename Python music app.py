import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.font as font
import pygame
from PIL import Image, ImageTk
import sqlite3
import hashlib
import os
import random

class RhythmBells:

    def __init__(self, root):

        self.root = root

        self.root.withdraw()  # Hide main window until login

        

        # Initialize pygame mixer

        pygame.mixer.init()

        

        # Database setup

        self.conn = sqlite3.connect('music_app.db')

        self.c = self.conn.cursor()

        self.create_database()

        

        # App state

        self.playlist = []

        self.current_song = 0

        self.paused = False

        self.shuffle = False

        self.repeat = False

        self.original_playlist = []

        

        # Custom fonts

        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")

        self.button_font = font.Font(family="Helvetica", size=12)

        self.song_font = font.Font(family="Helvetica", size=10)

        

        # Setup login page

        self.setup_login_page()

    

    def create_database(self):

        """Initialize the database tables"""

        self.c.execute('''CREATE TABLE IF NOT EXISTS users

                         (username TEXT PRIMARY KEY, password TEXT)''')

        self.conn.commit()

    

    def center_window(self, window, width, height):

        """Center a window on screen"""

        screen_width = window.winfo_screenwidth()

        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2

        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    

    def setup_login_page(self):

        """Create the centered login window with larger elements"""

        self.login_window = tk.Toplevel(self.root)

        self.login_window.title("Rhythm Bells - Login")

        self.login_window.configure(bg='black')

        self.center_window(self.login_window, 500, 400)

        

        # Main container frame for centering

        container = tk.Frame(self.login_window, bg='black')

        container.place(relx=0.5, rely=0.5, anchor='center')

        

        # Logo/Title

        tk.Label(container, text="♫ RhythmBells ♫", fg='red', bg='black', 

                font=self.title_font).pack(pady=(0, 30))

        

        # Username Frame

        user_frame = tk.Frame(container, bg='black')

        user_frame.pack(fill='x', pady=5)

        tk.Label(user_frame, text="Username:", fg='red', bg='black', 

                font=self.button_font).pack(side='left', padx=5)

        self.username_entry = tk.Entry(user_frame, font=self.button_font, width=25)

        self.username_entry.pack(side='right')

        

        # Password Frame

        pass_frame = tk.Frame(container, bg='black')

        pass_frame.pack(fill='x', pady=5)

        tk.Label(pass_frame, text="Password:", fg='red', bg='black',

                font=self.button_font).pack(side='left', padx=5)

        self.password_entry = tk.Entry(pass_frame, show='*', font=self.button_font, width=25)

        self.password_entry.pack(side='right')

        

        # Button Frame

        btn_frame = tk.Frame(container, bg='black')

        btn_frame.pack(pady=20)

        

        # Login Button (larger)

        tk.Button(btn_frame, text="Login", command=self.check_login,

                 bg='red', fg='black', font=self.button_font,

                 width=15, height=1).pack(side='left', padx=10)

        

        # Register Button (larger)

        tk.Button(btn_frame, text="Register", command=self.show_register,

                 bg='black', fg='red', font=self.button_font,

                 width=15, height=1).pack(side='left', padx=10)



    def show_register(self):

        """Show centered registration window"""

        self.register_window = tk.Toplevel(self.login_window)

        self.register_window.title("Register")

        self.register_window.configure(bg='black')

        self.center_window(self.register_window, 500, 400)

        

        container = tk.Frame(self.register_window, bg='black')

        container.place(relx=0.5, rely=0.5, anchor='center')

        

        tk.Label(container, text="Register New Account", fg='red', bg='black',

                font=self.title_font).pack(pady=(0, 30))

        

        # Username Frame

        user_frame = tk.Frame(container, bg='black')

        user_frame.pack(fill='x', pady=10)

        tk.Label(user_frame, text="Username:", fg='red', bg='black',

                font=self.button_font).pack(side='left', padx=5)

        self.new_username = tk.Entry(user_frame, font=self.button_font, width=25)

        self.new_username.pack(side='right')

        

        # Password Frame

        pass_frame = tk.Frame(container, bg='black')

        pass_frame.pack(fill='x', pady=10)

        tk.Label(pass_frame, text="Password:", fg='red', bg='black',

                font=self.button_font).pack(side='left', padx=5)

        self.new_password = tk.Entry(pass_frame, show='*', font=self.button_font, width=25)

        self.new_password.pack(side='right')

        

        # Register Button (centered)

        tk.Button(container, text="Register", command=self.register_user,

                 bg='red', fg='black', font=self.button_font,

                 width=15, height=1).pack(pady=20)



    def register_user(self):

        """Handle user registration"""

        username = self.new_username.get()

        password = self.new_password.get()

        

        if not username or not password:

            messagebox.showerror("Error", "Username and password cannot be empty!")

            return

        

        # Hash the password

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        

        try:

            self.c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))

            self.conn.commit()

            messagebox.showinfo("Success", "Registration successful!")

            self.register_window.destroy()

        except sqlite3.IntegrityError:

            messagebox.showerror("Error", "Username already exists!")



    def check_login(self):

        """Handle user login"""

        username = self.username_entry.get()

        password = self.password_entry.get()

        

        if not username or not password:

            messagebox.showerror("Error", "Please enter both username and password")

            return

        

        # Hash the input password

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        

        # Check credentials

        self.c.execute("SELECT * FROM users WHERE username=? AND password=?", 

                      (username, hashed_password))

        if self.c.fetchone():

            self.login_window.destroy()

            self.setup_main_app()

        else:

            messagebox.showerror("Error", "Invalid username or password")



    def setup_main_app(self):

        """Setup the main music player window with enhanced UI"""

        self.root.deiconify()

        self.root.title("RhythmBells")

        self.root.configure(bg='black')

        self.center_window(self.root, 900, 650)

        

        # Main container with RhythmBells branding

        main_container = tk.Frame(self.root, bg='black')

        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        

        # Header with RhythmBells title

        header = tk.Frame(main_container, bg='black')

        header.pack(fill='x', pady=(0, 20))

        

        tk.Label(header, text="♫ RhythmBells ♫", fg='red', bg='black',

                font=self.title_font).pack(side='left')

        

        # Navigation buttons with upgraded style

        nav_frame = tk.Frame(header, bg='black')

        nav_frame.pack(side='right')

        

        nav_buttons = [

            ("🎵 Favorites", lambda: self.show_category("favorites")),

            ("📋 Playlist", lambda: self.show_category("playlist")),

            ("🕒 Recent", lambda: self.show_category("recent"))

        ]

        

        for text, cmd in nav_buttons:

            tk.Button(nav_frame, text=text, command=cmd,

                     bg='black', fg='red', font=self.button_font,

                     bd=0, activebackground='#333', activeforeground='red').pack(side='left', padx=5)

        

        # Load Music button with better styling

        tk.Button(header, text="➕ Load Music", command=self.load_music,

                 bg='red', fg='black', font=self.button_font,

                 bd=0, activebackground='darkred').pack(side='right', padx=10)

        

        # Song list with upgraded style

        middle_frame = tk.Frame(main_container, bg='black')

        middle_frame.pack(fill='both', expand=True)

        

        # Custom style for treeview

        style = ttk.Style()

        style.theme_use('clam')

        style.configure("Treeview", 

                       background="black", 

                       foreground="red",

                       fieldbackground="black",

                       font=self.song_font)

        style.configure("Treeview.Heading", 

                       background="red", 

                       foreground="black",

                       font=self.button_font)

        style.map('Treeview', background=[('selected', 'red')], foreground=[('selected', 'black')])

        

        self.song_list = ttk.Treeview(middle_frame, columns=('Artist', 'Album', 'Duration'), 

                                    show='headings', selectmode='browse', height=15)

        

        # Configure columns

        self.song_list.heading('#0', text='Song', anchor='w')

        self.song_list.heading('Artist', text='Artist', anchor='w')

        self.song_list.heading('Album', text='Album', anchor='w')

        self.song_list.heading('Duration', text='Duration', anchor='w')

        

        self.song_list.column('#0', width=250, stretch=False)

        self.song_list.column('Artist', width=150, stretch=False)

        self.song_list.column('Album', width=150, stretch=False)

        self.song_list.column('Duration', width=80, stretch=False)

        

        scrollbar = ttk.Scrollbar(middle_frame, orient="vertical", command=self.song_list.yview)

        self.song_list.configure(yscrollcommand=scrollbar.set)

        

        self.song_list.pack(side='left', fill='both', expand=True)

        scrollbar.pack(side='right', fill='y')

        

        # Bottom controls with upgraded style

        self.create_bottom_bar(main_container)

        

        # Load default playlist if any

        self.load_default_playlist()



    def show_category(self, category):

        """Placeholder for category display"""

        messagebox.showinfo("Info", f"Showing {category} - this would filter songs in a full implementation")



    def create_bottom_bar(self, parent):

        """Create the bottom control bar with modern styling"""

        bottom_frame = tk.Frame(parent, bg='black')

        bottom_frame.pack(fill='x', pady=(20, 0))

        

        # Progress bar (modern line style)

        self.progress_canvas = tk.Canvas(bottom_frame, bg='black', height=4, highlightthickness=0)

        self.progress_canvas.pack(fill='x', padx=20, pady=5)

        self.progress_line = self.progress_canvas.create_line(0, 2, 0, 2, fill='red', width=4)

        

        # Controls frame

        controls_frame = tk.Frame(bottom_frame, bg='black')

        controls_frame.pack()

        

        # Control buttons with hover effects

        control_buttons = [

            ("⏮", self.prev_song),

            ("⏯", self.toggle_play),

            ("⏭", self.next_song),

            ("🔀", self.toggle_shuffle),

            ("🔁", self.toggle_repeat)

        ]

        

        for text, cmd in control_buttons:

            btn = tk.Button(controls_frame, text=text, command=cmd,

                          bg='black', fg='red', font=('Arial', 16),

                          bd=0, activebackground='#333', activeforeground='red')

            btn.pack(side='left', padx=10)

            

            # Special styling for play/pause button

            if text == "⏯":

                self.play_button = btn

        

        # Volume control with icon

        vol_frame = tk.Frame(bottom_frame, bg='black')

        vol_frame.pack(side='right', padx=20)

        

        tk.Label(vol_frame, text="🔈", bg='black', fg='red').pack(side='left')

        self.volume = ttk.Scale(vol_frame, from_=0, to=100, 

                               command=self.set_volume, orient='horizontal',

                               style='red.Horizontal.TScale')

        

        # Custom style for volume slider

        style = ttk.Style()

        style.theme_use('clam')

        style.configure("red.Horizontal.TScale", 

                       background='black',

                       troughcolor='#333',

                       slidercolor='red',

                       bordercolor='black',

                       lightcolor='black',

                       darkcolor='black')

        

        self.volume.set(70)

        self.volume.pack(side='right')



    def load_default_playlist(self):

        """Load the default playlist from file"""

        if os.path.exists("default_playlist.txt"):

            with open("default_playlist.txt", "r") as f:

                self.playlist = [line.strip() for line in f.readlines() if os.path.exists(line.strip())]

                for song in self.playlist:

                    self.song_list.insert('', 'end', text=os.path.basename(song), 

                                        values=('Unknown Artist', 'Unknown Album', '0:00'))



    def load_music(self):

        """Load music files into the playlist"""

        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])

        for file in files:

            self.playlist.append(file)

            song_name = os.path.basename(file)

            self.song_list.insert('', 'end', text=song_name, 

                                values=('Unknown Artist', 'Unknown Album', '0:00'))

        

        # Save to default playlist

        with open("default_playlist.txt", "w") as f:

            f.write("\n".join(self.playlist))



    def toggle_play(self):

        """Toggle play/pause state"""

        if not self.playlist:

            return

            

        if self.paused:

            pygame.mixer.music.unpause()

            self.paused = False

            self.play_button.config(text="⏸")

        elif pygame.mixer.music.get_busy():

            pygame.mixer.music.pause()

            self.paused = True

            self.play_button.config(text="⏯")

        else:

            self.play_music()

            self.play_button.config(text="⏸")



    def play_music(self):

        """Play the current song"""

        try:

            pygame.mixer.music.load(self.playlist[self.current_song])

            pygame.mixer.music.play()

            self.update_progress()

            self.paused = False

            

            # Handle song end event

            pygame.mixer.music.set_endevent(pygame.USEREVENT)

            self.root.bind(pygame.USEREVENT, self.song_ended)

        except Exception as e:

            messagebox.showerror("Error", f"Could not play file: {str(e)}")



    def song_ended(self, event):

        """Handle when a song finishes playing"""

        if self.repeat:

            self.play_music()

        else:

            self.next_song()



    def update_progress(self):

        """Update the progress bar"""

        if pygame.mixer.music.get_busy():

            current_time = pygame.mixer.music.get_pos() / 1000

            song_length = 180  # Default 3 minutes (replace with actual length)

            

            # Update progress line

            canvas_width = self.progress_canvas.winfo_width()

            progress = (current_time / song_length) * canvas_width

            self.progress_canvas.coords(self.progress_line, 0, 2, progress, 2)

            

            self.root.after(100, self.update_progress)



    def set_volume(self, val):

        """Set the playback volume"""

        volume = float(val) / 100

        pygame.mixer.music.set_volume(volume)



    def toggle_shuffle(self):

        """Toggle shuffle mode"""

        self.shuffle = not self.shuffle

        # Update button color

        for widget in self.root.winfo_children():

            if isinstance(widget, tk.Button) and widget['text'] == "🔀":

                widget.config(fg='white' if self.shuffle else 'red')

        

        if self.shuffle:

            self.original_playlist = self.playlist.copy()

            random.shuffle(self.playlist)

        elif hasattr(self, 'original_playlist'):

            self.playlist = self.original_playlist.copy()



    def toggle_repeat(self):

        """Toggle repeat mode"""

        self.repeat = not self.repeat

        # Update button color

        for widget in self.root.winfo_children():

            if isinstance(widget, tk.Button) and widget['text'] == "🔁":

                widget.config(fg='white' if self.repeat else 'red')



    def next_song(self):

        """Play the next song in playlist"""

        if not self.playlist:

            return

            

        self.current_song = (self.current_song + 1) % len(self.playlist)

        self.play_music()



    def prev_song(self):

        """Play the previous song in playlist"""

        if not self.playlist:

            return

            

        self.current_song = (self.current_song - 1) % len(self.playlist)

        self.play_music()



if __name__ == "__main__":

    root = tk.Tk()

    app = RhythmBells(root)

    root.mainloop()