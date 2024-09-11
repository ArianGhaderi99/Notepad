import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout

kivy.require('2.0.0')

class TextEditorApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # Text input
        self.text_input = TextInput(multiline=True, size_hint=(1, 0.8))
        self.layout.add_widget(self.text_input)

        # Labels for word, character and line count
        self.info_label = Label(size_hint_y=None, height=30)
        self.layout.add_widget(self.info_label)

        # Buttons for saving and opening files
        button_layout = BoxLayout(size_hint_y=None, height=50)
        save_button = Button(text='Save', on_press=self.save_text)
        open_button = Button(text='Open', on_press=self.open_file)

        button_layout.add_widget(save_button)
        button_layout.add_widget(open_button)

        self.layout.add_widget(button_layout)

        # Update counts in real-time
        self.text_input.bind(text=self.update_counts)

        return self.layout

    def update_counts(self, instance, value):
        num_chars = len(value)
        num_words = len(value.split()) if value.strip() else 0
        num_lines = len(value.splitlines())

        self.info_label.text = f'Chars: {num_chars}, Words: {num_words}, Lines: {num_lines}'

    def save_text(self, instance):
        content = self.text_input.text
        filename_popup = FileChooserPopup("Save File", self.save_to_file, 'txt')
        filename_popup.open()

    def save_to_file(self, path, filename):
        with open(f"{path}/{filename[0]}", 'w', encoding='utf-8') as f:
            f.write(self.text_input.text)

    def open_file(self, instance):
        file_selector = FileChooserPopup("Open File", self.load_from_file, 'txt')
        file_selector.open()

    def load_from_file(self, path, filename):
        with open(f"{path}/{filename[0]}", 'r', encoding='utf-8') as f:
            self.text_input.text = f.read()

class FileChooserPopup(Popup):
    def init(self, title, on_dismiss_action, file_type, kwargs):
        super().init(title=title, **kwargs)
        self.file_type = file_type
        self.chosen_file = None
        self.on_dismiss_action = on_dismiss_action
        
        layout = BoxLayout(orientation='vertical')
        self.filechooser = FileChooserIconView(filters=[f'*.{self.file_type}'])  
        layout.add_widget(self.filechooser)

        button_layout = BoxLayout(size_hint_y=None, height=50)
        choose_button = Button(text='Choose', on_press=self.choose_file)
        cancel_button = Button(text='Cancel', on_press=self.dismiss)

        button_layout.add_widget(choose_button)
        button_layout.add_widget(cancel_button)

        layout.add_widget(button_layout)
        self.content = layout

    def choose_file(self, instance):
        if self.filechooser.selection:
            self.chosen_file = self.filechooser.selection
            self.on_dismiss_action(self.filechooser.path, self.chosen_file)
            self.dismiss()

if __name__ == '__main__':
    TextEditorApp().run()