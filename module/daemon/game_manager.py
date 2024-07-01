from module.handler.login import LoginHandler
from module.logger import logger
from module.gg_manager.gg_manager import GGManager


class GameManager(LoginHandler):
    def run(self):
        logger.hr('Force Stop AzurLane', level=1)
        self.device.app_stop()
        logger.info('Force Stop finished')
        GGManager(self.config, self.device).check_config()
        if self.config.GameManager_AutoRestart:
            LoginHandler(config=self.config, device=self.device).app_restart()


if __name__ == '__main__':
    GameManager('alas', task='GameManager').run()
