import customtkinter as ctk
import threading

from chatbot import ask_ai
from speech import listen
from tts import speak
from history import clear_history

#TO EXIT WORDS
EXIT_WORDS = [
    "exit",
    "quit",
    "bye",
    "close",
    "close application",
    "shutdown"
]
# -------------------- Theme --------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ChatbotGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AI Learning Assistant")
        self.geometry("1000x700")
        self.minsize(900, 650)

        self.create_widgets()

    # ------------------------------------------------

    def create_widgets(self):

        # ================= Header =================

        header = ctk.CTkFrame(self, height=70)

        header.pack(fill="x")

        title = ctk.CTkLabel(
            header,
            text="🤖 AI Learning Assistant",
            font=("Arial", 28, "bold")
        )

        title.pack(pady=18)
        
        self.status = ctk.CTkLabel(
            self,
            text="Ready",
            text_color="lightgreen"
        )

        self.status.pack(pady=2)

        # ================= Chat Area =================

        self.chat_area = ctk.CTkScrollableFrame(
            self,
            corner_radius=10
        )

        self.chat_area.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # Welcome message

        self.add_message(
            "AI",
            "Hello 👋\n\nI am your AI Learning Assistant.\nAsk me anything."
        )

        # ================= Bottom =================

        bottom = ctk.CTkFrame(self)

        bottom.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.entry = ctk.CTkEntry(
            bottom,
            placeholder_text="Type your question..."
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        self.entry.bind(
            "<Return>",
            lambda e: self.send_message()
        )

        self.send_btn = ctk.CTkButton(
            bottom,
            text="Send",
            width=100,
            command=self.send_message
        )

        self.send_btn.pack(
            side="left",
            padx=5
        )

        self.voice_btn = ctk.CTkButton(
            bottom,
            text="🎤",
            width=60,
            command=self.voice_input
        )

        self.voice_btn.pack(
            side="left",
            padx=5
        )
        
        self.clear_button = ctk.CTkButton(
        bottom,
        text="Clear",
        width=80,
        command=self.clear_chat
        )

        self.clear_button.pack(
            side="left",
            padx=5
        )

    # ------------------------------------------------

    def add_message(self, sender, message):

        row = ctk.CTkFrame(
            self.chat_area,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            pady=8,
            padx=10
        )

        if sender == "You":

            bubble = ctk.CTkFrame(
                row,
                fg_color="#1F6AA5",
                corner_radius=12
            )

            bubble.pack(
                anchor="e",
                padx=10
            )

        else:

            bubble = ctk.CTkFrame(
                row,
                fg_color="#2B2B2B",
                corner_radius=12
            )

            bubble.pack(
                anchor="w",
                padx=10
            )

        label = ctk.CTkLabel(
            bubble,
            text=message,
            justify="left",
            wraplength=550,
            padx=15,
            pady=10
        )

        label.pack()
        
    # ------------------------------------------------

    def send_message(self):
        question = self.entry.get().strip()
        
        if question.lower() in EXIT_WORDS:
            self.destroy()
            return

        if not question:
            return

        self.add_message("You", question)
        self.entry.delete(0, "end")
        self.send_btn.configure(state="disabled")
        self.voice_btn.configure(state="disabled")

        self.status.configure(
            text="AI is thinking...",
            text_color="orange"
            )
        
        threading.Thread(
            target=self.get_ai_response,
            args=(question,),
            daemon=True
            ).start()
        
    #------------------------------------------------
    def get_ai_response(self, question):
        
        try:
            #asking gemini
            answer = ask_ai(question)

            # Show answer in GUI
            # Show answer first, then speak
            self.after(
                 0,self.show_answer(answer)
                    )

        except Exception as e:
            error_message = str(e)
            
            self.after(0,lambda msg=error_message: self.add_message("AI", msg))
            
            # Update status to Speaking
            self.after(
                0,
                lambda: self.status.configure(
                text="Ready",
                text_color="lightgreen"
                    )
                    )

        finally:
            self.after(
            0,
            lambda: self.send_btn.configure(state="normal")
            )

            self.after(
            0,
            lambda: self.voice_btn.configure(state="normal")
              )
#------------------------------------------------
    def show_answer(self, answer):

    # Display the answer immediately
        self.add_message("AI", answer)

    # Force the GUI to redraw
        self.update_idletasks()
        
        self.after(
            150,
            lambda: threading.Thread(
            target=self.speak_response,
            args=(answer,),
            daemon=True
        ).start()
        )
        
        #-------------------------------------------------   
    def voice_input(self):

        self.status.configure(
            text="Listening...",
            text_color="cyan"
        )
        self.send_btn.configure(state="disabled")
        self.voice_btn.configure(state="disabled")

        threading.Thread(
            target=self.process_voice,
            daemon=True
        ).start()
    
    #-------------------------------------------------
    def process_voice(self):

    # Listen for user's voice
        question = listen()

    # If nothing was recognized
        if not question:
            self.after(
            0,
            lambda: self.status.configure(
                text="Ready",
                text_color="lightgreen"
            )
            )

            self.after(
            0,
            lambda: self.send_btn.configure(state="normal")
            )

            self.after(
            0,
            lambda: self.voice_btn.configure(state="normal")
            )

            return

    # Close application if user says exit
        if question.lower() in EXIT_WORDS:

            self.after(0, self.destroy)
            return

    # Show user's message
        self.after(
            0,
            lambda: self.add_message("You", question)
            )

        self.after(
            0,
            lambda: self.status.configure(
                text="AI is thinking...",
                text_color="orange"
            )
        )

        try:

        # Get AI response
            answer = ask_ai(question)

        # Display AI response
            self.after(
                0,
                lambda: self.add_message("AI", answer)
            )

        # Speak AI response
            self.after(
                0,
                lambda: speak(answer)
            )

        except Exception as e:

            self.after(
                0,
                lambda: self.add_message("AI", f"Error: {e}")
            )

        finally:

            self.after(
                0,
                lambda: self.status.configure(
                    text="Ready",
                    text_color="lightgreen"
                )
            )

            self.after(
                0,
                lambda: self.send_btn.configure(state="normal")
            )

            self.after(
                0,
                lambda: self.voice_btn.configure(state="normal")
            )
#--------------------------------------------------------------
    def speak_response(self, answer):
        self.after(
            0,
            lambda: self.status.configure(
                text="Speaking...",
                text_color="deepskyblue"
                )
                )

        speak(answer)

        self.after(
            0,
            lambda: self.status.configure(
                text="Ready",
                text_color="lightgreen"
                )
                )
#---------------------------------------------------------------
    def clear_chat(self):
        print("Clear button clicked!")

    # Clear conversation history
        clear_history()

    # Remove all chat bubbles
        for widget in self.chat_area.winfo_children():
            widget.destroy()

    # Show welcome message again
        self.add_message(
            "AI",
            " Chat cleared.\n\nHow can I help you?"
        )

    # Clear input box
        self.entry.delete(0, "end")

    # Reset status
        self.status.configure(
            text="Ready",
            text_color="lightgreen"
        )


        
    
    
        