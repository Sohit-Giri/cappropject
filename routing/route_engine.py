import networkx as nx
import logging
from .graph_manager import GraphManager

logger = logging.getLogger(__name__)

# Speed constants in km/h
SPEED_PROFILES = {
    'walk': 5.0,
    'bike': 15.0,
    'car': 40.0
}

class RouteEngine:
    def __init__(self):
        self.gm = GraphManager.get_instance()

    def _get_custom_weight(self, u, v, data, mode):
        """
        Dynamically calculates edge cost (weight) based on the travel mode
        and OpenStreetMap highway attributes.
        """
        base_length = data.get('length', 1.0)
        highway = data.get('highway', '')

        # Ensure highway is a string or list of strings
        if isinstance(highway, list):
            highway = highway[0]
        
        highway = str(highway).lower()

        if mode == 'walk':
            # Walking penalties: Avoid motorways/trunks entirely
            if highway in ['motorway', 'motorway_link', 'trunk']:
                return base_length * 10.0  # Heavy penalty
            return base_length

        elif mode == 'bike':
            # Cycling penalties: Prefer cycleways, penalize major highways
            if highway in ['motorway', 'motorway_link']:
                return base_length * 20.0
            if highway in ['cycleway', 'living_street', 'residential']:
                return base_length * 0.8  # Incentive
            return base_length

        else:  # 'car'
            # Driving penalties: Block pedestrian tracks, steps, or footways
            if highway in ['footway', 'steps', 'pedestrian', 'path', 'cycleway']:
                return base_length * 50.0  # Heavily penalize or restrict
            return base_length

    def compute_mode_path(self, graph, src, dst, mode):
        """
        Computes a single path for a specific mode using dynamic weights.
        """
        try:
            # Dijkstra execution using our custom dynamic weight function
            path = nx.shortest_path(
                graph, src, dst, 
                weight=lambda u, v, d: self._get_custom_weight(u, v, d, mode), 
                method='dijkstra'
            )
            
            # Calculate the actual physical distance (meters) along that computed path
            actual_dist_meters = sum(graph.edges[path[i], path[i+1], 0].get('length', 0) for i in range(len(path)-1))
        except (nx.NetworkXNoPath, KeyError):
            return None
        except nx.NodeNotFound as e:
            raise ValueError(str(e))

        # Build coordinate geometry
        coords = []
        for n in path:
            node_data = graph.nodes[n]
            coords.append({
                'lat': round(node_data['y'], 6), 
                'lon': round(node_data['x'], 6), 
                'node_id': str(n)
            })

        dist_km = round(actual_dist_meters / 1000, 3)
        speed_kmh = SPEED_PROFILES[mode]
        eta_min = round((dist_km / speed_kmh) * 60, 1)

        return {
            'path_coords': coords,
            'total_distance_meters': round(actual_dist_meters, 2),
            'total_distance_km': dist_km,
            'node_count': len(path),
            'eta_minutes': eta_min,
            'speed_kmh': speed_kmh
        }

    def compute_all_routes(self, src, dst):
        """
        Executes Dijkstra 3 times to get distinct paths for Walk, Bike, and Car.
        """
        g = self.gm.get_graph()
        if g is None:
            raise RuntimeError('Graph unavailable')

        routes_response = {}
        for mode in ['walk', 'bike', 'car']:
            routes_response[mode] = self.compute_mode_path(g, src, dst, mode)
            
        return routes_response