import axios from 'axios';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { AuthService } from './auth.service';
import axiosInstance from './axios-instance';


@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private API_URL = environment.API_BASE_URL


  constructor(private auth: AuthService) {}

  async getAllTasks(): Promise<any> {
    return axiosInstance.get('/all')
  }

  createTask(task: any) {
    return axiosInstance.post('/', task)
  }

  updateTaskStatus(task_id: string, status: string) {
    return axiosInstance.post('/update-status', {
      task_id,
      status,
    });
  }
  
  
  assignTask(task_id: string, assigned_to: string): Promise<any> {
    return axiosInstance.post('/assign', {
      task_id,
      assigned_to,
    });
  }

  async getUserTasks(email: string): Promise<any>{
    return axiosInstance.get(`/user?assigned_to=${email}`);
  }
  
  async updateTask(taskId: string, taskData: any) {
    return axiosInstance.post('/update', {
      task_id: taskId,
      ...taskData,
    });
  }

  async deleteTask(taskId: string) {
    return axiosInstance.delete('/delete', {
      params: { task_id: taskId },
    });
  }
  
  }
  
  

