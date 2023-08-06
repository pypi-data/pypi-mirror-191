#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import threading
import time
from typing import Union, List, Any, Iterable, TypedDict, Optional, Tuple, cast, Callable

import Xlib.display
import Xlib.protocol
import Xlib.X
import Xlib.Xutil
from Xlib.protocol.rq import Struct
from Xlib.xobject.drawable import Window as XWindow

"""
Additional now-EWMH, but interesting things (maybe under 'extensions' module or similar):
- Hints (get/set for wm_hints and wm_normal_hints)
- Protocols (get/set for wm_protocols)
- Events (window/general listener in separate thread)
"""


def getAllDisplaysInfo() -> dict:
    """
    Gets relevant information on all present displays, including its screens and roots

    Returned dictionary has the following structure:

    "N": Sequential number to separate displays (not related to any actual value)
        "name": display name
        "is_default": ''True'' if it's the default display, ''False'' otherwise
        "screens": sub-dict containing all screens owned by the display
            "M": sequential number to separate screens
            "screen": Struct containing all screen info
            "root": root window (Xlib Window) which belongs to the screen
            "is_default": ''True'' if it's the default screen/root, ''False'' otherwise

    :return: dict with all displays info
    """
    dspInfo: dict = {}
    dsp: Xlib.display.Display = Xlib.display.Display()
    defaultDisplay: str = dsp.get_display_name()
    defaultRoot: XWindow = dsp.screen().root.id
    dsp.close()
    displays: List[str] = os.listdir("/tmp/.X11-unix")
    for i, d in enumerate(displays):
        dspKey: str = str(i)
        if d.startswith("X"):
            dspInfo[dspKey] = {}
            name: str = ":" + d[1:]
            display: Xlib.display.Display = Xlib.display.Display(name)
            dspInfo[dspKey]["name"] = name
            dspInfo[dspKey]["is_default"] = (display.get_display_name() == defaultDisplay)
            dspInfo[dspKey]["screens"] = {}
            for s in range(display.screen_count()):
                scrKey: str = str(s)
                try:
                    dspInfo[dspKey]["screens"][scrKey] = {}
                    screen: Struct = display.screen(s)
                    dspInfo[dspKey]["screens"][scrKey]["screen"] = screen
                    dspInfo[dspKey]["screens"][scrKey]["root"] = screen.root
                    dspInfo[dspKey]["screens"][scrKey]["is_default"] = (screen.root.id == defaultRoot)
                except:
                    pass
            display.close()
    return dspInfo


def getDisplayFromWindow(winId: int) -> Tuple[Xlib.display.Display, Struct, XWindow]:
    """
    Gets display connection and root window from a given window id to which it belongs

    :param winId: id of the window
    :return: tuple containing display name and root window
    """
    dsp: Xlib.display.Display = Xlib.display.Display()
    screen: Struct = dsp.screen()
    root: XWindow = dsp.screen().root
    displays: List[str] = os.listdir("/tmp/.X11-unix")
    check = False
    if len(displays) > 1:
        check = True
    elif len(displays) == 1:
        name: str = ":" + displays[0][1:]
        display: Xlib.display.Display = Xlib.display.Display(name)
        if display.screen_count() > 1:
            check = True
    if check:
        for i, d in enumerate(displays):
            if d.startswith("X"):
                name = ":" + d[1:]
                display = Xlib.display.Display(name)
                atom: int = display.get_atom(Props.Root.CLIENT_LIST)
                for s in range(display.screen_count()):
                    try:
                        windows = []
                        scr: Struct = display.screen(s)
                        r: XWindow = scr.root
                        ret: Union[Xlib.protocol.request.GetProperty, None] = r.get_full_property(atom, Xlib.X.AnyPropertyType)
                        if ret and hasattr(ret, "value"):
                            windows = ret.value
                        for w in windows:
                            if w == winId:
                                dsp.close()
                                return display, scr, r
                    except:
                        pass
                display.close()
    return dsp, screen, root


def getDisplayFromRoot(rootId: int) -> Tuple[Xlib.display.Display, Struct, XWindow]:
    """
    Gets display connection and root window from a given root id to which it belongs

    :param rootId: id of the target root
    :return: tuple containing display name and root window
    """
    dsp: Xlib.display.Display = Xlib.display.Display()
    screen: Struct = dsp.screen()
    root: XWindow = screen.root
    displays: List[str] = os.listdir("/tmp/.X11-unix")
    check = False
    if len(displays) > 1:
        check = True
    elif len(displays) == 1:
        name: str = ":" + displays[0][1:]
        display: Xlib.display.Display = Xlib.display.Display(name)
        if display.screen_count() > 1:
            check = True
    if check:
        for i, d in enumerate(displays):
            if d.startswith("X"):
                name = ":" + d[1:]
                display = Xlib.display.Display(name)
                for s in range(display.screen_count()):
                    try:
                        scr: Struct = display.screen(s)
                        r: XWindow = scr.root
                        if rootId == r.id:
                            dsp.close()
                            return display, scr, r
                    except:
                        pass
                display.close()
    return dsp, screen, root


class WmProtocols:
    # Is this necessary/interesting?

    class Requests:
        PING = "_NET_WM_PING"
        SYNC = "_NET_WM_SYNC_REQUEST"

    def ping(self, winId):
        pass

    def sync(self, winId):
        pass


