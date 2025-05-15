import xml.etree.ElementTree as ET
from datetime import datetime

class TaskManager:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tasks = []
        self.columns = ["Backlog", "A Fazer", "Em Progresso", "Concluído"]
        
    def load_tasks(self):
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            self.tasks = []
            
            for task_elem in root.findall('task'):
                task = {
                    'id': task_elem.get('id'),
                    'title': task_elem.find('title').text,
                    'description': task_elem.find('description').text,
                    'column': task_elem.find('column').text,
                    'created': task_elem.find('created').text,
                    'due_date': task_elem.find('due_date').text if task_elem.find('due_date') is not None else None,
                    'priority': task_elem.find('priority').text if task_elem.find('priority') is not None else 'medium'
                }
                self.tasks.append(task)
                
        except (ET.ParseError, FileNotFoundError):
            # Se o arquivo não existe ou está vazio, comece com uma lista vazia
            self.tasks = []
    
    def save_tasks(self):
        root = ET.Element('tasks')
        
        for task in self.tasks:
            task_elem = ET.SubElement(root, 'task')
            task_elem.set('id', task['id'])
            
            ET.SubElement(task_elem, 'title').text = task['title']
            ET.SubElement(task_elem, 'description').text = task['description']
            ET.SubElement(task_elem, 'column').text = task['column']
            ET.SubElement(task_elem, 'created').text = task['created']
            
            if task['due_date']:
                ET.SubElement(task_elem, 'due_date').text = task['due_date']
            
            if task['priority']:
                ET.SubElement(task_elem, 'priority').text = task['priority']
        
        tree = ET.ElementTree(root)
        tree.write(self.xml_file, encoding='utf-8', xml_declaration=True)
    
    def add_task(self, title, description, column="Backlog", due_date=None, priority="medium"):
        task_id = str(len(self.tasks) + 1)
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        new_task = {
            'id': task_id,
            'title': title,
            'description': description,
            'column': column,
            'created': created,
            'due_date': due_date,
            'priority': priority
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task
    
    def update_task(self, task_id, **kwargs):
        for task in self.tasks:
            if task['id'] == task_id:
                for key, value in kwargs.items():
                    if key in task:
                        task[key] = value
                self.save_tasks()
                return task
        return None
    
    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.save_tasks()
    
    def move_task(self, task_id, new_column):
        return self.update_task(task_id, column=new_column)
    
    def get_tasks_by_column(self, column_name):
        return [task for task in self.tasks if task['column'] == column_name]
    
    def get_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
