🎮 Gamer Arena - Oyun Koleksiyonu Uygulaması
Gamer Arena, oyun tutkunları için tasarlanmış, modern ve kullanıcı dostu bir masaüstü uygulamasıdır. Python ve Tkinter ile geliştirilen bu uygulama, oyun koleksiyonunuzu yönetmenizi, oyunlara puan vermenizi, yorum yapmanızı, favorilere eklemenizi ve kişiselleştirilmiş öneriler almanızı sağlar. Neon esintili, genç ve enerjik arayüzüyle (morumsu #12032b, sarı #ffcc00, neon yeşil #00ff00, pembe #ff0066) oyun keyfinizi bir üst seviyeye taşır! 😎
Bu proje, güvenli kullanıcı girişi, oyun arama/filtreleme, puanlama/yorum sistemi ve öneri algoritması ile donatılmıştır. Kanka, hadi oyun dünyasına dalalım! 🕹️
📋 Özellikler

Kullanıcı Girişi ve Kayıt: SHA-256 ile şifrelenmiş güvenli kullanıcı yönetimi (bellekte saklanır).
Oyun Koleksiyonu: Oyunları ekleyin, koleksiyonunuzu yönetin.
Arama ve Filtreleme: Oyun adına, türe veya platforma göre arama ve filtreleme.
Puanlama: Oyunlara 0-5 arası puan verin, ortalama puanları görün.
Yorum Yapma: Koleksiyonunuzdaki oyunlara yorum ekleyin.
Favoriler: En sevdiğiniz oyunları favorilere ekleyin.
Öneri Sistemi: Favori tür ve platformlarınıza göre kişiselleştirilmiş oyun önerileri.
Neon Arayüz: Morumsu (#12032b), sarı (#ffcc00), neon yeşil (#00ff00), pembe (#ff0066) tonlarla modern tasarım.
Hata Yönetimi: Loglama (game_app.log) ve kullanıcı dostu hata mesajları.
Emoji Desteği: 🎮🔍💬 ile samimi ve eğlenceli vibe.
20 Önyüklü Oyun: The Witcher 3, GTA V, Elden Ring gibi popüler oyunlarla başlangıç.

📸 Ekran Görüntüleri



Giriş Ekranı

<img src="(https://github.com/rojatkrty/oyun_app/blob/main/oyun_ss/login.png)" alt="Paris">


Ana Ekran

<img src="https://github.com/rojatkrty/oyun_app/blob/main/oyun_ss/main.png" alt="Paris">

🚀 Kurulum
Gamer Arena’yı çalıştırmak için aşağıdaki adımları izleyin:
Gereksinimler

Python 3.8 veya üstü
Tkinter (genellikle Python ile gelir)
İşletim sistemi: Windows, macOS veya Linux

Adımlar

Uygulamayı Çalıştırın:
python oyun2.py


Sorun Giderme:

Tkinter yüklü değilse: pip install tk
Hata alırsanız, game_app.log dosyasını kontrol edin.



🎮 Kullanım

Giriş veya Kayıt:

Giriş Yap: Kullanıcı adı ve şifrenizi girin (kayıtlı kullanıcılar için).
Kayıt Ol: Yeni bir kullanıcı adı ve şifre oluşturun (şifreler SHA-256 ile şifrelenir, bellekte saklanır).
Hata alırsanız, “Kullanıcı adı veya şifre yanlış” gibi mesajlar görürsünüz.


Ana Ekran:

Öneriler: Üstte, favori tür ve platformlarınıza göre 3 oyun önerisi görürsünüz.
Arama: Oyun adına göre arama yapın (ör. “Witcher”).
Filtreleme: Tür (ör. “RPG”) veya platform (ör. “PC”) girerek oyunları filtreleyin.
Sekmeler arasında geçiş yapın: “Koleksiyonum” ve “Tüm Oyunlar”.


Tüm Oyunlar Sekmesi:

20 önyüklü oyunu (The Witcher 3, GTA V, vb.) listeleyin.
Bir oyunu seçin, yorumlarını altta görün.
“Koleksiyona Ekle” butonuyla oyunu koleksiyonunuza ekleyin.


Koleksiyonum Sekmesi:

Koleksiyonunuzdaki oyunları görün (ad, tür, platform, ortalama puan).
Bir oyunu seçin, yorumlarını altta görün.
Puan Ver: 0-5 arası puan ekleyin.
Yorum Yap: Oyuna yorum yazın.
Favori Yap: Oyunu favorilere ekleyin (önerileri etkiler).


Yeni Oyun Ekle:

“Yeni Oyun” butonuna tıklayın.
Oyun adı, tür ve platform girin (ör. “Dune: Spice Wars”, “Strateji”, “PC”).
Oyun, tüm oyunlar listesine eklenir ve koleksiyona eklenebilir.



Örnek Kullanım

Kayıt ol: Kullanıcı adı “oyunsevdasi”, şifre “12345”.
Giriş yap, “Tüm Oyunlar” sekmesinde “Elden Ring”i seç.
“Koleksiyona Ekle”ye bas, sonra “Koleksiyonum” sekmesine git.
“Elden Ring”e tıkla, 4.5 puan ver, yorum yaz: “Epik boss savaşları!”.
“Favori Yap”a bas, önerilerin güncellendiğini gör.
Arama çubuğuna “RPG” yaz, sadece RPG oyunlarını filtrele.
“Yeni Oyun” ekle: “Starfield”, “RPG”, “PC”.

🤝 Katkıda Bulunma
Gamer Arena’ya katkıda bulunmak ister misiniz? Süper! İşte adımlar:

Depoyu fork edin.
Yeni bir özellik veya hata düzeltmesi için branch oluşturun: git checkout -b feature/yeni-ozellik.
Değişikliklerinizi yapın ve commit edin: git commit -m "Yeni özellik eklendi".
Push edin: git push origin feature/yeni-ozellik.
Pull request açın.

Önerilen İyileştirmeler:

SQLite ile kalıcı kullanıcı ve oyun verisi saklama.
Oyun kapak görselleri ekleme.
Daha gelişmiş öneri algoritması (ör. kullanıcı puanlarına dayalı).
Çevrimdışı oyun veri dosyası desteği.

📬 İletişim
Soruların mı var, kanka? Bize ulaş:

E-posta: rojatkirtay21@gmail.com
GitHub: github.com/rojatkrty

Hadi, klavyeyi kap ve oyun dünyasına dal! 🕹️
