import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import axios from 'axios';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private API_URL = environment.API_BASE_URL

  async getAllTasks(): Promise<any> {
    return axios.get(`${this.API_URL}/all`);
  }

  createTask(task: any) {
    return axios.post(this.API_URL, task, {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  updateTaskStatus(task_id: string, status: string) {
    return axios.post(`${this.API_URL}/update-status`, {
      task_id,
      status
    });
  }
  
  
  assignTask(task_id: string, assigned_to: string): Promise<any> {
    return axios.post(`${this.API_URL}/assign`, {
      task_id,
      assigned_to,
    });
  }
  
  async getUserTasks(email: string): Promise<any>{
    return await axios.get(`${this.API_URL}/user`, {
      params: { assigned_to: email }
    });
  }
  
  async updateTask(taskId: string, taskData: any) {
    return axios.post(`${this.API_URL}/update`, {
      task_id: taskId,
      ...taskData
    }, {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // async updateTask2(taskId: string, data: any) {
  //   return axios.post(`${this.API_URL}/update`, data);
  // }
  

  async deleteTask(taskId: string) {
    return axios.delete(`${this.API_URL}/delete`, {
      params: { task_id: taskId }
    });
  }
  
  
}
