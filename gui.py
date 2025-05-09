import tkinter as tk
from hsk import get_hsk_data, create_quiz, strip_tones, on_configure, on_mousewheel



class Gui(tk.Tk):
    # Main application window for the app
    
    def __init__(self) -> None:
        super().__init__()
        
        self.data = [
            get_hsk_data(1),
            get_hsk_data(2),
            get_hsk_data(3),
            get_hsk_data(4),
        ]

        self.title('HSK')
        self.geometry('600x500')
        self.resizable(False, False)

        tk.Label(self, text='HSK\n汉语水平考试\n(Hànyǔ Shuǐpíng Kǎoshì)', font=("Sans", 40)).pack(pady=50)
        
        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(pady=20)
        self.center_frame = tk.Frame(self.btn_frame)
        self.center_frame.pack(anchor='center')

        tk.Button(self.center_frame, text='Word Lists', width=10, height=2, command=self.open_wordlists).pack(side='left', padx=5)
        tk.Button(self.center_frame, text='Quiz', width=10, height=2, command=self.open_quiz).pack(side='left', padx=5)

    def open_wordlists(self) -> None:
        # opens wordlists window
        HSKMenu(self, 'wordlists', self.data)
    
    def open_quiz(self) -> None:
        # opens quiz window
        HSKMenu(self, 'quiz', self.data)

