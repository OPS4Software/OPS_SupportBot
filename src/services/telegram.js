const TelegramBot = require('node-telegram-bot-api');
const MessageReceiver = require('./messageReceiver');
const MessageSender = require('./messageSender');
const MessageProcessor = require('./messageProcessor');
const clickUpService = require('./clickup');

class TelegramService {
  constructor() {
    this.bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN, { polling: true });
    this.messageSender = new MessageSender(this.bot);
    this.messageProcessor = new MessageProcessor(this.bot, clickUpService, this.messageSender);
    this.messageReceiver = new MessageReceiver(this.bot, this.messageProcessor);
  }
}

module.exports = new TelegramService();