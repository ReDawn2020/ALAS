from module.logger import logger
from module.log_res import LogRes
from module.daily.dashboard_status import DashboardStatus
from module.ui.page import page_campaign_menu
from module.ui.assets import CAMPAIGN_MENU_NO_EVENT, EVENT_CHECK, SP_CHECK, RAID_CHECK

class DashboardUpdate(DashboardStatus):
    def dashboard_run(self):
        self.ui_goto_main()
        self.get_cube()
        self.ui_goto_main()
        self.ui_goto_shop()
        self.get_oilcoingem()
        if self.config.DashboardUpdate_Update:
            self.goto_shop()
            self.get_event_pt()
        self.ui_goto_main()
        logger.info('Update Dashboard Data Finished')

    def get_event_pt(self):
        self.ui_goto(page_campaign_menu)
        self.device.sleep(0.5)
        self.device.screenshot()
        pt = 0
        if self.appear(button=CAMPAIGN_MENU_NO_EVENT, offset=(50, 50)):
            logger.warning('Event is already closed')
            logger.attr('Event_PT', pt)
            LogRes(self.config).Pt = pt
        else:
            while 1:
                self.device.click(button=CAMPAIGN_MENU_NO_EVENT)
                self.device.sleep(0.5)
                self.device.screenshot()
                if self.appear(button=EVENT_CHECK, offset=(50, 50)):
                    break
                if self.appear(button=RAID_CHECK, offset=(50, 50)):
                    break
                if self.appear(button=SP_CHECK, offset=(50, 50)):
                    logger.warning('Event is SP, no PT')
                    LogRes(self.config).Pt = pt
                    return 1
                if not self.appear(button=EVENT_CHECK, offset=(50, 50)) and \
                    not self.appear(button=RAID_CHECK, offset=(50, 50)) and \
                    not self.appear(button=SP_CHECK, offset=(50, 50)):
                    logger.warning('Event is no PT')
                    LogRes(self.config).Pt = pt
                    return 1
            
            skip_first_screenshot = True
            while 1:
                if skip_first_screenshot:
                    skip_first_screenshot = False
                else:
                    self.device.sleep(0.5)
                    self.device.screenshot()
                if self.appear(button=EVENT_CHECK, offset=(50, 50)):
                    self._get_pt()
                    break
                if self.appear(button=RAID_CHECK, offset=(50, 50)):
                    self.get_raid_pt()
                    break

    def goto_shop(self):
        self.ui_goto_shop()
        self.shop_tab.set(main=self, left=2)
        self.shop_nav.set(main=self, upper=2)
        logger.hr('Get Merit')
        self.get_merit()

        self.shop_tab.set(main=self, left=2)
        self.shop_nav.set(main=self, upper=3)
        logger.hr('Get GuildCoin')
        self.get_guild_coins()

        self.shop_tab.set(main=self, left=1)
        self.shop_nav.set(main=self, upper=2)
        logger.hr('Get Core')
        self.get_core()

        self.shop_tab.set(main=self, left=1)
        self.shop_nav.set(main=self, upper=3)
        logger.hr('Get Medal')
        self.get_medal()
        self.ui_goto_main()

    def run(self):
        self.dashboard_run()
        self.config.task_delay(server_update=True)
