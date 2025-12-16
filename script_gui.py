import os
import re
import threading
from pathlib import Path
from tkinter import *
from tkinter import ttk, scrolledtext, messagebox
import yt_dlp

def get_downloads_folder():
    return str(Path.home() / "Downloads")

def is_youtube_url(url):
    youtube_patterns = [
        r'(https?://)?(www\.)?youtube\.com',
        r'(https?://)?(www\.)?youtu\.be'
    ]
    return any(re.search(pattern, url) for pattern in youtube_patterns)

def download_youtube_mp3(url, output_path, log_widget):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            log_widget.insert(END, f"📥 Baixando: {url}\n")
            log_widget.see(END)
            log_widget.update()
            
            info = ydl.extract_info(url, download=True)
            log_widget.insert(END, f"✅ Concluído: {info['title']}.mp3\n\n")
            log_widget.see(END)
            messagebox.showinfo("Sucesso", f"Música salva em:\n{output_path}")
            return True
    except Exception as e:
        log_widget.insert(END, f"❌ Erro: {str(e)}\n\n")
        log_widget.see(END)
        messagebox.showerror("Erro", f"Erro ao baixar:\n{str(e)}")
        return False

def start_download(url_entry, log_widget, downloads_folder):
    url = url_entry.get().strip()
    
    if not url:
        messagebox.showwarning("Aviso", "Cole uma URL do YouTube!")
        return
    
    if not is_youtube_url(url):
        messagebox.showerror("Erro", "URL não reconhecida. Use apenas links do YouTube.")
        return
    
    url_entry.delete(0, END)
    thread = threading.Thread(target=download_youtube_mp3, args=(url, downloads_folder, log_widget))
    thread.daemon = True
    thread.start()

def main():
    root = Tk()
    root.title("🎵 YMD - Youtube Musics Download")
    root.geometry("600x500")
    root.resizable(False, False)
    
    downloads_folder = get_downloads_folder()
    
    # Título
    title_label = Label(root, text="🎵 YMD - Youtube Musics Download", font=("Arial", 14, "bold"))
    title_label.pack(pady=10)
    
    # Frame para entrada
    input_frame = Frame(root)
    input_frame.pack(pady=10, padx=10, fill=X)
    
    Label(input_frame, text="URL do YouTube:").pack(anchor=W)
    url_entry = Entry(input_frame, width=70, font=("Arial", 10))
    url_entry.pack(fill=X, pady=5)
    url_entry.bind("<Return>", lambda e: start_download(url_entry, log_widget, downloads_folder))
    
    # Botão de download
    download_btn = ttk.Button(input_frame, text="📥 Baixar", 
                             command=lambda: start_download(url_entry, log_widget, downloads_folder))
    download_btn.pack(pady=5)
    
    # Log
    Label(root, text="Log de Downloads:", font=("Arial", 10, "bold")).pack(anchor=W, padx=10)
    log_widget = scrolledtext.ScrolledText(root, height=15, width=70, font=("Courier", 9))
    log_widget.pack(padx=10, pady=5, fill=BOTH, expand=True)
    
    # Info
    info_label = Label(root, text=f"📁 Salvando em: {downloads_folder}", font=("Arial", 9), fg="gray")
    info_label.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()