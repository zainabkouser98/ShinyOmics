# ShinyOmics: Interactive Data Visualization for Single-Cell Analysis
ShinyOmics is a Dash application designed for visualizing single-cell data with ease. Whether you're exploring distributions, correlations, or trends in your dataset, ShinyOmics provides a customizable platform to generate and export various types of plots.

**Features**  
**Upload CSV File:** Quickly load your single-cell data in CSV format.    
**Interactive Plotting:** Choose from a variety of plot types such as Histograms, Violin Plots, Pie Charts, Box Plots, Line Plots, Bar Plots, Scatter Plots, 3D Scatter Plots, and Hexbin Plots.  
**Customization:** Customize your plots with titles, select specific columns, and adjust display options.  
**Export:** Export your plots as high-quality images for presentations and publications.    
**Installation**  
Install the required dependencies using pip:
              "pip install dash dash-core-components dash-html-components dash-bootstrap-components plotly pandas jupyter-dash kaleido"   
**Running the App**  
Clone this repository to your local machine:                                                                                                    
              "git clone https://github.com/zainabkouser98/ShinyOmics.git"
Navigate to the directory where the app is located:                
              "cd ShinyOmics"  
Run the following command to start the Dash application:
              "python app.py"     
**Usage**   
**Upload Data:** Click on "Upload CSV File" to upload your single-cell data.  
**Select Plot Type:** Choose the type of plot you want to generate from the dropdown menu.  
**Customize:** Optionally, enter a title for your plot, select specific columns, and adjust other settings.  
**Generate Plot:** Click on "Generate Plot" to visualize your data.  
**Export as Image:** For certain plot types like Scatter Plots, 3D Scatter Plots, and Hexbin Plots, an "Export as Image or on camera icon" option will appear. Click on it to download the plot as an image file.

