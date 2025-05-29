import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskListComponent } from './pages/task-list/task-list.component';
import { CreateTaskComponent } from './pages/create-task/create-task.component';
import { AssignTaskComponent } from './pages/assign-task/assign-task.component';
import { UserTaskComponent } from './pages/user-task/user-task.component';
import { LoginComponent } from './pages/login/login.component';

const routes: Routes = [
  { path: '', component: TaskListComponent },
  { path: 'create', component: CreateTaskComponent },
  { path: 'create', component: CreateTaskComponent },
  { path: 'assign', component: AssignTaskComponent },
  { path: 'my-tasks', component: UserTaskComponent },
  { path: 'login', component: LoginComponent },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
