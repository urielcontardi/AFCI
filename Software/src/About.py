
import customtkinter as ctk

class AboutApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)

        self.label = ctk.CTkLabel(self, text="About ARC Generator", font=ctk.CTkFont(size=26, weight="bold"))
        self.label.pack(pady=20)

        about_text = (
            "O propósito deste software é manipular e configurar o gerador de arco para testes de AFCI."
        )

        self.info_text = ctk.CTkLabel(self, text=about_text, font=ctk.CTkFont(size=16), wraplength=600, justify="left")
        self.info_text.pack(pady=10, padx=20)
        
        space = "_________________________________________________________"
        self.space_label = ctk.CTkLabel(self, text=space, font=ctk.CTkFont(size=18, weight="bold"), justify="left")
        self.space_label.pack(pady=10, padx=20)

        developers = "Developer:\nUriel Abe Contardi"
        self.developers_label = ctk.CTkLabel(self, text=developers, font=ctk.CTkFont(size=18))
        self.developers_label.pack(pady=20, padx=20)
