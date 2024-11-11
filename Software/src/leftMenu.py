import customtkinter

class LeftMenu(customtkinter.CTkFrame):
    def __init__(self, master, ARCBtnEvent, AboutBtnEvent, changeModeEvent, changeScaleEvent):
        super().__init__(master, width=140, corner_radius=0)
        self.ARCBtnEvent = ARCBtnEvent
        self.changeModeEvent = changeModeEvent
        self.changeScaleEvent = changeScaleEvent
        self.AboutBtnEvent = AboutBtnEvent
        self.grid_rowconfigure(4, weight=1)
        
        # Logo
        self.logo = customtkinter.CTkLabel(self, text="ARC Generator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))

        # ARC app
        self.ARCBtn = customtkinter.CTkButton(self, text="Configurations", command=self.ARCBtnEvent)
        self.ARCBtn.grid(row=1, column=0, padx=20, pady=10)
      
        # Theme and Scale Options
        self.appTheme = customtkinter.CTkOptionMenu(self, values=["Dark", "Light", "System"],
                                                                       command=self.changeModeEvent)
        self.appTheme.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appScaling = customtkinter.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.changeScaleEvent)
        self.appScaling.grid(row=8, column=0, padx=20, pady=(10, 20))
        
        # About Button
        self.AboutBtn = customtkinter.CTkButton(self, text="About", command=self.AboutBtnEvent)
        self.AboutBtn.grid(row=9, column=0, padx=20, pady=10)