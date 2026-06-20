import asyncio
import os
import random
import threading
import requests
from edge_tts import Communicate

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

class ReelGeneratorUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        
        # App Title
        self.add_widget(Label(
            text="🎬 UNLIMITED REEL GENERATOR", 
            font_size='24sp', 
            size_hint_y=None, 
            height=50,
            bold=True
        ))
        
        # Theme Input Section
        self.add_widget(Label(text="1️⃣ Enter Visual Theme (e.g., cyberpunk, space):", size_hint_y=None, height=30, halign='left'))
        self.theme_input = TextInput(text="cyberpunk", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.theme_input)
        
        # Script Input Section
        self.add_widget(Label(text="2️⃣ Paste Voiceover Script / Tech Fact:", size_hint_y=None, height=30))
        self.script_input = TextInput(multiline=True, hint_text="Type or paste your reels script here...")
        self.add_widget(self.script_input)
        
        # Status Log Box (Scrollable text display)
        self.scroll = ScrollView(size_hint_y=0.3)
        self.status_label = Label(text="Status: Ready to build!", markup=True, halign='center', valign='middle')
        self.scroll.add_widget(self.status_label)
        self.add_widget(self.scroll)
        
        # Generate Button
        self.gen_btn = Button(
            text="🚀 Generate Assets Locally", 
            background_color=(0, 0.7, 1, 1), 
            size_hint_y=None, 
            height=60,
            bold=True
        )
        self.gen_btn.bind(on_press=self.start_generation_thread)
        self.add_widget(self.gen_btn)

    def update_status(self, text):
        self.status_label.text = text

    def start_generation_thread(self, instance):
        # Disable button during processing
        self.gen_btn.disabled = True
        self.update_status("[color=ffcc00]⏳ Processing started... Please wait.[/color]")
        
        # Run generation background thread to keep UI from freezing
        threading.Thread(target=self.run_production_pipeline).start()

    def run_production_pipeline(self):
        theme = self.theme_input.text.strip()
        script = self.script_input.text.strip()
        
        if not theme or not script:
            self.update_status("[color=ff3333]❌ Error: Missing fields![/color]")
            self.gen_btn.disabled = False
            return
            
        try:
            # 1. Run local Edge TTS voiceover generation
            self.update_status("🎙️ Generating high-retention AI Voiceover...")
            asyncio.run(self.generate_voice_logic(script))
            
            # 2. Fetch and download high-res background video
            self.update_status("🎬 Fetching premium HD video stream...")
            self.download_video_logic(theme)
            
            # 3. Export assets directly to mobile storage
            self.update_status("📦 Moving assets to Phone Storage...")
            os.system("cp voice.mp3 /sdcard/Download/ && cp background.mp4 /sdcard/Download/")
            
            self.update_status("[color=33ff33]🔥 SUCCESS! Files exported to your Downloads folder.[/color]")
        except Exception as e:
            self.update_status(f"[color=ff3333]❌ Automation Failed: {str(e)}[/color]")
            
        self.gen_btn.disabled = False

    async def generate_voice_logic(self, text):
        communicate = Communicate(text, "en-US-GuyNeural")
        await communicate.save("voice.mp3")

    def download_video_logic(self, search_term):
        public_url = f"https://api.pexels.com/videos/search?query={search_term}&orientation=portrait&per_page=15"
        headers = {
            "Authorization": "563492ad6f91700001000001bc93ef69ca904664879100220bc0a646",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
        }
        response = requests.get(public_url, headers=headers)
        videos = response.json().get('videos', [])
        
        if videos:
            long_videos = [v for v in videos if v.get('duration', 0) >= 12]
            video_data = random.choice(long_videos) if long_videos else random.choice(videos)
            video_files = video_data.get('video_files', [])
            video_url = sorted(video_files, key=lambda x: x.get('width', 0))[-1].get('link')
            
            with requests.get(video_url, headers=headers, stream=True) as video_stream:
                video_stream.raise_for_status()
                with open("background.mp4", 'wb') as f:
                    for chunk in video_stream.iter_content(chunk_size=8192):
                        f.write(chunk)
        else:
            raise Exception("No matching videos found.")

class MobileReelApp(App):
    def build(self):
        return ReelGeneratorUI()

if __name__ == "__main__":
    MobileReelApp().run()

