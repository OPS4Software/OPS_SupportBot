const logger = require('../config/logger');
const axios = require('axios');

class MessageProcessor {
  constructor(bot, clickUpService, messageSender) {
    this.bot = bot;
    this.clickUpService = clickUpService;
    this.messageSender = messageSender;
  }

  async processMessage(msg) {
    try {
      const photo = msg.photo;
      const text = msg.caption;

      if (!photo || !text) {
        logger.info('Skipping message - no photo or caption');
        return;
      }

      const id = this.extractId(text);
      if (!id) {
        logger.info('Skipping message - no valid ID found in caption');
        return;
      }

      const imageFile = photo[photo.length - 1];
      const fileLink = await this.bot.getFileLink(imageFile.file_id);
      
      logger.info(`Processing message with ID: ${id}`);
      
      // Download image buffer
      const imageResponse = await axios.get(fileLink, { responseType: 'arraybuffer' });
      const imageBuffer = Buffer.from(imageResponse.data);

      // Create ClickUp task with uploaded image
      const task = await this.clickUpService.createTask(id, imageBuffer, `image_${id}.jpg`);

      // Forward to destination chats
      await this.messageSender.broadcastImage(imageFile.file_id, `🆔 ID: ${id}`);

      logger.info(`Successfully processed message with ID: ${id}`);
    } catch (error) {
      logger.error('Error in processMessage:', {
        error: error.message,
        messageId: msg.message_id,
        chatId: msg.chat.id
      });
      throw error; // Re-throw to be handled by the error handler
    }
  }

  extractId(text) {
    const match = text.match(/\b([A-Za-z0-9]+)\b/);
    return match ? match[1] : null;
  }

  async handleError(error) {
    logger.error('Handling error in MessageProcessor:', error);
    await this.messageSender.broadcastError(error);
  }
}

module.exports = MessageProcessor;