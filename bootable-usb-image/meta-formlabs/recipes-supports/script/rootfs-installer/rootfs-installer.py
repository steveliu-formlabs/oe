#!/usr/bin/python
import curses
import os
import time
import subprocess


class CursesMenu(object):
    def __init__(self, menu_options):
        self.screen = curses.initscr()
        self.menu_options = menu_options
        self.selected_option = 0
        self._previously_selected_option = None

        # init curses and curses input
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)  # Hide cursor
        self.screen.keypad(1)

        # set up color pair for highlighted option
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.hilite_color = curses.color_pair(1)
        self.title_color = curses.color_pair(2)
        self.logo_color = curses.color_pair(3)
        self.normal_color = curses.A_NORMAL

    def prompt_selection(self, parent=None):
        option_count = len(self.menu_options['options'])
        input_key = None

        # get the input and then refresh screen
        ENTER_KEY = ord('\n')
        while input_key != ENTER_KEY:
            if self.selected_option != self._previously_selected_option:
                self._previously_selected_option = self.selected_option

            self._draw_title()
            self._draw_formlabs_logo()
            self.screen.border(0)
            for option in range(option_count):
                if self.selected_option == option:
                    self._draw_option(option, self.hilite_color)
                else:
                    self._draw_option(option, self.normal_color)

            max_y, max_x = self.screen.getmaxyx()
            if input_key is not None:
                self.screen.addstr(max_y - 3, max_x - 5, "{:3}".format(self.selected_option))
            self.screen.refresh()

            input_key = self.screen.getch()
            down_keys = [curses.KEY_DOWN, ord('j')]
            up_keys = [curses.KEY_UP, ord('k')]

            if input_key in down_keys:
                if self.selected_option < option_count - 1:
                    self.selected_option += 1

            if input_key in up_keys:
                if self.selected_option > 0:
                    self.selected_option -= 1

        return self.selected_option

    def _draw_option(self, option_number, style):
        self.screen.addstr(5 + option_number,
                           3,
                           "{:2} - {}".format(option_number + 1, self.menu_options['options'][option_number]['title']),
                           style)

    def _draw_title(self):
        self.screen.addstr(2, 2, self.menu_options['title'], self.title_color)
        self.screen.addstr(4, 2, self.menu_options['subtitle'], curses.A_BOLD)

    def _draw_formlabs_logo(self):
        with open('/usr/share/formlabs-ascii-logo.txt', 'r') as f:
            lines = f.readlines()
            m, n = len(lines), len(lines[0])
            max_y, max_x = self.screen.getmaxyx()
            for i in range(len(lines)):
                for j in range(len(lines[i])):
                    if lines[i][j] != '.':
                        self.screen.addstr(max_y - m + i, max_x - n + j, lines[i][j],  curses.A_DIM)

    def display(self):
        selected_option = self.prompt_selection()
        i, _ = self.screen.getmaxyx()
        return selected_option

    def clear(self):
        self.screen.erase()
        curses.endwin()


class CursesInfo(object):
    def __init__(self, options):
        self.screen = curses.initscr()
        self.options = options
        self.selected_option = 0
        self._previously_selected_option = None

        # init curses and curses input
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)  # Hide cursor
        self.screen.keypad(1)

        # set up color pair for highlighted option
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        self.hilite_color = curses.color_pair(1)
        self.title_color = curses.color_pair(2)
        self.logo_color = curses.color_pair(3)
        self.normal_color = curses.A_NORMAL

    def _draw_title(self):
        self.screen.addstr(2, 2, self.options['title'], self.title_color)
        self.screen.addstr(4, 2, self.options['subtitle'], curses.A_BOLD)

    def _draw_formlabs_logo(self):
        with open('/usr/share/formlabs-ascii-logo.txt', 'r') as f:
            lines = f.readlines()
            m, n = len(lines), len(lines[0])
            max_y, max_x = self.screen.getmaxyx()
            for i in range(len(lines)):
                for j in range(len(lines[i])):
                    if lines[i][j] != '.':
                        self.screen.addstr(max_y - m + i, max_x - n + j, lines[i][j],  curses.A_DIM)

    def display(self):
        self._draw_title()
        self._draw_formlabs_logo()
        self.screen.border(0)
        self.screen.refresh()
        if 'sleep' in self.options:
            time.sleep(int(self.options['sleep']))
        else:
            time.sleep(1)

    def clear(self):
        self.screen.erase()
        curses.endwin()


