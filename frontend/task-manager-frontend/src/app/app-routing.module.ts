import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskListComponent } from './pages/task-list/task-list.component';
import { CreateTaskComponent } from './pages/create-task/create-task.component';
import { AssignTaskComponent } from './pages/assign-task/assign-task.component';

const routes: Routes = [
  { path: '', component: TaskListComponent },
  { path: 'create', component: CreateTaskComponent },
  { path: 'create', component: CreateTaskComponent },
  { path: 'assign', component: AssignTaskComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
