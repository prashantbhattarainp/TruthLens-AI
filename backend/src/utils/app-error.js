class AppError extends Error {
  constructor({ statusCode, code, message, metadata = {} }) {
    super(message);
    this.name = 'AppError';
    this.statusCode = statusCode;
    this.code = code;
    this.metadata = metadata;
  }
}

module.exports = AppError;
