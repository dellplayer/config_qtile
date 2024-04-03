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

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import os
import subprocess
import re
import pytz

mod = "mod4"
terminal = guess_terminal()

colors = [
    ["#00000000", "#00000000"], #0 full transparent
    ["01acf2","01acf2"], #1 bleu de majUP
    ["ff9900","ff9900"], #2 orange de majUP
    ["00508D", "00508D"], #3 bleu foncé
    ["8D5000", "8D5000"], #4 marron
    ["215578", "215578"], #5 bleu foncé pâle
    ["#ff786a", "#ff786a"], #6 rouge pâle
    ["124466","124466"], #7 bleu foncé pâle 2
    ["306e97","306e97"], #8 bleu gris
    ["09686e","09686e"], #9 bleu vert
    ["5cf1a5","5cf1a5"], #10 vert clair
    ["426f58","426f58"], #11 vert foncé
    ["d4bb03","d4bb03"], #12 jaune
    ["e9ea09","e9ea09"], #13 jaune bright
    ["ffffff","ffffff"], #14 blanc
    ["000000","000000"], #15 noir
    ["00000000","00000000"], #16 noir 100% transparent
    ["00000080","00000080"], #17 noir 10% transparent
]


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "i", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "n", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "e", lazy.layout.up(), desc="Move focus up"),
#    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "space", lazy.group.next_window(), desc="Move window focus to other window"),
    Key([mod], "m", lazy.window.toggle_minimize(), desc="Minimize/Maximize"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "i", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "n", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "e", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink_main().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"),
    Key([mod, "control"], "i",
        lazy.layout.grow_right(),
        lazy.layout.grow_main().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the right"),
    Key([mod, "control"], "n",
        lazy.layout.grow_down(),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window down"),
    Key([mod, "control"], "e",
        lazy.layout.grow_up(),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window up"),
    Key([mod], "k", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "t",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
        #JIA additions
    Key([mod, "control"],
    "l", lazy.to_screen(1),
    desc='Focus to monitor 1'
    ),
    Key([mod, "control"],
    "u", lazy.to_screen(0),
    desc='Focus to monitor 0'
    ),
    Key([mod, "control"],
    "y", lazy.to_screen(2),
    desc='Focus to monitor 2'
    ),

    Key([mod],"l", lazy.spawn('xsecurelock')),
#    Key([mod], "361u", lazy.spawn('flameshot gui')),
    Key([mod],"p", lazy.spawn('/home/julien/scripts/flameshot_gui.sh')),
    Key([mod],"v", lazy.spawn('copyq toggle')),

]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


#groups = [Group(i) for i in "123456789"]
groups = [
#        Group(name="1", screen_affinity=1, matches=[Match(wm_class='VirtualBox Machine'), Match(wm_class='VirtualBox Manager'), Match=(wm_class=re.compile('.*remmina|Remmina.*'))]),
        Group(name="1", screen_affinity=1, matches=[Match(wm_class=re.compile('.*remmina|Remmina.*')),Match(wm_class=re.compile('.*VirtualBox.*')),Match(wm_class=re.compile('.*irt-manager,*'))],
              layouts = [layout.MonadTall(
        ratio=0.62,
        margin=6,
        border_width=4,
        border_focus=colors[2],
        new_client_position='after_current',
    ),
    layout.Max(),
    layout.Columns(border_focus=colors[2], border_width=5, margin=5),
]
              ),    
#    Group(name="1", screen_affinity=1, matches=Match(wm_class=[re.compile('.*remmina|Remmina.*'), 'firefox'])),
    Group(name="2", screen_affinity=0),
    Group(name="3", screen_affinity=2,
#          layout="max"
          ),
#    Group(name="3", screen_affinity=2),    
    Group(name="4"),
    Group(name="5"),
    Group(name="6"),
    Group(name="7"),
    Group(name="8", matches=[Match(wm_class=["keepassxc"])]),
    Group(name="9", matches=[Match(wm_class=re.compile('.*teams.*'))]),
]


for i in groups:
    keys.extend(
        [
            # mod1 + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(
        ratio=0.62,
        margin=6,
        border_width=4,
        border_focus=colors[2],
        new_client_position='top',
    ),
    layout.Max(),
    layout.Columns(border_focus=colors[2], border_width=5, margin=5),
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

widget_defaults = dict(
    font="sans",
    fontsize=20,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    #main screen
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth=1,
                    padding=10,
                    foreground=colors[0],
                    background=colors[16],
                ),

                widget.Image(
                    filename="/home/julien/pictures/jia.png",
                    iconsize=9,
                    background=colors[16],
                ),
                widget.GroupBox(
                    background=colors[17],
                    block_highlight_text_color=colors[2],
                    borderwidth=5,
#                    markup=False,
                    this_current_screen_border=colors[2],
                    this_screen_border=colors[1],
                    active=colors[1],
                    other_screen_border=colors[5],
                    other_current_screen_border=colors[11],
                    urgent_border=colors[6],
                ),
                widget.TaskList(
                    highlight_method='border',
                    icon_size=20,
                    max_title_width=150,
                    padding_x=0,
                    padding_y=0,
                    margin_y=0,
                    fontsize=17,
                    border=colors[2],
                    foreground=colors[2],
                    margin=2,
                    borderwidth=1,
                    background=colors[17],
                ),
                widget.Prompt(
                    background=colors[17],
                ),
                widget.Spacer(
                    background=colors[17],
                    length=40),
                widget.CurrentLayoutIcon(
                    background=colors[17],
                ),
                widget.CurrentLayout(
                    background=colors[17],
                ),
#                widget.GroupBox(active='ff9900'),
#                widget.Spacer(length=50),
                
#                widget.WindowName(foreground='ff9900'),
#                widget.Chord(
#                    chords_colors={
#                        "launch": ("#ff0000", "#ffffff"),
#                    },
#                    name_transform=lambda name: name.upper(),
#                ),
#                widget.TextBox("default config", name="default"),
#                widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
#                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
#                # widget.StatusNotifier(),
#                widget.Systray(),
#                widget.Volume(fmt='Vol {}'),
 #               widget.Spacer(length=40),


#                widget.Spacer(length=20),
                
#                widget.PulseVolume(fmt='Vol {}'),
#                widget.Spacer(length=20),
#                widget.BatteryIcon(),

                widget.Spacer(
                    background=colors[17],
                    length=20),
                widget.Wlan(                    
                    format='{essid} {percent:2.0%}',
#                    background=colors[5],
                    background=colors[17],                    
                ),
                widget.Net(
                    interface="wlan0",
                    format='{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}',
#                    background=colors[5],
                    background=colors[17],
                ),
                widget.Memory(
                    background=colors[17],
                    format='Mem{MemPercent}%',
#                    background=colors[9],
                ),
#                widget.Spacer(length=20),
                widget.Clock(
                    format="%H:%M",
                    timezone=pytz.timezone("America/Mexico_City"),
                    foreground=colors[10],
#                    background=colors[8],
                    background=colors[17],
                ),
                widget.Clock(
                    format="%H:%M",
                    timezone=pytz.timezone("America/New_York"),
                    foreground=colors[12],
                    background=colors[17],
                ),
                widget.Clock(
                    format="%Y-%m-%d %a %H:%M",
                    background=colors[17],
                ),
                widget.Clock(
                    format="%H:%M",
                    timezone=pytz.timezone("Asia/Calcutta"),
                    foreground=colors[13],
                    background=colors[17],
                ),
                widget.Clock(
                    format="%H:%M",
                    timezone=pytz.timezone("Australia/Sydney"),
                    foreground=colors[6],
                    background=colors[17],
                ),                
#                widget.Notify(
#                    size=48,
#                    scroll=True,
#                    #width=200,
#                    #height=100,
#                    #scroll_fixed_width=True,
#                ),
                widget.GenPollText(
                    name="do not disturb status",
                    update_interval=5,
                    foreground=colors[14], background=colors[17],
                    fontsize=10,
                    func=lambda: subprocess.check_output("/home/julien/scripts/get-dunst-pause-status.sh").decode("utf-8"),
                ),
                widget.LaunchBar(
                    background=colors[17],
                    progs=[('/home/julien/.local/share/icons/do-not-disturb-OFF.png','/home/julien/scripts/toggle_pause_on_dunst.sh','Do Not Disturb OFF')]
                ),
                widget.Systray(
                    background=colors[16],
                ),
                widget.Battery(
                    background=colors[16],
                    format='{char}{percent:2.0%}'),
#                widget.QuickExit(),
            ],
            24,
#            opacity=0.9,
            background = colors[16],
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    #2nd screen
        Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth=1,
                    padding=10,
                    foreground=colors[0],
                    background=colors[0],
                ),

                widget.Image(
                    filename="/home/julien/pictures/jia.png",
                    iconsize=9,
                    background=colors[0],
                ),
                widget.GroupBox(
                    block_highlight_text_color=colors[2],
                    borderwidth=5,
#                    markup=False,
                    this_current_screen_border=colors[2],
                    this_screen_border=colors[1],
                    active=colors[1],
                    other_screen_border=colors[5],
                    other_current_screen_border=colors[11],
                    urgent_border=colors[6],
                ),
                widget.TaskList(
                    highlight_method='border',
                    icon_size=20,
                    max_title_width=150,
                    padding_x=0,
                    padding_y=0,
                    margin_y=0,
                    fontsize=17,
                    borders=colors[1],
                    foreground=colors[2],
                    margin=2,
                    borderwidth=1,
                    background=colors[0],
                ),
                widget.Prompt(),
                widget.Spacer(length=40),
                widget.CurrentLayoutIcon(),
                widget.CurrentLayout(),
                widget.Clock(
                    format="%Y-%m-%d %a %H:%M",
                    background=colors[17],
                ),                
                ],24)),
#third screen
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth=1,
                    padding=10,
                    foreground=colors[0],
                    background=colors[0],
                ),

                widget.Image(
                    filename="/home/julien/pictures/jia.png",
                    iconsize=9,
                    background=colors[0],
                ),
                widget.GroupBox(
                    block_highlight_text_color=colors[2],
                    borderwidth=5,
#                    markup=False,
                    this_current_screen_border=colors[2],
                    this_screen_border=colors[1],
                    active=colors[1],
                    other_screen_border=colors[5],
                    other_current_screen_border=colors[11],
                    urgent_border=colors[6],
                ),
                widget.TaskList(
                    highlight_method='border',
                    icon_size=20,
                    max_title_width=150,
                    padding_x=0,
                    padding_y=0,
                    margin_y=0,
                    fontsize=17,
                    borders=colors[1],
                    foreground=colors[2],
                    margin=2,
                    borderwidth=1,
                    background=colors[0],
                ),
                widget.Prompt(),
                widget.Spacer(length=40),
                widget.CurrentLayoutIcon(),
                widget.CurrentLayout(),
                widget.Clock(
                    format="%Y-%m-%d %a %H:%M",
                    background=colors[17],
                ),                
                ],24)),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

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
    subprocess.Popen([home])
