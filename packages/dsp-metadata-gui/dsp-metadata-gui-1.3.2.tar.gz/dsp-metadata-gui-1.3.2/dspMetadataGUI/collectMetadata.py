import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from util.utils import Cardinality, Datatype, Validity, open_file
from util.metaDataSet import DataClass, MetaDataSet, Property
from util.dataHandling import DataHandling
from util import converter, rdfConverter
from typing import Optional, Tuple, Union
import wx
import wx.lib.scrolledpanel as scrolledPanel
import wx.lib.dialogs as dialogs
import wx.adv
import re
from glob import glob


data_handler: DataHandling


def collectMetadata():
    """
    Runner function that launches the app.

    Calling this method initiates a data handler and opens the GUI.

    Example:
        To run the application, simply call:
        ```
        $ collectMetadata()
        ```
    """
    # create a data handler
    global data_handler
    data_handler = DataHandling()
    # open GUI
    app = wx.App()
    ProjectFrame()
    app.MainLoop()


class ProjectFrame(wx.Frame):
    def __init__(self):
        """
        This class holds the frame of the main application window.
        """
        super().__init__(parent=None,
                         title='Project Data Editor', size=(1100, 750))
        self.panel = ProjectPanel(self)
        self.__create_menu()
        self.Show()

    def __create_menu(self):
        """
        Create the menu, add a folder dialog box
        """
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_folder_menu_item = file_menu.Append(wx.ID_NEW, 'Add new Project', 'Open a folder with project files')
        self.Bind(event=wx.EVT_MENU, handler=self.panel.on_add_new_project, source=open_folder_menu_item)
        save_menu_item = file_menu.Append(wx.ID_SAVE, "&Save")
        self.Bind(wx.EVT_MENU, self.__on_save, source=save_menu_item)
        menu_bar.Append(file_menu, '&File')
        options_menu = wx.Menu()
        menu_bar.Append(options_menu, '&Options')
        json_converter_menu_item = options_menu.Append(wx.ID_ANY, "Convert RDF to JSON (Old RDF -> New JSON Model)")
        self.Bind(wx.EVT_MENU, self.__on_convert, json_converter_menu_item)
        rdf_converter_menu_item = options_menu.Append(wx.ID_ANY, "Convert JSON to RDF (New JSON -> New RDF Model)")
        self.Bind(wx.EVT_MENU, self.__on_rdf_convert, rdf_converter_menu_item)
        options_help = wx.Menu()
        menu_bar.Append(options_help, '&Help')
        self.SetMenuBar(menu_bar)

    def __on_convert(self, event):
        dlg = JSONConverterDialog(None, title="JSON Converter")
        dlg.ShowModal()
        dlg.Destroy()

    def __on_rdf_convert(self, event):
        dlg = RDFConverterDialog(None, title="RDF Converter")
        dlg.ShowModal()
        dlg.Destroy()

    def __on_save(self, event):
        """
        Menu item for saving the current window
        """
        if data_handler.current_window:
            data_handler.current_window.save()
        else:
            data_handler.save_data()


