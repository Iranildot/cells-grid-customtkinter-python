# CellsGrid

`CellsGrid` is a GUI component based on `ctk.CTkFrame` (CustomTkinter)
that dynamically creates a grid (matrix) of `CTkFrame` cells.\
It's ideal for **dashboards**, **game boards**, **image galleries**, or
any layout that requires evenly spaced rectangular cells.

------------------------------------------------------------------------

## 📦 Overview

`CellsGrid` encapsulates:

-   A main container (`CTkFrame`)
-   An internal frame that holds the grid
-   A 2D matrix of cells (`CTkFrame`)
-   Support for:
    -   Outer margin
    -   Inner padding
    -   Cell spacing
    -   Custom borders, corner radius, and colors
    -   Dynamic grid size (rows x columns)

------------------------------------------------------------------------

## 🧩 Internal Structure

-   `self.container_frame`\
    Internal frame that holds the cells.

-   `self._cells_matrix`\
    2D matrix containing all created cells:

    ``` python
    list[list[ctk.CTkFrame]]
    ```

------------------------------------------------------------------------

## 🛠️ Constructor

``` python
CellsGrid(
    master,
    bg_color="transparent",
    fg_color="transparent",
    height=200,
    width=200,
    margin=0,
    padding=0
)
```

### Parameters

  Parameter    Type        Description
  ------------ ----------- -----------------------------------
  `master`     Any         Parent widget
  `bg_color`   str         Background color of the container
  `fg_color`   str         Foreground color of the container
  `height`     int/float   Grid height
  `width`      int/float   Grid width
  `margin`     int/tuple   Outer margin (1, 2, or 4 values)
  `padding`    int/tuple   Inner padding (1, 2, or 4 values)

Accepted formats for `margin` and `padding`:

-   `10` → (10, 10, 10, 10)\
-   `(10, 20)` → (10, 20, 10, 20)\
-   `(10, 5, 10, 5)` → (left, top, right, bottom)

------------------------------------------------------------------------

## 📐 Positioning with `grid()`

The `grid()` method is overridden to automatically apply outer margins:

``` python
cells_grid.grid(row=0, column=0, sticky="nsew")
```

------------------------------------------------------------------------

## 🧱 Creating the Grid

``` python
cells_grid.load_cells(
    array=4,
    cells_border_color=None,
    cells_border_width=0,
    cells_corner_radius=30,
    cells_fg_color=None,
    cells_height=None,
    cells_width=None,
    cells_size=100,
    cells_spacing=10
)
```

### Parameters

  Parameter               Type                  Description
  ----------------------- --------------------- -----------------------
  `array`                 int or (rows, cols)   Grid size
  `cells_border_color`    str                   Cell border color
  `cells_border_width`    int/float             Border width
  `cells_corner_radius`   int/float             Corner radius
  `cells_fg_color`        str                   Cell background color
  `cells_height`          int/float             Cell height
  `cells_width`           int/float             Cell width
  `cells_size`            int/float             Fallback size
  `cells_spacing`         int/tuple             Spacing between cells

Examples for `array`:

-   `4` → creates a 4x4 grid\
-   `(3, 5)` → creates 3 rows and 5 columns

------------------------------------------------------------------------

## 📏 Cell Spacing

Spacing is automatically divided by 2 per side to avoid doubled spacing
between adjacent cells.

Accepted formats:

-   `10` → uniform spacing\
-   `(10, 20)` → horizontal / vertical\
-   `(10, 5, 10, 5)` → left, top, right, bottom

Spacing is **not applied to the outer borders of the grid**, only
between cells.

------------------------------------------------------------------------

## 🔁 Updating the Grid

Whenever `load_cells()` is called:

-   All existing cells are destroyed
-   The grid is recreated from scratch

------------------------------------------------------------------------

## 🔎 Accessing the Cells

``` python
cells = cells_grid.get_cells_grid()
```

Returns:

``` python
list[list[ctk.CTkFrame]]
```

Example:

``` python
cells[0][0].configure(fg_color="red")
cells[1][2].configure(border_color="blue")
```

------------------------------------------------------------------------

## ⚠️ Validation and Errors

-   `array` must have exactly 2 values when provided as a tuple/list
-   `margin`, `padding`, and `cells_spacing` accept only:
    -   `int`
    -   `tuple/list` with 2 or 4 numeric values
-   Invalid types raise `TypeError`
-   Invalid value counts raise `ValueError`

------------------------------------------------------------------------

## 🧪 Usage Example

``` python
root = ctk.CTk()

root.geometry("600x600")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
ctk.set_appearance_mode("light")

grid = CellsGrid(root, width=400, height=400, margin=20, padding=10)
grid.grid(row=0, column=0)

grid.load_cells(
    array=(3, 3),
    cells_spacing=12,
    cells_corner_radius=12,
    cells_fg_color="#999999",
    cells_border_color="#444",
    cells_border_width=2
)

root.mainloop()
```

<img width="1920" height="1080" alt="cells_grid" src="https://github.com/user-attachments/assets/7e8bb2c3-6fb6-4b78-9212-3ff0138390ad" />

------------------------------------------------------------------------

## ✅ Use Cases

-   🎮 Game boards\
-   📊 Modular dashboards\
-   🖼️ Image galleries\
-   🧱 Grid-based layouts\
-   📦 Reusable visual containers

------------------------------------------------------------------------

## 🧠 Technical Notes

-   Cell spacing is calculated to avoid duplication
-   Uses Tkinter `grid()` internally
-   Fully reusable and dynamically reconfigurable
