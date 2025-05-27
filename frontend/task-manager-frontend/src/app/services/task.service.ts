import { Injectable } from '@angular/core';
import axios from 'axios';

const API_URL = 'https://p8ej9c9pi1.execute-api.eu-west-1.amazonaws.com/prod/tasks';

@Injectable({
  providedIn: 'root'
})
export class TaskService {

  // getTasks() {
  //   return axios.get(`${API_URL}/all`, {
  //     headers: { /* Add Authorization later if needed */ }
  //   });
  // }

  async getAllTasks(): Promise<any> {
    return axios.get(`${API_URL}/all`);
  }

  createTask(task: any) {
    return axios.post(API_URL, task, {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  updateTaskStatus(taskId: string, status: string) {
    return axios.put(`${API_URL}/${taskId}`, { status }, {
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
