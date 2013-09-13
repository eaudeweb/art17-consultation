#!/usr/bin/env python


def main():
    import os
    import logging
    os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.UTF8'  # encoding for cx_oracle
    logging.basicConfig()
    #logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    from art17.app import create_manager
    create_manager().run()


if __name__ == '__main__':
    main()
