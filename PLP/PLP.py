from tkinter import Tk, Label, Frame

import rx
from rx import operators as ops
from rx.subject import Subject
from rx.scheduler.mainloop import TkinterScheduler


def main():
    root = Tk()
    root.title("Python Tkinter")
    scheduler = TkinterScheduler(root)

    mousemove = Subject()

    frame = Frame(root, width=600, height=600)

    frame.bind("<Motion>", mousemove.on_next)

    text = 'ABCD  EFGH  IJKL  MNOP'

    def on_next(info):
        label, ev, i = info
        label.place(x=ev.x + i*12 + 15, y=ev.y)

    def handle_label(label, i):
        label.config(dict(borderwidth=0, padx=0, pady=0))

        mapper = ops.map(lambda ev: (label, ev, i)) # transform the items emitted by an Observable by applying a function to each item
        delayer = ops.delay(i*0.1) #shift the emissions from an Observable forward in time by a particular amount

        return mousemove.pipe(
            delayer,
            mapper
        )

    labeler = ops.flat_map_indexed(handle_label) # transform the items emitted by an Observable into Observables, then flatten the emissions from those into a single Observable
    mapper = ops.map(lambda c: Label(frame, text=c)) # transform the items emitted by an Observable by applying a function to each item

    rx.from_(text).pipe(
        mapper,
        labeler
    ).subscribe(on_next, on_error=print, scheduler=scheduler)

    frame.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
