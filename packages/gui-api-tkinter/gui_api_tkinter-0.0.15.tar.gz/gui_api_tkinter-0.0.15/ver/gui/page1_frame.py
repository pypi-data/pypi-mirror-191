import tkinter as tk

from ver.gui import mvc
from ver.gui.frame_base import FrameBase


# --------------------
## holds the Page1 Frame
class Page1Frame(FrameBase):

    # --------------------
    ## constructor
    def __init__(self):
        ## holds the name of this page
        self._page = 'page1'
        ## holds the string variable used for the label1 widget
        self._label1_text = None
        ## holds the string variable used for the label2 widget
        self._label2_text = None
        ## holds the string variable used for the label3 widget
        self._label3_text = None
        ## holds the string variable used for the Radiobutton widget
        self._rb_var = None
        ## holds the string variable used for the Listbox widget
        self._lbox_var = None

    # --------------------
    ## Creates and returns a frame containing status information about the operation of the program.
    #
    # @param root  reference to the parent this frame resides on
    # @return reference to the Frame object
    def init(self, root) -> tk.Widget:
        page1_frame = tk.Frame(master=root,
                               borderwidth=self.FRAME_BORDERWIDTH,
                               relief=tk.RIDGE)
        mvc.guiapi.set_name(page1_frame, 'page1_frame')

        title_label = tk.Label(master=page1_frame,
                               text='Page : ',
                               font='Helvetica 10 bold')
        mvc.guiapi.set_name(title_label, 'title')
        title_label.grid(column=0, columnspan=1, row=0, rowspan=1, sticky=tk.W)

        str_var = tk.StringVar()
        str_var.set(self._page)
        label = tk.Label(master=page1_frame, textvariable=str_var)
        mvc.guiapi.set_name(label, 'page')
        label.grid(column=1, columnspan=1, row=0, rowspan=1, sticky=tk.NSEW)

        button_frame = tk.Frame(master=page1_frame)
        mvc.guiapi.set_name(button_frame, 'button_frame')
        button_padding_x = 3
        button_padding_y = 2
        button_frame.grid(column=0, columnspan=2,
                          row=1, rowspan=1, sticky=tk.NSEW,
                          )

        # === Button widget
        row = 0
        col = 0
        button = tk.Button(button_frame,
                           font='Helvetica 10',
                           text='press me!',
                           command=self._on_button1_pressed,
                           )
        mvc.guiapi.set_name(button, 'button1')
        button.grid(column=col, columnspan=1,
                    row=row, rowspan=1, sticky=tk.NSEW,
                    padx=button_padding_x, pady=button_padding_y)

        # === Label widget
        col += 1
        self._label1_text = tk.StringVar()
        label = tk.Label(master=button_frame,
                         font='Helvetica 10',
                         textvariable=self._label1_text,
                         relief=tk.SUNKEN
                         )
        mvc.guiapi.set_name(label, 'label1')
        label.grid(column=col, columnspan=1,
                   row=row, rowspan=1, sticky=tk.EW)

        self._set_labels()

        # === Entry widget
        row += 1
        col = 1
        entry_var = tk.StringVar()
        entry = tk.Entry(master=button_frame,
                         font='Helvetica 10',
                         textvariable=entry_var,
                         relief=tk.SUNKEN)
        mvc.guiapi.set_name(entry, 'entry1')
        entry.grid(column=col, columnspan=1,
                   row=row, rowspan=1, sticky=tk.EW)

        # === Radiobutton widget
        row += 1
        col = 0
        self._rb_var = tk.StringVar()
        rb1 = tk.Radiobutton(master=button_frame,
                             text='option1', variable=self._rb_var,
                             value=1, command=self._on_rb_selection)
        mvc.guiapi.set_name(rb1, 'rb1')
        rb1.grid(column=col, columnspan=1,
                 row=row, rowspan=1, sticky=tk.W)

        col += 1
        self._label2_text = tk.StringVar()
        label = tk.Label(master=button_frame,
                         font='Helvetica 10',
                         textvariable=self._label2_text,
                         relief=tk.SUNKEN
                         )
        mvc.guiapi.set_name(label, 'label2')
        label.grid(column=col, columnspan=1,
                   row=row, rowspan=1, sticky=tk.EW)
        self._label2_text.set('rb: notset')

        row += 1
        col = 0
        rb2 = tk.Radiobutton(master=button_frame,
                             text='option2', variable=self._rb_var,
                             value=2, command=self._on_rb_selection)
        mvc.guiapi.set_name(rb2, 'rb2')
        rb2.grid(column=col, columnspan=1,
                 row=row, rowspan=1, sticky=tk.W)

        row += 1
        col = 0
        rb3 = tk.Radiobutton(master=button_frame,
                             text='option3', variable=self._rb_var,
                             value=3, command=self._on_rb_selection)
        mvc.guiapi.set_name(rb3, 'rb3')
        rb3.grid(column=col, columnspan=1,
                 row=row, rowspan=1, sticky=tk.W)

        # == Listbox
        row += 1
        col = 0
        self._lbox_var = tk.StringVar()
        lbox = tk.Listbox(master=button_frame,
                          selectmode=tk.SINGLE,
                          height=0,  # no blank rows
                          listvariable=self._lbox_var)
        lbox.bind("<<ListboxSelect>>", self._on_lbox_selection)
        mvc.guiapi.set_name(lbox, 'listbox1')
        for item in ['lbox_item1', 'lbox_item2', 'lbox_item3', 'lbox_item4']:
            lbox.insert('end', item)
        lbox.grid(column=col, columnspan=1,
                  row=row, rowspan=1, sticky=tk.W)

        col += 1
        self._label3_text = tk.StringVar()
        label = tk.Label(master=button_frame,
                         font='Helvetica 10',
                         textvariable=self._label3_text,
                         relief=tk.SUNKEN
                         )
        mvc.guiapi.set_name(label, 'label3')
        label.grid(column=col, columnspan=1,
                   row=row, rowspan=1, sticky=tk.EW)
        self._label3_text.set('lbox: notset')

        return page1_frame

    # --------------------
    ## reset the content of this frame
    #
    # @return None
    def clear(self):
        mvc.model.clear()
        self._set_labels()

    # --------------------
    ## callback used when button1 is pressed
    #
    # @return None
    def _on_button1_pressed(self):
        # toggle state
        mvc.model.toggle_state1()
        self._set_labels()

    # --------------------
    def _on_rb_selection(self):
        val = self._rb_var.get()
        self._label2_text.set(f'rb: {val}')

    # --------------------
    def _on_lbox_selection(self, event):
        lbox = event.widget
        sel = lbox.curselection()
        mvc.logger.info(f'lbox_selection: {sel}')
        if not sel:
            mvc.logger.info(f'lbox_selection is empty: {sel}')
            return

        val = ','.join([lbox.get(x) for x in sel])
        # for i in sel:
        #     val += lbox.get(sel[i])
        self._label3_text.set(f'lbox: {val}')

    # --------------------
    ## set the lable1 and lable2 based on the current model states
    #
    # @return None
    def _set_labels(self):
        self._label1_text.set(f'state: {mvc.model.state1}')
