from task_manager import TaskManager
from ui import TaskManagerUI

def main():
    # Inicializa o gerenciador com o arquivo XML
    manager = TaskManager("tasks.xml")
    
    # Carrega os dados existentes
    manager.load_tasks()
    
    # Inicializa a interface gráfica
    app = TaskManagerUI(manager)
    app.mainloop()

if __name__ == "__main__":
    main()
