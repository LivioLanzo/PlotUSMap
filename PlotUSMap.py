import json 
import matplotlib.pyplot as plt
import requests

class PlotUSMap(object):
    
    '''
        plots a US Map as line chart !
    '''
    
    _json_file_url  = 'https://web.archive.org/web/20130615162524/http://eric.clst.org/wupl/Stuff/gz_2010_us_040_00_500k.json'
    
    def _load_json(self):
        resp = requests.get(url=self._json_file_url)
        resp.raise_for_status()
        json_file = json.loads(resp.text)
        return json_file
    
    def _unzip_coordinates(self, coords):
        xs, ys = list(zip(*coords))
        return xs, ys
    
    def plot_us_map(self, ax=None):
        '''
            plots the US states in as a line chart 
            
            Parameters
            --------------------------------------
            ax: a matplotlib axes object on which to plot the US states, if omitted it will be created
            
            
            Returns a matplotlib axes object on which the map is drawn
        '''
        
        if ax is None:
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
        
        json_file = self._load_json()
        
        for state in json_file['features']:
            if state['properties']['NAME'] not in ('Alaska', 'Puerto Rico', 'Hawaii'):
                if state['geometry']['type'] == 'Polygon':
                    xs, ys = self._unzip_coordinates(state['geometry']['coordinates'][0])
                    ax.plot(xs, ys, color='grey')
                elif state['geometry']['type'] == 'MultiPolygon':
                    for coord in state['geometry']['coordinates']:
                        xs, ys = self._unzip_coordinates(coord[0])
                        ax.plot(xs, ys, color='grey')
                
                
        return ax