from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.storage.jsonstore import JsonStore
import random

# --- KESİN KADRO ---
OGRETMENLER = {
    "S. AHMET GÖRGÜLÜ": "Müzik", "HİCRET KAYA KARACA": "Matematik",
    "NESLİHAN ÖZBİLGİN": "İngilizce", "MÜYESSER ŞENGÜN": "Arapça",
    "ADEM BEKTAŞ": "Felsefe", "AHMET ASLAN": "Coğrafya",
    "BEKİR DOĞAN": "Edebiyat", "DİLEK DOĞAN KOÇ": "Matematik",
    "MEHMET DEMİR": "Fizik", "KADİR ALACAHAN": "Matematik",
    "ÜLKÜ POLAT": "Çocuk Gelişimi", "YUNUS KOÇAK": "Sosyal Bilgiler",
    "ZEYNEP K. YILDIRIM": "Kur'an-ı Kerim", "BOŞ": "---"
}

GUNLER = ["Pzt", "Sal", "Çar", "Per", "Cum"]
SAATLER = ["08:30", "09:20", "10:10", "11:00", "11:50", "13:20", "14:10", "15:00"]

class ProgramApp(App):
    def build(self):
        self.store = JsonStore('sivas_aihl.json')
        self.secili_hoca = None
        
        main_layout = BoxLayout(orientation='vertical', spacing=5, padding=10)
        
        # ÜST PANEL: Otomatik Doldur
        top_bar = BoxLayout(size_hint_y=0.1)
        btn_oto = Button(text="⚡ OTOMATİK DOLDUR", background_color=(1, 0.6, 0, 1))
        btn_oto.bind(on_press=self.otomatik_doldur)
        top_bar.add_widget(btn_oto)
        main_layout.add_widget(top_bar)

        # ORTA PANEL: Öğretmen Seçim Listesi (Yatay Kaydırılabilir)
        scroll_hoca = ScrollView(size_hint_y=0.15, do_scroll_x=True, do_scroll_y=False)
        self.hoca_box = BoxLayout(orientation='horizontal', size_hint_x=None, spacing=5)
        self.hoca_box.bind(minimum_width=self.hoca_box.setter('width'))
        
        for h in sorted(OGRETMENLER.keys()):
            btn = Button(text=h, size_hint_x=None, width=150, font_size='12sp')
            btn.bind(on_press=lambda instance, h=h: self.hoca_tut(h, instance))
            self.hoca_box.add_widget(btn)
        
        scroll_hoca.add_widget(self.hoca_box)
        main_layout.add_widget(scroll_hoca)

        # ALT PANEL: Ders Programı Tablosu
        self.grid = GridLayout(cols=6, spacing=2, size_hint_y=0.75)
        self.tabloyu_olustur()
        main_layout.add_widget(self.grid)
        
        return main_layout

    def hoca_tut(self, hoca, instance):
        self.secili_hoca = hoca
        self.msg_guncelle(f"Elinizde: {hoca}")

    def tabloyu_olustur(self):
        self.grid.clear_widgets()
        self.grid.add_widget(Label(text="Saat", bold=True, size_hint_x=0.5))
        for g in GUNLER:
            self.grid.add_widget(Label(text=g, bold=True))

        for r in range(8):
            self.grid.add_widget(Label(text=SAATLER[r], size_hint_x=0.5))
            for c in range(5):
                key = f"9A_{GUNLER[c]}_{r}" # Örnek sınıf 9A
                ders_hoca = self.store.get(key)['name'] if self.store.exists(key) else "BOŞ"
                
                btn = Button(text=f"{ders_hoca}\n{OGRETMENLER.get(ders_hoca,'')}", 
                             font_size='9sp', halign='center')
                btn.bind(on_press=lambda inst, k=key: self.hucre_tikla(k, inst))
                self.grid.add_widget(btn)

    def hucre_tikla(self, key, instance):
        if self.secili_hoca:
            self.store.put(key, name=self.secili_hoca)
            self.secili_hoca = None
            self.tabloyu_olustur()
        else:
            mevcut = self.store.get(key)['name'] if self.store.exists(key) else "BOŞ"
            if mevcut != "BOŞ":
                self.secili_hoca = mevcut
                self.store.put(key, name="BOŞ")
                self.tabloyu_olustur()

    def otomatik_doldur(self, instance):
        hocalar = [h for h in OGRETMENLER.keys() if h != "BOŞ"]
        for c in range(5):
            for r in range(8):
                key = f"9A_{GUNLER[c]}_{r}"
                self.store.put(key, name=random.choice(hocalar))
        self.tabloyu_olustur()

    def msg_guncelle(self, metin):
        print(metin) # Android loglarında görünür

if __name__ == '__main__':
    ProgramApp().run()
