# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 04:37:05 2017

@author: marks
"""
#import sys
import os
import platform
import webbrowser
import threading

import codecs
import shutil
import glob
import hashlib
import pickle
from urllib.parse import urlparse
import json
import re
from tkinter import Tk, filedialog, messagebox, StringVar, \
                    IntVar, NO, YES, Text, FALSE, Menu
from tkinter.ttk import Button, Checkbutton, Entry, Frame, Label, LabelFrame, \
                        Radiobutton, Scrollbar, Combobox, Notebook, \
                        Progressbar, Treeview, Style
from tkinter.font import Font
import ast
import psutil
from lxml import etree
from unidecode import unidecode
from operator import itemgetter
#from .myconst.regexs import FIND_LEADING_DIGITS, FIND_LEADING_ALPHANUM, \
#                            FIND_TRAILING_DIGITS, TRIM_LEADING_DIGITS, \
#                            TRIM_TRAILING_DIGITS
from .myconst.localizedText import INTERFACE_LANGS, LOCALIZED_TEXT, CLDR
from .myconst.therest import THIS_VERSION
from .tooltip import CreateToolTip
from .multi_column_listbox import MultiColumnListbox
#from .threads import MyThread

def get_script_directory():
    """return path to current script"""
    return os.path.dirname(__file__)

SCRIPT_DIR = get_script_directory()

#global index valuse for self.tree
#approved = ''
#conflicts = ''
#suggestions = ''
#unknown = ''
#cldr = ''
#current = ''

class GuiCore(Tk):
    """Handle the graphical interface for BibTermwizard and most of the logic"""
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self._initialize()

    def _initialize(self):
        """initialize the GuiCore"""
        self._initialize_variables()
        self._initialize_project_variables()

        lang = 'en-US'
        self._initialize_main_window(lang)

        if platform.system() not in  ['Windows', 'Linux']:
            # so on f0, the Project tab…
            messagebox.showwarning(\
                              'Warning', "Help I've been kidnaped by {}!!!".\
                                                   format(platform.system()))
            self.BibTerm = os.path.expanduser('~') + '/BibTerm'
            self.MapCreator = os.path.join(os.environ['USERPROFILE'], \
                                           "My Documents", "Map Creator")
        if platform.system() == 'Linux':
            self.BibTerm = os.path.expanduser('~/BibTerm')
            self.MapCreator = os.path.expanduser('~/Map Creator')
        elif platform.system() == 'Windows':
#            self.BibTerm = '/'.join(os.path.expanduser('~').split("\\")[0:3]) \
#                                  + '/BibTerm'
#            self.BibTerm = os.path.expanduser('~//BibTerm')
            self.BibTerm = os.path.normpath(\
                    os.environ['HomeDrive'] + os.environ['HomePath'] + '\\BibTerm')
            if not os.path.isdir(self.BibTerm):
                os.makedirs(self.BibTerm, 0o777) #make the dir
#            messagebox.showinfo('self.BibTerm', \
#                                    'self.BibTerm >{}<'.format(self.BibTerm))
            self.MapCreator =os.path.normpath(os.environ['HomeDrive'] + \
                                              os.environ['HomePath'] + \
                                              '/Documents/Map Creator')
#            messagebox.showinfo('self.MapCreator', \
#                                'self.MapCreator >{}<'.format(self.MapCreator))
#        self.MapCreator = os.path.normpath(\
#                os.environ['HomeDrive'] + os.environ['HomePath'] + '\\Map Creator')
#        if not os.path.isdir(self.MapCreator):
#            messagebox.showinfo('self.MapCreator', \
#                                "can't find >{}<".format(self.MapCreator))
#            os.makedirs(self.MapCreator, 0o777) #make the dir
#        messagebox.showinfo('self.BibTerm', \
#                            'self.BibTerm >{}<'.format(self.BibTerm))


        self._initialize_f0(lang) # Setup dictionaries
        self._initialize_f1(lang) # map transliteration
        self._initialize_f2(lang) # Terms

        bibterm_styles = Style()
        bibterm_styles.configure('lowlight.TButton', \
                                font=('Sans', 8, 'bold'),)
        bibterm_styles.configure('highlght.TButton', \
                                font=('Sans', 11, 'bold'), \
                                background='white', foreground='#007F00')
        bibterm_styles.configure('wleft.TRadiobutton', \
                                anchor='w', justify='left')

    def _initialize_project_variables(self):
        """The project variables that will be saved on clicking 'save project'.
        The sfn variable hold the settings for their associated tab (fn) of
        the notebook widget on the main window. The child 'tree'holds a copy
        of all the file locations and any modifications to their metadata"""
        self.Source = ''
        self.Regional = ''
        self.Vernacular = ''
        self.Fallback = dict()
        self.New_Target = dict()
        self.Biblical_Terms = dict()
        self.Old_Target = dict()

#        self.list_projects = []
#        self.project_lines = []
#        self.indent = 0
#        self.Treed = False
        self.root = etree.Element('root')
#        #add child 'settings', all user configurable bits under here
        self.settings = etree.SubElement(self.root, "settings")
#        self.old_mode = dict()
#        self.spreferred = etree.SubElement(self.settings, "preferred")
#        self.smode = etree.SubElement(self.settings, "mode")
#        self.stemp = etree.SubElement(self.settings, "template")
        self.sf0 = etree.SubElement(self.settings, "f0")
        self.sf1 = etree.SubElement(self.settings, "f1")
        self.sf2 = etree.SubElement(self.settings, "f2")
        self.trout = etree.SubElement(self.root, "tree")
#        self.project_id = ''

    def _initialize_variables(self):
        """initialize variables for GuiCore"""

        self.font = Font()
        self.BibTerm = ''

        self.illegalChars = [chr(i) for i in range(1, 0x20)]
        self.illegalChars.extend([chr(0x7F), '"', '*', '/', ':', '<', '>', \
                                                              '?', '\\', '|'])

        #define all StringVar(), BooleanVar(), etc… needed to hold info
        self.current_project = StringVar()
        self.dict_in = StringVar()
        self.terms_in = StringVar()
        self.old_dict = StringVar()
        self.dict_in_changed = IntVar()
        self.terms_in_changed = IntVar()
        self.old_dict_changed = IntVar()
        self.add_cldr_fields = IntVar()
        self.accept_regional_digits = IntVar()
        self.selected_lang = StringVar()
        self.int_var = IntVar()
        self.preferred = StringVar()
        self.PrefChar = StringVar()

    def _initialize_main_window_menu(self, lang='en-US'):
        """initialize the menubar on the main window"""

        self.option_add('*tearOff', FALSE)
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        self.filemenu = Menu(self.menubar)
        self.menubar.add_cascade(label=LOCALIZED_TEXT[lang]['File'], \
                                 menu=self.filemenu)
        self.filemenu.add_command(label=\
                            LOCALIZED_TEXT[lang]['Load project settings'], \
                                          command=self._on_click_f0_next)
        self.filemenu.add_command(label=LOCALIZED_TEXT[lang]['Save'], \
                                  command=self._on_save_project)
        self.filemenu.add_command(label=\
                            LOCALIZED_TEXT[lang]['Delete project settings'], \
                                          command=self._on_del_project)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=LOCALIZED_TEXT[lang]['Exit'], \
                                  command=self.quit)

        self.helpmenu = Menu(self.menubar)
        self.menubar.add_cascade(label=LOCALIZED_TEXT[lang]['Help'], \
                                 menu=self.helpmenu)
        self.helpmenu.add_command(label=LOCALIZED_TEXT[lang]['Read Me'], \
                                  command=self._on_read_me)
        self.helpmenu.add_command(label=LOCALIZED_TEXT[lang]['About...'], \
                                  command=on_copyright)
#                                  command=self._on_copyright)




    def _initialize_main_window(self, lang='en-US'):
        """ initialize the main window"""

        self._initialize_main_window_menu(lang)
        self.f_1 = Frame(self)
        self.f_1.grid(column=0, row=0, sticky='news')
        self.f_1.grid_rowconfigure(0, weight=0)
        self.f_1.grid_columnconfigure(0, weight=0)

        #in top of window
        self.btnSaveProject = Button(self.f_1, \
                                     text=LOCALIZED_TEXT[lang]["Save"], \
                                                command=self._on_save_project)
        self.btnSaveProject.grid(column=0, row=0, padx=5, pady=5, sticky='e')
        self.btnSaveProject['state'] = 'disabled'
        self.btnSaveProject_ttp = CreateToolTip(self.btnSaveProject, \
                                        LOCALIZED_TEXT[lang]['Save_ttp'])
        self.lblProject = Label(self.f_1, text=\
                                    LOCALIZED_TEXT[lang]['Current Project>'], \
                                                  width=50)
        self.lblProject.grid(column=1, row=0, columnspan=2, padx=5, pady=5, \
                             sticky='ew')
        self.lblProject['justify'] = 'left'

        self.lblGuiLanguage = Label(self.f_1, \
                            text=LOCALIZED_TEXT[lang]['Interface language>'])
        self.lblGuiLanguage.grid(column=4, row=0, padx=5, pady=5, sticky='e')
        self.lblGuiLanguage['justify'] = 'right'
        # Create and fill the dropdown ComboBox.
        self.ddnGuiLanguage = Combobox(self.f_1, \
                                       textvariable=self.selected_lang)
        self.ddnGuiLanguage.grid(column=5, columnspan=1, row=0, \
                                 padx=5, pady=5, sticky='w')
        self.ddnGuiLanguage['text'] = 'Interface language:'
        self.ddnGuiLanguage['justify'] = 'left'
        self.ddnGuiLanguage.bind('<<ComboboxSelected>>', self._change_lang)
        self.ddnGuiLanguage['values'] = [INTERFACE_LANGS['langs'][k] \
                                for k in sorted(INTERFACE_LANGS['langs'])]
        self.ddnGuiLanguage.set(INTERFACE_LANGS['langs']['0'])

        #assumes tab based interface
        #main frame holds gui interface lange pull down, lists current project,
        #and save settings button
        self._initialize_main_window_notebook(lang)
        self.progbar = Progressbar(self, maximum=100, variable=self.int_var)
        self.progbar.grid(column=0, row=6, columnspan=8, padx=5, pady=5, \
                          sticky='news')
        self.status = Label(self, text=LOCALIZED_TEXT[lang]['empty string'], \
                            anchor='w', justify='left')
        self.status.grid(column=0, row=7, columnspan=8, padx=5, pady=5, \
                         sticky='news')

    def _initialize_main_window_notebook(self, lang='en-US'):
        """initializes notebook widget on main window"""
        #self.n = Notebook(self, width=1400)
        #notebook
        self.n = Notebook(self, width=1015)
        self.n.grid(column=0, columnspan=7, row=1, padx=5, pady=5, sticky='ew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.n.grid_rowconfigure(0, weight=1)
        self.n.grid_columnconfigure(0, weight=1)
        # chose project name -
        #  defaults to last or pull downlist of existing ones?
        #  enter new, can delete selected project, move to next
        self.f0 = Frame(self.n) #Setup
        self.f1 = Frame(self.n) #Transliteration
        self.f2 = Frame(self.n) #Terms
        
        self._initialize_f0(lang)
        self._initialize_f1(lang)
        self._initialize_f2(lang)

        self.n.add(self.f0, text=LOCALIZED_TEXT[lang]['Setup'])
        self.n.add(self.f1, text=LOCALIZED_TEXT[lang]['Transliteration'])
        self.n.add(self.f2, text=LOCALIZED_TEXT[lang]['Terms'])

        self.n.hide(1)
        self.n.hide(2)
        if self.list_projects:
            self.ddnCurProject.set(self.list_projects[0])
            self._load_project(os.path.normpath('{}/{}.prj'.\
                                            format(self.BibTerm, \
                                            self.list_projects[0])))
        self.dict_in_changed.set(0)
        self.terms_in_changed.set(0)
        self.current_project.trace('w', self._load_project)



    def _initialize_f0(self, lang='en-US'):
        """initialize Setup - Project Name tab"""
        #left column
        self.f0_ttp = Label(self.f0, text=LOCALIZED_TEXT[lang]['f0_ttp'], \
                            anchor='w', justify='left', wraplength=600)
        self.f0_ttp.grid(column=0, row=0, columnspan=3, padx=5, pady=5, \
                                                                   sticky='ew')

        self.lblCurProject = Label(self.f0, \
                               text=LOCALIZED_TEXT[lang]['Current Project>'], \
                                                   anchor='w', justify='right')
        self.lblCurProject.grid(column=0, row=1, columnspan=2, \
                                padx=5, pady=5, sticky='e')

        self.ddnCurProject = Combobox(self.f0, validate='focusout', \
                        validatecommand=(self._check_project, '%s', '%P'), \
                                      textvariable=self.current_project)
#        self.current_project.trace('w', self._load_project)
        self.ddnCurProject.grid(column=2, row=1, columnspan=2, \
                                padx=5, pady=5, sticky='news')
        self.ddnCurProject.bind('<<ComboboxSelected>>', self._change_lang)
        self.ddnCurProject['text'] = 'Current Project:'
        self.ddnCurProject['justify'] = 'left'

        self.btnDelProject = Button(self.f0, \
                               text=LOCALIZED_TEXT[lang]['Delete Project'], \
                                                  command=self._on_del_project)
        self.btnDelProject.grid(column=4, row=1, padx=5, pady=5, sticky='news')
        self.btnDelProject_ttp = CreateToolTip(self.btnDelProject, \
                                    LOCALIZED_TEXT[lang]['Delete Project_ttp'])

        self.btnNewProject = Button(self.f0, \
                               text=LOCALIZED_TEXT[lang]['New Project'], \
                                                  command=self._on_new_project)
        self.btnNewProject.grid(column=5, row=1, padx=5, pady=5, sticky='news')
        self.btnNewProject_ttp = CreateToolTip(self.btnNewProject, \
                                    LOCALIZED_TEXT[lang]['New Project_ttp'])

        #browse to the source/fallback dictionary exported from Map Creator
        self.lblDictIn = Label(self.f0, \
                    text=LOCALIZED_TEXT[lang]['Source/Fallback dictionary'], \
                                    anchor='w', justify='left')
        self.lblDictIn.grid(column=0, row=2, columnspan=2, padx=5, pady=5, \
                           sticky='ew')
        self.etrDictIn = Entry(self.f0, \
                                 textvariable=self.dict_in, width=70)
        self.etrDictIn.grid(column=2, row=2, \
                              columnspan=3, padx=5, pady=5, sticky='news')
        self.btnDictIn = Button(self.f0, \
                               text=LOCALIZED_TEXT[lang]['...'], \
                               command=self._browse_to_dict)
        self.btnDictIn.grid(column=5, row=2, padx=5, pady=5, sticky='news')
        self.btnDictIn_ttp = CreateToolTip(self.btnDictIn, \
                                    LOCALIZED_TEXT[lang]['DictIn_ttp'])

        #browse to the html file exported from Paratext Bilical Terms tool
        self.lblTermsIn = Label(self.f0, \
                    text=LOCALIZED_TEXT[lang]['Biblical terms list'], \
                                    anchor='w', justify='left')
        self.lblTermsIn.grid(column=0, row=3, columnspan=2, padx=5, pady=5, \
                           sticky='ew')
        self.etrTermsIn = Entry(self.f0, \
                                 textvariable=self.terms_in, width=70)
        self.etrTermsIn.grid(column=2, row=3, \
                              columnspan=3, padx=5, pady=5, sticky='news')
        self.btnTermsIn = Button(self.f0, \
                               text=LOCALIZED_TEXT[lang]['...'], \
                               command=self._browse_to_terms)
        self.btnTermsIn.grid(column=5, row=3, padx=5, pady=5, sticky='news')
        self.btnTermsIn_ttp = CreateToolTip(self.btnTermsIn, \
                                    LOCALIZED_TEXT[lang]['TermsIn_ttp'])

        #browse to the existing source/target dict file exported from Paratext
        #Bilical Terms tool, if any.
        self.lblOldDict = Label(self.f0, \
                    text=LOCALIZED_TEXT[lang]['Old Source/Target dictionary'], \
                                    anchor='w', justify='left')
        self.lblOldDict.grid(column=0, row=4, columnspan=2, padx=5, pady=5, \
                           sticky='ew')
        self.etrOldDict = Entry(self.f0, \
                                 textvariable=self.old_dict, width=70)
        self.etrOldDict.grid(column=2, row=4, \
                              columnspan=3, padx=5, pady=5, sticky='news')
        self.btnOldDict = Button(self.f0, \
                               text=LOCALIZED_TEXT[lang]['...'], \
                               command=self._browse_to_old_dict)
        self.btnOldDict.grid(column=5, row=4, padx=5, pady=5, sticky='news')
        self.btnOldDict_ttp = CreateToolTip(self.btnDelProject, \
                                    LOCALIZED_TEXT[lang]['OldDict_ttp'])

        self.chkAddCLDRfields = Checkbutton(self.f0, \
                            text=LOCALIZED_TEXT[lang]["AddCLDRfields"], \
                                        variable=self.add_cldr_fields)
        self.chkAddCLDRfields.grid(column=0, row=6, columnspan=3, \
                                       padx=5, pady=5, \
                                       sticky='w')
        self.chkAcceptRegionalDigits = Checkbutton(self.f0, \
                            text=LOCALIZED_TEXT[lang]["AcceptRegionalDigits"], \
                                        variable=self.accept_regional_digits)
        self.chkAcceptRegionalDigits.grid(column=0, row=5, columnspan=3, \
                                       padx=5, pady=5, \
                                       sticky='w')
        self.accept_regional_digits.set(1)

        self.btnF0Next = Button(self.f0, \
                               text=LOCALIZED_TEXT[lang]['Next'], \
                               command=self._on_click_f0_next)
        self.btnF0Next.grid(column=4, row=7, padx=5, pady=5, sticky='news')
        self.btnF0Next_ttp = CreateToolTip(self.btnF0Next, \
                                    LOCALIZED_TEXT[lang]['F0Next_ttp'])

        # list projects in BibTerms2Dict and load to ddnCurProject
#        self.BibTerm = os.path.normpath(os.path.expanduser('~') + '/BibTerm')
#        print(self.BibTerm)
        self.BibTerm = os.path.normpath(\
                os.environ['HomeDrive'] + os.environ['HomePath'] + '\\BibTerm')
#        messagebox.showwarning('self.BibTerm', ">{}<".format(self.BibTerm))

        self.list_projects = sorted([f[:-4] for f in os.listdir(self.BibTerm) \
                                     if f.endswith('.prj')])

        self.ddnCurProject['values'] = self.list_projects
#        if len(self.list_projects) > 0:
#        if self.list_projects:
#            self.ddnCurProject.set(self.list_projects[0])
#            self._load_project(os.path.normpath('{}/{}.prj'.\
#                                            format(self.BibTerm, \
#                                            self.list_projects[0])))

    def _check_project(self, was, willbe):
        """verify project is in list"""
        self.BibTerm = os.path.normpath(\
                os.environ['HomeDrive'] + os.environ['HomePath'] + '\\BibTerm')
#        messagebox.showwarning('self.BibTerm', ">{}<".format(self.BibTerm))

        if willbe  in self.list_projects:
            self.ddnCurProject.set(willbe)
            return True
        else:
            self.ddnCurProject.set(was)
            return False


    def _initialize_f1(self, lang='en-US'):
        """initialize the transliteration scheme tab"""
        self.lblPreferred = Label(self.f1, \
                                  text=LOCALIZED_TEXT[lang]['lblPreferred'], \
                                anchor='w', justify='left', wraplength=600)
        self.lblPreferred.grid(column=0, row=0, columnspan=3, padx=5, pady=5, \
                               sticky='ew')

        self.lblLoadTemplate = Label(self.f1, \
                                text=LOCALIZED_TEXT[lang]['lblLoadTemplate'], \
                                anchor='w', justify='left')
        self.lblLoadTemplate.grid(column=4, row=1, columnspan=3, padx=5, \
                                  pady=5, sticky='ew')

        self.ddnPrefChar = Combobox(self.f1, textvariable=self.PrefChar)
        self.ddnPrefChar.grid(column=4, row=2, padx=5, pady=5, sticky='ew')
        self.ddnPrefChar.bind("<<ComboboxSelected>>", self._on_loadPrefChar)
        self.ddnPrefChar['text'] = 'Current template:'
        self.ddnPrefChar['justify'] = 'left'

        self.list_PrefChar = list()
        self.list_PrefChar.extend([f[:-4] \
                                            for f in os.listdir(self.BibTerm) \
                                            if f.endswith('.csv')])

        #self.list_PrefChar.insert(0, 'Latin1')
        #self.list_PrefChar.insert(1, '')

        self.ddnPrefChar['values'] = self.list_PrefChar

        self.btnSavePref = Button(self.f1, \
                                  text=LOCALIZED_TEXT[lang]["SavePref"], \
                                  command=lambda: \
                            self._on_SavePref('', '', \
                                self.txtPrefChar.get(0.0, 9999.9999).strip()))
        self.btnSavePref.grid(column=4, row=3, padx=5, pady=5, sticky='news')

        self.txtPrefChar = Text(self.f1, height=10, width=60)
        self.txtPrefChar.grid(column=0, row=1, \
                              columnspan=3, rowspan=10, padx=5, pady=5, \
                              sticky='news')
        ysb = Scrollbar(self.f2, orient='vertical', \
                              command=self.txtPrefChar.yview)
        self.txtPrefChar.configure(yscroll=ysb.set, font=("sans", 12), \
                                                       undo=True, wrap='word')
        ysb.grid(row=1, column=3, rowspan=6, sticky='nws')

        self.btnF2Next = Button(self.f1, \
                                text=LOCALIZED_TEXT[lang]["Set template"], \
                                              command=self._on_click_f1_next, \
                                              style='highlight.TButton')
        self.btnF2Next.grid(column=3, row=20, columnspan=2, padx=5, pady=5, \
                                                                 sticky='news')

    def _on_loadPrefChar(self, dummy, _prefchar=None, _lst='', _filein=''):
        """load a set of preferred character pairs from LATIN1 constant
                                                 or a utf8 coded  .csv file"""

        lst = _lst if len(_lst) > 0 else self.ddnPrefChar.get()
        prefchar = _prefchar if _prefchar is not None else self.txtPrefChar
#        if lst == 'Latin1':
##            if len(self.txtPrefChar.get(0.0, 9999.9999).rstrip()) > 0:
#            if prefchar.get(0.0, 9999.9999).rstrip():
#                prefchar.insert(9999.9999, ', ' + LATIN1)
#            else:
#                prefchar.insert(9999.9999, LATIN1)
        if lst == '': #del
            prefchar.delete(0.0, 9999.9999)
        else: #load txt file
            if len(_filein) == 0:
                filein = os.path.normpath(self.BibTerm + '/'+ lst + '.csv')
            else:
                filein = _filein
            fin = codecs.open(filein, mode='r', encoding='utf-8')
            text = fin.read()
#            if len(self.txtPrefChar.get(0.0, 9999.9999).strip()) > 0:
            if prefchar.get(0.0, 9999.9999).strip():
                text = ', ' + text
            prefchar.insert(9999.9999, text)
            fin.close()

    def _on_SavePref(self, _lang='en-US', _fileout='', _text=""):
        """save your list of preferred character pairs to a utf-8 coded
        .csv file. If _fileout is supplied the filedialog
        will not be called. If _text is supplied self.txtPrefChar will not
        be accessed"""

        lang = self.ddnGuiLanguage.get() if len(_lang) == 0 else _lang

        fileout = filedialog.asksaveasfilename(\
                        filetypes=[('Preferred characters file', '.csv'), ], \
                                    initialdir=self.BibTerm, \
                                    initialfile='', \
                                    title=LOCALIZED_TEXT[lang]['SavePref'], \
                                    defaultextension='.csv') \
                  if len(_fileout) == 0 else _fileout
        if len(fileout) != 0:
            text = self.txtPrefChar.get(0.0, 9999.9999).strip() \
                        if len(_text) == 0 else _text
            text = ' '.join(text.split('\n'))
            text = ' '.join(text.split('\r'))
            text = ' '.join(text.split('\f'))
            if ',' in text:
                pairs = [p.strip() for p in text.split(',')]
            else:
                pairs = [text,]
            fout = codecs.open(fileout, mode='w', encoding='utf-8')
            fout.write(', '.join(pairs))
            fout.close()



    def _initialize_f2(self, lang='en-US'):
        """initialize the 'Suggestions' tab"""
#        self.tree = Treeview(self.f2, selectmode="extended", height=8)
        self.tree = Treeview(self.f2)

        self.tree["columns"] = ['Term', 'Rendering']
#        self.tree['show'] = 'headings'
#        self.tree['show'] = 'tree'
        self.tree.column("#0", width=100, stretch=NO)
        self.tree.heading("#0", text='Type')
        self.tree.column('Term', minwidth=100, \
                                    width=200, stretch=YES)
        self.tree.heading('Term', text=LOCALIZED_TEXT[lang]['Term'])
        self.tree.column('Rendering', minwidth=100, \
                                    width=200, stretch=YES)
        self.tree.heading('Rendering', text=LOCALIZED_TEXT[lang]['Rendering'])
#        self.tree.column('Tags', minwidth=100, \
#                                    width=100, stretch=YES)
#        self.tree.heading('Tags', text='Tags')

        ysb = Scrollbar(self.f2, orient='vertical', command=self.tree.yview)
        xsb = Scrollbar(self.f2, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.bind("<ButtonRelease-1>", self._on_release_click)#do I need this?
#        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.grid(column=0, row=0, columnspan=8, rowspan=20, padx=5, \
                                                       pady=5, sticky='news')
        ysb.grid(row=0, column=7, rowspan=20, padx=5, sticky='nse')
        xsb.grid(row=20, column=0, columnspan=8, padx=5, sticky='ews')
        
        self.tree.tag_configure('approved',   background='palegreen')
        self.tree.tag_configure('conflict',   background='bisque')
        self.tree.tag_configure('suggestions',   background='lightblue')
        self.tree.tag_configure('unknown',   background='whitesmoke')
        self.tree.tag_configure('cldr',   background='violet')

        self.lbfShow = LabelFrame(self.f2, \
                            text=LOCALIZED_TEXT[lang]['Expand/Collapse'], \
                            labelanchor='nw')
        self.lbfShow.grid(column=0, row=21, columnspan=8, padx=5, pady=5, \
                          sticky='news')
        self.btnAll = Button(self.lbfShow, \
                               text=LOCALIZED_TEXT[lang]['btnAll'], \
                               command=self._collapse_all)
        self.btnAll.grid(column=0, row=0, padx=5, pady=5, sticky='news')
        self.btnAll_ttp = CreateToolTip(self.btnAll, \
                                    LOCALIZED_TEXT[lang]['All_ttp'])
        self.btnApproved = Button(self.lbfShow, \
                               text=LOCALIZED_TEXT[lang]['btnApproved'], \
                               command=self._expand_approved)
        self.btnApproved.grid(column=1, row=0, padx=5, pady=5, sticky='news')
        self.btnApproved_ttp = CreateToolTip(self.btnAll, \
                                    LOCALIZED_TEXT[lang]['Approved_ttp'])
        self.btnConflicts = Button(self.lbfShow, \
                               text=LOCALIZED_TEXT[lang]['btnConflicts'], \
                               command=self._expand_conflicts)
        self.btnConflicts.grid(column=2, row=0, padx=5, pady=5, sticky='news')
        self.btnConflicts_ttp = CreateToolTip(self.btnConflicts, \
                                    LOCALIZED_TEXT[lang]['Conflicts_ttp'])
        self.btnSuggestions = Button(self.lbfShow, \
                               text=LOCALIZED_TEXT[lang]['btnSuggestions'], \
                               command=self._expand_suggestions)
        self.btnSuggestions.grid(column=3, row=0, padx=5, pady=5, \
                                 sticky='news')
        self.btnSuggestions_ttp = CreateToolTip(self.btnConflicts, \
                                    LOCALIZED_TEXT[lang]['Suggestions_ttp'])
        self.btnUnknown = Button(self.lbfShow, \
                               text=LOCALIZED_TEXT[lang]['btnUnknown'], \
                               command=self._expand_unknown)
        self.btnUnknown.grid(column=4, row=0, padx=5, pady=5, sticky='news')
        self.btnUnknown_ttp = CreateToolTip(self.btnConflicts, \
                                    LOCALIZED_TEXT[lang]['Unknown_ttp'])
        self.btnCLDR = Button(self.lbfShow, \
                               text=LOCALIZED_TEXT[lang]['btnCLDR'], \
                               command=self._expand_cldr)
        self.btnCLDR.grid(column=5, row=0, padx=5, pady=5, sticky='news')
        self.btnCLDR_ttp = CreateToolTip(self.btnConflicts, \
                                    LOCALIZED_TEXT[lang]['CLDR_ttp'])

        self.lbfTerm = LabelFrame(self.f2, \
                             text=LOCALIZED_TEXT[lang]['Term'], \
                             labelanchor='nw')
        self.lbfTerm.grid(column=0, row=22, columnspan=8, padx=5, pady=5, \
                          sticky='news')

        self.lblSource = Label(self.lbfTerm, text='', anchor='w', \
                               justify='left')
        self.lblSource.grid(column=0, row=0, columnspan=3, padx=5, pady=5, \
                           sticky='news')
        self.lblFallback = Label(self.lbfTerm, text='', anchor='w', \
                                 justify='left')
        self.lblFallback.grid(column=0, row=1, columnspan=3, padx=5, pady=5, \
                           sticky='news')
        self.etrPreferred = Entry(self.lbfTerm, \
                                 textvariable=self.preferred, width=70)
        self.etrPreferred.grid(column=0, row=2, \
                              columnspan=3, padx=5, pady=5, sticky='news')
        #need to approve current preffered rendering, load fallback, transliterate
        #assumes term expanded, click on term, shows current rendering, 
        #click on fallback/suggestion loads it to preffered slot as well as term
        #then 'approve' preferred, transliterate
        self.btnRegional = Button(self.lbfTerm, \
                               text=LOCALIZED_TEXT[lang]['Load Regional'], \
                               command=self._load_regional)
        self.btnRegional.grid(column=0, row=3, padx=5, pady=5, \
                                   sticky='news')
        self.btnRegional_ttp = CreateToolTip(self.btnRegional, \
                                    LOCALIZED_TEXT[lang]['Load Regional_ttp'])
        self.btnTransliterate = Button(self.lbfTerm, \
                text=LOCALIZED_TEXT[lang]['Load Transliterated Regional'], \
                               command=self._load_transliterated_regional)
        self.btnTransliterate.grid(column=1, row=3, padx=5, pady=5, \
                                   sticky='news')
        self.btnTransliterate_ttp = CreateToolTip(self.btnTransliterate, \
                                    LOCALIZED_TEXT[lang]['Transliterate_ttp'])
        self.btnLoadSug = Button(self.lbfTerm, \
                               text=LOCALIZED_TEXT[lang]['Load Suggestion'], \
                               command=self._load_suggestion)
        self.btnLoadSug.grid(column=2, row=3, padx=5, pady=5, \
                                   sticky='news')
        self.btnLoadSug_ttp = CreateToolTip(self.btnLoadSug, \
                                    LOCALIZED_TEXT[lang]['Load Suggestion_ttp'])
        self.btnAccept = Button(self.lbfTerm, \
                               text=LOCALIZED_TEXT[lang]['Accept'], \
                               command=self._accept_preferred)
        self.btnAccept.grid(column=3, row=3, padx=5, pady=5, sticky='news')
        self.btnAccept_ttp = CreateToolTip(self.btnAccept, \
                                    LOCALIZED_TEXT[lang]['Accept_ttp'])
        self.btnReject = Button(self.lbfTerm, \
                               text=LOCALIZED_TEXT[lang]['Reject'], \
                               command=self._reject_rendering)
        self.btnReject.grid(column=4, row=3, padx=5, pady=5, sticky='news')
        self.btnReject_ttp = CreateToolTip(self.btnReject, \
                                    LOCALIZED_TEXT[lang]['Reject_ttp'])
        
        self.btnOutput = Button(self.f2, text=LOCALIZED_TEXT[lang]["Output Dictionary"], \
                                              command=self._output_dict, \
                                              style='highlight.TButton')
        self.btnOutput.grid(column=0, row=25, columnspan=2, padx=5, pady=5, \
                                                                 sticky='news')
#        self.btnF3Next = Button(self.f3, text=LOCALIZED_TEXT[lang]["Next"], \
#                                              command=self._on_click_f3_next, \
#                                              style='highlight.TButton')
#        self.btnF3Next.grid(column=11, row=25, columnspan=2, padx=5, pady=5, \
#                                                                 sticky='news')

        pass
    def _on_release_click(self, event):
        """fires after the focus has changed. 
        Is his different to <<TreeviewSelect>>?"""
        curItem = self.tree.focus()
#        curTerm = curItem
        parent = self.tree.parent(curItem)
#        categories = {'approved':'Approved', 'conflicts':'Conflicts', \
#                      'suggestions':'Suggestions', 'unknown':'Unknown', \
#                      'cldr':'CLDR',}
        categories = ['approved', 'conflicts', 'suggestions', 'unknown', \
                      'cldr',]
#        if parent not in [approved, conflicts, suggestions, unknown, cldr]:
        if parent is '':
            #will expand/collapse
            pass
        else:
            if parent not in categories:
                curTerm = parent
#                category = categories[self.tree.parent(parent)]
                category = self.tree.parent(parent)
            else:
                curTerm = curItem
#                category = categories[parent]
                category = parent
#                messagebox.showwarning("index?", "category {}=>{}=>{}".\
#                                format(category, curTerm, curItem))
            if category == 'approved':
                #is approved thetefore term with a single rendering only
                self.lblSource['text'] = '{}=>{}'.\
                            format(self.Source, self.tree.set(curTerm, 'Term'))
                self.lblFallback['text'] = '{}=>'.format(self.Regional)
                self.preferred.set(self.tree.set(curTerm, 'Rendering'))
                pass
            elif category == 'conflicts':
                self.lblSource['text'] = '{}=>{}'.\
                            format(self.Source, self.tree.set(curTerm, 'Term'))
                self.lblFallback['text'] = '{}=>'.format(self.Regional)
                self.preferred.set(self.tree.set(curTerm, 'Rendering'))
                if curTerm != curItem:
                    if self.tree.item(curItem)['text'] in ['fallback', ]:
                        self.lblFallback['text'] = '{}=>'.\
                            format(self.Regional, \
                                   self.tree.set(curItem, 'Rendering'))
                    elif self.tree.item(curItem)['text'] in ['rendering', ]:
                        self.preferred.set(self.tree.set(curTerm, 'Rendering'))
                pass
            elif category == 'suggestions':
                self.lblSource['text'] = '{}=>{}'.\
                            format(self.Source, self.tree.set(curTerm, 'Term'))
                self.lblFallback['text'] = '{}=>'.format(self.Regional)
                self.preferred.set(self.tree.set(curTerm, 'Rendering'))
                if curTerm != curItem:

                    if self.tree.item(curItem)['text'] in ['rendering', ]:
                        self.preferred.set(self.tree.set(curItem, 'Rendering'))
                    elif self.tree.item(curItem)['text'] in ['fallback', ]:
                        self.lblFallback['text'] = '{}=>{}'.\
                            format(self.Regional, \
                                   self.tree.set(curItem, 'Rendering'))
                pass
            elif category == 'unknown':
                self.lblSource['text'] = '{}=>{}'.\
                            format(self.Source, self.tree.set(curTerm, 'Term'))
                self.lblFallback['text'] = '{}=>'.format(self.Regional)
                self.preferred.set(self.tree.set(curTerm, 'Rendering'))
                if curTerm != curItem:
                    if self.tree.item(curItem)['text'] in ['fallback', ]:
                        self.lblFallback['text'] = '{}=>{}'.\
                            format(self.Regional, \
                                   self.tree.set(curItem, 'Rendering'))
                    else:
                        self.preferred.set(self.tree.set(curTerm, 'Rendering'))
            elif category == 'cldr':
                messagebox.showwarning("Selected cldr row", "Term {}=>{}".\
                                format(self.tree.set(curTerm, 'Term'), \
                                       self.tree.set(curTerm, 'Rendering')))
                if curTerm != curItem:
                    messagebox.showwarning("Selected cldr row", "CLDR {}=>{}".\
                                format(self.tree.set(curTerm, 'Term'), \
                                       self.tree.set(curItem, 'Rendering')))
                pass
            else:
                #error condition
                messagebox.showerror('_on_release_click', \
                                     'unknown category >{}<'.format(category))
                return
    
#    def _on_select(self, event):
#        pass
    
    def _count_children(self, item):
        """count children of item"""
        return len(self.tree.get_children(item))
    
    def _collapse_all(self):
        """Show all terms, defaulting to collapsed."""
#        global approved, conflicts, suggestions, unknown, cldr
        self.tree.item('approved', open=False, \
                       values=[self._count_children('approved'), ''])
        for child in self.tree.get_children('approved'):
            self.tree.item(child, tags='approved')

        self.tree.item('conflicts', open=False, \
                       values=[self._count_children('conflicts'), ''])
        for child in self.tree.get_children('conflicts'):
            self.tree.item(child, tags='conflicts')
            self.tree.item(child, open=False)
            for granchild in self.tree.get_children(child):
                self.tree.item(granchild, tags='conflicts',)
            
        self.tree.item('suggestions', open=False, \
                       values=[self._count_children('suggestions'), ''])
        for child in self.tree.get_children('suggestions'):
            self.tree.item(child, tags='suggestions')
            self.tree.item(child, open=False)
            for granchild in self.tree.get_children(child):
                self.tree.item(granchild, tags='suggestions')

        self.tree.item('unknown', open=False, \
                       values=[self._count_children('unknown'), ''])
        for child in self.tree.get_children('unknown'):
            self.tree.item(child, tags='unknown')
            self.tree.item(child, open=False)
            for granchild in self.tree.get_children(child):
                self.tree.item(granchild, tags='unknown')

        self.tree.item('cldr', open=False, \
                       values=[self._count_children('cldr'), ''])
        for child in self.tree.get_children('cldr'):
            self.tree.item(child, tags='cldr')
            self.tree.item(child, open=False)
            for granchild in self.tree.get_children(child):
                self.tree.item(granchild, tags='cldr')

        self.tree.tag_configure('approved',   background='palegreen')
        self.tree.tag_configure('conflict',   background='bisque')
        self.tree.tag_configure('suggestions',   background='lightblue')
        self.tree.tag_configure('unknown',   background='whitesmoke')
        self.tree.tag_configure('cldr',   background='violet')


    def _expand_approved(self):
        """Approved' showing all currently approved 'source'/'target' pairs. 
        Biblical terms which have a single rendering and no conflict with a 
        existing dictionary rendering will automaticly be shown as approved.
        Defaulting to collapsed."""
#        global approved
        self.tree.item('approved', open=True, \
                       values=[self._count_children('approved'), ''])

    def _expand_conflicts(self):
        """Conflicts' showing all terms which have confilcting renderings 
        between the  old source/target dictionary and the new set of 
        biblical terms from Paratext or the new source/fallback dictionary.
        Defaulting to expanded."""
#        global conflicts
        self.tree.item('conflicts', open=True, \
                       values=[self._count_children('conflicts'), ''])

    def _expand_suggestions(self):
        """'Suggestions' showing all unapproved terms, which have multiple 
        possibel renderings. (N.B. Additional renderings may be suggested 
        for terms without any renderings, based on the occurance of words 
        in the source term within other approved terms.)
        Defaulting to expanded."""
#        global suggestions
        self.tree.item('suggestions', open=False, \
                       values=[self._count_children('suggestions'), ''])

    def _expand_unknown(self):
        """'Unknown' shows all terms with no suggested rendering. These 
        will normally have the fallback (national/regional) languge term 
        shown. Defaulting to expanded."""
#        global unknown
        self.tree.item('unknown', open=False, \
                       values=[self._count_children('unknown'), ''])

    def _expand_cldr(self):
        """'CLDR'  button will show the terms required for submission to 
        prepare an application to include the language in the Common 
        Language Data Repository."""
#        global cldr
        self.tree.item('cldr', open=True, \
                       values=[self._count_children('cldr'), ''])

    def _load_regional(self):
        """load regional fallback into preferred entry box."""
#        global approved, conflicts, suggestions, unknown, cldr, current
        start = self.lblFallback['text'].find('=>') + 2
        if self.lblFallback['text'][start:]:
            self.preferred.set(self.lblFallback['text'][start:])
        pass

    def _transliterate_text(self, _text):
        """transliterates _text and returns result"""
        return _text.upper()

    def _load_transliterated_regional(self):
        """transliterates regional fallback and load it into preferred
        entry box."""
#        global approved, conflicts, suggestions, unknown, cldr, current
        start = self.lblFallback['text'].find('=>') + 2
        if self.lblFallback['text'][start:]:
            self.preferred.set(\
                    self._transliterate_text(self.lblFallback['text'][start:]))
        pass

    def _load_suggestion(self):
        """load suggestion from selected rendering into preferred entry box."""
        curItem = self.tree.focus()
        parent = self.tree.parent(curItem)

        categories = ['approved', 'conflicts', 'suggestions', 'unknown', \
                      'cldr',]
        if parent is '':
            #skip it
            pass
        else:
            if parent not in categories:
                curTerm = parent
                category = self.tree.parent(parent)
            else:
                curTerm = curItem
                category = parent
        if CurItem != CurTerm:
            self.preferred.set(self.tree.item(curItem)['values'][1])

    def _accept_preferred(self):
        """ Accept rendering in preferred entry box, removing Suggestions tag
        and adding Approved tag. Gives message box warning if no suggested 
        rendering selected, or multiple renderings selected."""

        curItem = self.tree.focus()
        parent = self.tree.parent(curItem)

        categories = ['approved', 'conflicts', 'suggestions', 'unknown', \
                      'cldr',]
        if parent is '':
            #skip it
            pass
        else:
            if parent not in categories:
                curTerm = parent
                category = self.tree.parent(parent)
            else:
                curTerm = curItem
                category = parent
        if not self.preferred.get():
            #is empty
            if category == 'approved':
                self.tree.item(curTerm, \
                             values=[self.tree.item(curTerm)['values'][0], ''])
                self.tree.move(curTerm, 'unknown', 'end')
                curItem = self.tree.insert(curTerm, 'end', text='fallback', \
                                    values=['', \
                        self.fallback[self.tree.item(curTerm)['values'][1]]])
                
        else: 
            self.tree.item(curTerm, values=[self.tree.item(curTerm)['values'][0], \
                                         self.preferred.get()])
            if category != 'approved':
                self.tree.delete(*self.tree.get_children(curTerm)) 
                #self.tree.item(curTerm)['tags'] = ('approved',)
                self.tree.item(curTerm, tags='approved')
                self.tree.move(curTerm, 'approved', 'end')

        self._make_suggestions()
        
        self.tree.tag_configure('approved',   background='palegreen')
        self.tree.tag_configure('conflict',   background='bisque')
        self.tree.tag_configure('suggestions',   background='lightblue')
        self.tree.tag_configure('unknown',   background='whitesmoke')
        self.tree.tag_configure('cldr',   background='violet')
        self.update()

    def _reject_rendering(self):
        """Reject the selected rendering. On an approved
        term this will move it to the 'Unknown' category unless
        suggestions can be made in which case it will be place
        in the 'Suggestions' category. On term with suggestions
        this will remove the selected suggestion, if only one
        rendering is left the term will be moved to the
        'Approved' category."""

        curItem = self.tree.focus()
        parent = self.tree.parent(curItem)

        categories = ['approved', 'conflicts', 'suggestions', 'unknown', \
                      'cldr',]
        if parent is '':
            #skip it
            pass
        else:
            if parent not in categories:
                curTerm = parent
                category = self.tree.parent(parent)
            else:
                curTerm = curItem
                category = parent
        if category == 'approved':
            #move from approved to unknown, with rendering deleted
            self.tree.item(curTerm, \
                             values=[self.tree.item(curTerm)['values'][0], ''])
            self.tree.move(curTerm, 'unknown', 'end')
            pass
        elif category == 'sugestions':
            if curTerm != curItem:
                self.tree.delete(curItem)
                if len(self.tree.get_children(curTerm)) < 1:
                    self.tree.move(curTerm, 'unknown', 'end')
                #   move curTrem from suggestions to unknown
            else: #if curTerm == curItem:
                    self.tree.delete(*self.tree.get_children(curTerm))
                    self.tree.move(curTerm, 'unknown', 'end')
            pass
        elif category == 'conflicts':
            if curTerm != curItem:
                self.tree.delete(curItem)
                if len(self.tree.get_children(curTerm)) == 1:
                    curItem = self.tree.get_children(curTerm)[0]
                    va = self.tree.item(curTerm)['values']
                    vb = self.tree.item(curItem)['values']
                    self.tree.item(curTerm, values=[va[0], vb[1]])
                    self.tree.item(curTerm, tags='approved')
                    self.tree.move(curTerm, 'approved', 'end')
            pass
        elif category == 'unknown':
            #ignore
            pass
        elif category == 'cldr':
            #ignore
            pass
        else:
            messagebox.showerror('_reject_rendering', \
                                 'Unknown category {}.'.format(category))

        self._make_suggestions()
        
        self.tree.tag_configure('approved',   background='palegreen')
        self.tree.tag_configure('conflict',   background='bisque')
        self.tree.tag_configure('suggestions',   background='lightblue')
        self.tree.tag_configure('unknown',   background='whitesmoke')
        self.tree.tag_configure('cldr',   background='violet')
        self.update()

        
    def _on_click_browse_to_pt_project(self):
        """Looks first for Pt8 project dir, if not found looks for Pt7 
        project dir, if not found starts at user home dir"""
        pass

    def _browse_to_dict(self):
        """browse to map creator source/fallback dictionary"""
        lang = self.ddnGuiLanguage.get()

        filein = filedialog.askopenfilename(\
                                filetypes=[('Map Creator Dictionary', '.xml'), ], \
                                           initialdir=self.MapCreator, \
                                           initialfile='', \
                                title=LOCALIZED_TEXT[lang]['Map Creator Dictionary'], \
                                           defaultextension='.xml')
        self.dict_in.set(filein)
        if self.ddnCurProject.get() \
                                and self.dict_in.get() and self.terms_in.get():
            self.btnSaveProject['state'] = 'normal'
        pass

    def _browse_to_old_dict(self):
        """browse to old map creator source/target dictionary"""
        lang = self.ddnGuiLanguage.get()

        filein = filedialog.askopenfilename(\
                                filetypes=[('Map Creator Dictionary', '.xml'), ], \
                                           initialdir=self.MapCreator, \
                                           initialfile='', \
                                title=LOCALIZED_TEXT[lang]['Map Creator Dictionary'], \
                                           defaultextension='.xml')
        self.old_dict.set(filein)
        pass

    def _browse_to_terms(self):
        """browse to paratext biblical terms list html file"""
        lang = self.ddnGuiLanguage.get()

        filein = filedialog.askopenfilename(\
                                filetypes=[('Paratext Biblical Terms', '.htm'), ], \
                                           initialdir=self.BibTerm, \
                                           initialfile='', \
                                title=LOCALIZED_TEXT[lang]['Paratext Biblical Terms'], \
                                           defaultextension='.htm')
        self.terms_in.set(filein)
        if self.ddnCurProject.get() \
                                and self.dict_in.get() and self.terms_in.get():
            self.btnSaveProject['state'] = 'normal'
            self._change_lang()
        pass

    def _on_click_f0_next(self):
        """loads dicts and html into trees tagged as Approved, Conflicts, 
        Suggestions and Unknown. Then moves to F1."""
        lang = self.ddnGuiLanguage.get()

        conf_file = self.ddnCurProject.get()
        #check for project name, fail if not specified.
        if not conf_file:
            messagebox.showinfo("'{}' {}.".format(\
                                LOCALIZED_TEXT[lang]['Current Project>'], \
                                LOCALIZED_TEXT[lang]['is empty']), \
                                "{}".format(LOCALIZED_TEXT[lang][\
                                     'Please enter a name for your project.']))
            return
        #check for source/fallback dict, fail with messagebox if not present.
        source_fallback_dict = self.etrDictIn.get()
        if not source_fallback_dict or not os.path.exists(source_fallback_dict):
            messagebox.showwarning("{} '{}'.".format(\
                        LOCALIZED_TEXT[lang]['Can not find the'], \
                        LOCALIZED_TEXT[lang]['Source/Fallback dictionary']), \
                        "{} '{}'".format(LOCALIZED_TEXT[lang][\
                             'Please enter a valid path to your'], \
                        LOCALIZED_TEXT[lang]['Source/Fallback dictionary']))
            return

        #check for biblical terms list, fail with messagebox if not present.
        biblical_terms_list = self.etrTermsIn.get()
        if not biblical_terms_list or not os.path.exists(biblical_terms_list):
            messagebox.showwarning("{} '{}'.".format(\
                                LOCALIZED_TEXT[lang]['Can not find the'], \
                                LOCALIZED_TEXT[lang]['Biblical terms list']), \
                                "{} '{}'".format(LOCALIZED_TEXT[lang][\
                                     'Please enter a valid path to your'], \
                                LOCALIZED_TEXT[lang]['Biblical terms list']))
            return

        #load source/fallback dict.
        self.Source, self.Regional, self.Fallback = \
                    self._load_map_creator_dict(source_fallback_dict)
        #load biblical terms list.
        self.Biblical_Terms = \
                        self._load_biblical_terms_list(biblical_terms_list)
        #if old source/target dictionary specified, load it.
        old_source_target_dict = self.old_dict.get()
        if not old_source_target_dict or \
                                    not os.path.exists(old_source_target_dict):
            messagebox.showinfo("{} '{}'.".format(\
                    LOCALIZED_TEXT[lang]['Can not find the'], \
                    LOCALIZED_TEXT[lang]['Old Source/Target dictionary']), \
                    LOCALIZED_TEXT[lang]["No '{}' will be loaded"].format(\
                    LOCALIZED_TEXT[lang]['Old Source/Target dictionary']))
        else:
            #load old_source_target_dict.
            _, _, self.Old_Target = \
                            self._load_map_creator_dict(old_source_target_dict)
        #append CLDR terms from CONSTANT.
        if self.add_cldr_fields:
            self.Fallback = self._append_CLDR_terms()
        
        #show working tabs
        self.n.add(self.f1)
        self.n.add(self.f2)
        self.n.select(self.f2)
        
        #now fill working tab
        self._compare_dictionaries(lang=lang)
#        self.n.add(self.f7)
        #hide setup tab
        self.n.hide(0)
        pass

    def _load_map_creator_dict(self, source_fallback_dict, _textin=''):
        """load map creator dictionary into self.Fallback dictionary"""
        global dictionary, attributes
        if not _textin:
            fin = codecs.open(source_fallback_dict, mode='r', encoding='utf-8-sig')
            lines = fin.readlines()
        else:
            lines = _textin
        line = ' '.join([aline.strip() for aline in lines[1:]])
        root = etree.fromstring(line)
#        messagebox.showerror('_load_map_creator_dict','{}'.format(etree.tostring(root[0])))
        dictionary = root[0]
        self.Source = dictionary.get("SourceLanguage")
        self.Regional = dictionary.get("TargetLanguage")
#        messagebox.showerror('_load_map_creator_dict','{}'.format(etree.tostring(dictionary)))
#        translation = dictionary[0]
        fallback = dict()
        for translation in dictionary:
            fallback[str(translation.get("Source"))] = str(translation.get("Target"))
        #messagebox.showerror('_load_map_creator_dict','{} => {}'.format(fallback[str(translation.get("Source"))], str(translation.get("Target"))))
#        aline = lines[2]
#        start = aline.find('SourceLanguage="')+len('SourceLanguage="') + 1
#        end = aline.find('"',start)
#        source = aline[start:end]
#        start = aline.find('TargetLanguage="')+len('TargetLanguage="') + 1
#        end = aline.find('"',start)
#        regional = aline[start:end]
#        for translation in lines[3:-2]:
#            start = translation.find('<Translation Source="') + len('<Translation Source="')
#            end = translation.find('"', start)
#            key = translation[start:end]
#            if not key:
#                messagebox.showerror('_load_map_creator_dict',' null key')
#                return
#            start = translation.find(' Target="', end) + len('<Translation Source="')
#            end = translation.find('"', start)
#            value = translation[start:end]
#            fallback[key] = value
##            else:
##                print('fallback empty')
        return(self.Source, self.Regional, fallback)

    def _load_biblical_terms_list(self, biblical_terms_list, _textin=''):
        """load biblicaterms list html file exported from Paratext"""
        if not _textin:
            fin = codecs.open(biblical_terms_list, mode='r', \
                                                  encoding='utf-16')
            lines = [l.strip() for l in fin.readlines()]
        else:
            lines = _textin
        line = ' '.join([aline.strip() for aline in lines])
        html = etree.HTML(line)
        #root = etree.fromstring(line)
        #body = etree.SubElement(html, "body")
        body = html[1]
        table = body[0]
        terms = dict()
        for tr in table[1:]:
            term = str(tr[3].text)
            rendering = str(tr[4].text)
            terms[term] = rendering
        return(terms)

    def _append_CLDR_terms(self, _fallback=dict()):
        """add the CLDR terms to fallback dict"""
        if _fallback:
            fallback = _fallback
        else:
            fallback = self.Fallback
        for term, value in CLDR:
            if term and term not in fallback:
                fallback[term] = value
            
        return(fallback)

    def _compare_dictionaries(self, _biblical=dict(), _fallback=dict(), _old=dict(), lang='en-US'):
        """look for matching terms and fill working tabs"""
#        global approved, conflicts, suggestions, unknown, cldr

        if _biblical:
            biblical = _biblical
        else:
            biblical = self.Biblical_Terms
        
        if _fallback:
            fallback = _fallback
        else:
            fallback = self.Fallback
        
        if _old:
            old = _old
        else:
            old = self.Old_Target
#        messagebox.showwarning('_compare_dictionaries','{}'.format(biblical))
#        messagebox.showwarning('_compare_dictionaries','{}'.format(fallback))
        if self.dict_in_changed.get() or self.terms_in_changed.get() or len(list(self.trout)) == 0:
            #for term in fallback, decide where it goes,
            #all terms should be under one of these five categories
            #messagebox.showwarning('_compare_dictionaries','dict {}, terms{}, trout {}'.format(self.dict_in_changed.get(), self.terms_in_changed.get(), len(list(self.trout))))
            approved = self.tree.insert('', 'end', iid='approved', values=['', ''], \
                        text=LOCALIZED_TEXT[lang]['Approved'], tags=('approved',))
            suggestions = self.tree.insert('', 'end', iid='suggestions', values=['', ''], \
                        text=LOCALIZED_TEXT[lang]['Suggestions'], tags=('suggestions',))
            conflicts = self.tree.insert('', 'end', iid='conflicts', values=['', ''], \
                        text=LOCALIZED_TEXT[lang]['Conflicts'], tags=('conflicts',))
            unknown = self.tree.insert('', 'end', iid='unknown', values=['', ''], \
                        text=LOCALIZED_TEXT[lang]['Unknown'], tags=('unknown',))
            cldr = self.tree.insert('', 'end', iid='cldr', values=['', ''], \
                        text=LOCALIZED_TEXT[lang]['CLDR'], tags=('cldr',))
            # if in biblical
            for term in fallback:
                if term in biblical:
                    #how many renderings?
                    if biblical[term] is None:
                        renderings = ['',]
                    else:
                        renderings = biblical[term].split(',')
                        if len(renderings) > 0:
                            renderings = [r.strip() for r in renderings]
                            renderings = [r.strip('*') for r in renderings]
                        else:
                            renderings = ["",]
                    #remove any duplicates
                    renderings = set(renderings)
                    #put it in target anyway
#                    if len(renderings) > 1: #at least one rendering exists
#                        messagebox.showwarning('_compare_dictionaries', 'term=>{}<, renderings=>{}'.format(term, renderings))
                    if len(renderings[0]) > 0: #at least one rendering exists
                        #messagebox.showwarning('_compare_dictionaries', 'term is =>{}<'.format(term))
                        #if term in target and has single non zero rendering
                        #   put in approved tab (stripping *?)
                        if len(renderings) == 1: #is just one renderings
                            if term in old and fallback[term] != old[term]:
                                #put in conflicts
                                item = self.tree.insert('conflicts', 'end', \
                                        values=["{}".format(term), "{}".format(renderings[0])], \
                                        text='term', tags=('conflicts',))
                                child = self.tree.insert(item, 'end', values=['', old[term]], text='old rendering', tags=('conflicts',))
                            else:
                                item = self.tree.insert('approved', 'end', \
                                        values=["{}".format(term), \
                                                "{}".format(renderings[0])], \
                                        text='term', tags=('approved',))
                            
                        else: #multiple possibilities so put in Suggestions
                            item = self.tree.insert('suggestions', 'end', \
                                        values=["{}".format(term), ""], \
                                        text='term', tags=('suggestions',))
                            for rendering in renderings:
#                                messagebox.showwarning('_compare_dictionaries', 'term=>{}<, rendering=>{}'.format(term, rendering))
                                if len(rendering) > 0:
                                    child = self.tree.insert(item, 'end', \
                                        values=["", \
                                                "{}".format(rendering)], \
                                        text='rendering', tags=('suggestions',))
            #   each rendering shown as child of term, terms with * put at top of list sans * or with and just strip when apply it
                            if term in old and fallback[term] != old[term]:
                                #put in conflicts
                                child = self.tree.insert(item, 'end', \
                                        values=["", \
                                                "{}".format(rendering.strip('*'))], \
                                        text='old rendering', \
                                        tags=('suggestions',))
                else:
                    if term in old and old[term]:
                        item = self.tree.insert('suggestions', 'end', \
                                        values=[term, old[term]], text='term', \
                                        tags=('suggestions'))
                        child = self.tree.insert(item, 'end', \
                                        values=["", "{}".format(fallback[term])], \
                                        text='fallback', \
                                        tags=('old-rendering', 'suggestions',))
                    elif term.isdigit() and fallback[term].isdigit() \
                                        and self.accept_regional_digits.get() > 0:
                        item = self.tree.insert('approved', 'end', \
                                                values=["{}".format(term), \
                                                        "{}".format(fallback[term])], \
                                                text='term', tags=('approved',))
                    else:
                                        
                        item = self.tree.insert('unknown', 'end', \
                                                values=[term, ''], text='term', \
                                                tags=('unknown',))
                        child = self.tree.insert(item, 'end', \
                                                 values=['', fallback[term]], \
                                                 text='fallback', \
                                                 tags=('suggestions',))
            self.dict_in_changed.set(0)
            self.terms_in_changed.set(0)
        else:
            #retain old tree
            #messagebox.showwarning("_compare_dictionaries pre-tree","{}".format(self.tree.get_children('')))
            self._from_etree_to_tree()
            if self.old_dict_changed.get():
                approved_terms = dict()
                #messagebox.showwarning("old_dict changed post-tree","{}".format(self.tree.get_children('')))
                for child in self.tree.get_children('approved'):
                    values = self.tree.item(child)['values']
                    approved_terms[values[0]] = child
                for term in approved_terms:
                    if term in old:
                        if fallback[term] != old[term]:
                            #move to conflicts and add old suggestion
                            self.tree.move(term, 'conflicts', 'end')
                            self.tree.item(term, tags='conflicts')
                            item = self.tree.insert(term, 'end', \
                                                    values=[term, old[term]], \
                                                    text='old rendering', \
                                                    tags="('conflicts',)")

        self._make_suggestions()
    
    def _look_in_concordance(self, term, concordance):
        """look up term in concordance and add suggestions, moving term to
        suggestions if necessary"""

        suggested = dict()
        words = [word.strip(',.:;*').lower() \
                 for word in str(self.tree.item(term)['values'][0]).split(' ')]
#        messagebox.showwarning("_look_in_concordance","words={}".format(words))
        for word in words:
            if word in concordance:
                for item in concordance[word]:
                    if item in suggested:
                        suggested[item] += 1
                    else:
                        suggested[item] = 1
#            if word == 'ad':
#                messagebox.showwarning("word 'ad' suggested?","suggested={}".format(suggested))
#                pass
        rank = sorted(suggested, key=suggested.get, reverse=True)
        for item in rank:
            if item not in self.tree.get_children(term):
                self.tree.insert(term,'end', \
                                 values=[self.tree.item(item)['values'][0], \
                                 self.tree.item(item)['values'][1]],\
                                 text='possible', tags=('suggestions',))
        if len(rank) > 0 and self.tree.parent(term) != 'suggestions':
            for child in self.tree.get_children(term):
                self.tree.item(item, tags='suggestions')
            self.tree.item(term, tags='suggestions')
            self.tree.move(term, 'suggestions', 'end') 
                   
    def _make_suggestions(self):
        """scan approved renderings looking for similarities to terms in \
        suggestions and unknown, moving unknown terms if necessary and adding \
        suggestions."""

        #build concordance based on current approved
        concordance = dict()
        for term in self.tree.get_children('approved'):
            words = [word.strip(',.:;*').lower() \
                     for word in str(self.tree.item(term)['values'][0]).split(' ')]
            for word in words:
#                if word == 'ad':
#                    messagebox.showwarning("word == 'ad'","concordance={}".format(concordance))
#                    pass
                if word not in ['and', 'the', 'a', 'to', 'of'] \
                                                    and not word.isdigit():
                    if word not in concordance:
                        concordance[word] = set([term, ])
                    else:
                        concordance[word].add(term)
#                if word == 'ad':
#                    messagebox.showwarning("word 'ad' added?","concordance={}".format(concordance))
#                    pass
                
                
        #so concordance now holds a list of words in approved terms along with\
        #list of index of terms() they occur in
        
        for term in self.tree.get_children('suggestions'):
            self._look_in_concordance(term, concordance)

        for term in self.tree.get_children('unknown'):
            self._look_in_concordance(term, concordance)

        self._collapse_all()
    
    def _on_click_f1_next(self):
        """moves to f2"""
        pass

    def _from_tree_to_etree(self):
        """loads contents of treeview into etree and returns it"""
        categories = self.tree.get_children('')
#        messagebox.showwarning('_from_tree_to_etree', \
#                               'categories={}'.format(categories))
        for category in categories:
            
            acategory = etree.SubElement(self.trout, self.tree.item(category)['text'])
            if category =='approved':
                acategory.set('tags', "('approved',)")
            elif category =='conflicts':
                acategory.set('tags', "('conflicts',)")
            elif category =='suggestions':
                acategory.set('tags', "('suggestions',)")
            elif category =='unknown':
                acategory.set('tags', "('unknown',)")
            elif category =='cldr':
                acategory.set('tags', "('cldr',)")
            else:
                messagebox.showerror('_from_tree_to_etree', \
                               'unrecognised category >{}<'.format(category))
                return
#            acategory.text = self.tree.item(category)['text']
            sons = self.tree.get_children(category)
#            messagebox.showwarning('_from_tree_to_etree', \
#                               '{}, sons={}'.format(category, sons))
            for son in sons:
                ason = etree.SubElement(acategory, son)
#                ason.text = self.tree.item(son)['text']
                ason.set('values', '{}'.format(self.tree.item(son)['values']))
                ason.set('tags', '{}'.format(tuple(self.tree.item(son)['tags'])))
                grandsons = self.tree.get_children(son)
                for grandson in grandsons:
                    agrandson = etree.SubElement(ason, grandson)
                    agrandson.text = self.tree.item(grandson)['text']
                    agrandson.set('values', \
                                  '{}'.format(self.tree.item(grandson)['values']))
                    agrandson.set('tags', \
                                  '{}'.format(tuple(self.tree.item(grandson)['tags'])))
#                    grandsons = self.tree.get_children(grandson)
#        messagebox.showwarning('','{}'.format(etree.tostring(self.trout, \
#                                       encoding='unicode', \
#                                       pretty_print=True)))
#        messagebox.showwarning('_from_tree_to_etree', \
#                               'filled with {} categories'.\
#                               format([child.tag for child in self.trout]))
        return self.trout

    def _output_dict(self):
        """output approved terms as a MapCreator dictionary file"""
        lang = self.ddnGuiLanguage.get()

        fileout = os.path.normpath('{}/{}-{}.xml'.\
                format(self.MapCreator, self.Source, self.ddnCurProject.get()))
        linesout = ['<?xml version="1.0" encoding="UTF-8"?>', \
                    '<DictionarySet xmlns:mc="urn:fmosoft-map-creator" xmlns="urn:fmosoft-map-creator" Version="1">', \
                    '   <Dictionary SourceLanguage="{}" SourceLanguageIsPredefined="true" TargetLanguage="{}" TargetLanguageIsPredefined="false">'.\
                            format(self.Source, self.ddnCurProject.get()), \
                    ]
        for child in self.tree.get_children('approved'):
            vv = self.tree.item(child)['values']
            linesout.append('       <Translation Source="{}" Target="{}"/>'.format(vv[0], vv[1]))
        linesout.append('   </Dictionary>')
        linesout.append('</DictionarySet>')
        linesout.append('')

        if os.path.exists(fileout):
            os.remove(fileout)

        if fileout:
            output = codecs.open(fileout, mode='w', encoding='utf-8')
            output.write('\n'.join(linesout))
            output.close()
        pass
                
    def _on_save_project(self, _project='', lang='en-US'):
        """save all current info from each tab"""
        lang = self.ddnGuiLanguage.get()
        if _project:
            project = _project
        else:
            project = self.ddnCurProject.get()

        fileout = filedialog.asksaveasfilename(\
                                    filetypes=[('Project file', '.prj'), ], \
                                          initialdir=self.BibTerm, \
                                          initialfile=project, \
                                          title=LOCALIZED_TEXT[lang]['Save'], \
                                          defaultextension='.prj')
        new_project = fileout.split('/')[-1]
        new_project = new_project[:-4]
        if new_project != project:
            self.lblProject['text'] = \
                           LOCALIZED_TEXT[lang]['Current Project>'] + \
                           ' ' + new_project
        #create new project tree, throwing away any existing tree
        self.root = etree.Element('root')
        #add child 'settings', all user configurable bits under here
        self.settings = etree.SubElement(self.root, "settings")
        self.sf0 = etree.SubElement(self.settings, "f0")
        self.sf1 = etree.SubElement(self.settings, "f1")
        self.sf2 = etree.SubElement(self.settings, "f2")
        self.trout = etree.SubElement(self.root, "tree")

        self.settings.attrib['guilang'] = self.selected_lang.get()
        
        self.sf0.attrib['fallback'] = self.dict_in.get()
        self.sf0.attrib['terms'] = self.terms_in.get()
        self.sf0.attrib['old'] = self.old_dict.get()
        self.sf0.attrib['digits'] = \
                                '{}'.format(self.accept_regional_digits.get())
        self.sf0.attrib['cldr'] = '{}'.format(self.add_cldr_fields.get())
        
        self.sf1.text = self.txtPrefChar.get(0.0, 9999.9999)

        self.sf1.attrib['template'] = self.ddnPrefChar.get() \
                                if self.ddnPrefChar.get() else ''
#        self.sf1.attrib['preferred'] = self.ddnPrefChar.get() \
#                                if self.ddnPrefChar.get() else ''

        temp = self._from_tree_to_etree()

        if os.path.exists(fileout):
            os.remove(fileout)

        if fileout:
            output = codecs.open(fileout, mode='w', encoding='utf-8')
            output.write(etree.tostring(self.root, encoding='unicode', \
                                         pretty_print=True))
            output.close()

            # list projects in Pub2SD and update list in self.ddnCurProject
            self.list_projects = [f.rstrip('.prj') \
                                  for f in os.listdir(self.BibTerm) \
                                                     if f.endswith('.prj')]
            self.ddnCurProject['values'] = self.list_projects
            self.ddnCurProject.set(new_project)
        else:
            pass
        pass

    def _load_project(self, _thefile='', _lang=''):
        """check if project files exists,
        load old values to f0 and set loading old pro flag,
        _compare_dictionaries() will test flag and load tree accordingly"""
#        messagebox.showwarning('_load_project', 'Entered')
#    def _load_project(self, thefile):
#        """loads an existing project (.prj) file,adapting it's contents
#                                      to the current Simple/Advanced choice"""
        #set current project label
        if len(_lang) > 0:
            lang = _lang
        else:
            lang = self.selected_lang.get()
        if lang == '':
            lang = 'en-US'
