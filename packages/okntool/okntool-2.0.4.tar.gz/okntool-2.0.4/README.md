# OKN TOOL PYTHON PACKAGE LIBRARY MANUAL
## Description
This program will draw the graph image in the ABI eye research group web experience recording folder according to config file information and plot type input. 

There are 4 types of plot which are:
1.  **Trial** plot which represents sensor timestamp vs pupil displacement/movement graph for each trial.
2.  **Summary** plot which is the combination of all trial plots with the same x and y axis scales.
3.  **Staircase/progress** plot which is the graph image to visualize whether there is okn or not and the visual acuity etdrs calculation steps.
4.  **Tidy** plot, the special plot for all trial protocol in which borders and boundaries are drawn in tidest format.

## Installation requirements and guide
### Anaconda
To install this program, `Anaconda python distributing program` and `Anaconda Powershell Prompt` are needed.  
If you do not have `Anaconda`, please use the following links to download and install:  
Download link: https://www.anaconda.com/products/distribution  
Installation guide link: https://docs.anaconda.com/anaconda/install/  
### PIP install
To install `okntool`, you have to use `Anaconda Powershell Prompt`.  
After that, you can use the `okntool` from any command prompt.  
In `Anaconda Powershell Prompt`:
```
pip install okntool
```  
## Usage guide
### Example usage
```
okntool -t "(plot_type)" -d "(directory to the folder)" -c "(directory to config file)"
```
plot_type: "trial", "summary" or "staircase"  
If you are using "trial" plot type, please -d "(directory to trial folder)".  
If you are using "summary" or "staircase" plot type, please -d "(directory to pim_recorded_folder/trials)".  
**Note: please put `directory to pim recorded folder` and `directory to config file` into the string indication "(dir_input)".**  

There is a example folder under `development` folder.  
If you want to test this program, you can clone this repository, install `okntool` and run the following command:  
**For trial plot**
```
okntool -t "trial" -d "development/example/trials/trials/trial-1-1_disk-condition-1-1"
```
**For summary plot**
```
okntool -t "summary" -d "development/example/trials/trials"
```
**For staircase/progress plot**
```
okntool -t "staircase" -d "development/example/trials/trials"
```
or
```
okntool -t "progress" -d "development/example/trials/trials"
```
**For tidy plot**
```
okntool -t "tidy" -d "development/example/trials/trials"
```
### oknserver_graph_plot_config.json
This is a built-in config file which contains the information how trial plot, summary plot and progress plot will be drawn.  
Please read more details about them in TRIAL_PLOT_README.md, SUMMARY_PLOT_README.md and PROGRESS_PLOT_README.md.
If you wanna change the parameters of config file, copy and paste the build-in config file into a different directory.
After that modify the config file and run the okntool with optional argument `-c (directory to new config file)`.  
```
okntool -t "(plot_type)" -d "(directory to the folder)" -c "(directory to new config file)"
```

### To upgrade version  
In `Anaconda Powershell Prompt`,
```
pip install -U okntool
```
or
```
pip install --upgrade okntool
```
