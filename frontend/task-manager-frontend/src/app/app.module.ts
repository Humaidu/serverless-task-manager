import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { ToastrModule } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TaskListComponent } from './admin/task-list/task-list.component';
import { CreateTaskComponent } from './admin/create-task/create-task.component';
import { UpdateTaskComponent } from './admin/update-task/update-task.component';
import { AssignTaskComponent } from './admin/assign-task/assign-task.component';
import { UserTaskComponent } from './user/user-task/user-task.component';
import { LoginComponent } from './auth/login/login.component';
import { AuthService } from './services/auth.service';
import { DashboardComponent } from './admin/dashboard/dashboard.component';
import { UnauthorizedComponent } from './shared/unauthorized/unauthorized.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { SetNewPasswordComponent } from './auth/set-new-password/set-new-password.component';

@NgModule({
  declarations: [
    AppComponent,
    TaskListComponent,
    CreateTaskComponent,
    UpdateTaskComponent,
    AssignTaskComponent,
    UserTaskComponent,
    LoginComponent,
    DashboardComponent,
    UnauthorizedComponent,
    NavbarComponent,
    SetNewPasswordComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot(),
  ],
  providers: [AuthService],
  bootstrap: [AppComponent],
})
export class AppModule {}