#        messagebox.showwarning('_load_project', \
#                               '_lang=>{}<, lang=>{}<'.format(_lang, lang))
        self.lblProject['text'] = '{} {}'.\
                            format(LOCALIZED_TEXT[lang]['Current Project>'], \
                                   self.current_project.get())
        self.update()

        linesin = list()
        #thefile comes from current project label or test
        if _thefile:
            thefile = _thefile
        else:
            thefile = ospath.normpath(\
                            self.BibTerm + '/' + self.current_project + '.prj')
        if os.path.exists(thefile):
            filein = codecs.open(thefile, mode='r', encoding='utf-8')
            for aline in filein.readlines():
    #            if len(aline.strip()) > 0:
                if aline.strip():
                    linesin.extend([aline.strip()])
            filein.close()
            lines = ''.join(linesin)
            self.root = etree.fromstring(lines)
            self.settings = self.root.find("settings")
            self.sf0 = self.settings.find("f0")
            if self.sf0.get('fallback') != self.dict_in.get():
                self.dict_in.set(self.sf0.get('fallback'))
                self.dict_in_changed.set(1)
            else:
                self.dict_in_changed.set(0)
            if self.sf0.get('terms') != self.terms_in.get():
                self.terms_in.set(self.sf0.get('terms'))
                self.terms_in_changed.set(1)
            else:
                self.terms_in_changed.set(0)
            if self.sf0.get('old') != self.terms_in.get():
                self.old_dict.set(self.sf0.get('old'))
                self.old_dict_changed.set(1)
            else:
                self.old_dict_changed.set(0)
            self.sf1 = self.settings.find("f1")
            self.sf2 = self.settings.find("f2")
            self.trout = self.root.find("tree")
