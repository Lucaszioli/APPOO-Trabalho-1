import tkinter
import tkinter.messagebox as messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
customtkinter.set_default_color_theme("app/themes/vaporwave.json")  # Themes: "blue", "green", "dark-blue"

class PaginaInicial(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento Acadêmico")
        self.geometry("1000x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        sidebar = customtkinter.CTkFrame(self, width=180, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(4, weight=1)

        customtkinter.CTkLabel(sidebar, text="HUB Acadêmico", font=customtkinter.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=(20,10))
        customtkinter.CTkButton(sidebar, text="Semestres").grid(row=1, column=0, padx=20, pady=10)
        customtkinter.CTkButton(sidebar, text="Disciplinas").grid(row=2, column=0, padx=20, pady=10)
        customtkinter.CTkButton(sidebar, text="Atividades").grid(row=3, column=0, padx=20, pady=10)

        # Main
        main = customtkinter.CTkFrame(self)
        main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        main.grid_columnconfigure(0, weight=1)

"""         # Semestre
        customtkinter.CTkLabel(main, text="Semestre:", anchor="w").grid(row=0, column=0, sticky="w", padx=(10,0))
        self.cmb_semester = customtkinter.CTkComboBox(main, values=[s.term for s in self.manager.semesters], command=self.on_semester_selected)
        self.cmb_semester.grid(row=1, column=0, sticky="ew", padx=(10,0))
        self.cmb_semester.configure(state="readonly")
        customtkinter.CTkButton(main, text="Adicionar Semestre", command=self.add_semester).grid(row=1, column=1, padx=10)

        # Disciplina
        customtkinter.CTkLabel(main, text="Disciplina:", anchor="w").grid(row=2, column=0, sticky="w", pady=(20,0), padx=(10,0))
        self.cmb_discipline = customtkinter.CTkComboBox(main, values=[], command=self.on_discipline_selected)
        self.cmb_discipline.grid(row=3, column=0, sticky="ew", padx=(10,0))
        self.cmb_discipline.configure(state="readonly")
        customtkinter.CTkButton(main, text="Adicionar Disciplina", command=self.add_discipline).grid(row=3, column=1, padx=10)

        # Atividade
        customtkinter.CTkLabel(main, text="Atividade:", anchor="w").grid(row=4, column=0, sticky="w", pady=(20,0), padx=(10,0))
        self.cmb_activity = customtkinter.CTkComboBox(main, values=[], command=self.on_activity_selected)
        self.cmb_activity.grid(row=5, column=0, sticky="ew", padx=(10,0))
        self.cmb_activity.configure(state="readonly")
        customtkinter.CTkButton(main, text="Adicionar Atividade", command=self.add_activity).grid(row=5, column=1, padx=10)

        # Detalhes
        self.txt_details = customtkinter.CTkTextbox(main, width=400, height=200, corner_radius=10)
        self.txt_details.configure(state="normal")
        self.txt_details.grid(row=6, column=0, columnspan=2, pady=(20,20), sticky="nsew", padx=10)

        # inicia seleção
        if self.manager.semesters:
            self.cmb_semester.set(self.manager.semesters[0].term)
            self.on_semester_selected(self.manager.semesters[0].term) """

""" def on_semester_selected(self, term):
        semester = self.manager.get_semester(term)
        if semester:
            self.cmb_discipline.configure(values=[d.name for d in semester.disciplines], state="normal")
            # limpa atividades
            self.cmb_activity.configure(values=[], state="disabled")
            self.txt_details.delete("0.0", "end")
            if semester.disciplines:
                first = semester.disciplines[0].name
                self.cmb_discipline.set(first)
                self.on_discipline_selected(first)

    def on_discipline_selected(self, name):
        term = self.cmb_semester.get()
        discipline = self.manager.get_semester(term).get_discipline(name)
        if discipline:
            self.cmb_activity.configure(values=[a.title for a in discipline.activities], state="normal")
            self.txt_details.delete("0.0", "end")
            if discipline.activities:
                first = discipline.activities[0].title
                self.cmb_activity.set(first)
                self.on_activity_selected(first)

    def on_activity_selected(self, title):
        term = self.cmb_semester.get()
        disc = self.cmb_discipline.get()
        activity = None
        semester = self.manager.get_semester(term)
        if semester:
            discipline = semester.get_discipline(disc)
            if discipline:
                for a in discipline.activities:
                    if a.title == title:
                        activity = a
                        break
        if activity:
            self.txt_details.delete("0.0", "end")
            self.txt_details.insert("0.0", f"Detalhes da Atividade:\n\nTítulo: {activity.title}\nStatus: {activity.status}\n")

    def add_semester(self):
        dialog = customtkinter.CTkInputDialog(text="Nome do novo semestre:", title="Adicionar Semestre")
        new_term = dialog.get_input()
        if new_term:
            if self.manager.get_semester(new_term):
                messagebox.showwarning("Aviso", "Semestre já existe.")
            else:
                self.manager.add_semester(new_term)
                values = [s.term for s in self.manager.semesters]
                self.cmb_semester.configure(values=values)

    def add_discipline(self):
        term = self.cmb_semester.get()
        semester = self.manager.get_semester(term)
        if not semester:
            messagebox.showwarning("Aviso", "Selecione um semestre primeiro.")
            return
        dialog = customtkinter.CTkInputDialog(text="Nome da nova disciplina:", title="Adicionar Disciplina")
        new_disc = dialog.get_input()
        if new_disc:
            semester.add_discipline(new_disc)
            self.on_semester_selected(term)

    def add_activity(self):
        term = self.cmb_semester.get()
        disc = self.cmb_discipline.get()
        semester = self.manager.get_semester(term)
        if not semester or not semester.get_discipline(disc):
            messagebox.showwarning("Aviso", "Selecione semestre e disciplina primeiro.")
            return
        dialog = customtkinter.CTkInputDialog(text="Nome da nova atividade:", title="Adicionar Atividade")
        new_act = dialog.get_input()
        if new_act:
            discipline = semester.get_discipline(disc)
            discipline.add_activity(new_act)
            self.on_discipline_selected(disc) """