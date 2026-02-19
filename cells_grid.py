from typing import Any
import customtkinter as ctk

class CellsGrid(ctk.CTkFrame):
    """
    A grid container that dynamically creates a matrix of CTkFrame cells.

    This component is useful for dashboards, game boards, image grids,
    or any layout that requires evenly spaced rectangular cells.
    """

    def __init__(
            self,
            master: Any,
            bg_color: str = "transparent",
            fg_color: str = "transparent",
            height: int | float = 200,
            margin: int | tuple[int | float, int | float] | tuple[int | float, int | float, int | float, int | float] = 0,
            padding: int | tuple[int | float, int | float] | tuple[int | float, int | float, int | float, int | float] = 0,
            width: int | float = 200,
        ):
        """
        Initialize the CellsGrid container.

        :param master: Parent widget.
        :param bg_color: Background color of the container.
        :param fg_color: Foreground color of the container.
        :param height: Height of the container.
        :param width: Width of the container.
        :param margin: External spacing around the grid (int, 2-tuple or 4-tuple).
        :param padding: Internal spacing inside the grid (int, 2-tuple or 4-tuple).
        """
        super().__init__(
            master,
            bg_color=bg_color,
            fg_color=fg_color,
            height=height,
            width=width,
        )

        # Layout spacing (normalized to 4-value tuples)
        self.outer_margin = self.__normalize_box_spacing(margin, "margin")
        self.inner_padding = self.__normalize_box_spacing(padding, "padding")

        # Internal frame that holds the grid cells
        self.container_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.container_frame.grid(
            padx=(self.inner_padding[0], self.inner_padding[2]),
            pady=(self.inner_padding[1], self.inner_padding[3]),
        )

        # 2D matrix of CTkFrame cells
        self._cells_matrix: list[list[ctk.CTkFrame]] = []
    
    def grid(self, **kwargs):
        """
        Override grid() to automatically apply outer margin spacing.
        """
        super().grid(
            padx=(self.outer_margin[0], self.outer_margin[2]),
            pady=(self.outer_margin[1], self.outer_margin[3]),
            **kwargs
        )
        
    def load_cells(
        self,
        array: tuple[int, int] | list[int, int] | int = 4,
        cells_border_color: str = None,
        cells_border_width: int | float = 0,
        cells_corner_radius: int | float = 30,
        cells_fg_color: str = None,
        cells_height: int | float = None,
        cells_size: int | float = 100,
        cells_spacing: int | float | tuple[int | float, int | float] | tuple[int | float, int | float, int | float, int | float] = 10,
        cells_width: int | float = None,
    ):
        """
        Create and display the grid cells.
        """

        # Remove previously created cells
        self.__destroy_all_cells()

        # Normalize grid size
        self.grid_shape = (array, array) if isinstance(array, int) else tuple(array)

        if len(self.grid_shape) != 2:
            raise ValueError(
                "`array` must be an int or a tuple/list with exactly 2 values: (rows, columns)."
            )

        self.cell_border_color = cells_border_color
        self.cell_border_width = cells_border_width
        self.cell_corner_radius = cells_corner_radius
        self.cell_fg_color = cells_fg_color

        # If width/height are not provided, fallback to cells_size
        self.cell_height = cells_height if cells_height is not None else cells_size
        self.cell_width = cells_width if cells_width is not None else cells_size

        # Normalize spacing to 4-value tuple: (left, top, right, bottom)
        self.cell_spacing = self.__normalize_cell_spacing(cells_spacing)

        self._last_row_index = self.grid_shape[0] - 1
        self._last_column_index = self.grid_shape[1] - 1
        self._cells_matrix = []

        # Create the grid of CTkFrame cells
        for row in range(self.grid_shape[0]):
            self._cells_matrix.append([])
            for col in range(self.grid_shape[1]):
                cell = ctk.CTkFrame(
                    self.container_frame,
                    bg_color="transparent",
                    border_color=self.cell_border_color,
                    border_width=self.cell_border_width,
                    corner_radius=self.cell_corner_radius,
                    fg_color=self.cell_fg_color,
                    height=self.cell_height,
                    width=self.cell_width
                )

                # Place each cell with dynamic spacing (no spacing at outer borders)
                cell.grid(
                    row=row,
                    column=col,
                    padx=(
                        self.cell_spacing[0] * (col != 0),
                        self.cell_spacing[2] * (col != self._last_column_index)
                    ),
                    pady=(
                        self.cell_spacing[1] * (row != 0),
                        self.cell_spacing[3] * (row != self._last_row_index)
                    )
                )

                self._cells_matrix[row].append(cell)

    def get_cells_grid(self):
        """
        Return the internal 2D list of cell frames.
        """
        return self._cells_matrix
    
    def __destroy_all_cells(self):
        """
        Destroy all existing cells in the grid.
        """
        if self._cells_matrix:
            for row in range(self.grid_shape[0]):
                for col in range(self.grid_shape[1]):
                    self._cells_matrix[row][col].destroy()
    
    def __normalize_cell_spacing(
        self,
        value: int | tuple[int | float, int | float] | tuple[int | float, int | float, int | float, int | float]
    ) -> tuple[int | float, int | float, int | float, int | float]:
        """
        Normalize spacing values to a 4-value tuple and divide by 2
        to apply half spacing to each adjacent cell side.
        """

        if not isinstance(value, (int, tuple, list)):
            raise TypeError(
                f"`cells_spacing` must be int, tuple, or list, but received {type(value).__name__}."
            )

        if isinstance(value, int):
            return (value / 2, value / 2, value / 2, value / 2)

        if len(value) == 2:
            self.__ensure_numeric_sequence(value, "cells_spacing")
            return (value[0] / 2, value[1] / 2, value[0] / 2, value[1] / 2)

        if len(value) == 4:
            self.__ensure_numeric_sequence(value, "cells_spacing")
            return (value[0] / 2, value[1] / 2, value[2] / 2, value[3] / 2)

        raise ValueError(
            "`cells_spacing` must contain 2 or 4 values. "
            "Valid examples: 10, (10, 20), (10, 5, 10, 5)."
        )
        
    def __normalize_box_spacing(
        self,
        value: int | tuple[int | float, int | float] | tuple[int | float, int | float, int | float, int | float],
        name: str,
    ) -> tuple[int | float, int | float, int | float, int | float]:
        """
        Normalize padding/margin values to a 4-value tuple.

        Accepted formats:
            - int: uniform spacing
            - (x, y): horizontal and vertical spacing
            - (l, t, r, b): per-side spacing
        """

        if not isinstance(value, (int, tuple, list)):
            raise TypeError(
                f"`{name}` must be int, tuple, or list, but received {type(value).__name__}."
            )

        if isinstance(value, int):
            return (value, value, value, value)

        if len(value) == 2:
            self.__ensure_numeric_sequence(value, name)
            return (value[0], value[1], value[0], value[1])

        if len(value) == 4:
            self.__ensure_numeric_sequence(value, name)
            return (value[0], value[1], value[2], value[3])

        raise ValueError(
            f"`{name}` must contain 2 or 4 values. "
            "Valid examples: 10, (10, 20), (10, 5, 10, 5)."
        )

    def __ensure_numeric_sequence(self, seq, name: str):
        """
        Ensure all values in a tuple/list are numeric (int or float).
        """
        if not all(isinstance(v, (int, float)) for v in seq):
            raise TypeError(
                f"All values in `{name}` must be int or float. Received: {seq}"
            )
