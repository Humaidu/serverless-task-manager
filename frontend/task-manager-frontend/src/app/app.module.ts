import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { ToastrModule } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TaskListComponent } from './pages/task-list/task-list.component';
import { CreateTaskComponent } from './pages/create-task/create-task.component';
import { UpdateTaskComponent } from './pages/update-task/update-task.component';

@NgModule({
  declarations: [
    AppComponent,
    TaskListComponent,
    CreateTaskComponent,
    UpdateTaskComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
