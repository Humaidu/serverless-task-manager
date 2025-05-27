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
  // assignTask(data: { task_id: string; email: string }): Promise<any> {
  //   return fetch(`${this.API_URL}/tasks/assign`, {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify(data)
  //   }).then(res => res.json());
  // }

  // // assignTask(task_id: string, email: string): Promise<any> {
  // //   return this.http.post(`${this.API_URL}/tasks/assign`, { task_id, email }).toPromise();
  // // }
  
  
}
