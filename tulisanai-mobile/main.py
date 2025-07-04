from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.factory import Factory
import requests
import os

class TulisanAILayout(BoxLayout):
    preview_source = StringProperty('assets/placeholder.png')
    result_text = StringProperty('Hasil akan tampil di sini')
    selected_image = None

    def pick_image(self):
        from plyer import filechooser
        file = filechooser.open_file(title="Pilih Gambar", filters=[("Image files", "*.jpg;*.png")])
        if file:
            self.selected_image = file[0]
            self.preview_source = file[0]

    def process_ocr(self):
        if not self.selected_image:
            self.result_text = 'Pilih gambar dulu!'
            return

        url = 'http://127.0.0.1:5000/api/ocr'
        try:
            with open(self.selected_image, 'rb') as f:
                files = {'image': f}
                res = requests.post(url, files=files)
                res.raise_for_status()
                data = res.json()
                self.result_text = data.get('text', 'Tidak ada teks')
        except Exception as e:
            self.result_text = f'Error: {e}'

class TulisanAIApp(App):
    def build(self):
        return Factory.TulisanAILayout()

if __name__ == '__main__':
    TulisanAIApp().run()
