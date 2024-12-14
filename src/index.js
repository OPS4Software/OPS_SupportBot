require('dotenv').config();
const logger = require('./config/logger');
const telegramService = require('./services/telegram');

process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception:', error);
  process.exit(1);
});

process.on('unhandledRejection', (error) => {
  logger.error('Unhandled Rejection:', error);
});

logger.info('Bot started successfully');