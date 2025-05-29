import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { TaskService } from 'src/app/services/task.service';
import { Modal } from 'bootstrap';  // Import Modal class

@Component({
  selector: 'app-task-list',
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.css']
})
export class TaskListComponent implements OnInit{
  updateModal: Modal | undefined;
  tasks: any[] = []
  selectedTask: any = {};


  constructor(private taskService: TaskService, private toastr: ToastrService){}
  
  async ngOnInit(): Promise<void> {
    await this.loadAllTasks()
  }

  async loadAllTasks() {
    try {
      const response = await this.taskService.getAllTasks();
      this.tasks = response.data['tasks'] || [];
    } catch (error) {
      console.error('Failed to fetch tasks', error);
    }
  }

  openUpdateModal(task: any) {
    this.selectedTask = { ...task }; 
    const modalElement = document.getElementById('updateTaskModal');
    if (modalElement) {
      this.updateModal = new Modal(modalElement);
      this.updateModal.show();
    }
  }
  
  async submitUpdate() {
    const task_id = this.selectedTask?.task_id;

    if (!task_id) {
      this.toastr.error('No task selected!');
      return;
    }

    try {
      await this.taskService.updateTask(task_id, {
        title: this.selectedTask.title,
        description: this.selectedTask.description,
        status: this.selectedTask.status
      });
      this.toastr.success('Task updated!');
      await this.loadAllTasks();
      this.updateModal?.hide();  // Hide modal after success
    } catch (err) {
      console.error(err);
      this.toastr.error('Failed to update task');
    }
  }

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

  async deleteTask(taskId: string) {
    if (confirm('Are you sure you want to delete this task?')) {
      try {
        await this.taskService.deleteTask(taskId);
        this.toastr.success('Task deleted!');
        await this.loadAllTasks();
      } catch (err) {
        console.error(err);
        this.toastr.error('Failed to delete task');
      }
    }
  }
  

}
