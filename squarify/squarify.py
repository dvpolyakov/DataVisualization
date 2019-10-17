# original idea and pseudocode described in https://www.win.tue.nl/~vanwijk/stm.pdf
# code was written using ideas from here: https://github.com/laserson/squarify

class Squarify:
    def _normalize_sizes(self, sizes, width, height):
        assert all(isinstance(elem, float) for elem in sizes)
        return list(map(lambda size: size * (width * height) / sum(sizes), sizes))
    
    def _layoutrow(self, sizes, x, y, dx, dy):
        width = sum(sizes) / dy
        rectangles_coords = []
        for size in sizes:
            rectangles_coords.append({"x": x, "y": y, "dx": width, "dy": size / width})
            y += size / width
        return rectangles_coords

    def _layoutcol(self, sizes, x, y, dx, dy):
        height = sum(sizes) / dx
        rectangles_coords = []
        for size in sizes:
            rectangles_coords.append({"x": x, "y": y, "dx": size / height, "dy": height})
            x += size / height
        return rectangles_coords

    def _layout(self, sizes, x, y, dx, dy):
        if dx >= dy:
            return self._layoutrow(sizes, x, y, dx, dy)
        return self._layoutcol(sizes, x, y, dx, dy)

    def _leftoverrow(self, sizes, x, y, dx, dy):
        width = sum(sizes) / dy
        leftover_x = x + width
        leftover_y = y
        leftover_dx = dx - width
        leftover_dy = dy
        return (leftover_x, leftover_y, leftover_dx, leftover_dy)

    def _leftovercol(self, sizes, x, y, dx, dy):
        height = sum(sizes) / dx
        leftover_x = x
        leftover_y = y + height
        leftover_dx = dx
        leftover_dy = dy - height
        return (leftover_x, leftover_y, leftover_dx, leftover_dy)

    def _leftover(self, sizes, x, y, dx, dy):
        if dx >= dy:
            return self._leftoverrow(sizes, x, y, dx, dy)
        return self._leftovercol(sizes, x, y, dx, dy)

    def _worst_ratio(self, sizes, x, y, dx, dy):
        return max(
            [max(rect["dx"] / rect["dy"], rect["dy"] / rect["dx"]) 
             for rect in self._layout(sizes, x, y, dx, dy)])

    def squarify(self, sizes, x, y, dx, dy):
        """
        Squarify visualization algorithm
        """
        assert all(isinstance(elem, float) for elem in sizes)
        sizes = self._normalize_sizes(sizes, dx, dy)

        if len(sizes) == 0:
            return []
        if len(sizes) == 1:
            return self._layout(sizes, x, y, dx, dy)

        index_to_split = 1
        while index_to_split < len(sizes) and self._worst_ratio(sizes[:index_to_split], x, y, dx, dy) >= self._worst_ratio(sizes[: (index_to_split + 1)], x, y, dx, dy):
            index_to_split += 1
        current = sizes[:index_to_split]
        remaining = sizes[index_to_split:]

        (leftover_x, leftover_y, leftover_dx, leftover_dy) = self._leftover(current, x, y, dx, dy)
        return self._layout(current, x, y, dx, dy) + self.squarify(
            remaining, leftover_x, leftover_y, leftover_dx, leftover_dy)