#            self.preferred.set(int(self.sf1.attrib['preferred'] == 'True'))
            self.txtPrefChar.delete(0.0, 9999.9999)
            if self.sf1.text != None:
                self.txtPrefChar.insert(9999.9999, self.sf1.text)
#        messagebox.showwarning('_load_project', 'Exit')

    def _from_etree_to_tree(self, lang='en-US'):
        """loads categories and terms into tree"""
        #clear existing tree
#        for i in self.tree.get_children():
#            self.tree.delete(i)
        self.tree.delete(*self.tree.get_children())
        #now insert old tree
        for category in self.trout:
            tagged = category.get('tags')
            if tagged is None:
                tagged = "('{}',)".format(category.tag)
            if tagged[-1] == ')':
                inserttext = tagged[2:3].upper() + tagged[3:tagged.find(')')-2]
            else:
                inserttext = tagged[1:2].upper() + tagged[2:-1]
            #messagebox.showwarning('_from_etree_to_tree', "{}, {}".format(lang, inserttext))
            thiscategory = self.tree.insert('', 'end', iid=inserttext.lower(), values=['', ''], \
                    text=LOCALIZED_TEXT[lang][inserttext], tags="{}".format(inserttext.lower()))
            for term in category:
                values = eval(term.get('values'))
                tags = term.get('tags')
