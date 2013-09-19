#!/usr/bin/env python


def main():
    import os
    import logging
    os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.UTF8'  # encoding for cx_oracle
    logging.basicConfig()
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    from art17.app import create_app, create_manager
    app = create_app()
    if app.config.get('SQL_DEBUG'):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    create_manager(app).run()


if __name__ == '__main__':
    main()
