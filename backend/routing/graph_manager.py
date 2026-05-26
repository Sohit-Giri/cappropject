import os
import logging
import networkx as nx

logger = logging.getLogger(__name__)


class GraphManager:
    _instance = None
    _graph = None
    _districts = []
    _loaded_count = 0

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_districts(self, districts, cache_dir=None):
        import osmnx as ox
        from django.conf import settings

        # Force the absolute path configured in settings.py
        if cache_dir is None:
            cache_dir = str(settings.GRAPH_CACHE_DIR)

        self._districts = districts
        os.makedirs(cache_dir, exist_ok=True)
        graphs = []

        for place in districts:
            safe = (
                place.replace(",", "")
                .replace(" ", "_")
                .replace("/", "_")
                .lower()[:50]
            )

            path = os.path.join(cache_dir, f"{safe}.graphml")

            # Fallback path if filename differs
            fallback_path = os.path.join(
                cache_dir,
                "kathmandu_nepal.graphml"
            )

            try:
                # 1. Exact cached graph
                if os.path.exists(path):
                    logger.info(
                        f"Loading cached absolute path: {path}"
                    )
                    g = ox.load_graphml(path)

                # 2. Kathmandu fallback graph
                elif (
                    "kathmandu" in safe
                    and os.path.exists(fallback_path)
                ):
                    logger.info(
                        f"Using fallback absolute cache: "
                        f"{fallback_path}"
                    )
                    g = ox.load_graphml(fallback_path)

                # 3. Do NOT attempt download on Vercel
                else:
                    logger.error(
                        f"Graph missing on disk at: {path}"
                    )
                    raise FileNotFoundError(
                        f"Map data not bundled in deployment for {place}"
                    )

                graphs.append(g)
                self._loaded_count += 1

                logger.info(
                    f"Loaded {self._loaded_count}/"
                    f"{len(districts)} districts"
                )

            except Exception as e:
                # Force output into Vercel logs
                print(
                    f"CRITICAL GRAPH ERROR for {place}: {str(e)}"
                )
                logger.warning(f"Skipping {place}: {e}")

        if graphs:
            self._graph = (
                nx.compose_all(graphs)
                if len(graphs) > 1
                else graphs[0]
            )

            logger.info(
                f"Combined graph: "
                f"{len(self._graph.nodes)} nodes, "
                f"{len(self._graph.edges)} edges"
            )
        else:
            logger.error(
                "No district graphs could be loaded!"
            )

    def get_nearest_node(self, lat, lon):
        import osmnx as ox

        if self._graph is None:
            raise RuntimeError("Graph not loaded yet")

        return ox.nearest_nodes(
            self._graph,
            X=lon,
            Y=lat
        )

    def get_graph(self):
        return self._graph

    def is_loaded(self):
        return self._graph is not None

    def get_info(self):
        if not self.is_loaded():
            loaded = self._loaded_count
            total = len(self._districts)

            return {
                "loaded": False,
                "message": f"Loading districts ({loaded}/{total})...",
                "loaded_count": loaded,
                "total": total,
            }

        return {
            "loaded": True,
            "districts": self._districts,
            "nodes": len(self._graph.nodes),
            "edges": len(self._graph.edges),
            "loaded_count": self._loaded_count,
            "total": len(self._districts),
        }