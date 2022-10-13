from models import Instance, Vertex
import re
import typing as t


class InstanceLoader:

    SPLITTER = "NODE_COORD_SECTION"

    def load(self, file_path: str) -> Instance:
        with open(file_path) as f:
            file_content = f.read()
            splitted_content = file_content.split(self.SPLITTER)
            raw_attributes = splitted_content[0]
            raw_vertices = splitted_content[1]

            instance = Instance(
                name=self._get_name(raw_attributes),
                type=self._get_type(raw_attributes),
                comment=self._get_comment(raw_attributes),
                dimension=self._get_dimension(raw_attributes),
                edge_weight_type=self._get_edge_weight_type(raw_attributes),
                display_data_type=self._get_display_data_type(raw_attributes),
                vertices=self._get_vertices(raw_vertices)
            )

            return instance

    def _find_attribute_value(self, attribute_name: str, raw_attributes: str):
        pattern = f'{attribute_name}: (.*)'
        return re.search(pattern, raw_attributes, re.IGNORECASE).group(1)

    def _get_name(self, raw_attributes: str) -> t.Optional[str]:
        try:
            return self._find_attribute_value('NAME', raw_attributes)
        except AttributeError:
            return None

    def _get_type(self, raw_attributes: str) -> t.Optional[str]:
        try:
            return self._find_attribute_value('TYPE', raw_attributes)
        except AttributeError:
            return None

    def _get_comment(self, raw_attributes: str) -> t.Optional[str]:
        try:
            return self._find_attribute_value('COMMENT', raw_attributes)
        except AttributeError:
            return None

    def _get_dimension(self, raw_attributes: str) -> int:
        try:
            return int(self._find_attribute_value('DIMENSION', raw_attributes))
        except AttributeError:
            return None

    def _get_edge_weight_type(self, raw_attributes: str) -> t.Optional[str]:
        try:
            return self._find_attribute_value('EDGE_WEIGHT_TYPE', raw_attributes)
        except AttributeError:
            return None

    def _get_display_data_type(self, raw_attributes: str) -> t.Optional[str]:
        try:
            return self._find_attribute_value('DISPLAY_DATA_TYPE', raw_attributes)
        except AttributeError:
            return None

    def _get_vertices(self, raw_vertices: str) -> t.List[Vertex]:
        vertices = []
        for line in raw_vertices.split('\n'):
            if not line:
                continue
            if line == 'EOF':
                break
            splitted_line = line.split(' ')
            splitted_line = list(filter(None, splitted_line))
            vertex = Vertex(
                vertex_number=int(splitted_line[0]),
                x=float(splitted_line[1]),
                y=float(splitted_line[2]),
            )
            vertices.append(vertex)
        return vertices


