import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { TaskService } from 'src/app/services/task.service';

@Component({
  selector: 'app-task-list',
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.css']
})
export class TaskListComponent implements OnInit{
  tasks: any[] = []

  constructor(private taskService: TaskService, private toastr: ToastrService){}
  
  async ngOnInit(): Promise<void> {
    try {
      const response = await this.taskService.getAllTasks();
      this.tasks = response.data['tasks'];
      console.log(this.tasks)
    } catch (error) {
      console.error('Failed to fetch tasks', error);
    }
  }

  // async markAsCompleted(taskId: string) {
  //   try {
  //     await this.taskService.updateTaskStatus(taskId, 'completed');
  //     this.toastr.success('Task marked as completed');
  //     const allTasksResponse = await this.taskService.getAllTasks();
  //     this.tasks = allTasksResponse.data.tasks;
  //   } catch (error) {
  //     console.error('Error updating task status:', error);
  //     this.toastr.error('Failed to update task status');
  //   }
  // }
  
  async toggleTaskStatus(task: any) {
    const newStatus = task.status === 'pending' ? 'completed' : 'pending';
  
    try {
      await this.taskService.updateTaskStatus(task.task_id, newStatus);
      this.toastr.success(`Task marked as ${newStatus}`);
      const response = await this.taskService.getAllTasks();
      this.tasks = response.data['tasks'];
    } catch (error) {
      console.error('Error updating task status:', error);
      this.toastr.error('Failed to update task status');
    }
  }
  

}
