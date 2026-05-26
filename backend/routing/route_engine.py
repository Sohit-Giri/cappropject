import networkx as nx
import logging
from .graph_manager import GraphManager
logger = logging.getLogger(__name__)

SPEED_KMH = {'walk': 5, 'bike': 15, 'car': 40}

class RouteEngine:
    def __init__(self):
        self.gm = GraphManager.get_instance()

    def compute_shortest_path(self, src, dst, mode='car'):
        g = self.gm.get_graph()
        if g is None:
            raise RuntimeError('Graph unavailable')
        try:
            path = nx.shortest_path(g, src, dst, weight='length', method='dijkstra')
            dist = nx.shortest_path_length(g, src, dst, weight='length', method='dijkstra')
        except nx.NetworkXNoPath:
            return None
        except nx.NodeNotFound as e:
            raise ValueError(str(e))

        coords = []
        for n in path:
            d = g.nodes[n]
            coords.append({'lat': round(d['y'], 6), 'lon': round(d['x'], 6), 'node_id': str(n)})

        dist_km   = round(dist / 1000, 3)
        speed_kmh = SPEED_KMH.get(mode, 40)
        eta_min   = round((dist_km / speed_kmh) * 60, 1)

        return {
            'path_coords':           coords,
            'total_distance_meters': round(dist, 2),
            'total_distance_km':     dist_km,
            'node_count':            len(path),
            'eta_minutes':           eta_min,
            'mode':                  mode,
            'speed_kmh':             speed_kmh,
        }