class ProjectPanel(wx.Panel):
    def __init__(self, parent: ProjectFrame):
        """
        Panel containing the contents of the application's main window.

        The Panel displays a list of projects on top.
        On the bottom left it shows a preview of the turtle serialization of the selected project.
        On the bottom right it holds a number of buttons for various tasks.
        (Adding/removing projects, modifying projects, exporting data, etc.)

        Args:
            parent (ProjectFrame): The parent frame to hold this panel.
        """
        super().__init__(parent)
        self.folder_path = ""
        self.row_obj_dict = {}  # type: ignore
        self.project_dependent_buttons = []

        # Create list for projects
        main_sizer = wx.FlexGridSizer(3, 1, 10, 10)
        # main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="DaSCH Service Platform - Metadata Collection")
        main_sizer.Add(title, 0, wx.ALL | wx.LEFT, 10)
        self.list_ctrl = wx.ListCtrl(self, size=(-1, 200), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_item_selected)
        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 10)

        # Create turtle preview
        bottom_sizer = wx.FlexGridSizer(1, 2, 10, 10)
        bottom_sizer.AddGrowableCol(0)
        bottom_sizer.AddGrowableRow(0)
        rdf_display = wx.TextCtrl(self, value="No Project selected.",
                                  style=wx.TE_READONLY | wx.TE_MULTILINE, size=(400, -1))
        try:
            rdf_display.OSXDisableAllSmartSubstitutions()
        except Exception:
            print("Info: Disabling smart substitutions not available. \
                 (Should not be a problem, to be sure, check that there are no typographic quotation marks when you copy-paste the .ttl preview.)")
        self.rdf_display = rdf_display
        bottom_sizer.Add(rdf_display, flag=wx.EXPAND)

        # Create Buttons
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        new_folder_button = wx.Button(self, label='Add new Project')
        new_folder_button.Bind(wx.EVT_BUTTON, self.on_add_new_project)
        button_sizer.Add(new_folder_button, 0, wx.ALL | wx.EXPAND, 7)

        import_project_button = wx.Button(self, label='Import Project')
        import_project_button.Bind(wx.EVT_BUTTON, self.on_import_project)
        button_sizer.Add(import_project_button, 0, wx.ALL | wx.EXPAND, 7)

        remove_folder_button = wx.Button(self, label='Remove selected Project')
        self.project_dependent_buttons.append(remove_folder_button)
        remove_folder_button.Bind(wx.EVT_BUTTON, self.on_remove_project)
        button_sizer.Add(remove_folder_button, 0, wx.ALL | wx.EXPAND, 7)

        edit_tabs_button = wx.Button(self, label='Edit selected Project')
        self.project_dependent_buttons.append(edit_tabs_button)
        edit_tabs_button.Bind(wx.EVT_BUTTON, self.on_edit_tabbed)
        button_sizer.Add(edit_tabs_button, 0, wx.ALL | wx.EXPAND, 7)

        validate_button = wx.Button(self, label='Validate selected Project')
        self.project_dependent_buttons.append(validate_button)
        validate_button.Bind(wx.EVT_BUTTON, self.on_validate)
        button_sizer.Add(validate_button, 0, wx.ALL | wx.EXPAND, 7)

        process_xml_button = wx.Button(self, label='Export selected Project as RDF')
        self.project_dependent_buttons.append(process_xml_button)
        process_xml_button.Bind(wx.EVT_BUTTON, self.export_data)
        button_sizer.Add(process_xml_button, 0, wx.ALL | wx.EXPAND, 7)

        zip_and_export_btn = wx.Button(self, label='ZIP and Export Project')
        self.project_dependent_buttons.append(zip_and_export_btn)
        zip_and_export_btn.Bind(wx.EVT_BUTTON, self.__on_zip_and_export)
        button_sizer.Add(zip_and_export_btn, 0, wx.ALL | wx.EXPAND, 7)

        # Layout it all
        bottom_sizer.Add(button_sizer, 0, wx.ALL, 10)
        main_sizer.Add(bottom_sizer, 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.AddGrowableRow(2)
        self.SetSizer(main_sizer)
        self.Fit()
        self.create_header()
        self.refresh_view()
        self.Layout()

    def __on_zip_and_export(self, event):
        """
        Export a ZIP archive containing the selected files, metadata and a pickle with the binaries.
        """
        title = "Where to export to?"
        with wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                print(path)
                data_handler.zip_and_export(self.get_selected_project(), path)

    def on_add_new_project(self, event):
        """
        Open a new folder and add it to projects.
        """
        title = "Enter Project Shortcode:\n(4 alphanumeric characters)\n\nIf your project doesn't have a shortcode assigned yet, \nplease contact the DaSCH Client Services)"
        dlg = wx.TextEntryDialog(self, message=title, caption="Enter Shortcode")
        if dlg.ShowModal() == wx.ID_OK:
            shortcode = dlg.GetValue()
            if not re.match('[a-zA-Z0-9]{4}$', shortcode):
                print("Invalid shortcode entered.")
                return
        else:
            return
        title = "Choose a directory:"
        dlg = wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.add_new_project(dlg.GetPath(), shortcode)
        dlg.Destroy()

    def refresh_repos(self):
        """
        Refresh all loaded repos in the list.
        """
        for i, project in enumerate(data_handler.projects):
            if i < self.list_ctrl.GetItemCount():
                self.list_ctrl.SetItem(i, 0, project.path)
            else:
                self.list_ctrl.InsertItem(i, project.path)
            self.list_ctrl.SetItem(i, 1, project.name)
            self.list_ctrl.SetItem(i, 2, project.shortcode)
            self.list_ctrl.SetItem(i, 3, str(project.files))
            self.list_ctrl.SetItem(i, 4, project.get_status())

    def create_header(self):
        """
        creates the header
        """
        self.list_ctrl.InsertColumn(0, 'Folder', width=300)
        self.list_ctrl.InsertColumn(1, 'Project', width=180)
        self.list_ctrl.InsertColumn(2, 'Shortcode', width=90)
        self.list_ctrl.InsertColumn(3, 'List of files', width=340)
        self.list_ctrl.InsertColumn(4, 'Status', width=350)

    def refresh_view(self):
        """refreshes the GUI after data changes"""
        self.refresh_repos()
        self.display_rdf()
        self.refresh_buttons()
        self.Layout()

    def refresh_buttons(self):
        """determins which buttons should be enabled and displays them accordingly"""
        if self.get_selected_project():
            flag = True
        else:
            flag = False
        for b in self.project_dependent_buttons:
            if flag:
                b.Enable()
            else:
                b.Disable()

    def display_rdf(self):
        """displays the RDF preview"""
        project = self.get_selected_project()
        if project:
            txt = project.get_turtle()
        else:
            txt = "No project selected."
        self.rdf_display.SetValue(txt)

    def get_selected_project(self) -> Optional[MetaDataSet]:
        """Gets the currently selected project/metadata set"""
        selection = self.list_ctrl.GetFirstSelected()
        if selection < 0:
            return None
        shortcode = self.list_ctrl.GetItem(selection, col=2).GetText()
        return data_handler.get_project_by_shortcode(shortcode)

    def on_edit_tabbed(self, event):
        """
        This function calls the EditBaseDialog and hands over pFiles, a list.
        """
        repo = self.get_selected_project()
        if repo:
            window = TabbedWindow(self, repo)
            data_handler.current_window = window
            window.Show()
            self.Disable()

    def export_data(self, event):
        """ Set selection and call create_xml """
        selection = self.list_ctrl.GetFocusedItem()
        if selection >= 0:
            res = data_handler.validate_and_export_data(selection)
            print(res[0])
            # LATER: let this return indication of success. display something to the user.

    def add_new_project(self, folder_path, shortcode):
        """ Add a new project."""
        dir_list = os.listdir(folder_path)
        if '.DS_Store' in dir_list:
            dir_list.remove('.DS_Store')
        data_handler.add_project(folder_path, shortcode, dir_list)
        self.refresh_view()

    def on_import_project(self, event):
        """handles event from 'import' button click"""
        with wx.FileDialog(self, "Choose file:",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fd:
            if fd.ShowModal() == wx.ID_OK:
                f = fd.GetPath()
                if not f.endswith('.data'):
                    print(f'Could not import file: {f}\n  For now, only .data supported.')
                    # LATER: allow RDF import here
                    return
                data_handler.import_project(f)
                self.refresh_view()

    def on_remove_project(self, event):
        """handles event from 'remove project' button click"""
        selected = self.get_selected_project()
        msg = f"Are you sure you want to delete the Project '{selected.name} ({selected.shortcode})'"
        with wx.MessageDialog(self, "Sure?", msg, wx.YES_NO) as dlg:
            if dlg.ShowModal() == wx.ID_YES:
                data_handler.remove_project(selected)
                self.list_ctrl.DeleteAllItems()
                self.refresh_view()

    def on_validate(self, event):
        """handles event from 'validate' button click"""
        repo = self.get_selected_project()
        if repo:
            conforms, results_graph, results_text = data_handler.validate_graph(repo)
            if conforms:
                with wx.MessageDialog(self, "Validation Successful", "Validation Successful", wx.OK | wx.ICON_INFORMATION) as dlg:
                    dlg.ShowModal()
            else:
                with dialogs.ScrolledMessageDialog(self, results_text, "Validation Failed", size=(800, 500)) as dlg:
                    dlg.ShowModal()

    def on_item_selected(self, event):
        """handles event from selection change"""
        # LATER: look into why this is called twice, which makes it slow
        self.refresh_view()


class TabbedWindow(wx.Frame):
    def __init__(self, parent: ProjectPanel, dataset: MetaDataSet):
        """
        A Window holding the different tabs

        Args:
            parent (ProjectPanel): the parent object
            dataset (MetaDataSet): the dataset
        """
        wx.Frame.__init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                          size=(1200, 600), style=wx.DEFAULT_FRAME_STYLE,
                          name="Metadata tabs")
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.panel = wx.Panel(self)
        self.parent = parent
        self.dataset = dataset

        # Create a panel and notebook (tabs holder)
        panel = self.panel
        nb = wx.Notebook(panel)
        nb.SetMinSize((-1, 200))
        nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_change)

        # Create the tab windows
        tab1 = TabOne(nb, self.dataset)
        tab2 = DataTab(nb, self.dataset, self.dataset.project, "Project")
        tab3 = DataTab(nb, self.dataset, self.dataset.dataset, "Dataset", multiple=True)
        tab4 = DataTab(nb, self.dataset, self.dataset.persons, "Person", multiple=True)
        tab5 = DataTab(nb, self.dataset, self.dataset.organizations, "Organization", multiple=True)
        tab6 = DataTab(nb, self.dataset, self.dataset.grants, "Grant", multiple=True)

        # Add the windows to tabs and name them.
        nb.AddPage(tab1, "Base Data")
        nb.AddPage(tab5, "Organization")
        nb.AddPage(tab4, "Person")
        nb.AddPage(tab6, "Grant")
        nb.AddPage(tab3, "Dataset")
        nb.AddPage(tab2, "Project")

        data_handler.tabs = [tab2, tab3, tab4, tab5, tab6]

        nb_sizer = wx.BoxSizer()
        nb_sizer.Add(nb, 1, wx.ALL | wx.EXPAND)

        # Buttons
        save_button = wx.Button(panel, label='Save')
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        saveclose_button = wx.Button(panel, label='Save and Close')
        saveclose_button.Bind(wx.EVT_BUTTON, self.on_saveclose)
        cancel_button = wx.Button(panel, label='Cancel')
        cancel_button.Bind(wx.EVT_BUTTON, self.on_close)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(save_button, 0, wx.ALL, 5)
        button_sizer.Add(saveclose_button, 0, wx.ALL, 5)
        button_sizer.Add(cancel_button, 0, wx.ALL, 5)
        feedback_text = wx.StaticText(panel)
        self.feedback_text = feedback_text
        button_sizer.Add(feedback_text, 0, wx.ALL, 5)

        # Set notebook in a sizer to create the layout
        sizer = wx.FlexGridSizer(1, 2, 10)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(nb_sizer, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_BOTTOM, 5)
        panel.SetSizer(sizer)
        # sizer.Fit(self)

    def on_tab_change(self, event):
        """handles 'tab changed' event"""
        data_handler.update_all()

    def on_save(self, event):
        """handles 'save' event"""
        self.save()
        self.feedback("Saved Successfully.")

    def on_saveclose(self, event):
        """handles 'save and close' event"""
        self.save()
        self.close()

    def on_close(self, event):
        """handles 'close' event"""
        self.close()

    def save(self):
        """executes the save logic"""
        data_handler.update_all()
        data_handler.save_data(dataset=self.dataset)
        data_handler.refresh_ui()

    def close(self):
        """executes the close logic"""
        self.parent.Enable()
        self.parent.refresh_view()
        data_handler.current_window = None
        self.Destroy()

    def get_persons(self):
        """returns the list of persons held by the MetaDataSet"""
        return self.dataset.persons

    def get_organizations(self):
        """returns the list of organizations held by the MetaDataSet"""
        return self.dataset.organizations

    def feedback(self, msg, success=True):
        """gives feedback to user on action (eg. 'saved successfully')"""
        if success:
            self.feedback_text.SetForegroundColour(wx.Colour(50, 200, 50))
        else:
            self.feedback_text.SetForegroundColour(wx.Colour(200, 50, 50))
        self.feedback_text.SetLabel(msg)
        try:
            wx.CallLater(2500, lambda: self.feedback_text.SetLabel(''))
        except Exception:
            pass


