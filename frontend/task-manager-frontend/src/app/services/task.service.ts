import axios from 'axios';
import { Injectable } from '@angular/core';
import axiosInstance from './axios-instance';

@Injectable({
  providedIn: 'root' 
})
export class TaskService {

  constructor() {}

  /**
   * Fetch all tasks from the backend.
   * Typically used by admins to view the complete task list.
   * 
   * @returns Promise resolving to a list of tasks.
   */
  async getAllTasks(): Promise<any> {
    return axiosInstance.get('/all');
  }

  /**
   * Create a new task.
   * 
   * @param task - An object containing task details (title, description, etc.)
   * @returns Promise resolving to the created task or success response.
   */
  createTask(task: any) {
    return axiosInstance.post('/', task);
  }

  /**
   * Update the status of a task.
   * 
   * @param task_id - The ID of the task to update.
   * @param status - The new status (e.g., "completed", "in-progress").
   * @returns Promise resolving to a success response.
   */
  updateTaskStatus(task_id: string, status: string) {
    return axiosInstance.post('/update-status', {
      task_id,
      status,
    });
  }

  /**
   * Assign a task to a user.
   * 
   * @param task_id - The ID of the task.
   * @param assigned_to - Email or ID of the user to assign the task to.
   * @returns Promise resolving to a success response.
   */
  assignTask(task_id: string, assigned_to: string): Promise<any> {
    return axiosInstance.post('/assign', {
      task_id,
      assigned_to,
    });
  }

  /**
   * Get tasks assigned to a specific user.
   * 
   * @param email - The email of the assigned user.
   * @returns Promise resolving to a list of user-specific tasks.
   */
  async getUserTasks(email: string): Promise<any> {
    return axiosInstance.get(`/user?assigned_to=${email}`);
  }

  /**
   * Update an existing task with new data.
   * 
   * @param taskId - ID of the task to update.
   * @param taskData - Object containing fields to update.
   * @returns Promise resolving to a success response.
   */
  async updateTask(taskId: string, taskData: any) {
    return axiosInstance.post('/update', {
      task_id: taskId,
      ...taskData,
    });
  }

  /**
   * Delete a task by its ID.
   * 
   * @param taskId - The ID of the task to delete.
   * @returns Promise resolving to a success response.
   */
  async deleteTask(taskId: string) {
    return axiosInstance.delete('/delete', {
      params: { task_id: taskId },
    });
  }
}