class Props:

    class Root:

        SUPPORTED = "_NET_SUPPORTED"
        CLIENT_LIST = "_NET_CLIENT_LIST"
        CLIENT_LIST_STACKING = "_NET_CLIENT_LIST_STACKING"
        NUMBER_OF_DESKTOPS = "_NET_NUMBER_OF_DESKTOPS"
        DESKTOP_GEOMETRY = "_NET_DESKTOP_GEOMETRY"
        DESKTOP_VIEWPORT = "_NET_DESKTOP_VIEWPORT"
        CURRENT_DESKTOP = "_NET_CURRENT_DESKTOP"
        DESKTOP_NAMES = "_NET_DESKTOP_NAMES"
        ACTIVE = "_NET_ACTIVE_WINDOW"
        WORKAREA = "_NET_WORKAREA"
        SUPPORTING_WM_CHECK = "_NET_SUPPORTING_WM_CHECK"
        VIRTUAL_ROOTS = "_NET_VIRTUAL_ROOTS"
        SHOWING_DESKTOP = "_NET_SHOWING_DESKTOP"

        DESKTOP_LAYOUT = "_NET_DESKTOP_LAYOUT"
        class DesktopLayout:
            ORIENTATION_HORZ = 0
            ORIENTATION_VERT = 1
            TOPLEFT = 0
            TOPRIGHT = 1
            BOTTOMRIGHT = 2
            BOTTOMLEFT = 3

        # Additional Root properties (always related to a specific window)
        CLOSE = "_NET_CLOSE_WINDOW"
        MOVERESIZE = "_NET_MOVERESIZE_WINDOW"
        WM_MOVERESIZE = "_NET_WM_MOVERESIZE"
        RESTACK = "_NET_RESTACK_WINDOW"
        REQ_FRAME_EXTENTS = "_NET_REQUEST_FRAME_EXTENTS"

    class Window:

        NAME = "_NET_WM_NAME"
        VISIBLE_NAME = "_NET_WM_VISIBLE_NAME"
        ICON_NAME = "_NET_WM_ICON_NAME"
        VISIBLE_ICON_NAME = "_NET_WM_VISIBLE_ICON_NAME"
        DESKTOP = "_NET_WM_DESKTOP"

        WM_WINDOW_TYPE = "_NET_WM_WINDOW_TYPE"
        class WindowType:
            DESKTOP = "_NET_WM_WINDOW_TYPE_DESKTOP"
            DOCK = "_NET_WM_WINDOW_TYPE_DOCK"
            TOOLBAR = "_NET_WM_WINDOW_TYPE_TOOLBAR"
            MENU = "_NET_WM_WINDOW_TYPE_MENU"
            UTILITY = "_NET_WM_WINDOW_TYPE_UTILITY"
            SPLASH = "_NET_WM_WINDOW_TYPE_SPLASH"
            DIALOG = "_NET_WM_WINDOW_TYPE_DIALOG"
            NORMAL = "_NET_WM_WINDOW_TYPE_NORMAL"

        CHANGE_STATE = "WM_CHANGE_STATE"
        WM_STATE = "_NET_WM_STATE"
        class State:
            MODAL = "_NET_WM_STATE_MODAL"
            STICKY = "_NET_WM_STATE_STICKY"
            MAXIMIZED_VERT = "_NET_WM_STATE_MAXIMIZED_VERT"
            MAXIMIZED_HORZ = "_NET_WM_STATE_MAXIMIZED_HORZ"
            SHADED = "_NET_WM_STATE_SHADED"
            SKIP_TASKBAR = "_NET_WM_STATE_SKIP_TASKBAR"
            SKIP_PAGER = "_NET_WM_STATE_SKIP_PAGER"
            HIDDEN = "_NET_WM_STATE_HIDDEN"
            FULLSCREEN = "_NET_WM_STATE_FULLSCREEN"
            ABOVE = "_NET_WM_STATE_ABOVE"
            BELOW = "_NET_WM_STATE_BELOW"
            DEMANDS_ATTENTION = "_NET_WM_STATE_DEMANDS_ATTENTION"
            FOCUSED = "_NET_WM_STATE_FOCUSED"

            class Action:
                REMOVE = 0
                ADD = 1
                TOGGLE = 2

        ALLOWED_ACTIONS = "_NET_WM_ALLOWED_ACTIONS"
        STRUT = "_NET_WM_STRUT"
        STRUT_PARTIAL = "_NET_WM_STRUT_PARTIAL"
        ICON_GEOMETRY = "_NET_WM_ICON_GEOMETRY"
        ICON = "_NET_WM_ICON"
        PID = "_NET_WM_PID"
        HANDLED_ICONS = "_NET_WM_HANDLED_ICONS"
        USER_TIME = "_NET_WM_USER_TIME"
        FRAME_EXTENTS = "_NET_FRAME_EXTENTS"

        # These are Root properties, but always related to a specific window
        ACTIVE = "_NET_ACTIVE_WINDOW"
        CLOSE = "_NET_CLOSE_WINDOW"
        
        MOVERESIZE = "_NET_MOVERESIZE_WINDOW"
        class MoveResize:
            SIZE_TOPLEFT = 0
            SIZE_TOP = 1
            SIZE_TOPRIGHT = 2
            SIZE_RIGHT = 3
            SIZE_BOTTOMRIGHT = 4
            SIZE_BOTTOM = 5
            SIZE_BOTTOMLEFT = 6
            SIZE_LEFT = 7
            MOVE = 8            # movement only
            SIZE_KEYBOARD = 9   # size via keyboard
            MOVE_KEYBOARD = 10  # move via keyboard
            
        WM_MOVERESIZE = "_NET_WM_MOVERESIZE"
        RESTACK = "_NET_RESTACK_WINDOW"
        REQ_FRAME_EXTENTS = "_NET_REQUEST_FRAME_EXTENTS"

    class Format:
        STR = 8
        INT = 32

    class Mode:
        REPLACE = Xlib.X.PropModeReplace
        APPEND = Xlib.X.PropModeAppend
        PREPEND = Xlib.X.PropModePrepend