#                messagebox.showwarning('_from_etree_to_tree', "{}, {}".format(values, tags))
                thisterm = self.tree.insert(thiscategory, 'end')
                self.tree.item(thisterm, tags=term.get('tags'))
                self.tree.item(thisterm, text=term.text)
                self.tree.item(thisterm, values=[str(values[0]), str(values[1])])
#                    tags=term.get('tags'))
                for rendering in term:
                    thisrendering = self.tree.insert(thisterm, 'end', \
                            text=rendering.text, values=term.get('values'), \
                            tags=rendering.get('tags'))
        self.tree.tag_configure('approved',   background='palegreen')
        self.tree.tag_configure('conflict',   background='bisque')
        self.tree.tag_configure('suggestions',   background='lightblue')
        self.tree.tag_configure('unknown',   background='whitesmoke')
        self.tree.tag_configure('cldr',   background='violet')
        self.tree.update()            
        pass
    
    def _on_del_project(self):
        """delete the project shown in self.ddnCurProject.get()"""
        project = self.ddnCurProject.get()
#        if len(project) > 0:
        if project:
            if '.prj'!= project[-4:]:
                project += '.prj'
            if os.path.exists(self.BibTerm + '/'+ project):
                os.remove(self.BibTerm + '/'+ project)
            self.list_projects = [f.rstrip('.prj') \
                                  for f in os.listdir(self.BibTerm) \
                                                     if f.endswith('.prj')]
            self.ddnCurProject['values'] = self.list_projects
