# BiofilmGui

Biofilms are communities of bacteria that grow in aqueous environments, 
forming after free-floating bacteria attach to a suitable surface and 
secrete substances that form a protective layer. Biofilms also play a 
significant role in infections when bioiflms formed by pathogenic bacteria, 
like Pseudomonas aeruginosa become established in the human body. 

This biofilm gui is a small application for calculating biofilm growth 
during the first 24 hours of development. There are three bacteria to 
choose from, but it is also possible to add data for new types of bacteria. 
It is easy to change the parameters for growth including the initial amount
of biofilm and the maximum amount of biofilm that can grow. It is also 
possible to look at the effect of different concentations of inhibitory 
treatments like antibiotics if you know the minimum inhibitory concentration
of an antibiotic against a bacteria. 

# How to Use

1. Clone this repository

`git clone https://github.com/mandyabernathy/BiofilmGui.git`

2. Use pip to install Matplotlib, SciPy, and tkinter.
```
pip install matplotlib
pip install scipy
pip install tkinter //or// sudo apt-get install python3-tk
```
(I don't rememember having 
any issues installing tkinter on Windows using pip, but pip would not work 
for tkinter when I tried it on linux. More investigation to follow.)

3. Start the program using 
    `python gui.py`

# Layout

The first tab show biofilm growth for the selected bacteria. Choose a different bacteria from the dropdown menu, or change any of the parameters.

The second tab shows the growth of planktonic bacteria, plotting data points from experiments involving each bacteria. Choose a different bacteria from
the dropdown menu.

The third tab is for data entry. If you would like to calculate biofilm growth for a different bacteria, you need to perform an experiment that periodically measures the planktonic growth of the bacteria (Turbidimetric Determination). Inoculate a sample with your bacteria and incubate it at the required temperature. Measure the optical density of the sample every hour. After the experiment, enter the bacteria name, the start and end times of your sampling period, and the OD measurements. If you receive no errors, the bacteria will be an option for plotting in the first and second tabs. 
