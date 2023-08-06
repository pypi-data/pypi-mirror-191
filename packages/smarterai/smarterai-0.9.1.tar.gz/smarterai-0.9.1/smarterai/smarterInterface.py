import inspect
from .smarterStore import SmarterStore
from abc import ABCMeta, abstractmethod
from typing import Callable, Optional, Any, Tuple


class SmarterMessage(dict):
    pass


class SmarterSender:
    def __init__(self,
                 deploy_dir: str,
                 delegate: Callable[[SmarterMessage, str], Optional[SmarterMessage]],
                 user_id: str,
                 user_email: str,
                 db):
        self.__smarter_store = SmarterStore(deploy_dir=deploy_dir)
        self.__core = self.__smarter_store.get_manifest_property(property_sequence="core")
        self.__usage_key = "_usageKey"
        self.__user_id = user_id
        self.__user_email = user_email
        self.delegate = delegate
        self.__db = db

    @staticmethod
    def __is_number(val: Any) -> bool:
        if type(val) in [int, float]:
            return True
        if type(val) != str:
            return False
        if val.isdigit() or val.replace(".", "", 1).isdigit():
            return True
        else:
            return False

    def __check_limit(self, usage_data, exp_slug) -> int:
        state = self.__core.get("state")
        if not exp_slug or state != "inUse":
            # Experiment's creator incrementing their own usage
            return 0
        trial_limit = self.__smarter_store.get_manifest_property(property_sequence="price.paygTrialUnits")
        trial_limit = eval(trial_limit) if SmarterSender.__is_number(trial_limit) else None
        is_subscribed = self.__core.get("isSubscribed")
        if not is_subscribed and trial_limit and usage_data.get(exp_slug) > trial_limit:
            # Reached the trial limit
            return -1
        return usage_data.get(exp_slug)

    def __increment_usage(self, inc: int, user_id: str) -> Any:
        exp_slug = self.__core.get("expSlug")
        usage_data = self.__smarter_store.read_global_store(pattern=self.__usage_key)
        if user_id not in usage_data:
            usage_data[user_id] = {}
        project_slug = self.__core.get("slug")
        if exp_slug not in usage_data:
            usage_data[user_id][exp_slug] = 0
        usage_data[user_id][exp_slug] += inc
        limit_reached = self.__check_limit(usage_data=usage_data, exp_slug=exp_slug)
        if limit_reached in [0, -1]:
            return limit_reached
        self.__smarter_store.write_global_store(pattern="index." + self.__usage_key,
                                                data=usage_data)
        new_message = SmarterMessage({"action": "updateUsage",
                                      "args": {"expSlug": exp_slug,
                                               "projectSlug": project_slug,
                                               "value": usage_data[exp_slug]
                                               }})
        self.send_message(message=new_message, port='#gui')
        return usage_data[exp_slug]

    def __get_usage(self, user_id: str) -> int:
        usage_data = self.__smarter_store.read_global_store(pattern=self.__usage_key)
        exp_slug = self.__core.get("expSlug")
        return usage_data.get(user_id, {}).get(exp_slug, 0)

    def send_message(self, message: SmarterMessage, port: str) -> Optional[SmarterMessage]:
        """
        Takes in a message from a python code component and sends it to its output port.
        :param message: A SmarterMessage to be sent through an output port
        :param port: The output port to be
        :return: Optional SmarterMessage if the receiver replies back with a message
        """
        return self.delegate(message, port)

    def set_data(self, pattern: str, data: Any) -> None:
        """
        Takes in JSON serializable data and sets it to a specific front-end GUI component.
        :param pattern: The front-end GUI pattern to set the data to
        :param data: The data to be sent to the GUI. It needs to match the format the pattern expects the data in.
                        Example a chart expects a table-like format, while a textField expects some text.
        :return: None
        """
        message = SmarterMessage({"action": "setData",
                                  "args": {"pattern": pattern, "data": data}})
        return_message = self.send_message(message=message, port='#gui')
        user_id = return_message.get("user", {}).get("id")
        self.__smarter_store.set_pattern_data(pattern=pattern, data=data, user_id=user_id)

    def clear_data(self, pattern: str) -> None:
        """
        Clears any data associated with a specific pattern in the GUI components
        :param pattern: The front-end GUI pattern to set the data to
        :return: None
        """
        message = SmarterMessage({"action": "setData",
                                  "args": {"pattern": pattern, "data": None}})
        return_message = self.send_message(message=message, port='#gui')
        user_id = return_message.get("user", {}).get("id")
        self.__smarter_store.set_pattern_data(pattern=pattern, data=None, user_id=user_id)

    def append_data(self, pattern: str, data: Any, limit: int) -> None:
        """
        Appends new data to previously sent data to a specific pattern.
        :param pattern: The front-end GUI pattern to append the data to.
        :param data: The data to be appended to a GUI component's previous data.
        :param limit: If the data's total size is bigger than limit, then a sliding window will be implemented to hold
            the latest added elements
        :return: None
        """
        message = SmarterMessage({"action": "setData",
                                  "args": {"pattern": pattern, "data": data if type(data) == list else [data]},
                                  "options": {"append": True, "limitLength": limit}})
        return_message = self.send_message(message=message, port='#gui')
        user_id = return_message.get("user", {}).get("id")
        self.__smarter_store.append_pattern_data(pattern=pattern, data=data, user_id=user_id)

    def prepend_data(self, pattern: str, data: Any, limit: int) -> None:
        """
        Prepends new data to previously sent data to a specific pattern.
        :param pattern: The front-end GUI pattern to append the data to.
        :param data: The data to be prepended to a GUI component's previous data.
        :param limit: If the data's total size is bigger than limit, then a sliding window will be implemented to hold
            the latest added elements
        :return: None
        """
        message = SmarterMessage({"action": "setData",
                                  "args": {"pattern": pattern, "data": data if type(data) == list else [data]},
                                  "options": {"prepend": True, "limitLength": limit}})
        return_message = self.send_message(message=message, port='#gui')
        user_id = return_message.get("user", {}).get("id")
        self.__smarter_store.prepend_pattern_data(pattern=pattern, data=data, user_id=user_id)

    def get_data(self, pattern: str) -> Any:
        """
        Returns the data set to a specific pattern if it exists, otherwise returns None
        :param pattern: The pattern to return
        :return: json serializable SmarterMessage
        """
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        user_id = return_message.get("user", {}).get("id")
        return self.__smarter_store.get_pattern_data(pattern=pattern, user_id=user_id)

    def reply_back(self, message: SmarterMessage) -> None:
        """
        Takes in a message to reply back to front-end REST/Websocket topics. An equivalent  to 'return' with a message.
        Uses built-in port #action to identify the front-end topic
        :param message: A SmarterMessage JSON Serializable
        :return: None
        """

        self.send_message(message=message, port='#action')

    def popup_message(self, popup_type: str, message: Any) -> None:
        """
        Shows a popup message in the GUI
        :param popup_type: = success OR info OR error OR warning
        :param message: A JSON Serializable message
        :return: None
        """
        new_message = SmarterMessage({"action": "message",
                                      "args": {"message": message,
                                               "type": popup_type}})
        self.send_message(message=new_message, port='#gui')

    def refresh(self) -> None:
        """
        Reloads the current page in the GUI
        :return: None
        """
        new_message = SmarterMessage({"action": "refresh"})
        self.send_message(message=new_message, port='#gui')

    def open_experiment(self, experiment_slug: str) -> None:
        """
        Opens a specific experiment in the GUI
        :param experiment_slug: The experiment you wish to open
        :return: None
        """
        new_message = SmarterMessage({"action": "gotoExperiment",
                                      "projectSlug": experiment_slug})
        self.send_message(message=new_message, port='#gui')

    def open_page(self, page_slug: str) -> None:
        """
        Go to a specific page in the GUI
        :param page_slug: The page slug to go to
        :return: None
        """
        new_message = SmarterMessage({"action": "gotoNav",
                                      "args": {"page": page_slug}})
        self.send_message(message=new_message, port='#gui')

    def set_page_json(self, page_id: str, page_json: Any) -> None:
        """
        Replaces all or parts of the page json with new json in the GUI
        :param page_id: The ID of the page or part of the page to be replaced
        :param page_json: The JSON content to be added
        :return: None
        """
        new_message = SmarterMessage({"action": "setPage",
                                      "args": {"pattern": page_id,
                                               "json": page_json}})
        self.send_message(message=new_message, port='#gui')

    def set_wait(self, wait_message: str = None) -> None:
        """
        Sets the wait text on the GUI (or set it to blank to hide)
        :param wait_message: Message to be rendered while "waiting"
        :return: None
        """
        new_message = SmarterMessage({"action": "setWait",
                                      "args": {"message": wait_message}})
        self.send_message(message=new_message, port='#gui')

    def increment_usage(self, increment_value: int = 1) -> int:
        """
        Increments the trial usage by the provided inc value. This is useful in the case of creating trial versions, it
        can be used to track the usage of the users of the solutions and allowing them to "try" it in a limited fashion.
        :param increment_value: incremental value to be added to the user's usage counter
        :return: The user's updated usage.
                 Returns -1 if they reached or exceeded the trial limit.
                 Returns 0 if no trial limit was set
                 Otherwise returns a value >= 1 depending on the user's current usage after increment.
        """
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        user_id = return_message.get("user", {}).get("id")
        return self.__increment_usage(increment_value, user_id=user_id)

    def get_usage(self) -> int:
        """
        Gets the current trial usage of the user.
        :return: The user's current usage.
                 Returns 0 if no trial limit was set or if the user is the solution's creator
                 Otherwise returns a value >= 1 depending on the user's current usage.
        """
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        user_id = return_message.get("user", {}).get("id")
        return self.__get_usage(user_id=user_id)

    def query_data_lake(self, sql_query: str, args=None, paramstyle: str = "format", commit=True) -> Tuple:
        """
        Takes an SQL query on the data lake and returns all remaining rows of a query result.
        Args:
            :param sql_query: The SQL statement to execute on the data Lake
            :param args: If :`paramstyle` is ``qmark``, ``numeric``, or ``format``,
                this argument should be an array of parameters to bind into the
                statement.  If :data:`paramstyle` is ``named``, the argument should
                be a dict mapping of parameters.  If the `paramstyle` is
                ``pyformat``, the argument value may be either an array or a
                mapping.
            :param paramstyle: can be one of ('qmark', 'numeric', 'format','named', 'pyformat')
            :param commit: commits the database update permanently
        Returns:
            A sequence, each entry of which is a sequence of field values
            making up a row.:tuple
        """
        data = self.__db.execute_sql_query(query=sql_query,
                                           args=args,
                                           paramstyle=paramstyle,
                                           commit=commit,
                                           fetch="all")
        return data


