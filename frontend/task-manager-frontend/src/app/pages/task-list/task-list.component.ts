import { Component, OnInit } from '@angular/core';
import { TaskService } from 'src/app/services/task.service';

@Component({
  selector: 'app-task-list',
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.css']
})
export class TaskListComponent implements OnInit{
  tasks: any[] = []

  constructor(private taskService: TaskService){}
  
  async ngOnInit(): Promise<void> {
    try {
      const response = await this.taskService.getAllTasks();
      this.tasks = response.data['tasks'];
      console.log(this.tasks)
    } catch (error) {
      console.error('Failed to fetch tasks', error);
    }
  }

  markCompleted(taskId: string){
    this.taskService.updateTaskStatus(taskId, 'completed')
      .then(() => alert('Task Updated'))
      .catch(err => console.error(err));
  }

}