# State memorize the user's current selection.
#
# 0. Init Page
#
# 1. Select Disk Page
#     11. Reboot to continue install.
#     12. Install
#
# 2. Reboot Page
#
def prompt0(prompt_stack):
    menu = {
        'title': 'Formlabs Calibration OS',
        'subtitle': 'Select one of the following options:',
        'options': [
            {'title': 'Install Formlabs Calibration OS', 'id': 'install'},
            {'title': 'Reboot', 'id': 'reboot'},
            {'title': 'Debug', 'id': 'debug'},
        ]
    }
    m = CursesMenu(menu)
    idx = m.display()
    m.clear()

    # options
    if idx == 0:
        prompt_stack.append(1)
    elif idx == 1:
        prompt_stack.append(2)
    elif idx == 2:
        prompt_stack.append(3)


def prompt1(prompt_stack):
    # list all block devices
    cmd = ['lsblk', '-n', '-So', 'KNAME,HOTPLUG,SIZE,FSTYPE,MOUNTPOINT']
    out = subprocess.check_output(cmd).decode('UTF-8')
    lines = out.strip().split('\n')

    # get all devices
    devices = []
    for line in lines:
        entries = line.split()
        devices.append({
            'name': entries[0],
            'path': '/dev/{}'.format(entries[0]),
            'hotplug': False if entries[1] == '0' else True,
            'size': entries[2],
            'fs_type': '',
            'mount_point': '',
        })
        if len(entries) == 4:
            if entries[3].startswith('/'):
                devices[-1]['mount_point'] = entries[3]
            else:
                devices[-1]['fs_type'] = entries[3]
        if len(entries) == 5:
            devices[-1]['fs_type'] = entries[3]
            devices[-1]['mount_point'] = entries[4]

    # create options for menu
    options = []
    for device in devices:
        if not device['hotplug']:
            options.append({
                'title': '{}  {}'.format(device['name'], device['size']),
                'id': device['name']
            })

    # create a menu
    menu = {
        'title': 'Formlabs Calibration OS',
        'subtitle': 'Select the disk to install:',
        'options': options
    }
    m = CursesMenu(menu)
    idx = m.display()
    m.clear()

    name = devices[idx]['name']
    dev_path = '/dev/{}'.format(name)

    is_dirty = False

    # check if the disk is already partitioned
    for device in os.listdir('/dev'):
        if device != name and device.startswith(name):
            is_dirty = True
            break
    # check if the fs type is already set
    if devices[idx]['fs_type']:
        is_dirty = True

    if is_dirty:
        cmd = ['wipefs', '-afq', devices[idx]['path']]
        subprocess.check_output(cmd)
        prompt_stack.append(11)
    else:
        info = {'title': 'Formlabs Calibration OS', 'subtitle': 'partitioning disk...1/5', 'sleep': '1'}
        m = CursesInfo(info)
        m.display()
        # partition the disk `fdisk /dev/sdx`
        cmd = ['fdisk', dev_path]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        _ = p.communicate(input=b'n\np\n1\n\n\nw\n')[0]
        m.clear()

        info = {'title': 'Formlabs Calibration OS', 'subtitle': 'formatting disk...2/5', 'sleep': '1'}
        m = CursesInfo(info)
        m.display()
        # make the ext4 file system
        partition_path = ''
        for device in os.listdir('/dev'):
            if device != name and device.startswith(name):
                partition_path = '/dev/{}'.format(device)
                break
        cmd = ['mkfs.ext4', partition_path]
        subprocess.check_output(cmd)
        m.clear()

        info = {'title': 'Formlabs Calibration OS', 'subtitle': 'mounting file system...3/5', 'sleep': '1'}
        m = CursesInfo(info)
        m.display()
        # mount the partition `mount /dev/sdx1 /mnt`
        cmd = ['mount', partition_path, '/mnt']
        subprocess.check_output(cmd)
        m.clear()

        # mount our calibration root file system `mount -o loop /xxxxx.ext4 /media`
        cmd = ['mount', '-o', 'loop', '/formlabs-rootfs-image-intel-corei7-64.ext4', '/media']
        subprocess.check_output(cmd)

        info = {'title': 'Formlabs Calibration OS', 'subtitle': 'copying file system...4/5', 'sleep': '1'}
        m = CursesInfo(info)
        m.display()
        # copy the file system `cp -a /media/* /mnt`
        cmd = ['bash', '-c', 'cp -a /media/* /mnt']
        subprocess.check_output(cmd)
        m.clear()

        info = {'title': 'Formlabs Calibration OS', 'subtitle': 'booting file system...5/5', 'sleep': '1'}
        m = CursesInfo(info)
        m.display()
        # grub install `grub-install --force --recheck --root-directory=/mnt /dev/sdx`
        cmd = ['grub-install', '--force', '--recheck', '--root-directory=/mnt', dev_path]
        subprocess.check_output(cmd)
        m.clear()

        # grub configuration file `vi grub.cfg`
        cfg = """\
set default="0"
set timeout="5"

menuentry 'Formlabs Calibration OS' {{
    insmod part_msdos
    insmod ext2
    set root='(hd0,1)'
    linux /boot/bzImage root={root}
}}
""".format(root=partition_path)
        with open('/mnt/boot/grub/grub.cfg', 'w') as f:
            f.write(cfg)
        prompt_stack.append(12)