class Structs:
    """
    Will this be really necessary?

    Leaving these as examples...
    """

    class GetProperty(TypedDict):
        # <class 'Xlib.protocol.request.GetProperty'> serial = 105, data = {'sequence_number': 105, 'property_type': 33, 'bytes_after': 0, 'value': (32, array('I', [44040202]))}, error = None>
        # how to parse this: (32, array('I', [44040202])). It contains format, type and value itself... useful!
        sequence_number: int
        property_type: int
        bytes_after: int
        value: Union[List[int], str]

    class WmHints(TypedDict):
        # {'flags': 103, 'input': 1, 'initial_state': 1, 'icon_pixmap': <Pixmap 0x02a22304>, 'icon_window': <Window 0x00000000>, 'icon_x': 0, 'icon_y': 0, 'icon_mask': <Pixmap 0x02a2230b>, 'window_group': <Window 0x02a00001>}
        flags: int
        input: int
        initial_state: int
        icon_pixmap: Xlib.xobject.drawable.Pixmap
        icon_window: Xlib.xobject.drawable.Window
        icon_x: int
        icon_y: int
        icon_mask: Xlib.xobject.drawable.Pixmap
        window_group: Xlib.xobject.drawable.Window


class RootWindow:
    """
    Base class to access root features
    """

    def __init__(self, rootId: int = 0):

        if rootId:
            self.display, self.screen, self.root = getDisplayFromRoot(rootId)
        else:
            self.display = Xlib.display.Display()
            self.screen = self.display.screen()
            self.root = self.screen.root
        self.id: int = self.root.id

    def getProperty(self, prop: Union[str, int]) -> Union[List[int], List[str], str, None]:

        if isinstance(prop, str):
            prop = self.display.get_atom(prop, True)

        if prop != 0:
            ret = self.root.get_full_property(prop, Xlib.X.AnyPropertyType)
            if ret and hasattr(ret, "value"):
                if isinstance(ret.value, str):
                    return ret.value
                elif isinstance(ret.value, bytes):
                    return ret.value.decode()
                elif isinstance(ret.value, Iterable):
                    return [a for a in ret.value]
                else:
                    return ret.value
        return None

    def setProperty(self, prop: Union[str, int], data: Union[List[int], str]):

        if isinstance(prop, str):
            prop = self.display.get_atom(prop, True)

        if prop != 0:
            ev: Xlib.protocol.event.ClientMessage = Xlib.protocol.event.ClientMessage(window=self.root, client_type=prop, data=(format, data))
            mask: int = Xlib.X.SubstructureRedirectMask | Xlib.X.SubstructureNotifyMask
            self.root.send_event(event=ev, event_mask=mask)
            self.display.flush()

    def sendMessage(self, winId, prop: Union[str, int], data: Union[List[int], str]):

        if isinstance(prop, str):
            prop = self.display.get_atom(prop, True)

        if prop != 0:
            # I think (to be confirmed) that 16 is not used in Python (no difference between short and long int)
            if isinstance(data, str):
                dataFormat: int = 8
            else:
                data = (data + [0] * (5 - len(data)))[:5]
                dataFormat = 32

            ev: Xlib.protocol.event.ClientMessage = Xlib.protocol.event.ClientMessage(window=winId, client_type=prop, data=(dataFormat, data))
            mask: int = Xlib.X.SubstructureRedirectMask | Xlib.X.SubstructureNotifyMask
            self.display.send_event(destination=self.root.id, event=ev, event_mask=mask)
            self.display.flush()

    def getSupported(self, text=False) -> Union[List[int], List[str]]:
        """
        Returns the list of supported hints by the Window Manager.

        This property MUST be set by the Window Manager to indicate which hints it supports. For example:
        considering _NET_WM_STATE both this atom and all supported states e.g. _NET_WM_STATE_MODAL,
        _NET_WM_STATE_STICKY, would be listed. This assumes that backwards incompatible changes will not be made
        to the hints (without being renamed).

        :param text: if ''True'' the values will be returned as strings, or as integers if ''False''
        :return: supported hints as a list of strings / integers
        """
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.SUPPORTED)
        hints: List[int] = []
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            hints = cast(List[int], ret)
            if text:
                res: List[str] = []
                for h in hints:
                    try:
                        name = self.display.get_atom_name(h)
                        res.append(name)
                    except:
                        pass
                return res
            else:
                return [h for h in hints]
        return hints

    def getClientList(self) -> List[int]:
        """
        Returns the list of XWindows currently opened and managed by the Window Manager, ordered older-to-newer.

        These arrays contain all X Windows managed by the Window Manager. _NET_CLIENT_LIST has initial mapping order,
        starting with the oldest window. These properties SHOULD be set and updated by the Window Manager.

        :return: list of integers (XWindows id's)
        """
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.CLIENT_LIST)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return cast(List[int], ret)
        res: List[int] = []
        return res

    def getClientListStacking(self) -> List[int]:
        """
        Returns the list of XWindows currently opened and managed by the Window Manager, ordered in bottom-to-top.

        These arrays contain all X Windows managed by the Window Manager. _NET_CLIENT_LIST_STACKING has
        bottom-to-top stacking order. These properties SHOULD be set and updated by the Window Manager.

        :return: list of integers (XWindows id's)
        """
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.CLIENT_LIST_STACKING)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return cast(List[int], ret)
        res: List[int] = []
        return res

    def getNumberOfDesktops(self) -> int:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.NUMBER_OF_DESKTOPS)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return ret[0]
        return 0

    def setNumberOfDesktops(self, number):
        self.setProperty(Props.Root.NUMBER_OF_DESKTOPS, [number])

    def getDesktopGeometry(self) -> Union[List[int], None]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.DESKTOP_GEOMETRY)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return cast(List[int], ret)
        return None

    def setDesktopGeometry(self, newWidth, newHeight):
        self.setProperty(Props.Root.DESKTOP_GEOMETRY, [newWidth, newHeight])

    def getDesktopViewport(self) -> Union[List[int], None]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.DESKTOP_VIEWPORT)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return cast(List[int], ret)
        return None

    def setDesktopViewport(self, newWidth, newHeight):
        self.setProperty(Props.Root.DESKTOP_VIEWPORT, [newWidth, newHeight])

    def getCurrentDesktop(self) -> Union[List[int], None]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.CURRENT_DESKTOP)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return cast(List[int], ret)
        return None

    def setCurrentDesktop(self, newDesktop):
        if newDesktop <= self.getNumberOfDesktops() and newDesktop != self.getCurrentDesktop():
            self.setProperty(Props.Root.CURRENT_DESKTOP, [newDesktop, Xlib.X.CurrentTime])

    def getDesktopNames(self) -> Union[List[str], None]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.DESKTOP_NAMES)
        if ret:
            res: List[str] = []
            if isinstance(ret, str):
                res = [ret.rstrip('\x00')]  # Where does that '\x00' comes out from?
            elif isinstance(ret, list) and isinstance(ret[0], str):
                res = cast(List[str], ret)
            return res
        return None

    def getActiveWindow(self) -> Union[int, None]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.ACTIVE)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return int(ret[0])
        return None

    def getWorkArea(self) -> Union[List[int], None]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.WORKAREA)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return cast(List[int], ret)
        return None

    def getSupportingWMCheck(self) -> Union[List[int], None]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.SUPPORTING_WM_CHECK)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return cast(List[int], ret)
        return None

    def getVirtualRoots(self) -> Union[List[int], None]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.VIRTUAL_ROOTS)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return cast(List[int], ret)
        return None

    def getDesktopLayout(self) -> Union[List[int], None]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.DESKTOP_LAYOUT)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return cast(List[int], ret)
        return None

    def setDesktopLayout(self, orientation, columns, rows, starting_corner):
        self.setProperty(Props.Root.DESKTOP_LAYOUT, [orientation, columns, rows, starting_corner])

    def getShowingDesktop(self) -> bool:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Root.SHOWING_DESKTOP)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return bool(ret and ret[0] != 0)
        return False

    def setShowingDesktop(self, show: bool):
        if self.getShowingDesktop() != show:
            self.setProperty(Props.Root.SHOWING_DESKTOP, [1 if show else 0])

    """
    Methods below are always related to a given window. 
    Makes it sense to include them within Window class instead of here?
    """

    def setClosed(self, winId, userAction: bool = False):
        atom: int = self.display.get_atom(Props.Root.CLOSE, True)
        self.sendMessage(winId, atom, [Xlib.X.CurrentTime, 2 if userAction else 1])

    def setMoveResize(self, winId, gravity=0, x=None, y=None, width=None, height=None, userAction=False):
        gravity_flags = gravity | 0b0000100000000000
        if x is None:
            x = 0
        else:
            gravity_flags = gravity_flags | 0b0000010000000000
        if y is None:
            y = 0
        else:
            gravity_flags = gravity_flags | 0b0000001000000000
        if width is None:
            width = 0
        else:
            gravity_flags = gravity_flags | 0b0000000100000000
        if height is None:
            height = 0
        else:
            gravity_flags = gravity_flags | 0b0000000010000000
        atom: int = self.display.get_atom(Props.Root.MOVERESIZE, True)  # type: ignore[annotation-unchecked]
        self.sendMessage(winId, atom, [gravity_flags, x, y, width, height, 2 if userAction else 1])

    def setWmMoveResize(self, winId, x_root, y_root, orientation, button, userAction=False):
        """
        This message allows Clients to initiate window movement or resizing. They can define their own move and size
        "grips", whilst letting the Window Manager control the actual operation. This means that all moves/resizes
        can happen in a consistent manner as defined by the Window Manager. See the section called “Source indication
        in requests” for details on the source indication.

        When sending this message in response to a button press event, button SHOULD indicate the button which
        was pressed, x_root and y_root MUST indicate the position of the button press with respect to the root window
        and direction MUST indicate whether this is a move or resize event, and if it is a resize event, which edges
        of the window the size grip applies to. When sending this message in response to a key event, the direction
        MUST indicate whether this is a move or resize event and the other fields are unused.

        The Client MUST release all grabs prior to sending such message.

        The Window Manager can use the button field to determine the events on which it terminates the operation
        initiated by the _NET_WM_MOVERESIZE message. Since there is a race condition between a client sending the
        _NET_WM_MOVERESIZE message and the user releasing the button, Window Managers are advised to offer some
        other means to terminate the operation, e.g. by pressing the ESC key.

        :param winId: id of the window to be moved/resized
        :param x_root: position of the button press with respect to the root window
        :param y_root: position of the button press with respect to the root window
        :param orientation: move or resize event
        :param button: button pressed
        :param userAction:
        """
        # Need to understand this property
        atom: int = self.display.get_atom(Props.Root.WM_MOVERESIZE, True)  # type: ignore[annotation-unchecked]
        self.sendMessage(winId, atom, [x_root, y_root, orientation, button, 2 if userAction else 1])

    def setStacking(self, winId, siblingId, detail, userAction = False):
        """
        This request is similar to ConfigureRequest with CWSibling and CWStackMode flags. It should be used only by
        pagers, applications can use normal ConfigureRequests. The source indication field should be therefore
        set to 2, see the section called “Source indication in requests” for details.

        Rationale: A Window Manager may put restrictions on configure requests from applications, for example it may
        under some conditions refuse to raise a window. This request makes it clear it comes from a pager or similar
        tool, and therefore the Window Manager should always obey it.

        :param winId: id of window to be restacked
        :param siblingId: id of sibling window related to restacking action
        :param detail: ???
        :param userAction: should be set to 2 (typically used by pagers)
        """
        # Need to understand this property
        atom: int = self.display.get_atom(Props.Root.RESTACK, True)  # type: ignore[annotation-unchecked]
        self.sendMessage(winId, atom, [2 if userAction else 1, siblingId, detail])

    def requestFrameExtents(self, winId: int):
        """
        A Client whose window has not yet been mapped can request of the Window Manager an estimate of the
        frame extents it will be given upon mapping. To retrieve such an estimate, the Client MUST send a
        _NET_REQUEST_FRAME_EXTENTS message to the root window. The Window Manager MUST respond by estimating
        the prospective frame extents and setting the window's _NET_FRAME_EXTENTS property accordingly.
        The Client MUST handle the resulting _NET_FRAME_EXTENTS PropertyNotify event. So that the Window Manager
        has a good basis for estimation, the Client MUST set any window properties it intends to set before
        sending this message. The Client MUST be able to cope with imperfect estimates.

        Rationale: A client cannot calculate the dimensions of its window's frame before the window is mapped,
        but some toolkits need this information. Asking the window manager for an estimate of the extents is a
        workable solution. The estimate may depend on the current theme, font sizes or other window properties.
        The client can track changes to the frame's dimensions by listening for _NET_FRAME_EXTENTS PropertyNotify event

        :param winId: id of window for which estimate the frame extents
        """
        # Need to understand this property
        atom: int = self.display.get_atom(Props.Root.REQ_FRAME_EXTENTS, True)  # type: ignore[annotation-unchecked]
        self.sendMessage(winId, atom, [])


