#!/usr/bin/env python3
""" Module containing functions for tasks 0 to 4  """

import re
import logging
from typing import List
from os import getenv
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str,
        separator: str) -> str:
    """ obfuscates log message(message) using (redaction) separated by
    separator """
    for field in fields:
        regex = r'(?<={}).*?(?={})'.format(field + '.', separator)
        message = re.sub(regex, redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filters data in incming log records """
        message = super(RedactingFormatter, self).format(record)
        filtered = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return filtered


def get_logger() -> logging.Logger:
    """ creates a configured logger """
    logger = logging.getLogger("user_date")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """creates and returns a mysql connector to the database using environment
    variable"""
    db_name = getenv('PERSONAL_DATA_DB_NAME', None)
    passwd = getenv("PERSONAL_DATA_DB_PASSWORD", None) or ""
    db_host = getenv("PERSONAL_DATA_DB_HOST", None) or "localhost"
    db_user = getenv("PERSONAL_DATA_DB_USERNAME", None) or "root"
    connector = mysql.connector.connect(user=db_user, database=db_name,
                                        host=db_host, password=passwd)
    return connector


def main() -> None:
    """ retrieves all rows in a database """
    conn = get_db()
    cursor = conn.cursor()
    logger = get_logger()
    query = "SELECT * from users;"
    cursor.execute(query)
    field_names = cursor.column_names
    for row in cursor:
        iterable = zip(field_names, row)
        data_list = [f"{k}={v}; " for k, v in iterable]
        message = "".join(data_list)
        logger.info(message)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
