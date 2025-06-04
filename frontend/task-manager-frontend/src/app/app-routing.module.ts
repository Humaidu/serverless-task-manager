import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskListComponent } from './admin/task-list/task-list.component';
import { CreateTaskComponent } from './admin/create-task/create-task.component';
import { AssignTaskComponent } from './admin/assign-task/assign-task.component';
import { UserTaskComponent } from './user/user-task/user-task.component';
import { LoginComponent } from './auth/login/login.component';
import { adminAuthGuard } from './guards/admin-auth.guard';
import { userAuthGuard } from './guards/user-auth.guard';
import { UnauthorizedComponent } from './shared/unauthorized/unauthorized.component';
import { SetNewPasswordComponent } from './auth/set-new-password/set-new-password.component';

const routes: Routes = [
  {
    path: 'admin',
    canActivate: [adminAuthGuard],
    children: [
      { path: 'all-tasks', component: TaskListComponent },
      { path: 'create', component: CreateTaskComponent },
      { path: 'assign', component: AssignTaskComponent },
      { path: '', redirectTo: 'all-tasks', pathMatch: 'full' },
    ],
  },
  {
    path: 'user',
    canActivate: [userAuthGuard],
    children: [
      { path: 'user-tasks', component: UserTaskComponent },
      { path: '', redirectTo: 'user-tasks', pathMatch: 'full' },
    ],
  },

  // { path: '', component: TaskListComponent },
  { path: 'login', component: LoginComponent },
  { path: 'set-new-password', component: SetNewPasswordComponent },
  { path: 'unauthorized', component: UnauthorizedComponent },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: 'login' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