def prompt11(prompt_stack):
    info = {
        'title': 'Formlabs Calibration OS',
        'subtitle': 'Format the disk. Reboot in 5 seconds...',
        'sleep': '5'
    }
    m = CursesInfo(info)
    m.display()
    cmd = ['/sbin/shutdown', '-r', 'now']
    subprocess.check_output(cmd)


def prompt12(prompt_stack):
    info = {
        'title': 'Formlabs Calibration OS',
        'subtitle': 'Successful Installation. Please remove the USB. Reboot in 5 seconds...',
        'sleep': '5'
    }
    m = CursesInfo(info)
    m.display()
    cmd = ['/sbin/shutdown', '-r', 'now']
    subprocess.check_output(cmd)


def prompt2(prompt_stack):
    info = {
        'title': 'Formlabs Calibration OS',
        'subtitle': 'Reboot in 5 second...',
        'sleep': '5'
    }
    m = CursesInfo(info)
    m.display()
    cmd = ['/sbin/shutdown', '-r', 'now']
    subprocess.check_output(cmd)


def prompt3(prompt_stack):
    info = {
        'title': 'Formlabs Calibration OS',
        'subtitle': 'Get into Bash in 5 second...',
        'sleep': '5'
    }
    m = CursesInfo(info)
    m.display()
    m.clear()
    os.system('exec /bin/bash')


def main():
    prompt_stack = []
    while True:
        if not prompt_stack:
            prompt_stack.append(0)
        if prompt_stack[-1] == 0:
            prompt0(prompt_stack)
        elif prompt_stack[-1] == 1:
            prompt1(prompt_stack)
        elif prompt_stack[-1] == 11:
            prompt11(prompt_stack)
        elif prompt_stack[-1] == 12:
            prompt12(prompt_stack)
        elif prompt_stack[-1] == 2:
            prompt2(prompt_stack)
        elif prompt_stack[-1] == 3:
            prompt3(prompt_stack)
        else:
            time.sleep(10)


if __name__ == '__main__':
    main()