class Window:

    def __init__(self, winId: int):

        # Can root change? If so, we can refresh it before any root-related action
        # Can display change? Don't think so. And, if so, better to invalidate the window object
        self.display, self.screen, self.root = getDisplayFromWindow(winId)
        self.rootWindow: RootWindow = RootWindow(self.root.id)
        self.xWindow: XWindow = self.display.create_resource_object('window', winId)
        self.id: int = winId
        self.extensions = self._Extensions(winId, self.display, self.root)

    def getProperty(self, prop: Union[str, int]) -> Union[List[int], List[str], str, None]:

        if isinstance(prop, str):
            prop = self.display.get_atom(prop, True)

        if prop != 0:
            ret: Optional[Xlib.protocol.request.GetProperty] = self.xWindow.get_full_property(prop, Xlib.X.AnyPropertyType)
            if ret and hasattr(ret, "value"):
                # Can also ask for getattr(ret, "value")[0] to check returned data format, but don't see much benefit
                if isinstance(ret.value, str):
                    return ret.value
                elif isinstance(ret.value, bytes):
                    return ret.value.decode()
                elif isinstance(ret.value, Iterable):
                    return [a for a in ret.value]
                else:
                    return ret.value
        return None

    def sendMessage(self, prop: Union[str, int], data: Union[List[int], str]):

        if isinstance(prop, str):
            prop = self.display.get_atom(prop, True)

        if prop != 0:
            # I think (to be confirmed) that 16 is not used in Python (no difference between short and long int)
            if isinstance(data, str):
                dataFormat = 8
            else:
                data = (data + [0] * (5 - len(data)))[:5]
                dataFormat = 32

            ev = Xlib.protocol.event.ClientMessage(window=self.xWindow.id, client_type=prop, data=(dataFormat, data))
            mask = Xlib.X.SubstructureRedirectMask | Xlib.X.SubstructureNotifyMask
            # Can root change? If so, we can refresh it before any root-related action
            # _, self.root = getDisplayFromWindow(self.id)
            self.display.send_event(destination=self.root.id, event=ev, event_mask=mask)
            self.display.flush()

    def changeProperty(self, prop: Union[str, int], dataFormat: int, data: List[int], propMode: int = Xlib.X.PropModeReplace):

        if propMode not in (Props.Mode.REPLACE, Props.Mode.APPEND, Props.Mode.PREPEND):
            return

        if isinstance(prop, str):
            prop = self.display.get_atom(prop, True)

        if prop != 0:
            self.xWindow.change_property(prop, Xlib.Xatom.ATOM, dataFormat, data, propMode)
            self.display.flush()

    def getName(self) -> str:
        name = ""
        try:
            ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Window.NAME)
            if ret:
                if isinstance(ret, str):
                    name = ret
                if isinstance(ret, bytes):
                    name = ret.decode()
        except:
            pass
        return name

    def setName(self, name: str):
        self.sendMessage(Props.Window.NAME, name)

    def getVisibleName(self) -> str:
        name = ""
        try:
            ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Window.VISIBLE_NAME)
            if ret:
                if isinstance(ret, str):
                    name = ret
                if isinstance(ret, bytes):
                    name = ret.decode()
        except:
            pass
        return name

    def setVisibleName(self, name: str):
        self.sendMessage(Props.Window.VISIBLE_NAME, name)

    def getIconName(self) -> str:
        name = ""
        try:
            ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Window.ICON_NAME)
            if ret:
                if isinstance(ret, str):
                    name = ret
                if isinstance(ret, bytes):
                    name = ret.decode()
        except:
            pass
        return name

    def setIconName(self, name: str):
        self.sendMessage(Props.Window.ICON, name)

    def getVisibleIconName(self) -> str:
        name = ""
        try:
            ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Window.VISIBLE_ICON_NAME)
            if ret:
                if isinstance(ret, str):
                    name = ret
                if isinstance(ret, bytes):
                    name = ret.decode()
        except:
            pass
        return name

    def setVisibleIconName(self, name: str):
        self.sendMessage(Props.Window.VISIBLE_ICON_NAME, name)

    def getDesktop(self) -> Union[int, None]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Window.DESKTOP)
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            return int(ret[0])
        return None

    def setDesktop(self, newDesktop, userAction=False):
        # Can root change? If so, we can refresh it before any root-related action
        # _, self.root = getDisplayFromWindow(self.id)
        if newDesktop <= self.rootWindow.getNumberOfDesktops() and newDesktop != self.rootWindow.getCurrentDesktop():
            self.sendMessage(Props.Window.DESKTOP, [newDesktop, Xlib.X.CurrentTime, 2 if userAction else 1])

    def getWmWindowType(self, text: bool = False) -> Union[List[int], List[str]]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Window.WM_WINDOW_TYPE)
        types: List[int] = []
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            types = cast(List[int], ret)
            if text:
                res: List[str] = []
                for t in types:
                    try:
                        res.append(self.display.get_atom_name(t))
                    except:
                        pass
                return res
            else:
                return [s for s in types]
        return types

    def setWmWindowType(self, winType: Union[int, str]):

        if isinstance(winType, str):
            winType = self.display.get_atom(winType, True)
        # self.win.unmap()  # -> Needed???
        self.changeProperty(Props.Window.WM_WINDOW_TYPE, 32, [winType])
        self.xWindow.map()
        self.display.flush()

    def getWmState(self, text: bool = False) -> Union[List[int], List[str]]:
        ret: Union[List[int], List[str], str, None] = self.getProperty(Props.Window.WM_STATE)
        states: List[int] = []
        if ret and isinstance(ret, list) and isinstance(ret[0], int):
            states = cast(List[int], ret)
            if text:
                res: List[str] = []
                for s in states:
                    try:
                        res.append(self.display.get_atom_name(s))
                    except:
                        pass
                return res
            else:
                return [s for s in states]
        return states

    def changeWmState(self, action: int, state: Union[int, str], state2: Union[int, str] = 0, userAction: bool = False):

        if action in (Props.Window.State.Action.ADD, Props.Window.State.Action.REMOVE, Props.Window.State.Action.TOGGLE):
            if isinstance(state, str):
                state = self.display.get_atom(state, True)
            if isinstance(state2, str):
                state2 = self.display.get_atom(state2, True)
            self.sendMessage(Props.Window.WM_STATE, [action, state, state2, 2 if userAction else 1])

    def setMaximized(self, maxHorz: bool, maxVert: bool):
        state1 = 0
        state2 = 0
        states = self.getWmState(True)
        if maxHorz and maxVert:
            if Props.Window.State.MAXIMIZED_HORZ not in states:
                state1 = self.display.get_atom(Props.Window.State.MAXIMIZED_HORZ, True)
            if Props.Window.State.MAXIMIZED_VERT not in states:
                state2 = self.display.get_atom(Props.Window.State.MAXIMIZED_VERT, True)
            if state1 or state2:
                self.changeWmState(1, state1 if state1 else state2, state2 if state1 else 0, False)
        elif maxHorz:
            if Props.Window.State.MAXIMIZED_HORZ not in states:
                state = self.display.get_atom(Props.Window.State.MAXIMIZED_HORZ, True)
                self.changeWmState(1, state, 0, False)
            if Props.Window.State.MAXIMIZED_VERT in states:
                state = self.display.get_atom(Props.Window.State.MAXIMIZED_VERT, True)
                self.changeWmState(0, state, 0, False)
        elif maxVert:
            if Props.Window.State.MAXIMIZED_HORZ in states:
                state = self.display.get_atom(Props.Window.State.MAXIMIZED_HORZ, True)
                self.changeWmState(0, state, 0, False)
            if Props.Window.State.MAXIMIZED_VERT not in states:
                state = self.display.get_atom(Props.Window.State.MAXIMIZED_VERT, True)
                self.changeWmState(1, state, 0, False)
        else:
            if Props.Window.State.MAXIMIZED_HORZ in states:
                state1 = self.display.get_atom(Props.Window.State.MAXIMIZED_HORZ, True)
            if Props.Window.State.MAXIMIZED_VERT in states:
                state2 = self.display.get_atom(Props.Window.State.MAXIMIZED_VERT, True)
            if state1 or state2:
                self.changeWmState(0, state1 if state1 else state2, state2 if state1 else 0, False)

    def setMinimized(self):
        if Props.Window.State.HIDDEN not in self.getWmState():
            atom = self.display.get_atom(Props.Window.CHANGE_STATE, True)
            self.sendMessage(atom, [Xlib.Xutil.IconicState])

    def getAllowedActions(self, text=False):
        acts = self.getProperty(Props.Window.ALLOWED_ACTIONS)
        if text:
            ret = []
            for a in acts:
                try:
                    ret.append(self.display.get_atom_name(a))
                except:
                    pass
            return ret
        else:
            return acts

    def setAllowedActions(self):
        # Can this be set??? Investigate wm_protocols, which might be related (e.g. 'WM_DELETE_WINDOW')
        pass

    def getStrut(self):
        """
        This property is equivalent to a _NET_WM_STRUT_PARTIAL property where all start values are 0 and all
        end values are the height or width of the logical screen. _NET_WM_STRUT_PARTIAL was introduced later
        than _NET_WM_STRUT, however, so clients MAY set this property in addition to _NET_WM_STRUT_PARTIAL to
        ensure backward compatibility with Window Managers supporting older versions of the Specification.

        :return:
        """
        return self.getProperty(Props.Window.STRUT)

    def setStrut(self, left, right, top, bottom):
        # Need to understand this
        self.sendMessage(Props.Window.STRUT, [left, right, top, bottom])

    def getStrutPartial(self):
        """
        This property MUST be set by the Client if the window is to reserve space at the edge of the screen.
        The property contains 4 cardinals specifying the width of the reserved area at each border of the screen,
        and an additional 8 cardinals specifying the beginning and end corresponding to each of the four struts.
        The order of the values is left, right, top, bottom, left_start_y, left_end_y, right_start_y, right_end_y,
        top_start_x, top_end_x, bottom_start_x, bottom_end_x. All coordinates are root window coordinates.
        The client MAY change this property at any time, therefore the Window Manager MUST watch for property
        notify events if the Window Manager uses this property to assign special semantics to the window.

        If both this property and the _NET_WM_STRUT property are set, the Window Manager MUST ignore the _NET_WM_STRUT
        property values and use instead the values for _NET_WM_STRUT_PARTIAL. This will ensure that Clients can safely
        set both properties without giving up the improved semantics of the new property.

        The purpose of struts is to reserve space at the borders of the desktop. This is very useful for a docking area,
        a taskbar or a panel, for instance. The Window Manager should take this reserved area into account when
        constraining window positions - maximized windows, for example, should not cover that area.

        The start and end values associated with each strut allow areas to be reserved which do not span the entire
        width or height of the screen. Struts MUST be specified in root window coordinates, that is, they are not
        relative to the edges of any view port or Xinerama monitor.

        For example, for a panel-style Client appearing at the bottom of the screen, 50 pixels tall, and occupying
        the space from 200-600 pixels from the left of the screen edge would set a bottom strut of 50, and set
        bottom_start_x to 200 and bottom_end_x to 600. Another example is a panel on a screen using the Xinerama
        extension. Assume that the set up uses two monitors, one running at 1280x1024 and the other to the right
        running at 1024x768, with the top edge of the two physical displays aligned. If the panel wants to fill the
        entire bottom edge of the smaller display with a panel 50 pixels tall, it should set a bottom strut of 306,
        with bottom_start_x of 1280, and bottom_end_x of 2303. Note that the strut is relative to the screen edge,
        and not the edge of the xinerama monitor.

        Rationale: A simple "do not cover" hint is not enough for dealing with e.g. auto-hide panels.

        Notes: An auto-hide panel SHOULD set the strut to be its minimum, hidden size. A "corner" panel that does not
        extend for the full length of a screen border SHOULD only set one strut.

        :return:
        """
        return self.getProperty(Props.Window.STRUT_PARTIAL)

    def setStrutPartial(self, left, right, top, bottom,
                        left_start_y, left_end_y, right_start_y, right_end_y,
                        top_start_x, top_end_x, bottom_start_x, bottom_end_x,):
        # Need to understand this
        pass

    def getIconGeometry(self):
        return self.getProperty(Props.Window.ICON_GEOMETRY)

    def getPid(self) -> Union[int, None]:
        ret = self.getProperty(Props.Window.PID)
        if ret:
            return int(ret[0])
        return None

    def getHandledIcons(self):
        return self.getProperty(Props.Window.HANDLED_ICONS)

    def getUserTime(self):
        return self.getProperty(Props.Window.USER_TIME)

    def getFrameExtents(self):
        prop = "_GTK_FRAME_EXTENTS"
        atom = self.display.intern_atom(prop, True)
        if not atom:
            prop = "_NET_FRAME_EXTENTS"
        return self.getProperty(prop)

    def setActive(self, userAction: bool = False):
        atom = self.display.get_atom(Props.Window.ACTIVE, True)
        self.sendMessage(atom, [2 if userAction else 1, Xlib.X.CurrentTime, self.xWindow.id])

    def setClosed(self, userAction: bool = False):
        atom = self.display.get_atom(Props.Window.CLOSE, True)
        self.sendMessage(atom, [Xlib.X.CurrentTime, 2 if userAction else 1])

    def setMoveResize(self, gravity=0, x=None, y=None, width=None, height=None, userAction=False):
        # gravity_flags directly taken from 'old' ewmh module
        gravity_flags = gravity | 0b0000100000000000
        if x is None:
            x = 0
        else:
            gravity_flags = gravity_flags | 0b0000010000000000
        if y is None:
            y = 0
        else:
            gravity_flags = gravity_flags | 0b0000001000000000
        if width is None:
            width = 0
        else:
            gravity_flags = gravity_flags | 0b0000000100000000
        if height is None:
            height = 0
        else:
            gravity_flags = gravity_flags | 0b0000000010000000
        # atom = self.display.get_atom(Props.Window.MOVERESIZE, True)
        # self.sendMessage(atom, [gravity_flags, x, y, width, height, 2 if userAction else 1])
        # This works much better and in all cases?!?!?!
        self.xWindow.configure(x=x, y=y, width=width, heihgt=height)
        self.display.flush()

    def setStacking(self, mode: int):
        self.xWindow.configure(stack_mode=mode)
        self.display.flush()

    def setWmMoveResize(self, x_root, y_root, orientation, button, userAction=False):
        # Need to understand this property
        atom = self.display.get_atom(Props.Window.WM_MOVERESIZE, True)
        self.sendMessage(atom, [x_root, y_root, orientation, button, 2 if userAction else 1])

    def setStacking(self):
        # Need to understand this property
        atom = self.display.get_atom(Props.Window.RESTACK, True)
        self.sendMessage(atom, [])

    def requestFrameExtents(self):
        # Need to understand this property -> Will the id be available if the window has not been mapped yet?
        atom = self.display.get_atom(Props.Window.REQ_FRAME_EXTENTS, True)
        self.sendMessage(atom, [])

    class _Extensions:

        def __init__(self, winId: int, display, root):
            self.winId = winId
            self.display = display
            self.root = root
            self.win = self.display.create_resource_object('window', winId)

        def getWmHints(self):
            return self.win.get_wm_hints()

        def setWmHints(self, hint: str, value: Any):
            hints: Xlib.protocol.rq.DictWrapper = self.win.get_wm_hints()
            if hints:
                hints[hint] = value
                # We should also re-calculate and re-write flags
            self.win.set_wm_hints(hints)
            self.display.flush()

        def getWmNormalHints(self):
            return self.win.get_wm_normal_hints()

        def setWmNormalHints(self, hint, value):
            pass

        def getWmProtocols(self, text=False):
            ret = self.win.get_wm_protocols()
            prots = ret if ret else []
            if text:
                res = []
                for p in prots:
                    try:
                        res.append(self.display.get_atom_name(p))
                    except:
                        pass
                return res
            else:
                return [p for p in prots]

        def addWmProtocol(self, atom):
            prots = self.win.get_wm_protocols()
            if atom not in prots:
                prots.append(atom)
            self.win.set_wm_protocols(prots)
            self.display.flush()

        def delWmProtocol(self, atom):
            prots = self.win.get_wm_protocols()
            new_prots = [p for p in prots if p != atom]
            prots = new_prots
            self.win.set_wm_protocols(prots)

        def checkEvents(self, events: List[int], mask: int, callback: Callable[[Xlib.protocol.rq.Event], None], winId: int = 0):
            if not winId:
                winId = self.winId
            eventsObject = self.CheckEvents(winId, self.display, self.root, events, mask, callback)
            return eventsObject

        class CheckEvents:

            def __init__(self, winId: int, display: Xlib.display.Display, root: XWindow, events: List[int], mask: int, callback: Callable[[Xlib.protocol.rq.Event], None]):

                self._winId = winId
                self._display = display
                self._root = root
                self._events = events
                self._mask = mask

                self._root.change_attributes(event_mask=self._mask)
                self._display.flush()

                self._keep = threading.Event()
                self._stopRequested = False
                self._callback = callback
                self._checkThread = None
                self._threadStarted = False

            def _checkDisplayEvents(self):

                while self._keep.wait():
                    if not self._stopRequested:
                        if self._root.display.pending_events():
                            event = self._root.display.next_event()
                            if self._winId == event.window.id and event.type in self._events:
                                self._callback(event)
                        time.sleep(0.1)
                    else:
                        # Is this necessary to somehow "free" the events catching???
                        self._root.change_attributes(event_mask=Xlib.X.NoEventMask)
                        self._display.flush()
                        break

            def start(self):
                self._keep.set()
                if not self._threadStarted and self._checkThread is None:
                    self._checkThread = threading.Thread(target=self._checkDisplayEvents)
                    self._checkThread.daemon = True
                    self._threadStarted = True
                    self._checkThread.start()

            def pause(self):
                self._keep.clear()

            def stop(self):
                if self._threadStarted:
                    self._threadStarted = False
                    self._stopRequested = True
                    self._keep.set()
                    self._checkThread.join()
                    self._checkThread = None

        def createSimpleWindow(self, parent, x, y, width, height, override, inputOnly: bool = True):

            if inputOnly:
                mask = Xlib.X.ButtonPressMask | Xlib.X.ButtonReleaseMask | Xlib.X.KeyPressMask | Xlib.X.KeyReleaseMask
            else:
                mask = Xlib.X.NoEventMask
            window: XWindow = parent.create_window(x=x, y=y, width=width, height=height,
                                                   border_width=0, depth=Xlib.X.CopyFromParent,
                                                   window_class=Xlib.X.InputOutput,
                                                   # window_class=Xlib.X.InputOnly,  # -> This fails!
                                                   visual=Xlib.X.CopyFromParent,
                                                   background_pixel=Xlib.X.CopyFromParent,
                                                   event_mask=mask,
                                                   colormap=Xlib.X.CopyFromParent,
                                                   override_redirect=override,
                                                  )
            window.map()
            self.display.flush()
            return window

