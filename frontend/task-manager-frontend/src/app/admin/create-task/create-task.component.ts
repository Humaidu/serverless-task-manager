import { Component } from '@angular/core';
import { TaskService } from 'src/app/services/task.service';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';


@Component({
  selector: 'app-create-task',
  templateUrl: './create-task.component.html',
  styleUrls: ['./create-task.component.css']
})
export class CreateTaskComponent {
  task = {
    title: '',
    description: '',
    assigned_to: '',
    deadline: ''
  };

  constructor(
    private taskService: TaskService,
    private router: Router,
    private toastr: ToastrService
  ){}

  createTask() {
    this.taskService.createTask(this.task)
      .then(() => { 
        this.toastr.success('Task Created Successfully');
        this.task = {
          title: '',
          description: '',
          assigned_to: '',
          deadline: ''
        };
        this.router.navigate(['/admin'])
      })
      .catch(err => {
        console.log(err);
        this.toastr.error('Failed to create task');
      })
  }
}