class _Smarter_SignatureCheckerMeta(ABCMeta):
    def __init__(cls, name, bases, attrs):
        errors = []
        for base_class in bases:
            for func_name in getattr(base_class, "__abstractmethods__", ()):
                smarter_signature = inspect.getfullargspec(
                    getattr(base_class, func_name)
                )
                flex_signature = inspect.getfullargspec(
                    getattr(cls, func_name)
                )
                if smarter_signature != flex_signature:
                    errors.append(
                        f"Abstract method {func_name} "
                        f"not implemented with correct signature in {cls.__name__}. Expected {smarter_signature}."
                    )
        if errors:
            raise TypeError("\n".join(errors))
        super().__init__(name, bases, attrs)


class SmarterPlugin(metaclass=_Smarter_SignatureCheckerMeta):
    """
    SmarterPlugin is designed for easy communication between the smarter.ai's platform and other Flex.
    In order to have the Flex's code accessible to the platform, this class needs to be inherited from
    a class explicitly named SmarterComponent.
    Example:
        Class SmarterComponent(SmarterPlugin):
            pass
    """

    @abstractmethod
    def invoke(
            self, port: str, message: SmarterMessage, sender: SmarterSender
    ) -> Optional[SmarterMessage]:
        """
        This is the flex's messages entry point. Any message sent to the current flex will be routed to this method.
        This method needs to be overwritten.

        Example:
            Class SmarterComponent(SmarterPlugin):
                def invoke(self, port: str,
                           msg: SmarterMessage,
                           send_message: SmarterSender) -> Optional[SmarterMessage]:
                    pass
        The message received and its associated port will be passed as inputs for this method,
        Along with a callable function that can be used to send messages to other flex.

        Arguments:
            port [str]: The input port name used to receive the message.
            msg [SmarterMessage]: The message passed to the flex.
            send_message[SmarterSender]: A Callable function used to send messages to other flex.
                                        The function has the signature:
                                            Callable[[SmarterMessage, str], SmarterMessage]
                                        Example:
                                            send_message(SmarterMessage(), 'out_port_name')

                                        Arguments:
                                            [SmarterMessage]: The new message to send out.
                                            [str]: The output port name used to send the new message.

                                        Returns:
                                            [SmarterMessage]: A return message.

        Returns:
            Optional[SmarterMessage]: If a message is being returned it should be of
                                      type SmarterMessage or None
        """
        raise NotImplementedError
