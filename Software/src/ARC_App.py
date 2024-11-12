import customtkinter as ctk
import serial
import serial.tools.list_ports
from PIL import Image, ImageTk
from src.utils import resource_path
import time

DEFAULT_BAUDRATE = 9600
DEFAULT_SPEED = 500
DEFAULT_DISTANCE = 200
DEFAULT_TIME = 5000
MAX_DISTANCE = 3500

class ARC_App(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True, anchor="center")  # Centralizando o frame principal

        # Central Frame
        self.central_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.central_frame.pack(expand=True)

        # Title
        self.label = ctk.CTkLabel(self.central_frame, text="Arc Generator", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        # Create Image Frame
        self.__createImageFrame()
        
        # Create COM Port Frame
        self.__createCOMPortFrame()
        # Serial connection variable
        self.serial_connection = None
        
        # Create Parameters Frame
        self.__createParametersFrame()
        
        # Create Button
        self.__createAppButton() 

    def __createImageFrame(self):
        imageFrame = ctk.CTkFrame(self.central_frame)
        imageFrame.pack(pady=5)

        # Load the image
        image_path = resource_path("../3D_Model/3D_Model.png")
        image = Image.open(image_path)
        
        # Resize the image (set your desired width and height)
        desired_width, desired_height = 440, 200
        image = image.resize((desired_width, desired_height), Image.LANCZOS)
        
        # Create a CTkImage
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(desired_width, desired_height))
        
        # Create an image label
        self.imageLabel = ctk.CTkLabel(imageFrame, image=ctk_image, text="")
        self.imageLabel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def __createCOMPortFrame(self):
        smartCodeFrame = ctk.CTkFrame(self.central_frame)
        smartCodeFrame.pack(pady=20)

        # Center alignment
        smartCodeFrame.columnconfigure((0, 1, 2, 3), weight=1)

        # Label
        self.smartCodeLabel = ctk.CTkLabel(smartCodeFrame, text="COM Port", font=("Helvetica", 14, "bold"))
        self.smartCodeLabel.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # ComboBox
        self.smartCodeComboBox = ctk.CTkComboBox(smartCodeFrame, 
                                                 values=self.__getCOMPorts(),
                                                 width=300, 
                                                 state="readonly"
                                                 )
        self.smartCodeComboBox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Buttons
        self.updateBtn = ctk.CTkButton(smartCodeFrame, text="Update", command=self.__updateCOMPorts, font=("Helvetica", 16))
        self.updateBtn.grid(row=0, column=2, padx=5, pady=5)
        
        self.connBtn = ctk.CTkButton(smartCodeFrame, text="Connect", command=self.__connCOM, font=("Helvetica", 16))
        self.connBtn.grid(row=0, column=3, padx=5, pady=5)

    def __getCOMPorts(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def __updateCOMPorts(self):
        self.smartCodeComboBox.configure(values=self.__getCOMPorts())
        
    def __connCOM(self):
        """Connects to the selected COM port."""
        selected_port = self.smartCodeComboBox.get()
        
        if not selected_port:
            print("No COM port selected.")
            return
        
        try:
            # Close any existing connection
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
                print(f"Closed previous connection on {self.serial_connection.port}")

            # Open new connection
            self.serial_connection = serial.Serial(selected_port, baudrate=DEFAULT_BAUDRATE, timeout=1)
            print(f"Connected to {selected_port}")

        except serial.SerialException as e:
            print(f"Failed to connect to {selected_port}: {e}")
            
    def __createParametersFrame(self):
        parametersFrame = ctk.CTkFrame(self.central_frame)
        parametersFrame.pack(pady=20)

        # Parameters Title
        titleLabel = ctk.CTkLabel(parametersFrame, text="Parameters", font=("Helvetica", 14, "bold"))
        titleLabel.grid(row=0, column=0, columnspan=4, pady=10, sticky="n")

        # Parameters
        self.speed1Entry = EntryBoxLabel(parametersFrame, "Velocidade (Steps/s)")
        self.speed1Entry.entry.insert(0, str(DEFAULT_SPEED))
        self.speed1Entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.distanceEntry = EntryBoxLabel(parametersFrame, "Distancia (Step/s)", min_value=0, max_value=MAX_DISTANCE)
        self.distanceEntry.entry.insert(0, str(DEFAULT_DISTANCE))
        self.distanceEntry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        self.delayEntry = EntryBoxLabel(parametersFrame, "Delay (ms)")
        self.delayEntry.entry.insert(0, str(DEFAULT_TIME))
        self.delayEntry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        
        self.speed2Entry = EntryBoxLabel(parametersFrame, "Velocidade 2 (Steps/s)")
        self.speed2Entry.entry.insert(0, str(DEFAULT_SPEED))
        self.speed2Entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
    def __createAppButton(self):
        
        self.resetBtn = ctk.CTkButton(self.central_frame, text="Reset", command=self.__reset, font=("Helvetica", 16))
        self.resetBtn.pack(pady=10)
        
        self.runBtn = ctk.CTkButton(self.central_frame, text="Run", command=self.__runCommand, font=("Helvetica", 16))
        self.runBtn.pack(pady=10)
        
    def __runCommand(self):
        if not self.serial_connection or not self.serial_connection.is_open:
            print("No open serial connection.")
            return
        
        try:
            # Get Configuration
            speed1 = self.speed1Entry.entry.get()
            speed2 = self.speed2Entry.entry.get()
            distance = self.distanceEntry.entry.get()
            delay = self.delayEntry.entry.get()
    
            # Configure Parameters
            response = self.serial_connection.readline().decode().strip() 
            print(f"Response: {response}")
            time.sleep(1)
            
            self.serial_connection.write(f"SPEED {speed1}\n".encode())
            print(f"Sent: SPEED {speed1}")
            response = self.serial_connection.readline().decode().strip()  # Lê e decodifica a resposta
            print(f"Response: {response}")
    
            self.serial_connection.write(f"DISTANCE {distance}\n".encode())
            print(f"Sent: DISTANCE {distance}")
            response = self.serial_connection.readline().decode().strip()
            print(f"Response: {response}")
    
            self.serial_connection.write(f"TIME {delay}\n".encode())
            print(f"Sent: DELAY {delay}")
            response = self.serial_connection.readline().decode().strip()
            print(f"Response: {response}")
            
            # Run App
            self.serial_connection.write("RUN\n".encode())
            
        except serial.SerialException as e:
            print(f"Error sending data: {e}")

    def __reset(self):
        if not self.serial_connection or not self.serial_connection.is_open:
            print("No open serial connection.")
            return

        try:
            # Send RESET
            self.serial_connection.write("RESET\n".encode())
            print("Sent: RESET")

            # Timeout
            timeout = 10
            start_time = time.time()

            # Wait for Reset
            while True:
                # Verify timeout
                if time.time() - start_time > timeout:
                    print("Timeout: Device not found.")
                    break

                # Read response
                response = self.serial_connection.readline().decode().strip()
                if "Encontrado!" in response:
                    print("Resetado")
                    break

                # Wait for a while
                time.sleep(0.1)

        except serial.SerialException as e:
            print(f"Error during reset: {e}")
        

class EntryBoxLabel(ctk.CTkFrame):
    def __init__(self, master, label_text, min_value=None, max_value=None):
        super().__init__(master)
        
        self.min_value = min_value  # Valor mínimo permitido
        self.max_value = max_value  # Valor máximo permitido

        # Label
        self.label = ctk.CTkLabel(self, text=label_text, font=("Helvetica", 14, "bold"))
        self.label.grid(row=0, column=0, padx=10, pady=(0, 0), sticky="ew")
        
        # Entry 
        vcmd = (self.register(self.validate_numeric), "%P")
        self.entry = ctk.CTkEntry(self, validate="key", validatecommand=vcmd)
        self.entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        
    def validate_numeric(self, value):
        """Permite apenas valores numéricos dentro do intervalo especificado."""
        # Permitir valor vazio para facilitar a edição
        if value == "":
            return True

        # Verifica se o valor é numérico
        if value.isdigit():
            numeric_value = int(value)

            # Verifica se está dentro dos limites, se forem definidos
            if (self.min_value is not None and numeric_value < self.min_value):
                return False
            if (self.max_value is not None and numeric_value > self.max_value):
                return False
            return True
        return False