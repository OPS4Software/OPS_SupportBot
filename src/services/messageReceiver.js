const logger = require('../config/logger');
const { sourceChats } = require('../config/chats');

class MessageReceiver {
  constructor(bot, messageProcessor) {
    this.bot = bot;
    this.messageProcessor = messageProcessor;
    this.setupMessageHandler();
  }

  setupMessageHandler() {
    this.bot.on('message', async (msg) => {
      if (!this.isValidSourceChat(msg.chat.id.toString())) return;
      
      try {
        await this.messageProcessor.processMessage(msg);
      } catch (error) {
        logger.error('Error processing message:', error);
        await this.messageProcessor.handleError(error);
      }
    });
  }

  isValidSourceChat(chatId) {
    return sourceChats.includes(chatId);
  }
}

module.exports = MessageReceiver;