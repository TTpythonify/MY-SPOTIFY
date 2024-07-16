import tkinter as tk
from tkinter import ttk
import os
import random
import threading
import pygame

FOLDER_PATH = "Songs"

# If the folder exists 
if os.path.exists(FOLDER_PATH):
    MY_SONGS = os.listdir(FOLDER_PATH)
else:
    MY_SONGS = []


class Spotify(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Spotify")
        self.geometry("800x350")

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.init()

        # Configure style "Got this from online"
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#E1D7C3')
        self.style.configure('TButton', background='#5E503F', foreground='black', borderwidth=0, relief="flat", font=('Arial', 14))
        self.style.map('TButton', background=[('active', '#786D5F')]) 
        self.style.configure('TLabel', background='#E1D7C3', foreground='#5E503F', font=('Arial', 12))
        self.style.configure('TEntry', background='white', foreground='#5E503F', font=('Arial', 14))
        self.style.configure('TText', background='white', foreground='#5E503F', font=('Arial', 12))
        self.style.configure('Vertical.TScrollbar', background='#5E503F')

        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create left frame for the display area
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True)

        # Create right frame for buttons and entry
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="y")

        # Entry widget and Search button frame
        self.entry_frame = ttk.Frame(self.right_frame)
        self.entry_frame.pack(pady=20, padx=20)

        self.entry = ttk.Entry(master=self.entry_frame, width=20, font=('Arial', 14))
        self.entry.pack(side="left", padx=(0, 10))

        self.search_button = ttk.Button(master=self.entry_frame, text="Search Song", command=self.search_song, width=15)
        self.search_button.pack(side="left")

        # Buttons
        self.shuffle_button = ttk.Button(master=self.right_frame, text="Shuffle", command=self.shuffle_songs, width=15)
        self.shuffle_button.pack(pady=10, padx=20)

        self.playlist_button = ttk.Button(master=self.right_frame, text="Playlist", command=self.view_songs, width=15)
        self.playlist_button.pack(pady=10, padx=20)

        self.play_songs_button = ttk.Button(master=self.right_frame, text="Play", command=self.play_songs, width=15)
        self.play_songs_button.pack(pady=10, padx=20)

        # Display area for song list and scrollbar
        self.display_songs_text = tk.Text(master=self.left_frame, wrap="none", width=40)
        self.display_songs_text.pack(pady=20, padx=20, fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(master=self.left_frame, command=self.display_songs_text.yview, style='Vertical.TScrollbar')
        self.scrollbar.pack(side="right", fill="y")

        self.display_songs_text.configure(yscrollcommand=self.scrollbar.set)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    # Search for a song
    def search_song(self):
        # Clear display area
        self.display_songs_text.delete("1.0", tk.END)

        user_entry = self.entry.get().lower()
        # Used list comprehension to search for songs
        searched_songs = [s for s in MY_SONGS if user_entry in s.lower()]

        # Convert each song to a button
        if searched_songs:
            for song in searched_songs:
                button = ttk.Button(
                    master=self.display_songs_text,
                    text=song,
                    command=lambda s=song: self.play_selected_song(s),
                    width=25,
                    style='TButton'
                )
                self.display_songs_text.window_create(tk.END, window=button)
                self.display_songs_text.insert(tk.END, "\n")
        else:
            self.display_songs_text.insert(tk.END, "Song not found")

        # Update scrollbar and text widget
        self.display_songs_text.update_idletasks()
        self.scrollbar.update_idletasks()
        self.display_songs_text.yview_moveto(0.0)


    # Shuffle the playlist
    def shuffle_songs(self):
        random.shuffle(MY_SONGS)  # Shuffle the songs

        self.display_songs_text.delete("1.0", tk.END) # Clear display area

        # Convert songs to buttons
        for song in MY_SONGS:
            button = ttk.Button(
                master=self.display_songs_text,
                text=song,
                command=lambda s=song: self.play_selected_song(s),
                width=25,
                style='TButton'
            )
            self.display_songs_text.window_create(tk.END, window=button)
            self.display_songs_text.insert(tk.END, "\n") 

        # Update scrollbar and text widget
        self.display_songs_text.update_idletasks()
        self.scrollbar.update_idletasks()
        self.display_songs_text.yview_moveto(0.0)  # Scroll to top

    # View songs in my playlist
    def view_songs(self):
        try:
            # Clear the display area
            self.display_songs_text.delete("1.0", tk.END)

            # Convert songs to buttons
            for song in MY_SONGS:
                button = ttk.Button(
                    master=self.display_songs_text,
                    text=song,
                    command=lambda s=song: self.play_selected_song(s),
                    width=25,
                    style='TButton'
                )
                self.display_songs_text.window_create(tk.END, window=button)
                self.display_songs_text.insert(tk.END, "\n") 

            # Update scrollbar and text widget
            self.display_songs_text.update_idletasks()
            self.scrollbar.update_idletasks()
            self.display_songs_text.yview_moveto(0.0)  # Scroll to top

        except Exception as e:
            print(f"Error while displaying songs: {e}")


    # Play songs in order displayed on the screen
    def play_songs(self):
        button_names = []

        # Collect song names from the buttons and construct their file paths
        for button in self.display_songs_text.winfo_children():
            song = button.cget("text")
            button_names.append(os.path.join(FOLDER_PATH, song))

        def play_next_song(song_paths):
            if song_paths:
                song_path = song_paths.pop(0)
                try:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()  # Stop the current song if one is playing
                    pygame.mixer.music.load(song_path)  # Load the new song
                    pygame.mixer.music.play()  # Play the new song
                    print(f"Playing: {song_path}")  # Debug purposes

                    # Set the end event to detect when the song finishes
                    pygame.mixer.music.set_endevent(pygame.USEREVENT)
                    # Schedule the check_event function to run after 100 milliseconds
                    self.after(100, check_event, song_paths)

                except Exception as e:
                    print(f"Error playing {song_path}: {e}")

        def check_event(song_paths):
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    play_next_song(song_paths)

            # Schedule the check_event function to run again
            self.after(100, check_event, song_paths)

        # Start playing the songs in a separate thread
        threading.Thread(target=play_next_song, args=(button_names,)).start()

    # Play the song that user selected
    def play_selected_song(self, song):
        song_path = os.path.join(FOLDER_PATH, song)

        def play():
            try:
                # Stop the current song if one is playing
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()

                pygame.mixer.music.load(song_path)  # Load the new song
                pygame.mixer.music.play()  # Play the new song

            except Exception as e:
                print(f"Error playing {song}: {e}")

        # Run the play function in a separate thread
        threading.Thread(target=play).start()

    def on_closing(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.destroy()

if __name__ == "__main__":
    app = Spotify()
    app.mainloop()