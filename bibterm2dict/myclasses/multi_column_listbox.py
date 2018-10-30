# -*- coding: utf-8 -*-

'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting in Python3.
'''
from tkinter.ttk import Treeview, Scrollbar, Label, Frame
from tkinter.font import Font
from tkinter import messagebox

class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, parent=None, aheader=['a', 'b',], items=[['','',],], \
                 _column=0, _row=0, _columnspan=12, _rowspan=20):
        self.parent = parent
        self.tree = None
        self._setup_widgets(aheader, items, _column, _row, _columnspan, _rowspan)
        self._build_tree(aheader, items)

    def _setup_widgets(self, aheader, items, _column, _row, _columnspan, _rowspan):
        """\click on header to sort by that column
to change width of column drag boundary
        """
#        self.tree = Treeview(self.f3, selectmode="extended", height=8)
#        self.tree.grid(column=0, row=0, \
#                       columnspan=12, rowspan=20, sticky='news', padx=5)
#        ysb = Scrollbar(self.f3, orient='vertical', command=self.tree.yview)
#        xsb = Scrollbar(self.f3, orient='horizontal', command=self.tree.xview)
#        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
#        ysb.grid(row=0, column=11, rowspan=20, padx=5, sticky='nse')
#        xsb.grid(row=20, column=0, columnspan=12, padx=5, sticky='ews')

#        msg = Label(wraplength="4i", justify="left", anchor="n")
#        msg.grid(column=0, row=0, padx=5, pady=5, sticky='news' text=s)
        container = Frame(self.parent, width=1000, height=400)
#        container.grid(column=_column, row=_row, columnspan=_columnspan, \
#                       rowspan=_rowspan, padx=5, pady=5, sticky='news' )

        # create a treeview with dual scrollbars
        self.tree = Treeview(container, selectmode="extended", height=8, show="headings")
#        self.tree.grid(column=_column, row=_row, \
#                       columnspan=_columnspan, rowspan=_rowspan, \
#                       padx=5,pady=5,sticky='news')
        vsb = Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        hsb = Scrollbar(self.parent, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
#        vsb.grid(column=(_column + _columnspan-1), row=0, rowspan=_rowspan, sticky='nse') #, in_=container)
#        hsb.grid(column=0, row=(_row + _rowspan), columnspan=_columnspan, sticky='ews') #, in_=container)
#        container.grid_columnconfigure(0, weight=1)
#        container.grid_rowconfigure(0, weight=1)

        container.pack_propagate(0)
        hsb.pack(side="bottom", fill="x")
        vsb.pack(side="right", fill="x")
        self.tree.pack(side="top", fill="both", expand=True)


    def _build_tree(self, aheader, items):
        self.tree['columns'] = aheader
        self.tree["displaycolumns"] = aheader
        self.tree.column("#0", minwidth=0, width=0, stretch=False)
#        self.tree.heading('#0', text=LOCALIZED_TEXT[lang]['#0'])
        widths = [Font().measure(col) for col in aheader]
        for item in items:
            for i in range(0,len(item)):
                if widths[i] < Font().measure(item[i]):
                    widths[i] = Font().measure(item[i])
        for i in range(0,len(aheader)):
            
            self.tree.column(aheader[i], minwidth=100, width=widths[i], \
                             anchor='center', stretch=True) 
#            print(self.tree['columns'], col)
#            self.tree.column(col, minwidth=100, width=400, stretch=False)
            self.tree.heading(aheader[i], text=aheader[i])

##        for col in aheader:
#        for col in range( 0, len(aheader)):
##            self.tree.heading(col, text=col.title(),
##                command=lambda c=col: sortby(self.tree, c, 0))
#            print('#{}'.format(col), aheader[col])
#            self.tree.heading('#{}'.format(col), text=aheader[col])
#            # adjust the column's width to the header string
##            self.tree.column(col, width= Font().measure(aheader[col]))

        for item in items:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
#            for ix, val in enumerate(item):
#                col_w = Font().measure(val)
#                if self.tree.column(aheader[ix], width=None) < col_w:
#                    self.tree.column(aheader[ix], width=col_w)

    def delete_selected_row(self):
        """deletes selected row, if no row selected gives warning message"""
        pass

    def add_row(self, _values):
        """adds a row at the bottom of table, but if the only row has zero 
                                       length contents it will be replaced"""
        return(self.tree.insert('', index='end', open=True))
        pass
    
#def getKey(item):
#    return item[0]
#
#def sortby(tree, col, descending):
#    """sort tree contents when a column header is clicked on"""
#    # grab values to sort
#    data = [(tree.set(child, col), child) \
#        for child in tree.get_children('')]
#    # if the data to be sorted is numeric change to float
#    #data =  change_numeric(data)
#    # now sort the data in place
#    data.sort(key=getKey, reverse=descending)
#    #for ix, item in enumerate(data):
#    for ix in range(0, len(data)):
#        tree.move(data[ix][1], '', ix)
#    # switch the heading so it will sort in the opposite direction
#    tree.heading(col, command=lambda col=col: sortby(tree, col, \
#        int(not descending)))


