import subprocess
import os
import sys

# Program yükleme bilgileri sözlüğü, kategorilere ayırılmış olarak
programs = {
    "Medya": {
        "VLC": {
            "command": "vlc",
            "description": "Açık kaynak medya oynatıcı"
        },
        "GIMP": {
            "command": "gimp",
            "description": "Resim düzenleme aracı"
        },
        "Audacity": {
            "command": "audacity", 
            "description": "Ses düzenleme aracı"
        }
    },
    "Ofis": {
        "LibreOffice": {
            "command": "libreoffice",
            "description": "Açık kaynak ofis yazılımı"
        }
    },
    "Geliştirme": {
        "Visual Studio Code": {
            "command": "code",
            "description": "Microsoft'un kod editörü"
        },
        "Google Chrome": {
            "command": "google-chrome-stable",
            "description": "Google'ın popüler web tarayıcısı"
        },
        "Firefox": {
            "command": "firefox",
            "description": "Açık kaynak web tarayıcısı"
        }
    },
    "İletişim": {
        "Telegram": {
            "command": "telegram-desktop",
            "description": "Anlık mesajlaşma uygulaması"
        },
        "Skype": {
            "command": "skypeforlinux",
            "description": "Anlık mesajlaşma ve video görüşme uygulaması"
        },
        "Slack": {
            "command": "slack",
            "description": "Ekip içi iletişim ve işbirliği aracı"
        }
    },
    "Araçlar": {
        "7-Zip": {
            "command": "p7zip-full",
            "description": "Sıkıştırma ve arşivleme aracı"
        },
        "Spotify": {
            "command": "spotify-client",
            "description": "Müzik akış platformu"
        },
        "GParted": {
            "command": "gparted",
            "description": "Disk bölümlerini yönetme aracı"
        },
        "VeraCrypt": {
            "command": "veracrypt",
            "description": "Veri şifreleme aracı"
        },
        "BleachBit": {
            "command": "bleachbit",
            "description": "Sistem temizleme ve optimizasyon aracı"
        },
        "Timeshift": {
            "command": "timeshift",
            "description": "Sistem yedekleme aracı"
        },
        "Stacer": {
            "command": "stacer", 
            "description": "Sistem izleyici ve bakım aracı"
        },
        "Synaptic Package Manager": {
            "command": "synaptic",
            "description": "Paket yönetimi ve yazılım yükleyici"
        }
    }
}

def clear_terminal():
    """Terminali temizler."""
    os.system('cls' if os.name == 'nt' else 'clear')

def is_program_installed(command):
    """Programın bilgisayarda yüklü olup olmadığını kontrol eder."""
    try:
        # dpkg-query ile programın yüklü olup olmadığını kontrol et
        result = subprocess.run(
            f"dpkg -s {command}", 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Kontrol hatası: {str(e)}")
        return False

def install_or_update_program(program, category):
    """Programı yükler veya günceller."""
    try:
        # Programın komut adını al
        command = programs[category][program]['command']
        
        if is_program_installed(command):
            # Program yüklü, güncelleme isteği sor
            response = input(f"{program} programı zaten yüklü. Güncellemek ister misiniz? (e/h): ")
            if response.lower() != 'e':
                print(f"{program} kurulumu iptal edildi.")
                return
            
            print(f"{program} güncelleniyor...")
            install_command = f"sudo apt-get update && sudo apt-get install --only-upgrade -y {command}"
        else:
            # Program yüklenmemiş, yeni yükleme
            print(f"{program} kurulumu başlıyor...")
            install_command = f"sudo apt-get update && sudo apt-get install -y {command}"

        # Komut çalıştırma
        try:
            result = subprocess.run(
                install_command, 
                shell=True, 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            print(f"✅ {program} başarıyla kuruldu veya güncellendi!")
        except subprocess.CalledProcessError as e:
            print(f"❌ {program} kurulumunda hata oluştu:")
            print(e.stderr)
    
    except KeyError:
        print(f"❌ {program} bulunamadı. Lütfen doğru kategoriden seçim yaptığınızdan emin olun.")

def update_system():
    """Sistem güncellemesi yapar."""
    response = input("Sistem güncellemesi yapmak ister misiniz? (e/h): ")
    if response.lower() == 'e':
        try:
            print("Sistem güncelleniyor...")
            command = "sudo apt-get update && sudo apt-get upgrade -y"
            subprocess.run(command, shell=True, check=True)
            print("Sistem başarıyla güncellendi!")
        except subprocess.CalledProcessError:
            print("❌ Sistem güncellenirken hata oluştu.")
    else:
        print("Sistem güncellenmedi.")

def ask_continue():
    """Devam etmek isteyip istemediğini sorar."""
    return input("Başka bir işlem yapmak ister misiniz? (e/h): ").lower() == 'e'

def display_title():
    """Ekranda başlığı gösterir."""
    print("\033[1;32m" + "Format Sonrası Yazılım Yükleyici" + "\033[0m")

def display_categories():
    """Kategorileri ekrana yazdırır."""
    print("\nKategoriler:")
    for index, category in enumerate(programs.keys(), 1):
        print(f"{index}. {category}")
    return list(programs.keys())

def display_programs(category):
    """Kategoriye ait programları ekrana yazdırır."""
    print(f"\n{category} kategorisindeki programlar:")
    for index, (program, details) in enumerate(programs[category].items(), 1):
        print(f"{index}. {program}: {details['description']}")
    return programs[category]

def main():
    """Ana fonksiyon, tüm programları kurar veya günceller."""
    try:
        clear_terminal()
        display_title()
        print("Bu programı kullanarak gerekli yazılımları hızlıca yükleyebilirsiniz.\n")
        
        # Sistem güncellemesi
        update_system()

        while True:
            clear_terminal()
            display_title()

            # Kategori seçimi
            categories = display_categories()
            
            try:
                category_choice = int(input("\nBir kategori seçin (1-5): "))
                if 1 <= category_choice <= len(categories):
                    category = categories[category_choice - 1]
                    
                    clear_terminal()
                    programs_in_category = display_programs(category)

                    # Program seçimi
                    try:
                        program_choice = int(input("\nYüklemek/güncellemek istediğiniz programın numarasını girin: "))
                        if 1 <= program_choice <= len(programs_in_category):
                            program = list(programs_in_category.keys())[program_choice - 1]
                            install_or_update_program(program, category)
                        else:
                            print("Geçersiz program seçimi.")
                    except ValueError:
                        print("Lütfen geçerli bir numara girin.")

                    # Devam etme kontrolü
                    if not ask_continue():
                        break
                else:
                    print("Geçersiz kategori seçimi.")
            except ValueError:
                print("Lütfen geçerli bir numara girin.")

    except KeyboardInterrupt:
        print("\n\nProgram kullanıcı tarafından sonlandırıldı.")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
    finally:
        print("\nMade from MKC")

if __name__ == "__main__":
    main()