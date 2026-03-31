import os, logging
import networkx as nx
logger = logging.getLogger(__name__)

class GraphManager:
    _instance = None
    _graph    = None
    _districts = []
    _loaded_count = 0

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_districts(self, districts, cache_dir='graph_cache'):
        import osmnx as ox
        self._districts = districts
        os.makedirs(cache_dir, exist_ok=True)
        graphs = []
        for place in districts:
            safe = place.replace(',','').replace(' ','_').replace('/','_').lower()[:50]
            path = os.path.join(cache_dir, f'{safe}.graphml')
            try:
                if os.path.exists(path):
                    logger.info(f'Loading cached: {place}')
                    g = ox.load_graphml(path)
                else:
                    logger.info(f'Downloading: {place} ...')
                    g = ox.graph_from_place(place, network_type='drive')
                    ox.save_graphml(g, path)
                    logger.info(f'Cached: {place}')
                graphs.append(g)
                self._loaded_count += 1
                logger.info(f'Loaded {self._loaded_count}/{len(districts)} districts')
            except Exception as e:
                logger.warning(f'Skipping {place}: {e}')

        if graphs:
            self._graph = nx.compose_all(graphs) if len(graphs) > 1 else graphs[0]
            logger.info(f'Combined graph: {len(self._graph.nodes)} nodes, {len(self._graph.edges)} edges')
        else:
            logger.error('No district graphs could be loaded!')

    def get_nearest_node(self, lat, lon):
        import osmnx as ox
        if self._graph is None:
            raise RuntimeError('Graph not loaded yet')
        return ox.nearest_nodes(self._graph, X=lon, Y=lat)

    def get_graph(self):
        return self._graph

    def is_loaded(self):
        return self._graph is not None

    def get_info(self):
        if not self.is_loaded():
            loaded = self._loaded_count
            total  = len(self._districts)
            return {'loaded': False, 'message': f'Loading districts ({loaded}/{total})...',
                    'loaded_count': loaded, 'total': total}
        return {
            'loaded':    True,
            'districts': self._districts,
            'nodes':     len(self._graph.nodes),
            'edges':     len(self._graph.edges),
            'loaded_count': self._loaded_count,
            'total':     len(self._districts),
        }
