import os
import logging

def is_this_a_pi():
    uname = os.uname()
    logging.info('Running {} on a {} machine.'.format(uname.sysname, uname.machine))
    # It is a guess. Raspberry Pis are Linux computers running on Arm.
    if uname.machine.startswith('arm') and uname.sysname=='Linux':
        logging.debug('This may be a Raspberry Pi.')
        return True
    else:
        logging.debug('This is very unlikely to be a Raspberry Pi.')
        return False
