import datetime
import sqlite3
import os

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    """Добавление пользователя"""
    def user_exists(self, user_id):
        result = self.cursor.execute('SELECT `id` FROM `users` WHERE `user_id` = ?', (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute('SELECT `id` FROM `users` WHERE `user_id` = ?', (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    """Покупка и добавление NFT"""
    def add_nft(self, user_id, value):
        all_nft = self.cursor.execute('SELECT `nft` FROM `users` WHERE `user_id` = ?', (user_id,))
        all_nft = all_nft.fetchone()[0]
        if all_nft:
            nft = all_nft + ',' + str(value)
        else:
            nft = str(value)
        self.cursor.execute('UPDATE `users` SET `nft` = (?) WHERE `user_id` = ?', (nft, user_id,))

        return self.conn.commit()

    """Получить NFT пользователя"""
    def get_nft(self, user_id):
        result = self.cursor.execute('SELECT `nft` FROM `users` WHERE `user_id` = ?', (user_id,))
        return result.fetchone()[0]


    """№ Сообщения"""
    def new_menu(self, user_id, value):
        self.cursor.execute('UPDATE `users` SET `msg` = (?) WHERE `user_id` = ?', (value, user_id,))
        return self.conn.commit()

    def get_menu(self, user_id):
        result = self.cursor.execute('SELECT `msg` FROM `users` WHERE `user_id` = ?', (user_id,))
        return result.fetchone()[0]


    """Добавление/изменение Tonkeepr"""
    def add_tonkeepr(self, user_id, value):
        self.cursor.execute('UPDATE `users` SET `tonkeepr` = (?) WHERE `user_id` = ?', (value, user_id,))
        return self.conn.commit()

    def get_tonkeepr(self, user_id):
        result = self.cursor.execute('SELECT `tonkeepr` FROM `users` WHERE `user_id` = ?', (user_id,))
        return result.fetchone()[0]


    """Отложить NFT"""
    def add_buy(self, user_id, value):
        os.replace(f'avaliable/{value}.png', f'inaccessible/{value}.png')
        self.cursor.execute(f'UPDATE `users` SET `delayed_nft` = (?), `delayed_time` = (?) WHERE `user_id` = ?', (value, datetime.datetime.now(), user_id,))
        return self.conn.commit()

    def get_buy(self, user_id):
        result = self.cursor.execute('SELECT `delayed_nft` FROM `users` WHERE `user_id` = ?', (user_id,))
        return result.fetchone()[0]

    def del_buy(self, user_id):
        self.cursor.execute(f'UPDATE `users` SET `delayed_nft` = (?), `delayed_time` = (?) WHERE `user_id` = ?',
                            (None, None, user_id,))
        return self.conn.commit()

    """Отложить NFT"""

    def add_proverka(self, user_id):
        self.cursor.execute(f'UPDATE `users` SET `proverka` = (?) WHERE `user_id` = ?',
                            (datetime.datetime.now(), user_id,))
        return self.conn.commit()

    def get_proverka(self, user_id):
        result = self.cursor.execute('SELECT `proverka` FROM `users` WHERE `user_id` = ?', (user_id,))
        return result.fetchone()[0]

    def del_proverka(self, user_id):
        self.cursor.execute(f'UPDATE `users` SET `proverka` = (?) WHERE `user_id` = ?', (None, user_id,))
        return self.conn.commit()



    """ADMIN PANEL"""
    def admin_avaliable(self):
        result = self.cursor.execute(f'SELECT `nft` FROM `users` WHERE `nft` is NOT NULL GROUP BY `nft`')
        return sorted([int(j) for i in result.fetchall() for j in i[0].split(',')])

    def admin_delayed_nft(self):
        result = self.cursor.execute(f'SELECT `delayed_nft` FROM `users` WHERE `delayed_nft` is NOT NULL GROUP BY `delayed_nft`')
        return sorted([j for i in result.fetchall() for j in i])

    def all_people(self):
        result = self.cursor.execute(
            f'SELECT `id` FROM `users` GROUP BY `id`')
        return len(result.fetchall())

    def active_people(self):
        result = self.cursor.execute(f'SELECT `nft` FROM `users` WHERE `nft` is NOT NULL GROUP BY `nft`')
        return len(result.fetchall())

    def not_active_people(self):
        result = self.cursor.execute(f'SELECT COUNT(*) FROM `users` WHERE `tonkeepr` is NULL')
        return result.fetchone()[0]

    def all_statistic(self):
        result = self.cursor.execute(f'SELECT `user_id`, `tonkeepr`, `nft` FROM `users` WHERE `nft` is NOT NULL')
        return result.fetchall()


    def update(self):
        result = self.cursor.execute(f'SELECT `id`, `delayed_time`, `delayed_nft` FROM `users` WHERE `delayed_time` is NOT NULL')
        user = []
        if result:
            d1 = datetime.datetime.strptime(str(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
            for i in result.fetchall():
                d2 = datetime.datetime.strptime(i[1], "%Y-%m-%d %H:%M:%S.%f")
                if (d1 - d2).seconds / 3600 > 2:
                    user.append(i[0])
                    os.replace(f'inaccessible/{i[2]}.png', f'avaliable/{i[2]}.png')
        if user:
            self.cursor.execute(
                f'UPDATE `users` SET `delayed_nft` = ?, `delayed_time` = ? WHERE `id` = ({str(user)[1:-1]})',
                (None, None,))
        return self.conn.commit()

    def close(self):
        self.conn.close()