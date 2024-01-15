const { format } = require('date-fns');

const logger = async (req, res, next) => {
    const dateTime = `${format(new Date(), 'yyyyMMdd HH:mm:ss')}`;
    console.log(`${dateTime}\t${req.method}\t${req.path}\t`);
    next();
}

module.exports = logger;
