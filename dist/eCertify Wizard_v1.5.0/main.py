import customtkinter as ctk
from View.login import open_login_page
from shutil import rmtree
from os import makedirs, getcwd, devnull
from os.path import exists, join, isdir
import sys
import time

sys.stdout = open(devnull, 'w')
sys.stderr = open(devnull, 'w')
app = 'root'

class MyApp(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_window()

    def configure_window(self):
        vp_width = self.winfo_screenwidth()
        vp_height = self.winfo_screenheight()

        screen_x = (vp_width - 600) // 2
        screen_y = (vp_height - 800) // 2
        self.geometry(f'600x700+{screen_x}+{screen_y}')
        
        self.title('E-CertifyWizard')
        icon_path = join(getcwd(), 'resources', 'logo1.ico')
        self.iconbitmap(icon_path)
        self.protocol("WM_DELETE_WINDOW", self.__on_exit)

        self.__loadComponents()

    def __loadComponents(self):
        open_login_page(self)

    def __on_exit(self):
        self.__clear_tempDir()
        self.destroy()

    def __clear_tempDir(self):
        temporary_dir = join(getcwd(), 'temporary')
        template_dir = join(getcwd(), 'custom_template')

        def retry_rmtree(directory, retries=5, delay=1):
            for _ in range(retries):
                try:
                    if exists(directory) and isdir(directory):
                        rmtree(directory)
                        makedirs(directory)
                    break
                except PermissionError:
                    time.sleep(delay)

        retry_rmtree(temporary_dir)
        retry_rmtree(template_dir)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = MyApp()

    app.mainloop()
