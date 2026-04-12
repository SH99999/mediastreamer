#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, signal, sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', required=True)
    parser.add_argument('--pidfile', required=True)
    parser.add_argument('--readyfile', required=True)
    args = parser.parse_args()

    try:
        import tkinter as tk
    except Exception as exc:
        print(f'tkinter unavailable: {exc}', file=sys.stderr)
        return 1

    pidfile = Path(args.pidfile)
    readyfile = Path(args.readyfile)
    image_path = Path(args.image)

    try:
        pidfile.unlink(missing_ok=True)
    except Exception:
        pass
    try:
        readyfile.unlink(missing_ok=True)
    except Exception:
        pass

    root = tk.Tk()
    root.configure(bg='black')
    root.overrideredirect(True)
    try:
        root.attributes('-fullscreen', True)
    except Exception:
        pass
    try:
        root.attributes('-topmost', True)
    except Exception:
        pass
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f'{sw}x{sh}+0+0')

    container = tk.Frame(root, bg='black')
    container.place(relx=0, rely=0, relwidth=1, relheight=1)

    photo = None
    try:
        if image_path.exists():
            photo = tk.PhotoImage(file=str(image_path))
    except Exception as exc:
        print(f'image load failed: {exc}', file=sys.stderr)
        photo = None

    if photo is not None:
        label = tk.Label(container, image=photo, bg='black', bd=0, highlightthickness=0)
        label.image = photo
        label.place(relx=0.5, rely=0.5, anchor='center')

    pidfile.write_text(str(os.getpid()), encoding='utf-8')

    def cleanup_files():
        try:
            pidfile.unlink(missing_ok=True)
        except Exception:
            pass
        try:
            readyfile.unlink(missing_ok=True)
        except Exception:
            pass

    def shutdown(*_args):
        cleanup_files()
        try:
            root.destroy()
        except Exception:
            pass

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    def heartbeat():
        try:
            root.lift()
            root.attributes('-topmost', True)
        except Exception:
            pass
        root.after(150, heartbeat)

    def mark_ready():
        try:
            readyfile.write_text('ready
', encoding='utf-8')
        except Exception as exc:
            print(f'readyfile write failed: {exc}', file=sys.stderr)

    # Force an initial map/paint before advertising readiness.
    root.update_idletasks()
    try:
        root.update()
    except Exception:
        pass
    root.after(120, mark_ready)
    root.after(50, heartbeat)

    try:
        root.mainloop()
    finally:
        cleanup_files()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