#            if len(self.list_projects) > 0:
            if self.list_projects:
                self.ddnCurProject.set(self.list_projects[0])
            else:
                self.ddnCurProject.set('')
        pass

    def _on_new_project(self):
        """create new project file and add to current list of projects"""
        lang = self.ddnGuiLanguage.get()
        projectfile = filedialog.asksaveasfilename(\
                                filetypes=[('Paratext Biblical Terms', '.htm'), ], \
                                           initialdir=self.BibTerm, \
                                           initialfile='', \
                                title=LOCALIZED_TEXT[lang]['BibTerms2Dict project'], \
                                           defaultextension='.prj')
        if os.path.exists(projectfile):
            messagebox.showwarning(LOCALIZED_TEXT[lang]['New Project'], \
                LOCALIZED_TEXT[lang]['{} already exist choose another name.'].\
                                        format(os.path.basename(projectfile)))
            return
        else:
            newfile = codecs.open(fileout, mode='w', encoding='utf-8')
            newfile.close()
            self.list_projects = [f.rstrip('.prj') \
                                  for f in os.listdir(self.BibTerm) \
                                                     if f.endswith('.prj')]
            self.ddnCurProject['values'] = self.list_projects
            self.ddnCurProject.set(os.path.basename(projectfile)[:-4])
            self.update

        pass

    def _on_read_me(self):
        """opens the appropriate localized read_me.html"""
        lang = self.ddnGuiLanguage.get()
        app_dir = get_script_directory()
        # open an HTML file on my own (Windows) computer
        if lang == 'en-US':
            url = os.path.normpath("file://" + app_dir + "/Read_Me.html")
        elif lang == 'fr-FR':
            url = os.path.normpath("file://" + app_dir + "/Lire_Moi.html")
        elif lang == 'pt-PT':
            #need portugese version, default to eng
            url = os.path.normpath("file://" + app_dir + "/Read_Me.html")
        else:
            messagebox.showwarning(\
            'Warning', "Error in on_read_me: " +\
            "{} is unrecognised lang, defaulting to 'en-US.'".format(lang))
            url = os.path.normpath("file://" + app_dir + "/Read_Me.html")
        webbrowser.open(url)
        pass

    def _change_lang(self):
        """change lang of interface"""
        lang = self.ddnGuiLanguage.get()
        self.lblProject['text'] = LOCALIZED_TEXT[lang]['Current Project>'] + \
                                               ' ' + self.ddnCurProject.get()

        pass
    
    def _add_row(self):
        """temp add row"""
        pass
    def _delete_selected_row(self):
        """temp delete row"""
        pass

def on_copyright():
    """displays copyright message and other details"""
    pass