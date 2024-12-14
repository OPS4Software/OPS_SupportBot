const axios = require('axios');
const FormData = require('form-data');
const logger = require('../config/logger');

class ClickUpService {
  constructor() {
    this.token = process.env.CLICKUP_TOKEN;
    this.listId = process.env.CLICKUP_LIST_ID;
    this.client = axios.create({
      baseURL: 'https://api.clickup.com/api/v2',
      headers: {
        'Authorization': this.token
      }
    });
  }

  async uploadImage(taskId, imageBuffer, filename) {
    try {
      const formData = new FormData();
      formData.append('attachment', imageBuffer, {
        filename: filename,
        contentType: 'image/jpeg'
      });

      const uploadResponse = await this.client.post(
        `/task/${taskId}/attachment`,
        formData,
        {
          headers: {
            ...formData.getHeaders()
          }
        }
      );

      return uploadResponse.data;
    } catch (error) {
      logger.error('ClickUp image upload failed:', {
        error: error.response?.data || error.message,
        taskId,
        filename
      });
      throw new Error('Failed to upload image to ClickUp');
    }
  }

  async createTask(id, imageBuffer, filename) {
    try {
      // First create the task
      const taskResponse = await this.client.post(`/list/${this.listId}/task`, {
        name: `Image Processing Task - ${id}`,
        description: `Image Reference ID: ${id}`,
        priority: 3,
        status: 'to do'
      });

      const taskId = taskResponse.data.id;
      logger.info(`Created ClickUp task: ${taskId}`);

      // Then upload and attach the image
      await this.uploadImage(taskId, imageBuffer, filename);
      logger.info(`Uploaded image to task: ${taskId}`);
      
      return taskResponse.data;
    } catch (error) {
      logger.error('ClickUp task creation failed:', {
        error: error.response?.data || error.message,
        id
      });
      throw new Error(`Failed to create ClickUp task: ${error.response?.data?.err || error.message}`);
    }
  }
}

module.exports = new ClickUpService();