# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
import socket

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"
alt = "mod1"
terminal = "kitty"
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())


keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown"),

    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="Rofi"),

    # User hotkeys
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 5%+"), desc="Increase volume"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 5%-"), desc="Decrease volume"),
    Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle"), desc="Toggle mute"),

    Key([], "XF86MonBrightnessUp", lazy.spawn("light -A 7"), desc="Increase brightness"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("light -U 7"), desc="Decrease brightness"),

    Key([mod], "Print", lazy.spawn("maim -o -s -t 1 | xclip -selection clipboard -t image/png", shell=True), desc="Clip screen"),
    Key([mod, "control"], "Print", lazy.spawn("maim -o -s -t 1 ~/screenshot.png", shell=True), desc="Clip screen"),

    Key([mod, alt], "l", lazy.spawn("xsecurelock"), desc="Lock screen"),

    Key([mod], "f", lazy.window.toggle_floating()),
]

groups = [Group(i) for i in "1234567890"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

colors = [
    ["#242831", "#242831"],  # 0 background
    ["#f8f8f2", "#f8f8f2"],  # 1 foreground
    ["#3b4252", "#3b4252"],  # 2 background lighter
    ["#bf616a", "#bf616a"],  # 3 red
    ["#a3be8c", "#a3be8c"],  # 4 green
    ["#ebcb8b", "#ebcb8b"],  # 5 yellow
    ["#81a1c1", "#81a1c1"],  # 6 blue
    ["#b48ead", "#b48ead"],  # 7 magenta
    ["#88c0d0", "#88c0d0"],  # 8 cyan
    ["#4c566a", "#4c566a"],  # 9 grey
    ["#e5e9f0", "#e5e9f0"],  # 10 white
    ["#d08770", "#d08770"],  # 11 orange
    ["#8fbcbb", "#8fbcbb"],  # 12 super cyan
    ["#5e81ac", "#5e81ac"],  # 13 super blue
    ["#2e3440", "#2e3440"],  # 14 super dark background
    ["#708090", "#708090"]   # 15 slate grey
]

layout_theme = {"border_width": 2,
                "margin": 5,
                "border_focus": colors[9],
                "border_normal": colors[0]
                }
layouts = [
    layout.MonadTall(ratio=0.7, **layout_theme),
    layout.MonadTall(ratio=0.6, **layout_theme),
    layout.Columns(**layout_theme),
    #layout.MonadWide(ratio=0.7, **layout_theme),
    layout.Max(**layout_theme),
#     layout.MonadTall(border_focus='#efefee', border_normal='#001100', ratio=0.70, border_width=4, margin=8),
#     layout.Columns(border_focus='#efefee', border_normal='#001100', border_width=4, margin=8),
#     layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

# widget_defaults = dict(
#     font='sans',
#     fontsize=14,
#    padding=3,
# )

widget_defaults = dict(
    # font='CozetteVector Bold',
#     font='mononoki Nerd Font Bold',
    font='Jetbrains Mono Nerd Font',
    fontsize=14,
#     padding=5,
    foreground = colors[10],
    background = colors[0]
    )

extension_defaults = widget_defaults.copy()

_screens = [
    Screen(
        top=bar.Bar(
            [
                #widget.CurrentLayout(),
                widget.GroupBox(highlight_method="box", highlight_color=["#d08770", "#000000"]),
                widget.Prompt(),
                widget.TaskList(padding=2),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.Clock(format='%a %I%M %p %Y/%m/%d ', padding=4),
                widget.Volume(fmt='Volume: {}', padding=4),
                widget.Battery(format='Battery: {percent:2.0%}', padding=4),
            ],
            26,
        ),
    ),
]

screens = [
  Screen(
        top=bar.Bar(
            [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       ),
              widget.GroupBox(
#                        fontsize = 21,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       inactive = colors[2],
                       active = colors[15],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[11],
                       this_screen_border = colors[15],
                       other_current_screen_border = colors[15],
                       other_screen_border = colors[9],
                       foreground = colors[15],
                       background = colors[0]
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 5,
                       ),
              widget.Prompt(
                       prompt = prompt,
                       padding = 6,
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 5,
                       ),
              widget.TaskList(
                       padding = 2,
#                        fontsize = 10
                       ),
#               widget.Sep(
#                        linewidth = 0,
#                        padding = 5,
#                        ),
#               widget.TextBox(
#                        text = "|",
# #                        fontsize = 12,
#                        foreground = colors[2],
#                        ),
              widget.Net(
                      foreground = colors[3],
                      interface = "wlan0",
                      format = ' {down} ↓↑ {up}',
                      padding = 5,
                      ),
#               widget.Sep(
#                       linewidth = 0,
#                       padding = 5,
#                       ),
#               widget.TextBox(
#                       text = "|",
# #                       fontsize = 12,
#                       foreground = colors[2],
#                       ),
              widget.Memory(
                      foreground = colors[4],
                      format = ' {MemUsed: .0f}{mm}',
                      mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e bpytop')},
                      padding = 5
                      ),
#               widget.Sep(
#                       linewidth = 0,
#                       padding = 5,
#                       ),
#               widget.TextBox(
#                       text = "|",
# #                       fontsize = 12,
#                       foreground = colors[2],
#                       ),
              widget.CPU(
                      foreground = colors[5],
                      padding = 5,
                      mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e bpytop')},
                      format = ' {load_percent}%',
                      ),
#               widget.Sep(
#                       linewidth = 0,
#                       padding = 5,
#                       ),
#               widget.TextBox(
#                       text = "|",
# #                       fontsize = 12,
#                       foreground = colors[2],
#                       ),
              widget.Wttr(
                      foreground = colors[6],
                       padding = 5,
                       location={'Dana Point': 'Dana Point'},
                       format = ' %t',
                       units = 'u'
                       ),
#               widget.Sep(
#                        linewidth = 0,
#                        padding = 5,
#                        ),
#               widget.TextBox(
#                        text = "|",
# #                        fontsize = 12,
#                        foreground = colors[2],
#                        ),
              widget.Volume(
                      fmt='奔 {}',
                      foreground = colors[7],
              ),
#               widget.Sep(linewidth = 0, padding = 5,),
#               widget.TextBox(text = "|", foreground = colors[2]),
              widget.Battery(
                foreground = colors[8],
                charge_char='',
                discharge_char='',
                empty_char='',
                full_char='',
                show_short_text=False,
                format='{char} {percent:2.0%} {hour:d}:{min:02d}'
              ),
#               widget.Sep(linewidth = 0, padding = 5,),
#               widget.TextBox(text = "|", foreground = colors[2]),
              widget.Clock(
                        foreground = colors[9],
                       format = " %m/%d/%y %H:%M ",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e calcure')},
                       ),
#               widget.Sep(
#                        linewidth = 0,
#                        padding = 5,
#                        ),
#               widget.TextBox(
#                        text = "|",
# #                        fontsize = 12,
#                        foreground = colors[2],
#                        ),
              widget.Systray(),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       padding = 5,
                       scale = 0.7
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 5,
                       ),
            ], 28, ), ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='win0'),  # Jetbrains
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
