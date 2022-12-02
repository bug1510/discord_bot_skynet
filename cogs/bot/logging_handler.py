
    async def init_logger(self):
        #logging
        #check log folder

        if not os.path.exists(self.logpath):
            os.makedirs(self.logpath)

        self.logger = logging.getLogger('SkyNet-Core')
        self.logger.setLevel(logging.INFO)

        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s | %(message)s')

        rotatinglogs = TimedRotatingFileHandler(
            filename=self.logpath + '/skynet_bot.log',
            when="midnight",
            interval=1,
            backupCount=5
            )
        rotatinglogs.setLevel(logging.INFO)
        rotatinglogs.setFormatter(format)

        self.logger.addHandler(rotatinglogs)

