import tkinter as tk
from views.project_view import ProjectView

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------
# these are just the colors we'll be using to paint our rooms (frames)
selection_color = '#eff5f6'
sidebar_color = '#616e78'
header_color = '#0a61a3'
visualisation_frame_color = "#ffffff"


class Quantalysis(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Quantitative Risk Analysis Tool")
        self.sidebar_color = sidebar_color

        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1100x900")
        self.resizable(0, 0)
        self.title('Quantitative Risk Analysis Tool')
        self.config(background=selection_color)
        icon = tk.PhotoImage(file='images\\logo.png')
        self.iconphoto(True, icon)

        # ------------- MENU BAR -----------------
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Create File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Load Project", command=self.load_project)
        # file_menu.add_command(label="Save Project", command=self.save_project)  # Move save_project here
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # ---------------- HEADER ------------------------

        self.header = tk.Frame(self, bg=header_color)
        self.header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.1)

        # ---------------- SIDEBAR -----------------------
        # SIDEBAR FRAME
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        # BRANDING FRAME (APP NAME AND LOGO)
        self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.20)
        self.app_logo = icon.subsample(9)
        logo = tk.Label(self.brand_frame, image=self.app_logo, bg=sidebar_color)
        logo.place(x=5, y=20)
        # Create an instance of the ProjectView class
        self.project_view = ProjectView(self)

        tool_name = tk.Label(self.brand_frame,
                             text='Quantitative Risk',
                             bg=sidebar_color,
                             font=("", 15, "bold")
                             )
        tool_name.place(x=55, y=27, anchor="w")

        tool_name = tk.Label(self.brand_frame,
                             text='Analysis Tool',
                             bg=sidebar_color,
                             font=("", 15, "bold")
                             )
        tool_name.place(x=55, y=60, anchor="w")

        new_project_button = tk.Button(self.brand_frame,
                                       text="New Project",
                                       bg=sidebar_color,
                                       fg="white",
                                       font=("", 12, "bold"),
                                       command=self.project_view.new_project)
        new_project_button.place(x=5, y=100, anchor="w")

        load_project_button = tk.Button(self.brand_frame,
                                        text="Load Project",
                                        bg=sidebar_color,
                                        fg="white",
                                        font=("", 12, "bold"),
                                        command=self.project_view.load_existing_projects)
        load_project_button.place(x=150, y=100, anchor="w")

        # --------------------  MAIN FRAME ---------------------------

        main_frame = tk.Frame(self)
        main_frame.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        # ADDING FRAMES TO MAIN FRAME
        self.frames = {}

        for F in (Frame1, Frame2):
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(Frame1)

    def show_frame(self, cont):
        """
        this function enable us to switch between frames
        """
        frame = self.frames[cont]
        frame.tkraise()

    # ----------------------- MENU BAR FUNCTIONS---------------------------
    def load_project(self):
        # Open the load project window in the ProjectView
        self.project_view.load_existing_projects()

    def new_project(self):
        print("Quantalysis - New Project button clicked")  # Add this line to check if the button is clicked
        # Open the new project window in the ProjectView
        self.project_view.new_project()
        print("After calling project_view.new_project()")


class Frame1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Frame1", font=("Helvetica", 17))
        label.pack(fill=tk.BOTH)


class Frame2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Frame2", font=("Helvetica", 17))
        label.pack(fill=tk.BOTH)


app = Quantalysis()
app.mainloop()
