# Third-Party Libraries
import customtkinter as ctk

# Libraries
from src.leftMenu import LeftMenu
from src.ARC_App import ARC_App
from src.utils import resource_path
from src.About import AboutApp

# Set Default
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def changeTheme(new_mode):
    ctk.set_appearance_mode(new_mode)

def changeScale(new_scaling):
    scaling_values = {
        "80%": 0.8,
        "90%": 0.9,
        "100%": 1.0,
        "110%": 1.1,
        "120%": 1.2,
    }
    ctk.set_widget_scaling(scaling_values[new_scaling])

# Main application
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        revision = 'r00' # Revision control

        self.title("Arc Generator - " + revision)
        self.geometry("800x800")

        # Create and add the left menu to the main window
        self.leftMenu = LeftMenu(self, self.showARC_App, 
                                 self.showAbout, 
                                 changeTheme, 
                                 changeScale
                                 )
        self.leftMenu.pack(side="left", fill="y")

        # Placeholder for the main content area
        self.mainContent = ctk.CTkFrame(self, width=660)
        self.mainContent.pack(side="right", fill="both", expand=True)

        # Set Default
        self.__default()

    def __default(self):
        # Minimal Size
        self.minsize(1000, 400) 
        # Inital App
        self.showARC_App()

    def showARC_App(self):
        self.clearMainContent()
        MVW01Widget = ARC_App(self.mainContent)
        MVW01Widget.pack(fill="both", expand=True)
            
    def showAbout(self):
        self.clearMainContent()
        AboutWidget = AboutApp(self.mainContent)
        AboutWidget.pack(fill="both", expand=True)
        

    def clearMainContent(self):
        # Clear main content area
        for widget in self.mainContent.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
