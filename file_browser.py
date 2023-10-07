import tkinter
import tkinter.filedialog

class FileBrowser:
    def prompt_file():
        top = tkinter.Tk()
        top.withdraw()  # hide window
        filetypes = (
                            ('maps', '*.txt'),
                            ('All files', '*.*')
                        )
        file_name = tkinter.filedialog.askopenfilename(parent=top, filetypes=filetypes)
        top.destroy()
        return file_name

    def prompt_savepath():
        top = tkinter.Tk()
        top.withdraw()  # hide window
        file_path = tkinter.filedialog.asksaveasfilename(defaultextension='.txt', initialfile = 'my_map')
        top.destroy()
        return file_path