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

  updateTaskStatus(taskId: string, status: string) {
    return axios.put(`${this.API_URL}/update-status/${taskId}`, { status }, {
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
