import os
import base64

def export_report(OUTPUT):
    print('[LOG] Exporting HTML report')
    try:
        with open(OUTPUT, 'w', encoding="utf-8") as output_file:
            if any(os.listdir('./output/temp_results')):
                output_file.write('<div style="display: flex; justify-content: center;"><h3>Results</h3></div>')
                output_file.write('<div style="display: flex; justify-content: center;">\n')
                output_file.write('\t<table style="border:none; width:30%;">\n')
                for result_file in os.listdir('./output/temp_results'):
                    with open('./output/temp_results/' + result_file, 'r') as res:
                        output_file.write(f'{res.read()}')
                    os.remove('./output/temp_results/' + result_file)
                output_file.write('\t</table>\n')
                output_file.write('</div><br><br>\n')
            if any(os.listdir('./output/temp_statistics')):
                output_file.write('<div style="display: flex; justify-content: center;"><h3>Statistics</h3></div>')
                output_file.write('<div style="display: flex; justify-content: center;">\n')
                output_file.write('\t<table style="border:none; width:75%;">\n')
                output_file.write('\t\t<tr>\n')
                output_file.write('\t\t\t<th style="text-align:left;">Statistic</th>\n')
                output_file.write('\t\t\t<th style="text-align:left;">Real dataset</th>\n')
                output_file.write('\t\t\t<th style="text-align:left;">Simulated dataset</th>\n')
                output_file.write('\t\t</tr>\n')
                for result_file in os.listdir('./output/temp_statistics'):
                    with open('./output/temp_statistics/' + result_file, 'r') as res:
                        output_file.write(f'{res.read()}')
                    os.remove('./output/temp_statistics/' + result_file)
                output_file.write('\t</table>\n')
                output_file.write('</div><br><br>\n')
            if any(os.listdir('./output/temp_figures')):
                fig_type = os.listdir('./output/temp_figures')[0][:5]
                for figure_file in os.listdir('./output/temp_figures'):
                    with open('./output/temp_figures/' + figure_file, 'rb') as svg:
                        if figure_file[:5] != fig_type:
                            output_file.write('<br>\n')
                            fig_type = figure_file[:5]
                        svg_base64 = str(base64.b64encode(svg.read()),'utf-8')
                        output_file.write(f'<img style="border-style:solid; border-width:3px; border-color:#AAAAAA;" src="data:image/svg+xml;base64,{svg_base64}" />\n')
                        
                    os.remove('./output/temp_figures/' + figure_file)
            os.rmdir('./output/temp_results')
            os.rmdir('./output/temp_statistics')
            os.rmdir('./output/temp_figures')
    
        print('[LOG] HTML report created')
    except:
        print('[ERROR] Failed to create HTML report')