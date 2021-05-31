from copy import deepcopy

from telegram.ext import BasePersistence
from collections import defaultdict


class SqlPersistence(BasePersistence):
    """Using python's builtin pickle for making you bot persistent.

    Attributes:
        store_user_data (:obj:`bool`): Optional. Whether user_data should be saved by this
            persistence class.
        store_chat_data (:obj:`bool`): Optional. Whether user_data should be saved by this
            persistence class.
        store_bot_data (:obj:`bool`): Optional. Whether bot_data should be saved by this
            persistence class.
        on_flush (:obj:`bool`, optional): When ``True`` will only save to database when :meth:`flush`
            is called and keep data in memory until that happens. When ``False`` will store data
            on any transaction *and* on call fo :meth:`flush`. Default is ``False``.

    Args:
        store_user_data (:obj:`bool`, optional): Whether user_data should be saved by this
            persistence class. Default is ``True``.
        store_chat_data (:obj:`bool`, optional): Whether user_data should be saved by this
            persistence class. Default is ``True``.
        store_bot_data (:obj:`bool`, optional): Whether bot_data should be saved by this
            persistence class. Default is ``True`` .
        on_flush (:obj:`bool`, optional): When ``True`` will only save to file when :meth:`flush`
            is called and keep data in memory until that happens. When ``False`` will store data
            on any transaction *and* on call fo :meth:`flush`. Default is ``False``.
    """

    def __init__(self,
                 store_user_data=True,
                 store_chat_data=True,
                 store_bot_data=True,
                 on_flush=False,
                 db_name: str = "assignment_alert_bot",
                 db_user: str = "root",
                 db_url: str = "127.0.0.1:3306"):
        super().__init__(store_user_data=store_user_data,
                         store_chat_data=store_chat_data,
                         store_bot_data=store_bot_data)
        self.on_flush = on_flush
        self.user_data = None
        self.chat_data = None
        self.bot_data = None
        self.conversations = None
        self.db_name = db_name

    # Table name:
    # base_table_name_user_data
    # base_table_name_bot_data
    # base_table_name_chat_data
    def get_user_data(self):
        """Returns the user_data from the sql database if it exsist or an empty defaultdict.

        Returns:
            :obj:`defaultdict`: The restored user data.
        """
        return defaultdict()

    def get_chat_data(self):
        """Returns the chat_data from the pickle file if it exsists or an empty defaultdict.
        Returns:
            :obj:`defaultdict`: The restored chat data.
        """
        filename = "{}_chat_data".format(self.filename)
        data = self.load_file(filename)
        if not data:
            data = defaultdict(dict)
        else:
            data = defaultdict(dict, data)
        self.chat_data = data
        return deepcopy(self.chat_data)

    def get_bot_data(self):
        """Returns the bot_data from the pickle file if it exsists or an empty dict.

        Returns:
            :obj:`defaultdict`: The restored bot data.
        """
        if self.bot_data:
            pass
        elif not self.single_file:
            filename = "{}_bot_data".format(self.filename)
            data = self.load_file(filename)
            if not data:
                data = {}
            self.bot_data = data
        else:
            self.load_singlefile()
        return deepcopy(self.bot_data)

    def get_conversations(self, name):
        """Returns the conversations from the pickle file if it exsists or an empty defaultdict.

        Args:
            name (:obj:`str`): The handlers name.

        Returns:
            :obj:`dict`: The restored conversations for the handler.
        """
        if self.conversations:
            pass
        elif not self.single_file:
            filename = "{}_conversations".format(self.filename)
            data = self.load_file(filename)
            if not data:
                data = {name: {}}
            self.conversations = data
        else:
            self.load_singlefile()
        return self.conversations.get(name, {}).copy()

    def update_conversation(self, name, key, new_state):
        """Will update the conversations for the given handler and depending on :attr:`on_flush`
        save the pickle file.

        Args:
            name (:obj:`str`): The handlers name.
            key (:obj:`tuple`): The key the state is changed for.
            new_state (:obj:`tuple` | :obj:`any`): The new state for the given key.
        """
        if self.conversations.setdefault(name, {}).get(key) == new_state:
            return
        self.conversations[name][key] = new_state
        if not self.on_flush:
            if not self.single_file:
                filename = "{}_conversations".format(self.filename)
                self.dump_file(filename, self.conversations)
            else:
                self.dump_singlefile()

    def update_user_data(self, user_id, data):
        """Will update the user_data (if changed) and depending on :attr:`on_flush` save the
        pickle file.

        Args:
            user_id (:obj:`int`): The user the data might have been changed for.
            data (:obj:`dict`): The :attr:`telegram.ext.dispatcher.user_data` [user_id].
        """
        if self.user_data is None:
            self.user_data = defaultdict(dict)
        if self.user_data.get(user_id) == data:
            return
        self.user_data[user_id] = data
        if not self.on_flush:
            if not self.single_file:
                filename = "{}_user_data".format(self.filename)
                self.dump_file(filename, self.user_data)
            else:
                self.dump_singlefile()

    def update_chat_data(self, chat_id, data):
        """Will update the chat_data (if changed) and depending on :attr:`on_flush` save the
        pickle file.

        Args:
            chat_id (:obj:`int`): The chat the data might have been changed for.
            data (:obj:`dict`): The :attr:`telegram.ext.dispatcher.chat_data` [chat_id].
        """
        if self.chat_data is None:
            self.chat_data = defaultdict(dict)
        if self.chat_data.get(chat_id) == data:
            return
        self.chat_data[chat_id] = data
        if not self.on_flush:
            if not self.single_file:
                filename = "{}_chat_data".format(self.filename)
                self.dump_file(filename, self.chat_data)
            else:
                self.dump_singlefile()

    def update_bot_data(self, data):
        """Will update the bot_data (if changed) and depending on :attr:`on_flush` save the
        pickle file.

        Args:
            data (:obj:`dict`): The :attr:`telegram.ext.dispatcher.bot_data`.
        """
        if self.bot_data == data:
            return
        self.bot_data = data.copy()
        if not self.on_flush:
            if not self.single_file:
                filename = "{}_bot_data".format(self.filename)
                self.dump_file(filename, self.bot_data)
            else:
                self.dump_singlefile()

    def flush(self):
        """ Will save all data in memory to pickle file(s).
        """
        if self.single_file:
            if self.user_data or self.chat_data or self.conversations:
                self.dump_singlefile()
        else:
            if self.user_data:
                self.dump_file("{}_user_data".format(self.filename), self.user_data)
            if self.chat_data:
                self.dump_file("{}_chat_data".format(self.filename), self.chat_data)
            if self.bot_data:
                self.dump_file("{}_bot_data".format(self.filename), self.bot_data)
            if self.conversations:
                self.dump_file("{}_conversations".format(self.filename), self.conversations)
