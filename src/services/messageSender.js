const logger = require('../config/logger');
const { destinationChats } = require('../config/chats');

class MessageSender {
  constructor(bot) {
    this.bot = bot;
  }

  async broadcastImage(fileId, caption) {
    const results = await Promise.allSettled(
      destinationChats.map(chatId => 
        this.bot.sendPhoto(chatId, fileId, { caption })
      )
    );

    const failures = results.filter(result => result.status === 'rejected');
    if (failures.length > 0) {
      logger.error('Failed to send messages to some chats:', {
        failureCount: failures.length,
        errors: failures.map(f => f.reason.message)
      });
    }
  }

  async broadcastError(error) {
    const errorMessage = `❌ Error occurred:\n${error.message}`;
    
    try {
      const results = await Promise.allSettled(
        destinationChats.map(chatId => 
          this.bot.sendMessage(chatId, errorMessage)
        )
      );

      const failures = results.filter(result => result.status === 'rejected');
      if (failures.length > 0) {
        logger.error('Failed to send error messages to some chats:', {
          failureCount: failures.length,
          errors: failures.map(f => f.reason.message)
        });
      }
    } catch (err) {
      logger.error('Critical error in broadcastError:', err);
    }
  }
}

module.exports = MessageSender;