class TabOne(wx.Panel):

    def __init__(self, parent: wx.Notebook, dataset: MetaDataSet):
        """Tab holding the project base information"""
        wx.Panel.__init__(self, parent)
        self.dataset = dataset

        # Project name as caption
        sizer = wx.GridBagSizer(10, 10)
        project_label = wx.StaticText(self, label="Current Project:")
        project_name = wx.StaticText(self, label=self.dataset.name)
        sizer.Add(project_label, pos=(0, 0))
        sizer.Add(project_name, pos=(0, 1))

        # Path to folder
        path_label = wx.StaticText(self, label="Path: ")
        sizer.Add(path_label, pos=(1, 0))
        path_field = wx.TextCtrl(self, style=wx.TE_READONLY, size=(550, -1))
        path_field.SetValue(self.dataset.path)
        sizer.Add(path_field, pos=(1, 1))
        path_help = wx.Button(self, label="?")
        path_help.Bind(wx.EVT_BUTTON, lambda event: self.show_help(event,
                                                                   "Path to the folder with the data",
                                                                   "/some/path/to/folder"))
        sizer.Add(path_help, pos=(1, 2))

        # Files
        files_label = wx.StaticText(self, label="Files: ")
        sizer.Add(files_label, pos=(2, 0))
        data_sizer = wx.BoxSizer()
        file_list = wx.ListBox(self, size=(550, -1))
        for f in dataset.files:
            file_list.Append(f)
        data_sizer.Add(file_list)
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        btn_add = wx.Button(self, label="Add File(s)")
        btn_add.Bind(wx.EVT_BUTTON, lambda event: self.add_file(
            dataset, file_list))
        btn_del = wx.Button(self, label="Remove Selected")
        btn_del.Bind(wx.EVT_BUTTON, lambda event: self.remove_file(
            dataset, file_list))
        button_sizer.Add(btn_add, flag=wx.EXPAND)
        button_sizer.Add(btn_del, flag=wx.EXPAND)
        data_sizer.Add(button_sizer)
        sizer.Add(data_sizer, pos=(2, 1))
        path_help = wx.Button(self, label="?")
        path_help.Bind(wx.EVT_BUTTON, lambda event: self.show_help(event,
                                                                   "Files associated with the project",
                                                                   "sample_project.zip"))
        sizer.Add(path_help, pos=(2, 2))
        sizer.AddGrowableCol(1)
        self.SetSizer(sizer)

    def show_help(self, evt, message: str, sample: str):
        """Handles events from 'help' button. Opens a help popup"""
        msg = f"Description:\n{message}\n\nExample:\n{sample}"
        win = HelpPopup(self, msg)
        btn = evt.GetEventObject()
        pos = btn.ClientToScreen((0, 0))
        sz = btn.GetSize()
        win.Position(pos, (0, sz[1]))
        win.Popup()

    def add_file(self, dataset: MetaDataSet, listbox: wx.ListBox):
        """Associate a file with project base data."""
        with wx.FileDialog(self, "Choose file(s):",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fd:
            if fd.ShowModal() == wx.ID_OK:
                for p in fd.GetPaths():
                    f = str(p)
                    if f.startswith(dataset.path):
                        f = f.replace(f'{dataset.path}/', '')
                    else:
                        continue
                    if f and f not in dataset.files:
                        dataset.files.append(f)
                        listbox.Append(f)

    def remove_file(self, dataset: MetaDataSet, file_list: wx.ListBox):
        """Removes a file from base information association."""
        selection = file_list.GetSelection()
        if selection >= 0:
            string_selected = file_list.GetString(selection)
            dataset.files.remove(string_selected)
            file_list.Delete(selection)


class DataTab(scrolledPanel.ScrolledPanel):

    def __init__(self, parent: wx.Notebook, metadataset: MetaDataSet, dataset: DataClass, title: str, multiple=False):
        """
        A Tab in the window displaying data.

        Args:
            parent (wx.Notebook): parent object in which the tab is placed.
            metadataset (MetaDataSet): the Metadataset to which the data belongs.
            dataset (DataClass): The data object to display.
            title (str): Title of the tab.
            multiple (bool, optional): Flag true, if there can be multiple instances of the DataClass in the Metadataset. Defaults to False.
        """
        scrolledPanel.ScrolledPanel.__init__(self, parent, -1)

        self.parent = parent
        self.dataset = dataset
        self.multiple = multiple
        self.metadataset = metadataset
        self.rows = []
        self.multiple_selection = 0
        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.FlexGridSizer(4, 10, 10)

        if dataset:
            ds = dataset
            if multiple:
                ds = self.active_dataset
            for i, prop in enumerate(ds.get_properties()):
                row = PropertyRow(self, prop, sizer, i, metadataset)
                self.rows.append(row)

        sizer.AddGrowableCol(1)

        if multiple:
            dataset_sizer = wx.BoxSizer()
            dataset_listbox = wx.ListBox(self, size=(200, -1))
            for ds in dataset:
                dataset_listbox.Append(str(ds))
            dataset_listbox.Bind(
                wx.EVT_LISTBOX, lambda e: self.change_selection(e))
            dataset_listbox.Select(0)
            self.multiple_listbox = dataset_listbox
            dataset_sizer.Add(dataset_listbox, wx.EXPAND)
            dataset_sizer.AddSpacer(5)
            button_sizer = wx.BoxSizer(wx.VERTICAL)
            button_add = wx.Button(self, label="Add New")
            button_add.Bind(wx.EVT_BUTTON, lambda e: self.add_object(
                e, dataset_listbox, title))
            button_sizer.Add(button_add, flag=wx.EXPAND)
            button_remove = wx.Button(self, label="Remove Selected")
            button_remove.Bind(
                wx.EVT_BUTTON, lambda e: self.remove_object(e, dataset_listbox))
            button_sizer.Add(button_remove)
            dataset_sizer.Add(button_sizer)
            outer_sizer.Add(dataset_sizer, flag=wx.EXPAND)
            outer_sizer.AddSpacer(20)
        outer_sizer.Add(sizer, flag=wx.EXPAND)
        self.SetSizer(outer_sizer)
        self.SetupScrolling(scroll_x=False, scroll_y=True)
        self.Fit()
        self.Layout()

    @property
    def active_dataset(self) -> DataClass:
        if self.multiple:
            return self.dataset[self.multiple_selection]
        else:
            return self.dataset

    def update_data(self):
        """Updates the data for all rows."""
        for row in self.rows:
            row.update_data()

    def refresh_ui(self):
        """Refreshes all UI components."""
        if self.multiple:
            self.multiple_listbox.SetItems([str(ds) for ds in self.dataset])
            if self.multiple_selection < 0:
                self.multiple_selection = len(self.multiple_listbox.GetItems()) - 1
            self.multiple_listbox.SetSelection(self.multiple_selection)
        for row in self.rows:
            row.refresh_ui()
        self.Layout()

    def add_object(self, event, listbox, title: str):
        """Adds an object (Person, Dataset, etc.) to the tab."""
        if title == "Person":
            self.metadataset.add_person()
        if title == "Dataset":
            self.metadataset.add_dataset()
        elif title == "Organization":
            self.metadataset.add_organization()
        elif title == "Grant":
            self.metadataset.add_grant()
        self.multiple_selection = -1
        data_handler.refresh_ui()

    def remove_object(self, event, listbox):
        """Removes an object (Person, Dataset, etc.) from the tab."""
        selection = listbox.GetSelection()
        if selection < 0:
            return
        if listbox.GetCount() > 1:
            self.multiple_selection = selection - 1
        s = listbox.GetStringSelection()
        self.metadataset.remove(self.metadataset.get_by_string(s))
        data_handler.refresh_ui()

    def change_selection(self, event):
        """Handles selection-change event."""
        sel = event.GetEventObject().GetSelection()
        data_handler.update_all()
        self.multiple_selection = sel
        data_handler.refresh_ui()

    def add_to_list(self, event, content_list: wx.ListBox, widget: Union[wx.Control, Tuple[wx.Control]], addable: Union[str, Tuple[str, str]]):
        """add an object to a list"""
        if not addable:  # is None
            return
        if isinstance(widget, tuple):  # Attribution, i.e. two inputs
            role = addable[0]
            agent = addable[1]
            if not role or not agent or \
                    role.isspace() or agent.isspace() or \
                    agent == "Select to add":
                print('invalid input')
                return
            for i in range(content_list.GetItemCount()):
                r = content_list.GetItem(i, 0).GetText()
                a = content_list.GetItem(i, 1).GetText()
                if r == role and a == agent:
                    print('Item already exists')
                    return
            content_list.Append((role, agent))
            self.reset_widget(widget)
        else:
            if str(addable).isspace() or \
                    addable == "Select to add" or \
                    str(addable) in content_list.GetStrings():
                self.reset_widget(widget)
                return
            content_list.Append(str(addable))
            self.reset_widget(widget)
        data_handler.update_all()

    def reset_widget(self, widget: Union[wx.Control, Tuple[wx.Control]]):
        """reset widget to an empty value"""
        if isinstance(widget, wx.StaticText) or \
                isinstance(widget, wx.TextCtrl):
            widget.SetValue('')
        elif isinstance(widget, wx.Choice):
            widget.SetSelection(0)
        elif isinstance(widget, tuple):
            for w in widget:
                self.reset_widget(w)

    def remove_from_list(self, event, content_list: Union[wx.ListBox, wx.ListCtrl]):
        """
        remove an object from a listbox.
        """
        if isinstance(content_list, wx.ListCtrl):
            selection = content_list.GetFirstSelected()
            if selection >= 0:
                content_list.DeleteItem(selection)
        else:
            selection = content_list.GetSelection()
            if selection >= 0:
                content_list.Delete(selection)
        data_handler.update_all()

    def show_help(self, evt, message: str, sample: str):
        """
        Show a help dialog
        """
        msg = f"Description:\n{message}\n\nExample:\n{sample}"
        win = HelpPopup(self, msg)
        btn = evt.GetEventObject()
        pos = btn.ClientToScreen((0, 0))
        sz = btn.GetSize()
        win.Position(pos, (0, sz[1]))
        win.Popup()

    def show_validity(self, evt, val: str, card: str):
        """
        Show a help dialog
        """
        msg = f"Validation Result:\n{val}\n\nExpected Cardinality:\n{card}"
        win = HelpPopup(self, msg)
        btn = evt.GetEventObject()
        pos = btn.ClientToScreen((0, 0))
        sz = btn.GetSize()
        win.Position(pos, (0, sz[1]))
        win.Popup()

    def pick_date(self, evt, label: wx.StaticText, prop: Property):
        """let user pick a date with date picker dialog"""
        with CalendarDlg(self, prop.name, label.GetLabel()) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                label.SetLabel(dlg.cal.Date.FormatISODate())
                data_handler.update_all()


class PropertyRow:

    def __init__(self, parent: DataTab, prop: Property, sizer: wx.FlexGridSizer, index: int, metadataset: MetaDataSet):
        """
        A row in a tab of the UI

        This Class organizes a single row in the data tabs.
        Upon initiation, the UI elements ara generated and placed.
        Later on, the data handler can let this class return the value that the property should be assigned.

        Args:
            parent (wx.ScrolledWindow): The scrolled panel in which the row is to be placed.
            prop (Property): The property to be displayed
            sizer (wx.Sizer): The sizer that organizes the layout of the parent component
            index (int): the row in the sizer grid
            metadataset (MetaDataSet): the MetaDataSet, to which the property belongs.
        """
        self.prop_name = prop.name
        self.metadataset = metadataset
        self.data_widget = None
        self.choice_widget = None
        self.parent = parent
        self.validity_msg = ""
        name_label = wx.StaticText(parent, label=prop.name + ": ")
        sizer.Add(name_label)
        if Datatype.is_string_like(prop.datatype):
            self.__setup_string(parent, sizer, prop)
        elif prop.datatype == Datatype.DATE:
            if prop.cardinality == Cardinality.ONE \
                    or prop.cardinality == Cardinality.ZERO_OR_ONE:
                inner_sizer = wx.BoxSizer()
                date = wx.StaticText(parent, size=(100, -1))
                pick_date_button = wx.Button(parent, label="Pick Date")
                pick_date_button.Bind(
                    wx.EVT_BUTTON, lambda event: parent.pick_date(event, date, prop))
                inner_sizer.Add(date)
                inner_sizer.Add(pick_date_button)
                sizer.Add(inner_sizer, flag=wx.EXPAND)
                self.data_widget = date
        elif prop.datatype == Datatype.PROJECT:
            txt = wx.StaticText(parent, label=str(prop.value))
            self.data_widget = txt
            sizer.Add(txt, flag=wx.EXPAND)
        elif Datatype.is_dropdownable(prop.datatype):
            self.__setup_dropdown(parent, sizer, prop)
        elif prop.datatype == Datatype.DATA_MANAGEMENT_PLAN:
            inner_sizer = wx.BoxSizer(wx.VERTICAL)
            cb = wx.CheckBox(parent, label='is available')
            cb.Bind(wx.EVT_CHECKBOX, lambda e: data_handler.update_all())
            inner_sizer.Add(cb, flag=wx.EXPAND)
            text = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
            text.SetHint('Optional URL')
            text.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer.Add(text, flag=wx.EXPAND)
            sizer.Add(inner_sizer, flag=wx.EXPAND)
            self.data_widget = [cb, text]
        elif prop.datatype == Datatype.ADDRESS:
            self.__setup_address(parent, sizer)
        elif prop.datatype == Datatype.ATTRIBUTION:
            self.__setup_attribution(parent, sizer)
        elif prop.datatype == Datatype.SHORTCODE:
            text = wx.StaticText(parent)
            self.data_widget = text
            sizer.Add(text, flag=wx.EXPAND)

        btn = wx.Button(parent, label="?")
        btn.Bind(wx.EVT_BUTTON, lambda event: parent.show_help(event, prop.description, prop.example))
        sizer.Add(btn)
        opt = wx.Button(parent, label=Cardinality.get_optionality_string(prop.cardinality))
        opt.Bind(wx.EVT_BUTTON, lambda event: parent.show_validity(event,
                                                                   self.validity_msg,
                                                                   Cardinality.as_sting(prop.cardinality)))
        self.validity_widget = opt
        sizer.Add(opt, flag=wx.RIGHT, border=5)
        self.refresh_ui()

    def __setup_string(self, parent: DataTab, sizer: wx.FlexGridSizer, prop: Property):
        """Set up UI form widgets for a string-like. Delegates to different cardinalities."""
        if prop.cardinality == Cardinality.ONE \
                or prop.cardinality == Cardinality.ZERO_OR_ONE:  # String or similar, exactly 1 or 0-1
            self.__setup_string_one_card(parent, sizer, prop)
        elif prop.cardinality == Cardinality.ONE_TO_TWO \
                or prop.cardinality == Cardinality.ZERO_TO_TWO:
            self.__setup_string_two_card(parent, sizer, prop)
        elif prop.cardinality == Cardinality.ONE_TO_UNBOUND \
                or prop.cardinality == Cardinality.ONE_TO_UNBOUND_ORDERED \
                or prop.cardinality == Cardinality.UNBOUND:  # String or similar, 1-n or 0-n
            self.__setup_string_multi_card(parent, sizer, prop)

    def __setup_string_multi_card(self, parent: DataTab, sizer: wx.FlexGridSizer, prop: Property):
        """Set up UI form widgets for a string-like with multi cardinality."""
        scroller = wx.lib.scrolledpanel.ScrolledPanel(parent)
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        if prop.multiline:
            inner_sizer = wx.BoxSizer()
            text_sizer = wx.BoxSizer(wx.VERTICAL)
            textcontrol = wx.TextCtrl(scroller, style=wx.TE_PROCESS_ENTER)
            text_sizer.Add(textcontrol, flag=wx.EXPAND)
            text_sizer.AddSpacer(5)
            content_list = wx.ListBox(scroller)
            textcontrol.Bind(wx.EVT_TEXT_ENTER,
                             lambda e: parent.add_to_list(e,
                                                          content_list,
                                                          textcontrol,
                                                          textcontrol.GetValue()))
            text_sizer.Add(content_list, 1, flag=wx.EXPAND)
            inner_sizer.Add(text_sizer, 1, flag=wx.EXPAND)
            inner_sizer.AddSpacer(5)
            button_sizer = wx.BoxSizer(wx.VERTICAL)
            plus_button = wx.Button(scroller, label="+")
            plus_button.Bind(wx.EVT_BUTTON,
                             lambda e: parent.add_to_list(e,
                                                          content_list,
                                                          textcontrol,
                                                          textcontrol.GetValue()))
            button_sizer.Add(plus_button, flag=wx.EXPAND)

            remove_button = wx.Button(scroller, label="Del Selected")
            remove_button.Bind(wx.EVT_BUTTON,
                               lambda event: parent.remove_from_list(event,
                                                                     content_list))
            button_sizer.Add(remove_button)
            inner_sizer.Add(button_sizer)
        else:
            inner_sizer = wx.BoxSizer()
            textcontrol = wx.TextCtrl(scroller, style=wx.TE_PROCESS_ENTER, size=(300, -1))
            textcontrol.Bind(wx.EVT_TEXT_ENTER,
                             lambda e: parent.add_to_list(e,
                                                          content_list,
                                                          textcontrol,
                                                          textcontrol.GetValue()))
            inner_sizer.Add(textcontrol, 0)
            inner_sizer.AddSpacer(5)
            button_sizer = wx.BoxSizer(wx.VERTICAL)
            plus_button = wx.Button(scroller, label="+")
            plus_button.Bind(wx.EVT_BUTTON,
                             lambda e: parent.add_to_list(e,
                                                          content_list,
                                                          textcontrol,
                                                          textcontrol.GetValue()))
            button_sizer.Add(plus_button, flag=wx.EXPAND)

            remove_button = wx.Button(scroller, label="Del Selected")
            remove_button.Bind(wx.EVT_BUTTON,
                               lambda event: parent.remove_from_list(event,
                                                                     content_list))
            button_sizer.Add(remove_button)
            inner_sizer.Add(button_sizer)
            inner_sizer.AddSpacer(5)
            content_list = wx.ListBox(scroller)
            inner_sizer.Add(content_list, 1, flag=wx.EXPAND)
        # sizer.Add(inner_sizer, flag=wx.EXPAND)
        scroll_sizer.Add(inner_sizer, flag=wx.EXPAND)
        scroller.Sizer = scroll_sizer
        scroller.SetupScrolling(scroll_x=True, scroll_y=False)
        sizer.Add(scroller, flag=wx.EXPAND)
        self.data_widget = content_list

    def __setup_string_two_card(self, parent: DataTab, sizer: wx.FlexGridSizer, prop: Property):
        """Set up UI form widgets for a string-like with two cardinality."""
        if prop.cardinality == Cardinality.ONE_TO_TWO:  # String or similar, 1-2
            inner_sizer = wx.BoxSizer(wx.VERTICAL)
            textcontrol1 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
            textcontrol1.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer.Add(textcontrol1, flag=wx.EXPAND)
            inner_sizer.AddSpacer(5)
            textcontrol2 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
            textcontrol2.SetHint('Second value is optional')
            textcontrol2.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer.Add(textcontrol2, flag=wx.EXPAND)
            sizer.Add(inner_sizer, flag=wx.EXPAND)
            self.data_widget = [textcontrol1, textcontrol2]
        elif prop.cardinality == Cardinality.ZERO_TO_TWO:  # String or similar, 0-2
            inner_sizer = wx.BoxSizer(wx.VERTICAL)
            textcontrol1 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
            textcontrol1.SetHint('Optional')
            textcontrol1.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer.Add(textcontrol1, flag=wx.EXPAND)
            inner_sizer.AddSpacer(5)
            textcontrol2 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
            textcontrol2.SetHint('Optional')
            textcontrol2.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
            inner_sizer.Add(textcontrol2, flag=wx.EXPAND)
            sizer.Add(inner_sizer, flag=wx.EXPAND)
            self.data_widget = [textcontrol1, textcontrol2]

    def __setup_string_one_card(self, parent: DataTab, sizer: wx.FlexGridSizer, prop: Property):
        """Set up UI form widgets for a string-like with single cardinality."""
        scroller = wx.lib.scrolledpanel.ScrolledPanel(parent)
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        if prop.multiline:
            textcontrol = wx.TextCtrl(scroller, style=wx.TE_MULTILINE)
        else:
            textcontrol = wx.TextCtrl(scroller, style=wx.TE_PROCESS_ENTER)
            textcontrol.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
        scroll_sizer.Add(textcontrol, flag=wx.EXPAND)
        scroller.Sizer = scroll_sizer
        scroller.SetupScrolling(scroll_x=True, scroll_y=False)
        sizer.Add(scroller, flag=wx.EXPAND)
        # sizer.Add(textcontrol, flag=wx.EXPAND)
        self.data_widget = textcontrol

    def __setup_dropdown(self, parent: DataTab, sizer: wx.FlexGridSizer, prop: Property):
        """Set up dropdown widget"""
        if prop.cardinality == Cardinality.ZERO_OR_ONE \
                or prop.cardinality == Cardinality.ONE:
            choice = wx.Choice(parent, size=(400, -1))
            choice.Bind(wx.EVT_CHOICE, lambda e: self.onValueChange(e, False))
            self.data_widget = choice
            self.choice_widget = choice
            sizer.Add(choice, flag=wx.EXPAND)
        if prop.cardinality == Cardinality.ONE_TO_UNBOUND or \
                prop.cardinality == Cardinality.UNBOUND:
            scroller = scrolledPanel.ScrolledPanel(parent)
            inner_sizer = wx.BoxSizer()
            box = wx.ListBox(scroller, size=(400, -1))
            self.data_widget = box
            inner_sizer.Add(box, 1)
            control_sizer = wx.BoxSizer(wx.VERTICAL)
            choice = wx.Choice(scroller, size=(150, -1))
            choice.Bind(wx.EVT_CHOICE,
                        lambda e: parent.add_to_list(e, box, choice,
                                                     choice.GetStringSelection()))
            self.choice_widget = choice
            control_sizer.Add(choice)
            remove_button = wx.Button(scroller, label="Del Selected")
            remove_button.Bind(wx.EVT_BUTTON, lambda event: parent.remove_from_list(event, box))
            control_sizer.Add(remove_button)
            inner_sizer.Add(control_sizer)
            scroller.Sizer = inner_sizer
            scroller.SetupScrolling(scroll_x=True, scroll_y=False)
            sizer.Add(scroller, flag=wx.EXPAND)

    def __setup_address(self, parent: DataTab, sizer: wx.FlexGridSizer):
        """Set up widgets for address."""
        inner_sizer = wx.BoxSizer(wx.VERTICAL)
        text1 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
        text1.SetHint('Street')
        text1.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
        inner_sizer.Add(text1, flag=wx.EXPAND)
        text2 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
        text2.SetHint('Postal Code')
        text2.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
        inner_sizer2 = wx.BoxSizer()
        inner_sizer2.Add(text2, 2)
        inner_sizer2.AddSpacer(5)
        text3 = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
        text3.SetHint('Locality')
        text3.Bind(wx.EVT_TEXT_ENTER, self.onValueChange)
        inner_sizer2.Add(text3, 10)
        inner_sizer.AddSpacer(5)
        inner_sizer.Add(inner_sizer2, flag=wx.EXPAND)
        sizer.Add(inner_sizer, flag=wx.EXPAND)
        self.data_widget = [text1, text2, text3]

    def __setup_attribution(self, parent: DataTab, sizer: wx.FlexGridSizer):
        """Set up widgets for attribution."""
        scroller = scrolledPanel.ScrolledPanel(parent)
        inner_sizer = wx.BoxSizer()
        input_sizer = wx.BoxSizer(wx.VERTICAL)
        textcontrol = wx.TextCtrl(scroller, style=wx.TE_PROCESS_ENTER, size=(200, -1))
        textcontrol.SetHint("Role")
        input_sizer.Add(textcontrol)
        choice = wx.Choice(scroller, size=(200, -1))
        choice.SetToolTip("Add a Person or Organization")
        self.choice_widget = choice
        input_sizer.Add(choice)
        inner_sizer.Add(input_sizer)
        inner_sizer.AddSpacer(5)
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        plus_button = wx.Button(scroller, label="+")
        button_sizer.Add(plus_button, flag=wx.EXPAND)
        remove_button = wx.Button(scroller, label="Del Selected")
        button_sizer.Add(remove_button)
        inner_sizer.Add(button_sizer)
        inner_sizer.AddSpacer(5)
        content_list = wx.ListCtrl(scroller, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        content_list.InsertColumn(0, 'Role')
        content_list.InsertColumn(1, 'Agent')
        inner_sizer.Add(content_list, 1)
        scroller.Sizer = inner_sizer
        scroller.SetupScrolling(scroll_x=True, scroll_y=False)
        sizer.Add(scroller, flag=wx.EXPAND)
        self.data_widget = content_list
        remove_button.Bind(wx.EVT_BUTTON,
                           lambda event: parent.remove_from_list(event,
                                                                 content_list))
        plus_button.Bind(wx.EVT_BUTTON,
                         lambda e: parent.add_to_list(e,
                                                      content_list,
                                                      (textcontrol, choice),
                                                      (textcontrol.GetValue(), choice.GetStringSelection())))

    @property
    def data_class(self):
        return self.parent.active_dataset

    @property
    def prop(self) -> Property:
        return self.data_class.get_prop_by_name(self.prop_name)

    def update_data(self):
        """Update data according to the value that is currently in the UI."""
        self.prop.value = self.get_value()

    def get_value(self):
        """
        Returns the new property value that has been entered to the UI
        """
        datatype = self.prop.datatype
        cardinality = self.prop.cardinality
        # String or String/URL etc.
        if Datatype.is_string_like(datatype):
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                return self.data_widget.GetValue().strip()
            if cardinality == Cardinality.ONE_TO_TWO \
                    or cardinality == Cardinality.ZERO_TO_TWO:
                return [self.data_widget[0].GetValue().strip(),
                        self.data_widget[1].GetValue().strip()]
            if cardinality == Cardinality.ONE_TO_UNBOUND \
                    or cardinality == Cardinality.ONE_TO_UNBOUND_ORDERED \
                    or cardinality == Cardinality.UNBOUND:
                return [s.strip() for s in self.data_widget.GetStrings()]
        elif datatype == Datatype.DATE:
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                return self.data_widget.GetLabel()
        elif datatype == Datatype.PERSON_OR_ORGANIZATION or \
                datatype == Datatype.PERSON or \
                datatype == Datatype.ORGANIZATION:
            if cardinality == Cardinality.ZERO_OR_ONE:
                selection = self.data_widget.GetSelection()
                if selection < 0:
                    selection = 0
                string = self.data_widget.GetString(selection)
                return self.metadataset.get_by_string(string)
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                strs = self.data_widget.GetStrings()
                objs = [self.metadataset.get_by_string(s) for s in strs]
                return objs
            if cardinality == Cardinality.UNBOUND:
                strs = self.data_widget.GetStrings()
                objs = [self.metadataset.get_by_string(s) for s in strs]
                return objs
        elif datatype == Datatype.DATA_MANAGEMENT_PLAN:
            return (
                self.data_widget[0].GetValue(),
                self.data_widget[1].GetValue().strip(),
            )
        elif datatype == Datatype.PROJECT:
            return self.metadataset.project
        elif datatype == Datatype.ADDRESS:
            return (
                self.data_widget[0].GetValue().strip(),
                self.data_widget[1].GetValue().strip(),
                self.data_widget[2].GetValue().strip(),
            )
        elif datatype == Datatype.CONTROLLED_VOCABULARY:
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                return self.data_widget.GetStrings()
            elif cardinality == Cardinality.ONE:
                sel = self.data_widget.GetSelection()
                if sel >= 0:
                    s = self.data_widget.GetString(sel)
                    if s in self.prop.value_options:
                        return s
                    else:
                        return ""
                else:
                    return ""
        elif datatype == Datatype.GRANT:
            if cardinality == Cardinality.UNBOUND:
                strs = self.data_widget.GetStrings()
                objs = [self.metadataset.get_by_string(s) for s in strs]
                return objs
        elif datatype == Datatype.ATTRIBUTION:
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                w = self.data_widget
                res = []
                for i in range(w.GetItemCount()):
                    t = w.GetItem(i, 0).GetText()
                    o = self.metadataset.get_by_string(w.GetItem(i, 1).GetText())
                    if t and not t.isspace() and o:
                        res.append((t, o,))
                return res
        elif datatype == Datatype.SHORTCODE:
            return self.data_widget.GetLabel()
        print(f"Couldn't find a type here... weird... {datatype}")
        return "Couldn't find my value... sorry"

    def refresh_ui(self):
        """Update the value in the UI according to what is stored in the property (delegator)."""
        self.set_value(self.prop.value)
        if self.choice_widget:
            self.refresh_choice()
        self.validate()

    def refresh_choice(self):
        """Update dropdown menu according to currently available options."""
        options = []
        if self.prop.datatype == Datatype.GRANT:
            options = self.metadataset.grants
        elif self.prop.datatype == Datatype.PERSON:
            options = self.metadataset.persons
        elif self.prop.datatype == Datatype.CONTROLLED_VOCABULARY:
            options = self.prop.value_options
        elif self.prop.datatype == Datatype.ORGANIZATION:
            options = self.metadataset.organizations
        elif self.prop.datatype == Datatype.PERSON_OR_ORGANIZATION or \
                self.prop.datatype == Datatype.ATTRIBUTION:
            options = self.metadataset.persons + self.metadataset.organizations
        options_strs = ["Select to add"] + [str(o) for o in options]
        self.choice_widget.SetItems(options_strs)
        if self.choice_widget == self.data_widget:
            self.set_value(self.prop.value)

    def validate(self):
        """validate current value and display the result in the UI."""
        widget = self.validity_widget
        res, msg = self.prop.validate()
        if res == Validity.VALID:
            widget.SetForegroundColour(wx.Colour(30, 170, 30))
        elif res == Validity.INVALID_VALUE:
            widget.SetForegroundColour(wx.Colour(170, 30, 30))
        elif res == Validity.REQUIRED_VALUE_MISSING:
            widget.SetForegroundColour(wx.Colour(170, 30, 30))
        elif res == Validity.OPTIONAL_VALUE_MISSING:
            widget.SetForegroundColour(wx.NullColour)
        elif res == Validity.UNDEFINED:
            widget.SetBackgroundColour(wx.Colour(255, 0, 0))
            widget.SetForegroundColour(wx.Colour(0, 0, 0))
        self.validity_msg = msg

    def set_value(self, val):
        """Update the value in the UI according to what is stored in the property."""
        datatype = self.prop.datatype
        cardinality = self.prop.cardinality
        undefined = False
        if not val:
            undefined = True
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                val = ""
            elif cardinality == Cardinality.ONE_TO_TWO \
                    or cardinality == Cardinality.ZERO_TO_TWO:
                val = ("", "",)
            else:
                val = []
        # String or String/URL etc.
        if datatype == Datatype.STRING \
                or datatype == Datatype.STRING_OR_URL \
                or datatype == Datatype.URL \
                or datatype == Datatype.EMAIL \
                or datatype == Datatype.DOWNLOAD \
                or datatype == Datatype.PLACE:
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                self.data_widget.SetValue(val)
            if cardinality == Cardinality.ONE_TO_TWO \
                    or cardinality == Cardinality.ZERO_TO_TWO:
                self.data_widget[0].SetValue(val[0])
                self.data_widget[1].SetValue(val[1])
            if cardinality == Cardinality.ONE_TO_UNBOUND \
                    or cardinality == Cardinality.ONE_TO_UNBOUND_ORDERED \
                    or cardinality == Cardinality.UNBOUND:
                self.data_widget.SetItems(val)
        elif datatype == Datatype.DATE:
            if cardinality == Cardinality.ONE \
                    or cardinality == Cardinality.ZERO_OR_ONE:
                self.data_widget.SetLabel(val)
        elif datatype == Datatype.PROJECT:
            self.data_widget.SetLabel(str(val))
        elif datatype == Datatype.CONTROLLED_VOCABULARY or \
                datatype == Datatype.GRANT or \
                datatype == Datatype.PERSON_OR_ORGANIZATION or \
                datatype == Datatype.PERSON or \
                datatype == Datatype.ORGANIZATION:
            if cardinality == Cardinality.ZERO_OR_ONE \
                    or cardinality == Cardinality.ONE:
                self.data_widget.SetSelection(
                    self.data_widget.FindString(str(val)))
            if cardinality == Cardinality.ONE_TO_UNBOUND:
                self.data_widget.SetItems([str(v) for v in val])
            if cardinality == Cardinality.UNBOUND:
                self.data_widget.SetItems([str(v) for v in val])
        elif datatype == Datatype.DATA_MANAGEMENT_PLAN:
            if undefined:
                val = (False, "",)
            self.data_widget[0].SetValue(val[0])
            self.data_widget[1].SetValue(val[1])
        elif datatype == Datatype.ADDRESS:
            if undefined:
                val = ("", "", "",)
            self.data_widget[0].SetValue(val[0])
            self.data_widget[1].SetValue(val[1])
            self.data_widget[2].SetValue(val[2])
        elif datatype == Datatype.ATTRIBUTION:
            if undefined:
                val = [("", "",)]
            self.data_widget.DeleteAllItems()
            for v in val:
                self.data_widget.Append((v[0], str(v[1])))
                self.data_widget.SetColumnWidth(0, -1)
                self.data_widget.SetColumnWidth(1, -1)
        elif datatype == Datatype.SHORTCODE:
            return self.data_widget.SetLabel(val)

    def onValueChange(self, event, navigate: bool = True):
        data_handler.update_all()
        if navigate:
            event.GetEventObject().Navigate()


class HelpPopup(wx.PopupTransientWindow):
    def __init__(self, parent: Union[DataTab, TabOne], msg: str):
        """
        This class provides a help message
        Args:
            parent (object): the parent class
            msg (str): the help text with examples
        """
        wx.PopupTransientWindow.__init__(self, parent)
        panel = wx.Panel(self)
        st = wx.StaticText(panel, -1, msg)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, 0, wx.ALL, 5)
        panel.SetSizer(sizer)
        sizer.Fit(panel)
        sizer.Fit(self)
        self.Layout()


class CalendarDlg(wx.Dialog):
    def __init__(self, parent: DataTab, title: str, date_str: str):
        """A calendar picker dialog."""
        wx.Dialog.__init__(self, parent, title=title)
        panel = wx.Panel(self, -1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)

        date = wx.DateTime()
        date.ParseDate(date_str)
        cal = wx.adv.GenericCalendarCtrl(panel, date=date)

        if sys.platform != 'win32':
            # gtk truncates the year - this fixes it
            w, h = cal.Size
            cal.Size = (w + 15, h + 85)
            cal.MinSize = cal.Size

        sizer.Add(cal, 0)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add((0, 0), 1)
        btn_ok = wx.Button(panel, wx.ID_OK)
        btn_ok.SetDefault()
        button_sizer.Add(btn_ok, 0, wx.ALL, 2)
        button_sizer.Add((0, 0), 1)
        btn_can = wx.Button(panel, wx.ID_CANCEL)
        button_sizer.Add(btn_can, 0, wx.ALL, 2)
        button_sizer.Add((0, 0), 1)
        sizer.Add(button_sizer, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Fit(panel)
        self.ClientSize = panel.Size

        cal.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        cal.SetFocus()
        self.cal = cal

    def on_key_down(self, evt):
        code = evt.KeyCode
        if code == wx.WXK_TAB:
            self.cal.Navigate()
        elif code in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.EndModal(wx.ID_OK)
        elif code == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)
        else:
            evt.Skip()


class JSONConverterDialog(wx.Dialog):
    """Dialog that lets the user select which files to convert to the new metadata format in json."""
    class InType:
        SINGLE_FILE = 0
        MULTI_FILE = 1
        DIRECTORY = 2

    def __init__(self, *args, **kw):
        """Create a new Converter Dialog.

        Subclass of wx.Dialog.

        Should be displayed with `.ShowModal()`
        """
        super(JSONConverterDialog, self).__init__(*args, **kw)
        self.__in_files = None
        self.__out_dir = None
        self.Size = ((800, 650))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(panel, label="The DSP Metadata GUI tool models project metadata " +
                             "according to the first iteration of DSP Metadata, " +
                             "and produces RDF data (serialized as turtle, XML and JSON-LD).\n\n" +
                             "The second iteration introduced major changes in the data model, " +
                             "which proved to be breaking.\n\n" +
                             "This converter allows to convert metadata from a .ttl file in the old model to the new model " +
                             "requiring minimal manual work.\n\n" +
                             "Some places will definitely require manual work, these are marked with `XX` in the data " +
                             "so that they are easy to find.\n\n" +
                             "It is advisable however, to check all data thoroughly to ensure they are correct.")
        text.Wrap(780)
        box.Add(text, 0, wx.ALL | wx.EXPAND, 7)
        box.Add(wx.StaticLine(panel, -1), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        # Input
        input_panel = wx.Panel(panel)
        in_box = wx.BoxSizer(wx.VERTICAL)
        txt_in_header = wx.StaticText(input_panel, label="Select Input for Conversion:")
        in_box.Add(txt_in_header, 0, wx.ALL | wx.EXPAND, 7)
        input_panel.SetSizer(in_box)
        box.Add(input_panel, 0, wx.ALL | wx.EXPAND, 7)
        buttons_panel = wx.Panel(input_panel)
        btns_box = wx.BoxSizer(wx.HORIZONTAL)
        buttons_panel.SetSizer(btns_box)
        in_file_btn = wx.Button(buttons_panel, label="Single File")
        btns_box.Add(in_file_btn, 1, wx.ALL, 7)
        in_files_btn = wx.Button(buttons_panel, label="Multiple Files")
        btns_box.Add(in_files_btn, 1, wx.ALL, 7)
        in_dir_btn = wx.Button(buttons_panel, label="Directory (Bulk Transform)")
        btns_box.Add(in_dir_btn, 1, wx.ALL, 7)
        in_box.Add(buttons_panel, 0, wx.ALL | wx.EXPAND, 7)
        in_lbl = wx.StaticText(input_panel, label="No Input Selected")
        in_lbl.SetMinSize((200, 80))
        in_box.Add(in_lbl, 0, wx.ALL | wx.EXPAND, 7)
        box.Add(wx.StaticLine(panel, -1), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        in_file_btn.Bind(wx.EVT_BUTTON, lambda x: self._on_select_input(in_lbl, JSONConverterDialog.InType.SINGLE_FILE))
        in_files_btn.Bind(wx.EVT_BUTTON, lambda x: self._on_select_input(in_lbl, JSONConverterDialog.InType.MULTI_FILE))
        in_dir_btn.Bind(wx.EVT_BUTTON, lambda x: self._on_select_input(in_lbl, JSONConverterDialog.InType.DIRECTORY))
        # Output
        output_panel = wx.Panel(panel)
        out_box = wx.BoxSizer(wx.VERTICAL)
        txt_out_header = wx.StaticText(output_panel, label="Select Output Directory for Conversion:")
        out_box.Add(txt_out_header, 0, wx.ALL | wx.EXPAND, 7)
        out_btn = wx.Button(output_panel, label="Output Directory")
        out_box.Add(out_btn, 0, wx.ALL, 7)
        out_path_lbl = wx.StaticText(output_panel, label="No Output Directory Selected")
        out_box.Add(out_path_lbl, 0, wx.ALL | wx.EXPAND, 7)
        out_btn.Bind(wx.EVT_BUTTON, lambda x: self._on_select_output(out_path_lbl))
        output_panel.SetSizer(out_box)
        box.Add(output_panel, 0, wx.ALL | wx.EXPAND, 7)
        box.Add(wx.StaticLine(panel, -1), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        # Run Conversion
        self.btn_convert = wx.Button(panel, label="Convert")
        self.btn_convert.Bind(wx.EVT_BUTTON, lambda x: self._run_conversion())
        box.Add(self.btn_convert, 0, wx.ALL | wx.EXPAND, 7)
        panel.SetSizer(box)
        self._refresh()

    def _run_conversion(self):
        """Button `Convert` has been clicked."""
        if self.__in_files:
            print(f'saving to: {self.__out_dir}')
            res = converter.convert_and_save(self.__in_files, self.__out_dir)
            print(f"Converted: {res} files")
            open_file(self.__out_dir)

    def _on_select_output(self, label: wx.StaticText):
        """Select output/target directory by opening a DirDialog."""
        with wx.DirDialog(self, "Select Output Folder") as dirDialog:
            res = dirDialog.ShowModal()
            if res == wx.ID_OK:
                self.__out_dir = dirDialog.GetPath()
                label.SetLabel(self.__out_dir)
            else:
                self.__out_dir = None
                label.SetLabel("No Output Directory Selected")
        self._refresh()

    def _on_select_input(self, label: wx.StaticText, mode):
        """Select input file(s) by opening FileDialog/DirDialog, depending on the selected mode."""
        if mode == JSONConverterDialog.InType.SINGLE_FILE:
            with wx.FileDialog(self, "Select Input File", wildcard="*.ttl") as fileDialog:
                res = fileDialog.ShowModal()
                if res == wx.ID_OK:
                    path = fileDialog.GetPath()
                    self.__in_files = [path]
                    label.SetLabel(str(self.__in_files))
        elif mode == JSONConverterDialog.InType.MULTI_FILE:
            with wx.FileDialog(self, "Select Input Files", style=wx.FD_MULTIPLE, wildcard="*.ttl") as fileDialog:
                res = fileDialog.ShowModal()
                if res == wx.ID_OK:
                    paths = fileDialog.GetPaths()
                    self.__in_files = paths
                    if len(self.__in_files) < 6:
                        label.SetLabel("\n".join(self.__in_files))
                    else:
                        label.SetLabel(f"Selected files: {len(self.__in_files)}")
        elif mode == JSONConverterDialog.InType.DIRECTORY:
            with wx.DirDialog(self, "Select Input File") as dirDialog:
                res = dirDialog.ShowModal()
                if res == wx.ID_OK:
                    path = dirDialog.GetPath()
                    files = glob(f'{path}/*.ttl')
                    self.__in_files = files
                    if len(self.__in_files) < 6:
                        label.SetLabel("\n".join(self.__in_files))
                    else:
                        label.SetLabel(f"Selected files: {len(self.__in_files)}")
        self._refresh()

    def _refresh(self):
        if self.__in_files and self.__out_dir:
            self.btn_convert.Enable()
        else:
            self.btn_convert.Disable()


class RDFConverterDialog(wx.Dialog):
    """Dialog that lets the user select which files to convert from json to RDF in the new data format."""
    class InType:
        SINGLE_FILE = 0
        MULTI_FILE = 1
        DIRECTORY = 2

    def __init__(self, *args, **kw):
        """Create a new Converter Dialog.

        Subclass of wx.Dialog.

        Should be displayed with `.ShowModal()`
        """
        super(RDFConverterDialog, self).__init__(*args, **kw)
        self.__in_files = None
        self.__out_dir = None
        self.Size = ((800, 650))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(panel,
                             label="This requires metadata converted to JSON already. (See menu 'option' > 'Convert RDF to JSON')\n\n" +
                             "First, clean up the JSON data. Once this is sound and finished, it can be converted to RDF here.")
        text.Wrap(780)
        box.Add(text, 0, wx.ALL | wx.EXPAND, 7)
        box.Add(wx.StaticLine(panel, -1), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        # Input
        input_panel = wx.Panel(panel)
        in_box = wx.BoxSizer(wx.VERTICAL)
        txt_in_header = wx.StaticText(input_panel, label="Select Input for Conversion:")
        in_box.Add(txt_in_header, 0, wx.ALL | wx.EXPAND, 7)
        input_panel.SetSizer(in_box)
        box.Add(input_panel, 0, wx.ALL | wx.EXPAND, 7)
        buttons_panel = wx.Panel(input_panel)
        btns_box = wx.BoxSizer(wx.HORIZONTAL)
        buttons_panel.SetSizer(btns_box)
        in_file_btn = wx.Button(buttons_panel, label="Single File")
        btns_box.Add(in_file_btn, 1, wx.ALL, 7)
        in_files_btn = wx.Button(buttons_panel, label="Multiple Files")
        btns_box.Add(in_files_btn, 1, wx.ALL, 7)
        in_dir_btn = wx.Button(buttons_panel, label="Directory (Bulk Transform)")
        btns_box.Add(in_dir_btn, 1, wx.ALL, 7)
        in_box.Add(buttons_panel, 0, wx.ALL | wx.EXPAND, 7)
        in_lbl = wx.StaticText(input_panel, label="No Input Selected")
        in_lbl.SetMinSize((200, 80))
        in_box.Add(in_lbl, 0, wx.ALL | wx.EXPAND, 7)
        box.Add(wx.StaticLine(panel, -1), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        in_file_btn.Bind(wx.EVT_BUTTON, lambda x: self._on_select_input(in_lbl, RDFConverterDialog.InType.SINGLE_FILE))
        in_files_btn.Bind(wx.EVT_BUTTON, lambda x: self._on_select_input(in_lbl, RDFConverterDialog.InType.MULTI_FILE))
        in_dir_btn.Bind(wx.EVT_BUTTON, lambda x: self._on_select_input(in_lbl, RDFConverterDialog.InType.DIRECTORY))
        # Output
        output_panel = wx.Panel(panel)
        out_box = wx.BoxSizer(wx.VERTICAL)
        txt_out_header = wx.StaticText(output_panel, label="Select Output Directory for Conversion:")
        out_box.Add(txt_out_header, 0, wx.ALL | wx.EXPAND, 7)
        out_btn = wx.Button(output_panel, label="Output Directory")
        out_box.Add(out_btn, 0, wx.ALL, 7)
        out_path_lbl = wx.StaticText(output_panel, label="No Output Directory Selected")
        out_box.Add(out_path_lbl, 0, wx.ALL | wx.EXPAND, 7)
        out_btn.Bind(wx.EVT_BUTTON, lambda x: self._on_select_output(out_path_lbl))
        output_panel.SetSizer(out_box)
        box.Add(output_panel, 0, wx.ALL | wx.EXPAND, 7)
        box.Add(wx.StaticLine(panel, -1), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)
        # Run Conversion
        self.btn_convert = wx.Button(panel, label="Convert")
        self.btn_convert.Bind(wx.EVT_BUTTON, lambda x: self._run_conversion())
        box.Add(self.btn_convert, 0, wx.ALL | wx.EXPAND, 7)
        panel.SetSizer(box)
        self._refresh()

    def _run_conversion(self):
        """Button `Convert` has been clicked."""
        if self.__in_files:
            print(f'saving to: {self.__out_dir}')
            res = rdfConverter.convert_and_save(self.__in_files, self.__out_dir)
            print(f"Converted: {res} files")
            open_file(self.__out_dir)

    def _on_select_output(self, label: wx.StaticText):
        """Select output/target directory by opening a DirDialog."""
        with wx.DirDialog(self, "Select Output Folder") as dirDialog:
            res = dirDialog.ShowModal()
            if res == wx.ID_OK:
                self.__out_dir = dirDialog.GetPath()
                label.SetLabel(self.__out_dir)
            else:
                self.__out_dir = None
                label.SetLabel("No Output Directory Selected")
        self._refresh()

    def _on_select_input(self, label: wx.StaticText, mode):
        """Select input file(s) by opening FileDialog/DirDialog, depending on the selected mode."""
        if mode == JSONConverterDialog.InType.SINGLE_FILE:
            with wx.FileDialog(self, "Select Input File", wildcard="*.json") as fileDialog:
                res = fileDialog.ShowModal()
                if res == wx.ID_OK:
                    path = fileDialog.GetPath()
                    self.__in_files = [path]
                    label.SetLabel(str(self.__in_files))
        elif mode == JSONConverterDialog.InType.MULTI_FILE:
            with wx.FileDialog(self, "Select Input Files", style=wx.FD_MULTIPLE, wildcard="*.json") as fileDialog:
                res = fileDialog.ShowModal()
                if res == wx.ID_OK:
                    paths = fileDialog.GetPaths()
                    self.__in_files = paths
                    if len(self.__in_files) < 6:
                        label.SetLabel("\n".join(self.__in_files))
                    else:
                        label.SetLabel(f"Selected files: {len(self.__in_files)}")
        elif mode == JSONConverterDialog.InType.DIRECTORY:
            with wx.DirDialog(self, "Select Input File") as dirDialog:
                res = dirDialog.ShowModal()
                if res == wx.ID_OK:
                    path = dirDialog.GetPath()
                    files = glob(f'{path}/*.json')
                    self.__in_files = files
                    if len(self.__in_files) < 6:
                        label.SetLabel("\n".join(self.__in_files))
                    else:
                        label.SetLabel(f"Selected files: {len(self.__in_files)}")
        self._refresh()

    def _refresh(self):
        if self.__in_files and self.__out_dir:
            self.btn_convert.Enable()
        else:
            self.btn_convert.Disable()


if __name__ == '__main__':
    collectMetadata()
