import { Component } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { TaskService } from 'src/app/services/task.service';

@Component({
  selector: 'app-user-task',
  templateUrl: './user-task.component.html',
  styleUrls: ['./user-task.component.css']
})
export class UserTaskComponent {
  userEmail: string = 'h@gmail.com'; // eventually from Cognito
  tasks: any[] = [];

  constructor(private taskService: TaskService, private toastr: ToastrService){}

  async ngOnInit(): Promise<void> {
    try {
      const response = await this.taskService.getUserTasks(this.userEmail);
      this.tasks = response.data['tasks'];
      console.log(this.tasks)
    } catch (error) {
      console.error('Failed to load tasks for user', error);
      this.toastr.error('Failed to load tasks for user, ${error}')
    }
  }
}
