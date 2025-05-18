import tkinter as tk
from tkinter import ttk, messagebox
import uuid
import logging
import random
import hashlib
import sys

# Loglama ayarları
logging.basicConfig(filename='game_app.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Game:
    def __init__(self, name: str, genre: str, platform: str, game_id: str = None):
        try:
            self.game_id = game_id or str(uuid.uuid4())
            self.name = name
            self.genre = genre
            self.platform = platform
            self.ratings = []
            self.comments = []
            logging.info(f"Oyun oluşturuldu: {self.name}")
        except Exception as e:
            logging.error(f"Oyun oluşturma hatası: {str(e)}")
            raise

    def add_rating(self, rating: float):
        try:
            if 0 <= rating <= 5:
                self.ratings.append(rating)
            else:
                raise ValueError("Puan 0-5 arasında olmalı, kanka!")
        except Exception as e:
            logging.error(f"Puan ekleme hatası: {str(e)}")
            raise

    def add_comment(self, comment: str):
        try:
            self.comments.append(comment)
        except Exception as e:
            logging.error(f"Yorum ekleme hatası: {str(e)}")
            raise

    def get_average_rating(self):
        try:
            return sum(self.ratings) / len(self.ratings) if self.ratings else 0.0
        except Exception as e:
            logging.error(f"Ortalama puan hatası: {str(e)}")
            return 0.0

class Player:
    def __init__(self):
        try:
            self.collection = {}
            self.favorites = []
            logging.info("Oyuncu oluşturuldu")
        except Exception as e:
            logging.error(f"Oyuncu oluşturma hatası: {str(e)}")
            raise

    def add_to_collection(self, game: 'Game'):
        try:
            if game.game_id not in self.collection:
                self.collection[game.game_id] = game
                logging.info(f"Koleksiyona eklendi: {game.name}")
                return True
            logging.info(f"Oyun zaten koleksiyonda: {game.name}")
            return False
        except Exception as e:
            logging.error(f"Koleksiyona ekleme hatası: {str(e)}")
            raise

    def rate_game(self, game_id: str, rating: float):
        try:
            if game_id in self.collection:
                self.collection[game_id].add_rating(rating)
            else:
                raise ValueError("Oyun koleksiyonda değil!")
        except Exception as e:
            logging.error(f"Puanlama hatası: {str(e)}")
            raise

    def comment_game(self, game_id: str, comment: str):
        try:
            if game_id in self.collection:
                self.collection[game_id].add_comment(comment)
            else:
                raise ValueError("Oyun koleksiyonda değil!")
        except Exception as e:
            logging.error(f"Yorum yapma hatası: {str(e)}")
            raise

    def add_favorite(self, game_id: str):
        try:
            if game_id in self.collection and game_id not in self.favorites:
                self.favorites.append(game_id)
            else:
                raise ValueError("Oyun koleksiyonda değil veya zaten favorilerde!")
        except Exception as e:
            logging.error(f"Favorilere ekleme hatası: {str(e)}")
            raise

    def get_recommendations(self, all_games):
        try:
            if not self.favorites:
                return random.sample(all_games, min(3, len(all_games)))  # Rastgele 3 oyun
            favorite_genres = {self.collection[game_id].genre for game_id in self.favorites}
            favorite_platforms = {self.collection[game_id].platform for game_id in self.favorites}
            recommendations = [
                game for game in all_games
                if game.game_id not in self.collection
                and (game.genre in favorite_genres or game.platform in favorite_platforms)
            ]
            return sorted(recommendations, key=lambda x: x.get_average_rating(), reverse=True)[:3]
        except Exception as e:
            logging.error(f"Öneri alma hatası: {str(e)}")
            return random.sample(all_games, min(3, len(all_games)))

class LoginApp:
    def __init__(self, root, on_login_success):
        try:
            self.root = root
            self.on_login_success = on_login_success
            self.root.title("Gamer Arena - Giriş")
            self.root.geometry("400x300")
            self.root.configure(bg="#12032b")  # Neon morumsu arka plan
            logging.info("Giriş ekranı başlatılıyor")

            # Kullanıcılar bellekte saklanacak
            self.users = {}  # {username: hashed_password}

            # Stil
            style = ttk.Style()
            style.configure("TButton", padding=8, font=("Arial", 12, "bold"), background="#ffcc00", foreground="#000000")
            style.map("TButton",
                      background=[("active", "#00ff00")],  # Hover neon yeşil
                      foreground=[("active", "#000000")])
            style.configure("TLabel", background="#12032b", foreground="#00ffcc", font=("Arial", 11, "bold"))
            style.configure("TEntry", padding=5, font=("Arial", 11))

            # Ana çerçeve
            self.main_frame = tk.Frame(self.root, bg="#12032b")
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

            # Başlık
            tk.Label(self.main_frame, text="🎮 Gamer Arena", font=("Arial", 24, "bold"), bg="#12032b", fg="#ff0066").pack(pady=10)

            # Sekmeler
            self.notebook = ttk.Notebook(self.main_frame)
            self.notebook.pack(fill=tk.BOTH, expand=True)

            # Giriş sekmesi
            self.login_frame = tk.Frame(self.notebook, bg="#12032b")
            self.notebook.add(self.login_frame, text="Giriş Yap")
            tk.Label(self.login_frame, text="Kullanıcı Adı:", bg="#12032b", fg="#00ffcc").pack(pady=5)
            self.login_username_var = tk.StringVar()
            tk.Entry(self.login_frame, textvariable=self.login_username_var, font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(pady=5)
            tk.Label(self.login_frame, text="Şifre:", bg="#12032b", fg="#00ffcc").pack(pady=5)
            self.login_password_var = tk.StringVar()
            tk.Entry(self.login_frame, textvariable=self.login_password_var, show="*", font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(pady=5)
            ttk.Button(self.login_frame, text="Giriş Yap", command=self.login).pack(pady=10)

            # Kayıt sekmesi
            self.register_frame = tk.Frame(self.notebook, bg="#12032b")
            self.notebook.add(self.register_frame, text="Kayıt Ol")
            tk.Label(self.register_frame, text="Kullanıcı Adı:", bg="#12032b", fg="#00ffcc").pack(pady=5)
            self.register_username_var = tk.StringVar()
            tk.Entry(self.register_frame, textvariable=self.register_username_var, font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(pady=5)
            tk.Label(self.register_frame, text="Şifre:", bg="#12032b", fg="#00ffcc").pack(pady=5)
            self.register_password_var = tk.StringVar()
            tk.Entry(self.register_frame, textvariable=self.register_password_var, show="*", font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(pady=5)
            ttk.Button(self.register_frame, text="Kayıt Ol", command=self.register).pack(pady=10)

            logging.info("Giriş ekranı arayüzü yüklendi")
        except Exception as e:
            logging.error(f"Giriş ekranı başlatma hatası: {str(e)}")
            messagebox.showerror("Hata", f"Oops! Giriş ekranı açılamadı, kanka: {str(e)}")
            self.root.destroy()
            sys.exit(1)

    def login(self):
        try:
            username = self.login_username_var.get()
            password = self.login_password_var.get()
            if not username or not password:
                raise ValueError("Kanka, kullanıcı adı ve şifreyi doldur!")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if username in self.users and self.users[username] == hashed_password:
                messagebox.showinfo("Başarılı", f"Hoş geldin, {username}! Hadi oyunlara dalalım!")
                logging.info(f"Giriş başarılı: {username}")
                self.on_login_success(username)
            else:
                raise ValueError("Kanka, kullanıcı adı veya şifre yanlış!")
        except Exception as e:
            logging.error(f"Giriş hatası: {str(e)}")
            messagebox.showerror("Hata", str(e))

    def register(self):
        try:
            username = self.register_username_var.get()
            password = self.register_password_var.get()
            if not username or not password:
                raise ValueError("Kanka, kullanıcı adı ve şifreyi doldur!")
            if username in self.users:
                raise ValueError("Bu kullanıcı adı zaten var, başka bir tane seç!")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.users[username] = hashed_password
            messagebox.showinfo("Başarılı", f"Kayıt oldun, {username}! Şimdi giriş yap!")
            logging.info(f"Kayıt başarılı: {username}")
            self.notebook.select(self.login_frame)  # Giriş sekmesine geç
        except Exception as e:
            logging.error(f"Kayıt hatası: {str(e)}")
            messagebox.showerror("Hata", str(e))

class GameApp:
    def __init__(self, root, username):
        try:
            self.root = root
            self.username = username
            self.root.title("Gamer Arena")
            self.root.geometry("750x600")
            self.root.configure(bg="#12032b")  # Neon morumsu arka plan
            logging.info(f"Uygulama başlatılıyor: {username}")

            self.player = Player()
            self.all_games = self.preload_games()

            # Stil
            style = ttk.Style()
            style.configure("TButton", padding=8, font=("Arial", 12, "bold"), background="#ffcc00", foreground="#000000")
            style.map("TButton",
                      background=[("active", "#00ff00")],  # Hover neon yeşil
                      foreground=[("active", "#000000")])
            style.configure("TLabel", background="#12032b", foreground="#00ffcc", font=("Arial", 11, "bold"))
            style.configure("TEntry", padding=5, font=("Arial", 11))
            style.configure("Treeview", background="#1a0b3d", foreground="#00ffcc", fieldbackground="#1a0b3d", font=("Arial", 11))
            style.map("Treeview", background=[("selected", "#ff0066")])

            # Ana çerçeve
            self.main_frame = tk.Frame(self.root, bg="#12032b")
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

            # Başlık
            tk.Label(self.main_frame, text=f"🎮 Gamer Arena - {username}", font=("Arial", 24, "bold"), bg="#12032b", fg="#ff0066").pack(pady=10)

            # Önerilen oyunlar
            tk.Label(self.main_frame, text="🔥 Sana Özel Öneriler", font=("Arial", 16, "bold"), bg="#12032b", fg="#ffcc00").pack(anchor="w", pady=5)
            self.recommend_frame = tk.Frame(self.main_frame, bg="#12032b")
            self.recommend_frame.pack(fill=tk.X, pady=5)
            self.recommend_labels = []
            for i in range(3):
                lbl = tk.Label(self.recommend_frame, text="", font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", relief="ridge", padx=8, pady=5)
                lbl.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
                self.recommend_labels.append(lbl)

            # Arama ve filtreleme
            search_frame = tk.Frame(self.main_frame, bg="#12032b")
            search_frame.pack(fill=tk.X, pady=10)
            tk.Label(search_frame, text="🔍 Oyun Ara:", bg="#12032b", fg="#00ffcc").pack(side=tk.LEFT, padx=5)
            self.search_var = tk.StringVar()
            tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            filter_frame = tk.Frame(self.main_frame, bg="#12032b")
            filter_frame.pack(fill=tk.X, pady=5)
            tk.Label(filter_frame, text="🎮 Tür:", bg="#12032b", fg="#00ffcc").pack(side=tk.LEFT, padx=5)
            self.genre_var = tk.StringVar()
            tk.Entry(filter_frame, textvariable=self.genre_var, width=15, font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(side=tk.LEFT, padx=5)
            tk.Label(filter_frame, text="🖱️ Platform:", bg="#12032b", fg="#00ffcc").pack(side=tk.LEFT, padx=5)
            self.platform_var = tk.StringVar()
            tk.Entry(filter_frame, textvariable=self.platform_var, width=15, font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(side=tk.LEFT, padx=5)
            ttk.Button(filter_frame, text="Filtrele", command=self.show_games).pack(side=tk.LEFT, padx=5)

            # Sekmeler
            self.notebook = ttk.Notebook(self.main_frame)
            self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)

            # Koleksiyon sekmesi
            self.collection_frame = tk.Frame(self.notebook, bg="#12032b")
            self.notebook.add(self.collection_frame, text="🎲 Koleksiyonum")
            self.collection_tree = ttk.Treeview(self.collection_frame, columns=("Name", "Genre", "Platform", "Rating"), show="headings")
            self.collection_tree.heading("Name", text="Oyun")
            self.collection_tree.heading("Genre", text="Tür")
            self.collection_tree.heading("Platform", text="Platform")
            self.collection_tree.heading("Rating", text="Puan")
            self.collection_tree.column("Name", width=200)
            self.collection_tree.column("Genre", width=100)
            self.collection_tree.column("Platform", width=100)
            self.collection_tree.column("Rating", width=80)
            self.collection_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.collection_tree.bind("<<TreeviewSelect>>", self.on_collection_select)

            # Tüm oyunlar sekmesi
            self.all_games_frame = tk.Frame(self.notebook, bg="#12032b")
            self.notebook.add(self.all_games_frame, text="🕹️ Tüm Oyunlar")
            self.game_tree = ttk.Treeview(self.all_games_frame, columns=("Name", "Genre", "Platform", "Rating"), show="headings")
            self.game_tree.heading("Name", text="Oyun")
            self.game_tree.heading("Genre", text="Tür")
            self.game_tree.heading("Platform", text="Platform")
            self.game_tree.heading("Rating", text="Puan")
            self.game_tree.column("Name", width=200)
            self.game_tree.column("Genre", width=100)
            self.game_tree.column("Platform", width=100)
            self.game_tree.column("Rating", width=80)
            self.game_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.game_tree.bind("<<TreeviewSelect>>", self.on_game_select)

            # Butonlar
            button_frame = tk.Frame(self.main_frame, bg="#12032b")
            button_frame.pack(fill=tk.X, pady=10)
            ttk.Button(button_frame, text="Yeni Oyun", command=self.add_game_window).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Koleksiyona Ekle", command=self.add_to_collection).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Puan Ver", command=self.rate_game).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Yorum Yap", command=self.comment_game).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Favori Yap", command=self.add_favorite).pack(side=tk.LEFT, padx=5)

            # Yorumlar
            tk.Label(self.main_frame, text="💬 Yorumlar:", bg="#12032b", fg="#00ffcc").pack(anchor="w", pady=5)
            self.comments_text = tk.Text(self.main_frame, height=4, bg="#1a0b3d", fg="#00ffcc", font=("Arial", 11))
            self.comments_text.pack(fill=tk.X, pady=5)
            self.comments_text.config(state="disabled")

            self.show_games()
            self.show_collection()
            self.update_recommendations()
            logging.info("Uygulama arayüzü yüklendi")
        except Exception as e:
            logging.error(f"Uygulama başlatma hatası: {str(e)}")
            messagebox.showerror("Hata", f"Oops! Bir şeyler ters gitti, kanka: {str(e)}")
            self.root.destroy()

    def preload_games(self):
        try:
            predefined_games = [
                Game("The Witcher 3: Wild Hunt", "RPG", "PC"),
                Game("Grand Theft Auto V", "Action", "PS4"),
                Game("Elden Ring", "RPG", "PS5"),
                Game("Cyberpunk 2077", "RPG", "PC"),
                Game("Super Mario Odyssey", "Platformer", "Switch"),
                Game("Red Dead Redemption 2", "Action", "Xbox One"),
                Game("The Legend of Zelda: Breath of the Wild", "Adventure", "Switch"),
                Game("God of War", "Action", "PS4"),
                Game("Hollow Knight", "Metroidvania", "PC"),
                Game("Dark Souls III", "RPG", "PS4"),
                Game("Horizon Zero Dawn", "Action", "PS4"),
                Game("The Elder Scrolls V: Skyrim", "RPG", "PC"),
                Game("Among Us", "Party", "PC"),
                Game("Animal Crossing: New Horizons", "Simulation", "Switch"),
                Game("DOOM Eternal", "FPS", "PC"),
                Game("Final Fantasy VII Remake", "RPG", "PS4"),
                Game("Hades", "Rogue-like", "PC"),
                Game("The Last of Us Part II", "Action", "PS4"),
                Game("Portal 2", "Puzzle", "PC"),
                Game("Stardew Valley", "Simulation", "PC")
            ]
            logging.info("20 oyun yüklendi")
            return predefined_games
        except Exception as e:
            logging.error(f"Oyun yükleme hatası: {str(e)}")
            return []

    def show_games(self):
        try:
            for item in self.game_tree.get_children():
                self.game_tree.delete(item)
            games = self.all_games
            search = self.search_var.get().lower()
            genre = self.genre_var.get().lower()
            platform = self.platform_var.get().lower()
            for game in games:
                if (search in game.name.lower() and
                    (not genre or genre in game.genre.lower()) and
                    (not platform or platform in game.platform.lower())):
                    self.game_tree.insert("", tk.END, values=(
                        game.name,
                        game.genre,
                        game.platform,
                        f"{game.get_average_rating():.1f}"
                    ), tags=(game.game_id,))
            logging.info("Oyunlar gösterildi")
        except Exception as e:
            logging.error(f"Oyunları gösterme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Oyunlar yüklenemedi: {str(e)}")

    def show_collection(self):
        try:
            for item in self.collection_tree.get_children():
                self.collection_tree.delete(item)
            for game in self.player.collection.values():
                self.collection_tree.insert("", tk.END, values=(
                    game.name,
                    game.genre,
                    game.platform,
                    f"{game.get_average_rating():.1f}"
                ), tags=(game.game_id,))
            logging.info("Koleksiyon gösterildi")
        except Exception as e:
            logging.error(f"Koleksiyon gösterme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Koleksiyon yüklenemedi: {str(e)}")

    def update_recommendations(self):
        try:
            recommendations = self.player.get_recommendations(self.all_games)
            for lbl, game in zip(self.recommend_labels, recommendations + [None] * (3 - len(recommendations))):
                if game:
                    lbl.config(text=f"{game.name} ({game.genre}, {game.platform})")
                else:
                    lbl.config(text="")
            logging.info("Öneriler güncellendi")
        except Exception as e:
            logging.error(f"Öneri güncelleme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Öneriler yüklenemedi: {str(e)}")

    def add_game_window(self):
        try:
            window = tk.Toplevel(self.root)
            window.title("Yeni Oyun Ekle")
            window.geometry("300x200")
            window.configure(bg="#12032b")
            tk.Label(window, text="Oyun Adı:", bg="#12032b", fg="#00ffcc", font=("Arial", 11)).pack(pady=5)
            name_var = tk.StringVar()
            tk.Entry(window, textvariable=name_var, font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(pady=5)
            tk.Label(window, text="Tür:", bg="#12032b", fg="#00ffcc", font=("Arial", 11)).pack(pady=5)
            genre_var = tk.StringVar()
            tk.Entry(window, textvariable=genre_var, font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(pady=5)
            tk.Label(window, text="Platform:", bg="#12032b", fg="#00ffcc", font=("Arial", 11)).pack(pady=5)
            platform_var = tk.StringVar()
            tk.Entry(window, textvariable=platform_var, font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(pady=5)
            def submit():
                try:
                    if not all([name_var.get(), genre_var.get(), platform_var.get()]):
                        raise ValueError("Hepsini doldur, kanka!")
                    game = Game(name_var.get(), genre_var.get(), platform_var.get())
                    self.all_games.append(game)
                    self.show_games()
                    self.update_recommendations()
                    window.destroy()
                    messagebox.showinfo("Başarılı", "Oyun eklendi, hadi dalalım!")
                    logging.info(f"Yeni oyun eklendi: {name_var.get()}")
                except Exception as e:
                    logging.error(f"Oyun ekleme hatası: {str(e)}")
                    messagebox.showerror("Hata", str(e))
            ttk.Button(window, text="Ekle", command=submit).pack(pady=10)
        except Exception as e:
            logging.error(f"Oyun ekleme penceresi hatası: {str(e)}")
            messagebox.showerror("Hata", f"Pencere açılamadı: {str(e)}")

    def add_to_collection(self):
        try:
            selected = self.game_tree.selection()
            if not selected:
                raise ValueError("Bir oyun seç, kanka!")
            selected_item = selected[0]  # İlk seçili öğeyi al
            tags = self.game_tree.item(selected_item).get("tags", [])
            if not tags:
                raise ValueError("Seçilen oyunun ID’si bulunamadı, kanka!")
            game_id = tags[0]
            logging.debug(f"Seçilen oyun ID: {game_id}")

            # Oyun listesinde var mı kontrol et
            game = next((g for g in self.all_games if g.game_id == game_id), None)
            if not game:
                raise ValueError("Seçilen oyun bulunamadı!")

            # Koleksiyona ekle
            added = self.player.add_to_collection(game)
            if added:
                self.show_collection()
                self.update_recommendations()
                messagebox.showinfo("Başarılı", f"{game.name} koleksiyona eklendi!")
                logging.info(f"Koleksiyona eklendi: {game.name}, {self.username}")
            else:
                messagebox.showinfo("Bilgi", f"{game.name} zaten koleksiyonunda!")
        except ValueError as ve:
            logging.error(f"Koleksiyona ekleme ValueError: {str(ve)}")
            messagebox.showerror("Hata", str(ve))
        except Exception as e:
            logging.error(f"Koleksiyona ekleme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Koleksiyona eklenemedi: {str(e)}")

    def rate_game(self):
        try:
            selected = self.collection_tree.selection()
            if not selected:
                raise ValueError("Koleksiyonundan bir oyun seç!")
            game_id = self.collection_tree.item(selected)["tags"][0]
            window = tk.Toplevel(self.root)
            window.title("Puan Ver")
            window.geometry("250x150")
            window.configure(bg="#12032b")
            tk.Label(window, text="Puan (0-5):", bg="#12032b", fg="#00ffcc", font=("Arial", 11)).pack(pady=5)
            rating_var = tk.StringVar()
            tk.Entry(window, textvariable=rating_var, font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(pady=5)
            def submit():
                try:
                    rating = float(rating_var.get())
                    self.player.rate_game(game_id, rating)
                    self.show_collection()
                    self.update_recommendations()
                    window.destroy()
                    messagebox.showinfo("Başarılı", "Puanın kaydedildi, efsane!")
                    logging.info(f"Puan verildi: {game_id}, {self.username}, {rating}")
                except Exception as e:
                    logging.error(f"Puan verme hatası: {str(e)}")
                    messagebox.showerror("Hata", str(e))
            ttk.Button(window, text="Ekle", command=submit).pack(pady=10)
        except Exception as e:
            logging.error(f"Puan verme hatası: {str(e)}")
            messagebox.showerror("Hata", str(e))

    def comment_game(self):
        try:
            selected = self.collection_tree.selection()
            if not selected:
                raise ValueError("Koleksiyonundan bir oyun seç!")
            game_id = self.collection_tree.item(selected)["tags"][0]
            window = tk.Toplevel(self.root)
            window.title("Yorum Yap")
            window.geometry("300x200")
            window.configure(bg="#12032b")
            tk.Label(window, text="Yorum:", bg="#12032b", fg="#00ffcc", font=("Arial", 11)).pack(pady=5)
            comment_var = tk.StringVar()
            tk.Entry(window, textvariable=comment_var, font=("Arial", 11), bg="#1a0b3d", fg="#00ffcc", insertbackground="#00ffcc").pack(pady=5)
            def submit():
                try:
                    comment = comment_var.get()
                    if not comment:
                        raise ValueError("Yorum yaz, boş bırakma kanka!")
                    self.player.comment_game(game_id, comment)
                    self.on_collection_select(None)
                    window.destroy()
                    messagebox.showinfo("Başarılı", "Yorumun ateş gibi!")
                    logging.info(f"Yorum eklendi: {game_id}, {self.username}")
                except Exception as e:
                    logging.error(f"Yorum yapma hatası: {str(e)}")
                    messagebox.showerror("Hata", str(e))
            ttk.Button(window, text="Ekle", command=submit).pack(pady=10)
        except Exception as e:
            logging.error(f"Yorum yapma hatası: {str(e)}")
            messagebox.showerror("Hata", str(e))

    def add_favorite(self):
        try:
            selected = self.collection_tree.selection()
            if not selected:
                raise ValueError("Koleksiyonundan bir oyun seç!")
            game_id = self.collection_tree.item(selected)["tags"][0]
            self.player.add_favorite(game_id)
            self.update_recommendations()
            messagebox.showinfo("Başarılı", "Favorilere eklendi, kral!")
            logging.info(f"Favorilere eklendi: {game_id}, {self.username}")
        except Exception as e:
            logging.error(f"Favorilere ekleme hatası: {str(e)}")
            messagebox.showerror("Hata", str(e))

    def on_game_select(self):
        try:
            self.comments_text.config(state="normal")
            self.comments_text.delete("1.0", tk.END)
            selected = self.game_tree.selection()
            if selected:
                game_id = self.game_tree.item(selected)["tags"][0]
                game = next((g for g in self.all_games if g.game_id == game_id), None)
                if game:
                    for comment in game.comments:
                        self.comments_text.insert(tk.END, f"{comment}\n")
            self.comments_text.config(state="disabled")
            logging.info("Oyun seçildi, yorumlar güncellendi")
        except Exception as e:
            logging.error(f"Oyun seçme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Yorumlar yüklenemedi: {str(e)}")

    def on_collection_select(self, event):
        try:
            self.comments_text.config(state="normal")
            self.comments_text.delete("1.0", tk.END)
            selected = self.collection_tree.selection()
            if selected:
                game_id = self.collection_tree.item(selected)["tags"][0]
                game = self.player.collection.get(game_id)
                if game:
                    for comment in game.comments:
                        self.comments_text.insert(tk.END, f"{comment}\n")
            self.comments_text.config(state="disabled")
            logging.info("Koleksiyon oyunu seçildi, yorumlar güncellendi")
        except Exception as e:
            logging.error(f"Koleksiyon seçme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Yorumlar yüklenemedi: {str(e)}")

class MainApp:
    def __init__(self, root):
        try:
            self.root = root
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.show_login()
            logging.info("MainApp başlatıldı")
        except Exception as e:
            logging.error(f"MainApp başlatma hatası: {str(e)}")
            messagebox.showerror("Hata", f"Uygulama başlatılamadı, kanka: {str(e)}")
            self.root.destroy()
            sys.exit(1)

    def clear_frame(self):
        try:
            for widget in self.root.winfo_children():
                widget.destroy()
            logging.info("Pencere temizlendi")
        except Exception as e:
            logging.error(f"Pencere temizleme hatası: {str(e)}")

    def show_login(self):
        try:
            self.clear_frame()
            LoginApp(self.root, self.show_game_app)
            logging.info("Giriş ekranı gösterildi")
        except Exception as e:
            logging.error(f"Giriş ekranı gösterme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Giriş ekranı yüklenemedi: {str(e)}")
            self.root.destroy()
            sys.exit(1)

    def show_game_app(self, username):
        try:
            self.clear_frame()
            GameApp(self.root, username)
            logging.info(f"Oyun uygulaması gösterildi: {username}")
        except Exception as e:
            logging.error(f"Oyun uygulaması gösterme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Oyun ekranı yüklenemedi: {str(e)}")
            self.root.destroy()
            sys.exit(1)

    def on_closing(self):
        try:
            logging.info("Uygulama kapatılıyor")
            self.root.destroy()
        except Exception as e:
            logging.error(f"Kapatma hatası: {str(e)}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = MainApp(root)
        root.mainloop()
        logging.info("Uygulama başarıyla çalıştı")
    except Exception as e:
        logging.error(f"Uygulama başlatma hatası: {str(e)}")
        print(f"Hata: {str(e)}")
        input("Hata oluştu, log dosyasını kontrol et (game_app.log). Çıkmak için bir tuşa bas...")