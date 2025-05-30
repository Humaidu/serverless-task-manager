import { Component } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { AuthService } from 'src/app/services/auth.service';
import { TaskService } from 'src/app/services/task.service';

@Component({
  selector: 'app-user-task',
  templateUrl: './user-task.component.html',
  styleUrls: ['./user-task.component.css']
})
export class UserTaskComponent {
  email: string | null = null;
  tasks: any[] = [];

  constructor(
    private taskService: TaskService, 
    private toastr: ToastrService,
     private auth: AuthService
  ){}

  async ngOnInit(): Promise<void> {
    this.email = this.auth.getUserEmail();
    try {
      if (this.email){
        const response = await this.taskService.getUserTasks(this.email);
        this.tasks = response.data['tasks'];
      }
      else{
        this.toastr.error("Unable to determine logged-in use")
      }
    } catch (error) {
      console.error('Failed to load tasks for user', error);
      this.toastr.error('Failed to load tasks for user, ${error}')
    }
  }


  
}