class HSKMenu(tk.Toplevel):
    # window for selecting hsk level for wordlists or quiz
    def __init__(self, parent, mode, data) -> None:
        super().__init__(parent)

        self.geometry('600x500')
        self.resizable(False, False)
        self.mode = mode
        self.data = data
        self.create_hsk_level_buttons()
    
    def create_hsk_level_buttons(self) -> None:
        # shows buttons 1-4 depending on selected mode
        mode_text = 'Word Lists' if self.mode == 'wordlists' else 'Quiz'
        tk.Label(self, text=f'HSK 1-4 ({mode_text})', font=('Sans', 40)).pack(pady=30)

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(pady=20)
        self.center_frame = tk.Frame(self.btn_frame)
        self.center_frame.pack(anchor='center')

        #anonymous function to create buttons
        for lvl in range(1,5):                                                          
            if self.mode == 'wordlists':
                tk.Button(self.center_frame, text=f'HSK {lvl}',font='Sans',
                    command=lambda l = lvl: self.wordlists_window(l)).pack(side='left', padx=5)
            elif self.mode =='quiz':
                tk.Button(self.center_frame, text=f'HSK {lvl}', font='Sans',
                    command=lambda l = lvl: self.quiz_window(l)).pack(side='left', padx=5)
    
    def wordlists_window(self, level) -> None:
        # displays a scrollable wordlist depending on the selected level 
        window = tk.Toplevel(self)
        window.title('HSK - Word Lists')
        window.geometry("1600x900")

        container = tk.Frame(window)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        scrollable_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        scrollable_frame.bind('<Configure>', on_configure(canvas))
        canvas.bind_all('<MouseWheel>', on_mousewheel(canvas))

        headers = ['','Simplified', 'Traditional', 'Tone', 'Pinyin', 'Definition']
        for col, header in enumerate(headers):
            tk.Label(scrollable_frame, text=header, font=('Sans', 24, 'bold'),
                padx=5, pady=5
            ).grid(row=1, column=col, sticky='nw')

        hsk_data = self.data[level - 1]
        num_rows = len(hsk_data['simplified'])

        for i in range(num_rows):
            tk.Label(scrollable_frame, text=f'{i + 1}', font=('Sans', 18),
                padx=5, pady=5).grid(row=i+2, column=0, sticky='nw')
            tk.Label(scrollable_frame, text=hsk_data['simplified'][i], font=('Sans', 18),
                padx=5, pady=5).grid(row=i+2, column=1, sticky='nw')
            tk.Label(scrollable_frame, text=hsk_data['traditional'][i], font=('Sans', 18),
                padx=5, pady=5).grid(row=i+2, column=2, sticky='nw')
            tk.Label(scrollable_frame, text=hsk_data['tone'][i], font=('Sans', 18),
                padx=5, pady=5).grid(row=i+2, column=3, sticky='nw')
            tk.Label(scrollable_frame, text=hsk_data['pinyin'][i], font=('Sans', 18),
                padx=5, pady=5).grid(row=i+2, column=4, sticky='nw')
            tk.Label(scrollable_frame, text=hsk_data['definition'][i], font=('Sans', 18),
                padx=5, pady=5, justify='left', wraplength=720).grid(row=i+2, column=5, sticky='nw')

        for col in range(6):
            scrollable_frame.grid_columnconfigure(col, weight=1)

    def quiz_window(self, level) -> None:
        # shows the quiz menu
        hsk_data = self.data[level - 1]
        window = tk.Toplevel(self)
        window.title(f'HSK Quiz (HSK {level})')
        window.geometry('900x800')
        window.resizable(False,True)

        container = tk.Frame(window)
        container.pack(fill='both', expand=True)

        quiz_canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=quiz_canvas.yview)
        quiz_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        quiz_canvas.pack(side='left', fill='both', expand=True)

        scrollable_frame = tk.Frame(quiz_canvas)
        quiz_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        scrollable_frame.bind('<Configure>', on_configure(quiz_canvas))
        quiz_canvas.bind_all('<MouseWheel>', on_mousewheel(quiz_canvas))
        
        tk.Label(scrollable_frame, text='Enter number of questions:', font=('Sans', 18), padx=5, pady=5).grid(row=1, column=1)
        
        question_count = tk.StringVar()
        tk.Entry(scrollable_frame, textvariable=question_count, font=('Sans', 18), width=12).grid(row=2, column=1,padx=5,pady=5)

        reset_button = None
        
        
        
        def clear_window() -> None:
            # clears the quiz window
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

        def start_quiz() -> None:
            # contains the quiz interface, entry, submit, start, and reset buttons, handles a value error 
            error_label = tk.Label(scrollable_frame, text='',font=('Sans',18),fg='red')
            error_label.grid(row=3,column=0,columnspan=3,pady=5)

            try:
                count = int(question_count.get())
                if count > len(hsk_data['simplified']):
                    count = len(hsk_data['simplified'])

                quiz = create_quiz(hsk_data, count)
                clear_window()

                nonlocal reset_button

                reset_button = tk.Button(scrollable_frame, text='Reset Quiz', font=('Sans',12), command=reset_quiz)
                reset_button.grid(row=count + 2, column=1, pady=10)
                reset_button.grid_remove()  

                answer_var = []

                instruction_label = tk.Label(scrollable_frame, text='Enter Pinyin in entry box',font=('Sans', 24))
                instruction_label.grid(row=0, column=1, padx=5, pady =5)
                
                for n in range(0,count):
                    tk.Label(scrollable_frame, text=f'Q{n+1}: {hsk_data['simplified'][quiz[n]]}', font=('Sans', 24)).grid(row=n+1, column=0, padx=5, pady=5)
                    var = tk.StringVar()

                    tk.Entry(scrollable_frame, textvariable=var, font=('Sans', 24), width=12).grid(row=n+1, column=1, padx=5, pady=5)
                    answer_var.append((var, quiz[n]))

                def check_answers() -> None:
                    """
                    compares answers to the original index, strips tones off of characters using unicode module,
                    shows how many you got right and dispays the answer in red or green dependending on if you were correct or not
                    """ 
                    correct_answers = 0
                    
                    for s, (var, index) in enumerate(answer_var):
                        answer = var.get().strip().lower().replace(' ', '')
                        correct_answer = hsk_data['pinyin'][index].strip().lower().replace(' ', '')
                        if strip_tones(answer) == strip_tones(correct_answer):
                            correct_answers += 1
                            color = 'green'
                        else:
                            color = 'red'

                        tk.Label(scrollable_frame, text=f'Ans:{correct_answer}',font=('Sans', 24),fg = color).grid(row=s+1, column=2, padx=5, pady=5)

                    tk.Label(scrollable_frame, text=f'Score: {correct_answers}/{count}',font=('Sans', 24)).grid(row=count+1, column= 1, padx=5, pady=5)
                    reset_button.grid()
                    
                tk.Button(scrollable_frame, text='Submit', font=('Sans', 24), command=check_answers).grid(row=count + 1, column=0, padx=5, pady=5)

            except ValueError:
                error_label.config(text='Enter a number greater than 0')
            
        def reset_quiz() -> None:
            # resets the quiz
            clear_window()
            tk.Label(scrollable_frame, text='Enter number of questions:', font=('Sans', 18), padx=5, pady=5).grid(row=1, column=1)
            tk.Entry(scrollable_frame, textvariable=question_count, font=('Sans', 18), width=12).grid(row=2, column=1, padx=5, pady=5)
            tk.Button(scrollable_frame, text='Start Quiz', font=('Sans',12), command=start_quiz).grid(row=2,column=2,padx=5)

        tk.Button(scrollable_frame, text='Start Quiz', font=('Sans',12), command=start_quiz).grid(row=2,column=2,padx=5)
