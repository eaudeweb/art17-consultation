#!/usr/bin/env python


def main():
    import logging
    logging.basicConfig()
    #logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    from art17.app import manager
    manager.run()


if __name__ == '__main__':
    main()
