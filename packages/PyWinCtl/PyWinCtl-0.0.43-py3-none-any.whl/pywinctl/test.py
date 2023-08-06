#!/usr/bin/env python
# encoding: utf-8

import sys
assert sys.platform == "darwin"
import time

from AppKit import (
    NSApp, NSObject, NSApplication, NSMakeRect, NSWindow, NSWindowStyleMaskTitled, NSWindowStyleMaskClosable,
    NSWindowStyleMaskMiniaturizable, NSWindowStyleMaskResizable, NSBackingStoreBuffered, NSMakeRect)

import pywinctl


def _moveTo(handle, newLeft: int, newTop: int, width, height):
    handle.setFrame_display_animate_(
        NSMakeRect(newLeft, pywinctl.getScreenSize().height - newTop - height, width, height),
        True, True)


def _moveToUnflipped(handle, newLeft: int, newTop: int, width, height):
    handle.setFrame_display_animate_(NSMakeRect(newLeft, newTop, width, height), True, True)


class Delegate(NSObject):

    npw = None
    demoMode = False

    def getDemoMode(self):
        return self.demoMode

    def setDemoMode(self):
        self.demoMode = True

    def unsetDemoMode(self):
        self.demoMode = False

    def applicationDidFinishLaunching_(self, aNotification: None):
        NSApp().activateIgnoringOtherApps_(True)
        for win in NSApp().orderedWindows():
            print(win.title(), win.frame(), type(win.frame().origin))

        if self.demoMode:

            if not self.npw:
                self.npw = pywinctl.getActiveWindow(NSApp())

                if self.npw:
                    print("ACTIVE WINDOW:", self.npw.title)
                else:
                    print("NO ACTIVE WINDOW FOUND")
                    return

            print("BEFORE MOVE", self.npw.box, "Window should be at the left and near the bottom")
            time.sleep(1)
            _moveToUnflipped(self.npw.getHandle(), 1800, 50, self.npw.width, self.npw.height)
            time.sleep(1)
            print("AFTER MOVE", self.npw.box, "Window should be at the right and near the bottom")
            time.sleep(1)
            _moveTo(self.npw.getHandle(), 50, 50, self.npw.width, self.npw.height)
            time.sleep(1)
            print("AFTER FLIPPED MOVE", self.npw.box, "Window should be at left and near the top")

    def windowWillClose_(self, aNotification: None):
        '''Called automatically when the window is closed'''
        print("Window has been closed")
        NSApp().terminate_(self)

    def windowDidBecomeKey_(self, aNotification: None):
        print("Now I'm ACTIVE")


def demo():
    a = NSApplication.sharedApplication()
    delegate = Delegate.alloc().init()
    delegate.setDemoMode()
    a.setDelegate_(delegate)

    frame = NSMakeRect(50, 50, 250, 100)
    mask = NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable
    w = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(frame, mask, NSBackingStoreBuffered, False)

    w.setDelegate_(delegate)
    w.setTitle_(u'Hello, World!')
    w.orderFrontRegardless()

    w._display()
    a.run()


if __name__ == '__main__':
    demo()
