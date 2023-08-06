import logging
logging.basicConfig(level=logging.DEBUG)

__import__("pkg_resources").declare_namespace(__name__)
# orangecontrib is a namespace modules shared by multiple Orange add-on so it
# needs to declare namespace.