def main():
    print("ALL DISPLAYS")
    # print(getAllDisplaysInfo())
    root = RootWindow()
    print("DESKTOP LAYOUT")
    print(root.getDesktopLayout())
    print("NUMBER OF DESKTOPS")
    print(root.getNumberOfDesktops())
    print("CLIENT LIST")
    print(root.getClientList())
    print("CLIENT LIST STACKING")
    print(root.getClientListStacking())
    print("SUPPORTED HINTS")
    print(root.getSupported(True))
    print("DESKTOP GEOMETRY")
    print(root.getDesktopGeometry())
    print("DESKTOP NAMES")
    print(root.getDesktopNames())
    print("DESKTOP VIEWPORT")
    print(root.getDesktopViewport())
    print("SHOWING DESKTOP")
    print(root.getShowingDesktop())
    print("SUPPORTING WM CHECK")
    print(root.getSupportingWMCheck())
    w = root.getActiveWindow()
    print("REQ FRAME EXTENTS")
    print(root.requestFrameExtents(w))
    if w:
        win = Window(w)
        print("NAME", win.getName())
        print("TYPE", win.getWmWindowType())
        print("TYPE STR", win.getWmWindowType(text=True))
        print("STATE", win.getWmState())
        print("STATE STR", win.getWmState(text=True))
        print("ALLOWED ACTIONS", win.getAllowedActions(True))
        print("PID", win.getPid())
        print("FRAME EXT", win.getFrameExtents())
        # These are returning None... is it OK???
        print("STRUT", win.getStrut())
        print("STRUT PARTIAL", win.getStrutPartial())
        print("ICON GEOM", win.getIconGeometry())
        print("HANDLED ICONS", win.getHandledIcons())
        print("USER TIME", win.getUserTime())

        print("MOVING/RESIZING")
        # root.setMoveResize(w, 0, 100, 100, 800, 600, False)  # -> final size is (795, 587)... Why? How to determine?
        root.setMoveResize(w, 0, 100, 100, 795, 587, False)
        dsp = Xlib.display.Display()
        Xwin = dsp.create_resource_object('window', w)
        print(Xwin.get_geometry())

        def callback(event):
            print("EVENT", event)

        eventLoop = win.extensions.checkEvents([Xlib.X.ConfigureNotify],
                                               Xlib.X.StructureNotifyMask | Xlib.X.SubstructureNotifyMask,
                                               callback)
        eventLoop.start()

        print("BELOW ON")
        win.changeWmState(Props.Window.State.Action.ADD, Props.Window.State.BELOW)
        time.sleep(4)
        print("BELOW OFF")
        win.changeWmState(Props.Window.State.Action.REMOVE, Props.Window.State.BELOW)
        time.sleep(4)
        print("DESKTOP")
        win.setWmWindowType(Props.Window.WindowType.DESKTOP)
        time.sleep(4)
        print("NORMAL")
        win.setWmWindowType(Props.Window.WindowType.NORMAL)
        print("MAX HORZ ON")
        win.setMaximized(True, False)
        time.sleep(4)
        print("MAX HORZ OFF")
        win.setMaximized(False, False)
        time.sleep(4)
        print("MAX")
        win.setMaximized(True, True)
        time.sleep(4)
        print("MAX HORZ OFF")
        win.setMaximized(False, True)
        time.sleep(4)
        print("MAX OFF")
        win.setMaximized(False, False)
        time.sleep(4)
        print("ICONIFY")
        win.setMinimized()
        time.sleep(4)
        print("RESTORE")
        win.setActive()
        time.sleep(4)
        print("END EVENT LOOP")
        eventLoop.stop()

        print("WM HINTS")
        print(win.extensions.getWmHints())
        print("WM NORMAL HINTS")
        print(win.extensions.getWmNormalHints())
        print("WM PROTOCOLS")
        print(win.extensions.getWmProtocols(True))
        print("REQUEST CLOSE")
        root.setClosed(win.id)  # equivalent to win.setClosed(), but accepts any window id


if __name__ == "__main__":
    main()
