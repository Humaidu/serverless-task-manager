import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import axios from 'axios';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private API_URL = environment.API_BASE_URL


  constructor(private auth: AuthService) {}

  async getAllTasks(): Promise<any> {
    const token = localStorage.getItem('authToken'); // or 'access_token', depending on your app
    return axios.get(`${this.API_URL}/all`, {
      headers: {
        Authorization: token,
      },
    });
  }

  createTask(task: any) {
    const token = this.auth.getToken();
    return axios.post(this.API_URL, task, {
      headers: { 
        'Content-Type': 'application/json' ,
        Authorization: token,
      }
    });
  }

  updateTaskStatus(task_id: string, status: string) {
    const token = this.auth.getToken();
    return axios.post(`${this.API_URL}/update-status`, {
      task_id,
      status
    }, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: token,
      },
    });
  }
  
  
  assignTask(task_id: string, assigned_to: string): Promise<any> {
    const token = this.auth.getToken();
    return axios.post(`${this.API_URL}/assign`, {
      task_id,
      assigned_to,
    },{
      headers: {
        'Content-Type': 'application/json',
        Authorization: token,
     },   
   });
  }

  async getUserTasks(email: string): Promise<any>{
    const token = this.auth.getToken();
    const res = await axios.get(`${this.API_URL}/user?assigned_to=${email}`, {
      headers: {
        Authorization: token,
      },
    });
    return res.data
  }
  
  async updateTask(taskId: string, taskData: any) {
    const token = this.auth.getToken();
    return axios.post(`${this.API_URL}/update`, {
      task_id: taskId,
      ...taskData
    }, {
      headers: {
         'Content-Type': 'application/json',
         Authorization: token,
      }
    });
  }

  async deleteTask(taskId: string) {
    const token = this.auth.getToken();
    return axios.delete(`${this.API_URL}/delete`, {
      params: { task_id: taskId },
      headers: {
        Authorization: token,
      },
    });
  }
  
  
}
