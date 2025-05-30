import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { TaskService } from 'src/app/services/task.service';

interface Task {
  task_id: string;
  title: string;
  description: string;
  deadline: string;
  status: string;
  assigned_to?: string;
}

@Component({
  selector: 'app-assign-task',
  templateUrl: './assign-task.component.html',
  styleUrls: ['./assign-task.component.css'],
})
export class AssignTaskComponent {
  tasks: Task[] = [];
  selectedTaskId: string = '';
  assigneeEmail: string = '';

  task = {
    task_id: '',
    assigned_to: '',
  };

  constructor(
    private taskService: TaskService,
    private router: Router,
    private toastr: ToastrService
  ) {}

  async ngOnInit(): Promise<void> {
    try {
      const response = await this.taskService.getAllTasks();
      console.log('All tasks response:', response.data);
      this.tasks = Array.isArray(response.data)
        ? response.data
        : response.data.tasks;
    } catch (error) {
      console.error('Failed to fetch tasks', error);
    }
  }

  async assignTask() {
    if (!this.selectedTaskId || !this.assigneeEmail) {
      this.toastr.error('Please select a task and provide an email.');
      return;
    }
    try {
      await this.taskService.assignTask(
        this.selectedTaskId,
        this.assigneeEmail
      );
      this.toastr.success('Task Assigned Successfully');

      // Optionally reload tasks or update UI accordingly
      const allTasksResponse = await this.taskService.getAllTasks();
      this.tasks = allTasksResponse.data.tasks;
      this.task = {
        task_id: '',
        assigned_to: ''
      };
      this.router.navigate(['/admin'])
    } catch (error) {
      console.error('Error assigning task:', error);
      this.toastr.success('Failed to assign task.');
    }
  }
}
