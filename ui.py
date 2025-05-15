import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class TaskManagerUI(tk.Tk):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        
        self.title("Gerenciador de Tarefas")
        self.geometry("1000x600")
        
        self.create_widgets()
        self.refresh_ui()
    
    def create_widgets(self):
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cabeçalho
        header = ttk.Frame(self.main_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header, text="Gerenciador de Tarefas", font=('Arial', 16)).pack(side=tk.LEFT)
        
        add_btn = ttk.Button(header, text="+ Nova Tarefa", command=self.show_add_task_dialog)
        add_btn.pack(side=tk.RIGHT)
        
        # Quadro de colunas
        self.columns_frame = ttk.Frame(self.main_frame)
        self.columns_frame.pack(fill=tk.BOTH, expand=True)
        
        # Criar colunas
        self.column_uis = {}
        for column in self.task_manager.columns:
            col_frame = ttk.LabelFrame(self.columns_frame, text=column)
            col_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            # Lista de tarefas na coluna
            task_list = tk.Listbox(col_frame, selectmode=tk.SINGLE)
            task_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Botões de ação
            btn_frame = ttk.Frame(col_frame)
            btn_frame.pack(fill=tk.X, pady=(0, 5))
            
            edit_btn = ttk.Button(btn_frame, text="Editar", 
                                command=lambda c=column: self.edit_selected_task(c))
            edit_btn.pack(side=tk.LEFT, expand=True)
            
            delete_btn = ttk.Button(btn_frame, text="Excluir", 
                                  command=lambda c=column: self.delete_selected_task(c))
            delete_btn.pack(side=tk.LEFT, expand=True)
            
            # Para colunas que não são a última, adicione um botão para mover para a direita
            if column != self.task_manager.columns[-1]:
                next_col = self.task_manager.columns[self.task_manager.columns.index(column) + 1]
                move_btn = ttk.Button(btn_frame, text=f"→ {next_col}", 
                                     command=lambda c=column: self.move_selected_task(c, 1))
                move_btn.pack(side=tk.LEFT, expand=True)
            
            # Para colunas que não são a primeira, adicione um botão para mover para a esquerda
            if column != self.task_manager.columns[0]:
                prev_col = self.task_manager.columns[self.task_manager.columns.index(column) - 1]
                move_btn = ttk.Button(btn_frame, text=f"← {prev_col}", 
                                     command=lambda c=column: self.move_selected_task(c, -1))
                move_btn.pack(side=tk.LEFT, expand=True)
            
            self.column_uis[column] = {
                'frame': col_frame,
                'task_list': task_list
            }
    
    def refresh_ui(self):
        for column, ui in self.column_uis.items():
            ui['task_list'].delete(0, tk.END)
            
            tasks = self.task_manager.get_tasks_by_column(column)
            for task in tasks:
                ui['task_list'].insert(tk.END, f"{task['title']} (Prioridade: {task['priority']})")
    
    def show_add_task_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Nova Tarefa")
        
        # Campos do formulário
        ttk.Label(dialog, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Descrição:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        desc_entry = tk.Text(dialog, width=40, height=5)
        desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Coluna:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        column_combo = ttk.Combobox(dialog, values=self.task_manager.columns)
        column_combo.grid(row=2, column=1, padx=5, pady=5)
        column_combo.current(0)
        
        ttk.Label(dialog, text="Prioridade:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        priority_combo = ttk.Combobox(dialog, values=["low", "medium", "high"])
        priority_combo.grid(row=3, column=1, padx=5, pady=5)
        priority_combo.current(1)
        
        ttk.Label(dialog, text="Data de Vencimento (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        due_entry = ttk.Entry(dialog, width=40)
        due_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Botões
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        def add_task():
            title = title_entry.get()
            description = desc_entry.get("1.0", tk.END).strip()
            column = column_combo.get()
            priority = priority_combo.get()
            due_date = due_entry.get() if due_entry.get() else None
            
            if not title:
                messagebox.showerror("Erro", "O título da tarefa é obrigatório!")
                return
            
            self.task_manager.add_task(
                title=title,
                description=description,
                column=column,
                priority=priority,
                due_date=due_date
            )
            
            self.refresh_ui()
            dialog.destroy()
        
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Adicionar", command=add_task).pack(side=tk.LEFT, padx=5)
    
    def get_selected_task(self, column_name):
        task_list = self.column_uis[column_name]['task_list']
        selection = task_list.curselection()
        
        if not selection:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa primeiro.")
            return None
        
        index = selection[0]
        tasks = self.task_manager.get_tasks_by_column(column_name)
        
        if index >= len(tasks):
            return None
        
        return tasks[index]
    
    def edit_selected_task(self, column_name):
        task = self.get_selected_task(column_name)
        if not task:
            return
        
        dialog = tk.Toplevel(self)
        dialog.title("Editar Tarefa")
        
        # Campos do formulário
        ttk.Label(dialog, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.insert(0, task['title'])
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Descrição:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        desc_entry = tk.Text(dialog, width=40, height=5)
        desc_entry.insert("1.0", task['description'])
        desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Coluna:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        column_combo = ttk.Combobox(dialog, values=self.task_manager.columns)
        column_combo.grid(row=2, column=1, padx=5, pady=5)
        column_combo.set(task['column'])
        
        ttk.Label(dialog, text="Prioridade:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        priority_combo = ttk.Combobox(dialog, values=["low", "medium", "high"])
        priority_combo.grid(row=3, column=1, padx=5, pady=5)
        priority_combo.set(task['priority'])
        
        due_date = task['due_date'] if task['due_date'] else ""
        ttk.Label(dialog, text="Data de Vencimento (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        due_entry = ttk.Entry(dialog, width=40)
        due_entry.insert(0, due_date)
        due_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Botões
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        def update_task():
            updates = {
                'title': title_entry.get(),
                'description': desc_entry.get("1.0", tk.END).strip(),
                'column': column_combo.get(),
                'priority': priority_combo.get(),
                'due_date': due_entry.get() if due_entry.get() else None
            }
            
            if not updates['title']:
                messagebox.showerror("Erro", "O título da tarefa é obrigatório!")
                return
            
            self.task_manager.update_task(task['id'], **updates)
            self.refresh_ui()
            dialog.destroy()
        
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Atualizar", command=update_task).pack(side=tk.LEFT, padx=5)
    
    def delete_selected_task(self, column_name):
        task = self.get_selected_task(column_name)
        if not task:
            return
        
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir a tarefa '{task['title']}'?"):
            self.task_manager.delete_task(task['id'])
            self.refresh_ui()
    
    def move_selected_task(self, column_name, direction):
        task = self.get_selected_task(column_name)
        if not task:
            return
        
        current_index = self.task_manager.columns.index(column_name)
        new_index = current_index + direction
        
        if 0 <= new_index < len(self.task_manager.columns):
            new_column = self.task_manager.columns[new_index]
            self.task_manager.move_task(task['id'], new_column)
            self.refresh_ui()
