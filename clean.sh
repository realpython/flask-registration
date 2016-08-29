#!/usr/bin/env bash

function clean_env() {
    unset APP_MAIL_SERVER
    unset APP_MAIL_PORT
    unset APP_MAIL_USE_TLS
    unset APP_MAIL_USE_SSL
    unset APP_MAIL_USERNAME
    unset APP_MAIL_PASSWORD
    unset APP_MAIL_DEFAULT_SENDER
    unset APP_SQLALCHEMY_DATABASE_URI
}

clean_env

rm -rf migrations
rm -rf tmp
rm -f project/dev.sqlite
